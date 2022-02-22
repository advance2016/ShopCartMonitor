

from concurrent.futures import ProcessPoolExecutor
import re
import uuid
from json import dumps
from operator import eq
from operator import ne
from queue import Queue
from random import randint
from functools import partial
from datetime import datetime
from urllib.parse import parse_qsl, unquote
from concurrent.futures.thread import ThreadPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler


from api.models import engine
from api.models import ProductInfo
from api.models import Cookie
from settings.default_settings import MAX_WORKERS, TEST_COOKIES
from settings.default_settings import UNIDBG_SIGN_API
from settings.default_settings import SCHEDULE_INTERVAL
from settings.default_settings import ORDER_INTERVAL
from settings.default_settings import DEBUG
from settings.default_settings import DING_ACCESS_TOKEN
from settings.default_settings import DING_SECRET_KEY

import requests
from jsonpath import jsonpath
from api.ding import WebHookAPI
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists


class JDCartMonitor(object):
    def __init__(self, *args, **kwargs):
        self.orm_session = sessionmaker(engine)()
        cookieobj = self.orm_session.query(Cookie).filter().first()
        if not cookieobj:
            print("数据库没cookies,请重新登录")
            exit(0)
        self.session = requests.Session()
        self.uuid = uuid.uuid4().hex[:16]
        self.cartuuid = str(uuid.uuid4())
        self.longitude = "111.699272"  # TODO 湖南常德市经纬度
        self.latitude = "29.032768"
        self.cvhv = "".join((str(randint(0, 9)) for _ in range(15)))  # 15数字组合
        self.cookies = cookieobj.compose_cookie() or TEST_COOKIES

        eid_match = re.search('"devicefinger":"(.*?)"', self.cookies)
        if eid_match:
            self.eid = eid_match.group(1)
        else:
            # [ERROR] invalid cookies
            exception_message = "invalid cookies cookie={}".format(
                self.cookies)
            raise Exception(exception_message)
        self.queue = Queue(maxsize=1000)
        self.worker = ThreadPoolExecutor(max_workers=MAX_WORKERS)
        self.scheduler = BlockingScheduler({
            'apscheduler.executors.default': {
                'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
                'max_workers': '20'
            },
            'apscheduler.job_defaults.coalesce': 'false',
            'apscheduler.job_defaults.max_instances': '1000',
            'apscheduler.timezone': 'Asia/Shanghai',
        })
        self.webhook = WebHookAPI(access_token=DING_ACCESS_TOKEN,
                             secret_key=DING_SECRET_KEY)

        # 实例化这个类一次就把第一个cookie删掉
        self.orm_session.query(Cookie).filter(Cookie.id==cookieobj.id).delete()
        self.orm_session.commit()

        
    def wareBesiness(self, skuId, *args, **kwargs) -> dict:
        url = "http://api.m.jd.com/client.action"
        querystring = {"functionId": "wareBusiness", "clientVersion": "10.1.2", "build": "89743", "client": "android", "d_brand": "Google", "d_model": "Pixel3", "osVersion": "9", "screen": "2028*1080", "partner": "au_jddcqj010", "oaid": "", "eid": self.eid, "sdkVersion": "28", "lang": "zh_CN", "eu": "3353831323330383031393235383",
                       "fv": "23D2333623835346036663935383", "uuid": self.uuid, "aid": self.uuid, "networkType": "wifi", "wifiBssid": "unknown", "uts": "0f31TVRjBSspx2ZitN2ua13QZfhAntC5vKhhadjLR8wO3wx88aJNTw7wf8HYgCUhmQW5MG6GdpeDHWB40qGLB7xncizWeUTar2Y/LXcAiclHi6vTdCW6etCvnSzNILzYpwSRGU3+5HSkpOgK8Xpp/xPjGNz9+NVAjkdS6OWbJLcwsI+A72dtyO5QGvzfa+V8pyrPi6ct6vSYdaR7Tbq6xw==", "uemps": "0-0", "harmonyOs": "0", "scval": skuId}
        payload = "body=%7B%22abTest800%22%3Atrue%2C%22avoidLive%22%3Afalse%2C%22brand%22%3A%22google%22%2C%22cityId%22%3A0%2C%22cpsNoTuan%22%3Anull%2C%22darkModelEnum%22%3A3%2C%22districtId%22%3A0%2C%22eventId%22%3A%22Shopcart_Productid%22%2C%22fromType%22%3A0%2C%22isDesCbc%22%3Atrue%2C%22latitude%22%3A%220.0%22%2C%22lego%22%3Atrue%2C%22longitude%22%3A%220.0%22%2C%22model%22%3A%22Pixel+3%22%2C%22ocrFlag%22%3Afalse%2C%22pluginVersion%22%3A101020%2C%22plusClickCount%22%3A0%2C%22plusLandedFatigue%22%3A0%2C%22provinceId%22%3A%220%22%2C%22skuId%22%3A%22" + \
            skuId+"%22%2C%22source_type%22%3A%22shoppingCart_pack%22%2C%22source_value%22%3A%22%22%2C%22townId%22%3A0%2C%22uAddrId%22%3A%220%22%2C%22utmMedium%22%3Anull%7D&"
        headers = {
            'cookie': self.cookies,
            'user-agent': "okhttp/3.12.1;jdmall;android;version/10.1.2;build/89743;screen/1080x2028;os/9;network/wifi;",
            'jdc-backup': self.cookies,
            'host': "api.m.jd.com",
            'charset': "UTF-8",
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
        }
        body_match = re.match("body=(.*?)&", payload)
        body = body_match.group(1)
        params_dict = self.getSign(
            funcType="wareBusiness", body=unquote(body), uuid=self.uuid)
        querystring.update(params_dict)
        response = requests.request(
            "POST", url, data=payload, headers=headers, params=querystring)
        if False:
            with open("{}.json".format(skuId), "w", encoding="utf8") as f:
                f.write(response.text)
        return response.json()

    def cart_data_info(self, data: dict) -> list:
        vendors_query = "$.cartInfo.vendors[*]"
        vendors = jsonpath(data, vendors_query)
        products = []
        for vendor in vendors:
            for sort_item in vendor.get("sorted"):
                sitems = sort_item["item"].get("items")
                if sitems:
                    for sitem in sitems:
                        # print(sitem)
                        Name = sitem["item"]["Name"]
                        PriceShow = sitem["item"].get("PriceShow") or sitem["item"].get("priceRevert")
                        Price = sitem["item"]["Price"]
                        Id = sitem["item"]["Id"]
                        stockState = sitem["item"]["stockState"]
                        ProductDetail = "https://item.jd.com/{}.html".format(
                            Id)
                        products.append({
                            "PriceShow": PriceShow,
                            "Price": Price,
                            "Name": Name,
                            "Id": Id,
                            "stockState": stockState,
                            "ProductDetail": ProductDetail
                        })
                else:
                    # JD PLUS VIP
                    PriceShow = sort_item["item"]["PriceShow"]
                    Price = sort_item["item"]["Price"]
                    Name = sort_item["item"]["Name"]
                    Id = sort_item["item"]["Id"]
                    stockState = sort_item["item"]["stockState"]
                    ProductDetail = "https://item.jd.com/{}.html".format(Id)
                    products.append({
                        "Name": Name,
                        "Price": Price,
                        "PriceShow": PriceShow,
                        "stockState": stockState,
                        "Id": Id,
                        "ProductDetail": ProductDetail
                    })
        return products

    def product_details(self, data: dict) -> str:
        # 普通商品
        # 闪购商品
        general_product = jsonpath(data, "$..handPriceBanner")
        # 预约商品  【预约】
        # 秒杀商品
        # 预售商品 【缴纳定金】
        subscribe_product = jsonpath(
            data, "$..preferentialGuide.vipJumpType")  # vipJumpType:2
        if general_product:
            result = ""
            coupon_price = jsonpath(
                data, "$..handPriceBanner.couponDctMap.price")
            coupon_text = jsonpath(
                data, "$..handPriceBanner.couponDctMap.text")
            promotion_price = jsonpath(
                data, "$..handPriceBanner.promotionDctMap.price")
            promotion_text = jsonpath(
                data, "$..handPriceBanner.promotionDctMap.text")
            if all([coupon_price, coupon_text]):
                result += "{}:{}\n".format(coupon_text.pop(),
                                           coupon_price.pop())
            if all([promotion_price, promotion_text]):
                result += "{}:{}\n".format(promotion_text.pop(),
                                           promotion_price.pop())
            return result
        elif subscribe_product:
            actives = []
            texts = jsonpath(
                data, "$..preferentialGuide.promotion.activity[*].text")
            values = jsonpath(
                data, "$..preferentialGuide.promotion.activity[*].value")
            for tv in zip(texts, values):
                if "返豆" in tv[-1]:
                    continue
                if "换购" in tv[-1]:
                    continue
                if "限购" in tv[0]:
                    continue
                actives.append("{}:{}\n".format(*tv))
            if not actives:
                texts = jsonpath(
                    data, "$..promotion.bestProList[*].value") or []
                values = jsonpath(
                    data, "$..preferentialGuide.couponInfo[*].discountText") or []
                texts = set(texts)
                values = set(values)
                return "商品活动:{}\n优惠券:{}\n".format(",".join(texts), ",".join(map(lambda x: x.replace("以下商品可使用", ""), values)))
            return "商品活动:{}\n".format(",".join(actives))
        # TODO:无商品活动
        else:
            return "商品活动:\n优惠券:\n"

    def getSign(self, **kwargs) -> str:
        """
        params:  cart {"addressId":"0","appleCare":0,"businessId":"","cartBundleVersion":"10120","cartRequestType":12,"cartuuid":"c8045df7-eefa-4a39-9b77-40fd9852bf91","coord_type":"","cvhv":"213724367249618","hitNewUIStatus":1,"homeWishListUserFlag":"2","latitude":"0.0","longitude":"0.0","mqTriggerStatus":"0","showPlusEntry":"2","syntype":"1","updateTag":false,"userType":"1"} a8dfc48a8def7b4f android 10.1.2
        getSignFromJni:  st=1644849012681&sign=556f786aeb89e56762c1f1c10d150aba&sv=101
        """
        funcType = kwargs.get("funcType")
        body = kwargs.get("body")
        uuid = kwargs.get("uuid")
        resp = requests.get(UNIDBG_SIGN_API.format(funcType, uuid, body))
        resp_data = resp.json()
        sign = resp_data.get("sign")
        return dict(parse_qsl(sign))

    def cartInfo(self, *args, **kwargs):
        url = "http://api.m.jd.com/client.action"
        querystring = {"functionId": "cart", "clientVersion": "10.1.2", "build": "89743", "client": "android", "d_brand": "Google", "d_model": "Pixel3", "osVersion": "9", "screen": "2028*1080", "partner": "au_jddcqj010", "oaid": "", "eid": self.eid, "sdkVersion": "28", "lang": "zh_CN",
                       "eu": "3353831323330393031393235383", "fv": "23D2333623836346036663935383", "uuid": self.uuid, "aid": self.uuid, "networkType": "wifi", "wifiBssid": "unknown", "uts": "0f31TVRjBSvoFB9T2pZwlRNwdkBbq8pt+f7VJQIU+TidTwvvhlRKXIsoR3NP11HXOxTB+/7BVGjRRxcPXY2ZazAv5lOq1MRbjhbX0HewgSlqHXedaPBxxggnpS5VhoPXn+N1Cxy9uSBE1wF5OsvF1Scu1ZZ4Dm5/yHvqTm/p1ut9uQ0flmVyN5BdoFszm4iEG86iw6hgNmtVIHWs7DafQg==", "uemps": "0-0", "harmonyOs": "0"}
        payload = "body=%7B%22addressId%22%3A%220%22%2C%22appleCare%22%3A0%2C%22businessId%22%3A%22%22%2C%22cartBundleVersion%22%3A%2210120%22%2C%22cartRequestType%22%3A12%2C%22cartuuid%22%3A%22{}%22%2C%22coord_type%22%3A%22%22%2C%22cvhv%22%3A%22{}%22%2C%22hitNewUIStatus%22%3A1%2C%22homeWishListUserFlag%22%3A%222%22%2C%22latitude%22%3A%22{}%22%2C%22longitude%22%3A%22%{}22%2C%22mqTriggerStatus%22%3A%220%22%2C%22showPlusEntry%22%3A%222%22%2C%22syntype%22%3A%221%22%2C%22updateTag%22%3Afalse%2C%22userType%22%3A%221%22%7D&".format(
            self.cartuuid, self.cvhv, self.latitude, self.longitude)

        # pin=jd_70d9ec2acb99a;wskey=AAJiCcJLAEBHyuNO-45nknVjG3eDDFgULn_4b3RTEuEsy7JLwtbDAYFIZJx_Rwqa-0nVjbMJYKOPV7hhxQuOdqHJvKa2MloA;whwswswws=yuNirsyci2_G3jD43XLRwYZupG4GUqBeqM91lbZmpsirfZZmGLIayQZNxsQJWas6UxqkbpK7UthZriC0i-dyfTxt0gCL6Haky9dJJPyjVOOM;unionwsws={"devicefinger":"eidA3683812337s1sJTwGtEvRnShhTRuZcwwQbCU8Zm1vvezHOW97ARksEpJRsVj6c1EhG00i9g1csVXaQb+pizpyF\/QYUXYvrqpzBmXtf3RJS0G23ZZ","jmafinger":"yuNirsyci2_G3jD43XLRwYZupG4GUqBeqM91lbZmpsirfZZmGLIayQZNxsQJWas6UxqkbpK7UthZriC0i-dyfTxt0gCL6Haky9dJJPyjVOOM"};
        headers = {
            'cookie': self.cookies,
            'user-agent': "okhttp/3.12.1;jdmall;android;version/10.1.2;build/89743;screen/1080x2028;os/9;network/wifi;",
            'jdc-backup': self.cookies,
            'host': "api.m.jd.com",
            'charset': "UTF-8",
            'accept-encoding': "br,gzip,deflate",
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
            'connection': "keep-alive"
        }
        body_match = re.match("body=(.*?)&", payload)
        body = body_match.group(1)
        params_dict = self.getSign(
            funcType="cart", body=unquote(body), uuid=self.uuid)
        querystring.update(params_dict)
        try:
            response = requests.request(
                "POST", url, data=payload, headers=headers, params=querystring)
        except Exception as e:
            print(str(e))
        else:
            data_json = response.json()
            code = data_json.get("code")
            if code == "600":
                print("echo:{}".format(data_json.get("echo")))
            else:
                print("code: ", code)
                return data_json

    def message_compose(self, data_info: dict, product_details_str: str) -> str:
        # 活动变更\新增商品
        # TODO sqlite里面查不到数据就去，新增商品。指纹配对不成功则是活动变更。
        message = ""
        skuid_exists = self.orm_session.query(exists().where(ProductInfo.sku==data_info["Id"])).scalar()
        print("skuid_exists:",skuid_exists)
        _hash = ProductInfo.hash(data_info["Id"],
        data_info["Name"],data_info["stockState"],
        data_info["ProductDetail"],data_info["PriceShow"],
        data_info["Price"],product_details_str)
        print("product info hash:{}".format(_hash))
        if not skuid_exists:
            # 如果不存在该SKU的商品,状态为新增
            message = "新增商品:{}\n购物车价格:{}\n原始价格:{}\n商品库存:{}\n商品sku:{}\n{}链接:{}\n历史低价:{}\n\n\n数据获取时间:{}\n区域:湖南常德市".format(data_info["Name"],
                                                                                                                    data_info["PriceShow"],
                                                                                                                    data_info["Price"],
                                                                                                                    data_info["stockState"],
                                                                                                                    data_info["Id"],
                                                                                                                    product_details_str,
                                                                                                                    data_info["ProductDetail"],
                                                                                                                    data_info["PriceShow"],
                                                                                                                    datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))

            pinfo = ProductInfo(sku=data_info["Id"],name=data_info["Name"],
            stock_state=data_info["stockState"],detail=data_info["ProductDetail"],
            min_price=data_info["PriceShow"],max_price=data_info["Price"],
            activate_info=product_details_str,fp=_hash)
            self.orm_session.add(pinfo)
        else:
            # 如果存在该商品，需要校验指纹
            obj = self.orm_session.query(ProductInfo).filter(ProductInfo.sku==data_info["Id"]).first()
            if ne(obj.fp,_hash):
                message = "活动变更:{}\n购物车价格:{}\n原始价格:{}\n商品库存:{}\n商品sku:{}\n{}链接:{}\n历史低价:{}\n\n\n数据获取时间:{}\n区域:湖南常德市".format(data_info["Name"],
                                                                                                                    data_info["PriceShow"],
                                                                                                                    data_info["Price"],
                                                                                                                    data_info["stockState"],
                                                                                                                    data_info["Id"],
                                                                                                                    product_details_str,
                                                                                                                    data_info["ProductDetail"],
                                                                                                                    data_info["PriceShow"],
                                                                                                                   datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S"))
            else:
                # 存在该商品，校验指纹相同不做任何操作
                pass
        self.orm_session.commit()
        return message

    def executor(self):
        jdcart_info_data = self.cartInfo()
        infos = self.cart_data_info(jdcart_info_data)
        ids_generator = list(map(lambda x: partial(
            dict.__getitem__, x)("Id"), infos))
        besiness_info_generator = self.worker.map(
            self.wareBesiness, ids_generator)
        details = []
        for besiness in besiness_info_generator:
            details.append(self.product_details(besiness))
        msgs = []
        for info,actinfo in zip(infos,details):
            msgs.append(self.message_compose(info,actinfo))
        for msg in msgs:
            if msg:
                self.queue.put(msg)

    def schedule(self):
        # self.executor()
        self.scheduler.add_job(self.executor, "interval", args=(), seconds=SCHEDULE_INTERVAL)
        self.scheduler.add_job(self.product_delive, "interval", args=(), seconds=ORDER_INTERVAL)

    def run(self):
        self.worker.submit(self.webhook.send_loop, self.queue, self.worker)
        self.schedule()
        try:
            self.scheduler.start()
        except(SystemExit, KeyboardInterrupt) as error:
            self.scheduler.shutdown(True)
        else:
            self.scheduler.shutdown(True)


    # TODO 检查待收货订单状态
    def product_delive(self):
        res_dict = self.wait4DeliveryAll()
        orders = self.worker.map(self.orderTrackBusiness,[orderitem.get("orderid") for orderitem in res_dict])
        # indexs = []
        # NOTE 模拟索引为1的存在收获
        indexs = []
        for _index,ele in enumerate(map(self.discernOrderTrack,orders)):
            if ele:
                indexs.append(_index)
        items = []
        for index in indexs:
            if isinstance(res_dict[index].get("sku"),list):
                items.extend(res_dict[index].get("sku"))
            else:
                items.append(res_dict[index].get("sku"))
        # 查询items里面的所有sku
        for sku in items:
            ds = datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
            model_item = self.orm_session.query(ProductInfo).filter(ProductInfo.sku==sku).first()
            if model_item:
                message = f"商品到货:{model_item.name}\n购物车价格:{model_item.min_price}\n原始价格:{model_item.max_price}\n商品库存:{model_item.stock_state}\n商品sku:{model_item.sku}\n{model_item.activate_info}链接:{model_item.detail}\n历史低价:{model_item.min_price}\n\n\n数据获取时间:{ds}\n区域:湖南常德市"
                self.webhook.message(message)
            else:
                pass
        self.orm_session.commit()
    # 订单跟踪
    # TODO 到货关键字："已配送"
    # TODO 1.京东快递
    #      2.普通快递 【例如：话费、游戏点卡类网络类的产品是不能通过关键字来判断是否收货】
    def orderTrackBusiness(self, orderId):
        url = "https://api.m.jd.com/client.action"
        querystring = {"functionId": "orderTrackBusiness", "clientVersion": "10.1.2", "build": "89743", "client": "android", "d_brand": "Google", "d_model": "Pixel3", "osVersion": "9", "screen": "2028*1080", "partner": "au_jddcqj010", "oaid": "", "eid": self.eid, "sdkVersion": "28", "lang": "zh_CN", "uuid": self.uuid,
                       "aid": self.uuid, "networkType": "wifi", "wifiBssid": "unknown", "uts": "0f31TVRjBSspx2ZitN2ua13QZfhAntC5vKhhadjLR8wO3wx88aJNTw7wf8HYgCUhmQW5MG6GdpeDHWB40qGLB7xncizWeUTar2Y/LXcAiclHi6vTdCW6etCvnSzNILzYpwSRGU3+5HSkpOgK8Xpp/xPjGNz9+NVAjkdS6OWbJLcwsI+A72dtyO5QGvzfa+V8pyrPi6ct6vSYdaR7Tbq6xw==", "uemps": "0-0", "harmonyOs": "0"}
        payload = "body=%7B%22bigTrack%22%3A%221%22%2C%22orderId%22%3A%22{}%22%2C%22packageCode%22%3A%22%22%2C%22plugin_version%22%3A101002%2C%22showMap%22%3A%220%22%7D&".format(
            orderId)
        headers = {
            'cookie': self.cookies,
            'user-agent': "okhttp/3.12.1;jdmall;android;version/10.1.2;build/89743;screen/1080x2028;os/9;network/wifi;",
            'jdc-backup': self.cookies,
            'host': "api.m.jd.com",
            'charset': "UTF-8",
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
        }
        body_match = re.match("body=(.*?)&", payload)
        body = body_match.group(1)
        params_dict = self.getSign(
            funcType="orderTrackBusiness", body=unquote(body), uuid=self.uuid)
        querystring.update(params_dict)
        response = requests.request(
            "POST", url, data=payload, headers=headers, params=querystring)
        if DEBUG:
            print(dumps(response.json(), ensure_ascii=False))
        return response.json()
        pass

    # 请求->订单列表
    # def wait4Delivery(self, page=1, passData='') -> dict:
        # passData ==> '' 默认为第一页
        # if passData:
        #     passData = repr(passData)[1:-1].replace("'", '\"') + "%2C"  # %2C ==> ,
    def wait4Delivery(self, page=1) -> dict:

        url = "https://api.m.jd.com/client.action"
        querystring = {"functionId": "wait4Delivery", "clientVersion": "10.1.2", "build": "89743", "client": "android", "d_brand": "Google", "d_model": "Pixel3", "osVersion": "9", "screen": "2028*1080", "partner": "au_jddcqj010", "oaid": "", "eid": self.eid, "sdkVersion": "28", "lang": "zh_CN", "uuid": self.uuid, "aid": self.uuid,
                       "networkType": "wifi", "wifiBssid": "unknown", "uts": "0f31TVRjBSspx2ZitN2ua13QZfhAntC5vKhhadjLR8wO3wx88aJNTw7wf8HYgCUhmQW5MG6GdpeDHWB40qGLB7xncizWeUTar2Y/LXcAiclHi6vTdCW6etCvnSzNILzYpwSRGU3+5HSkpOgK8Xpp/xPjGNz9+NVAjkdS6OWbJLcwsI+A72dtyO5QGvzfa+V8pyrPi6ct6vSYdaR7Tbq6xw==", "uemps": "0-0", "harmonyOs": "0"}
        # 访问订单页首页
        payload = "body=%7B%22deis%22%3A%22dy%22%2C%22phcre%22%3A%22v%22%2C%22newUiSwitch%22%3A%221%22%2C%22page%22%3A%22"+ str(page) +"%22%2C%22pagesize%22%3A%2210%22%2C%22plugin_version%22%3A101002%7D&"
        headers = {
            'cookie': self.cookies,
            'user-agent': "okhttp/3.12.1;jdmall;android;version/10.1.2;build/89743;screen/1080x2028;os/9;network/wifi;",
            'jdc-backup': self.cookies,
            'host': "api.m.jd.com",
            'charset': "UTF-8",
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
        }
        body_match = re.match("body=(.*?)&", payload)
        body = body_match.group(1)
        params_dict = self.getSign(
            funcType="wait4Delivery", body=unquote(body), uuid=self.uuid)
        querystring.update(params_dict)
        response = requests.request(
            "POST", url, data=payload, headers=headers, params=querystring)
        if DEBUG:
            print(dumps(response.json(), ensure_ascii=False))
        return response.json()
    # 提取 -> 订单列表

    def extractWaitOrderList(self, data: dict) -> dict: 
        # 待收货query
        # $.orderList[*].stepFloor.eventData.pageParam
        res_dict = {}
        # 产品SKUs
        # NOTE 其实用jsonpath的解析方式不够好
        order_root = jsonpath(data, "$.orderList[*]") or []
        return_list = []
        for order_data in order_root:
            item = {}
            orderId = order_data.get("orderId")
            item["orderid"] = orderId
            skuids = jsonpath(order_data, "$.orderMsg")
            for skuid in skuids:
                wareInfolist = skuid.get("wareInfoList")
                if wareInfolist and len(wareInfolist) > 1:
                    skuIds = []
                    for winfo in wareInfolist:
                        skuId = winfo.get("wareId")
                        skuIds.append(skuId)
                    item['sku'] = skuIds
                elif wareInfolist:
                    for winfo in wareInfolist:
                        skuId = winfo.get("wareId")
                        item['sku'] = skuId
            # 订单收货状态
            order_state = jsonpath(
                order_data, "$.stepFloor.eventData.pageParam") or []
            if order_state:
                item['state'] = order_state.pop()
            else:
                item['state'] = ''
            return_list.append(item)
            # [{'orderid': '239202976519', 'sku': '100027423982', 'state': '待收货'}, {'orderid': '239202955911', 'sku': '100030182178', 'state': '待收货'}, {'orderid': '236383136593', 'sku': '100016514282', 'state': '待收货'}, {'orderid': '239202900678', 'sku': '100004914551', 'state': '待收货'}, {'orderid': '236380997776', 'sku': '100008885238', 'state': '待收货'}, {'orderid': '239199763594', 'sku': ['100008885238', '100009254925'], 'state': '待收货'}, {'orderid': '239199533095', 'sku': '7919366', 'state': '待收货'}, {'orderid': '239201059238', 'sku': '8132725', 'state': '待收货'}, {'orderid': '236379853137', 'sku': '100023821194', 'state': '待收货'}, {'orderid': '236376522550', 'sku': ['100008885238', '100009254925'], 'state': '待收货'}]
        #
        pass_ = jsonpath(data, "$.pass")
        if pass_:
            res_dict['pass'] = pass_.pop()
        res_dict['data'] = return_list
        # TODO 待收货JSON信息返回
        # {'pass': '{"datas":{},"sig":"AEF251E70A","timestamp":1645177700201,"uuid":"3d0c54a2-9e2c-4fab-ac16-ce241ca544bf"}', 'data': [{'orderid': '239202976519', 'sku': '100027423982', 'state': '待收货'}, {'orderid': '239202955911', 'sku': '100030182178', 'state': '待收货'}, {'orderid': '236383136593', 'sku': '100016514282', 'state': '待收货'}, {'orderid': '239202900678',
        # 'sku': '100004914551', 'state': '待收货'}, {'orderid': '236380997776', 'sku': '100008885238', 'state': '待收货'}, {'orderid': '239199763594', 'sku': ['100008885238', '100009254925'],
        # 'state': '待收货'}, {'orderid': '239199533095', 'sku': '7919366', 'state': '待收货'}, {'orderid': '239201059238', 'sku': '8132725', 'state': '待收货'}, {'orderid': '236379853137', 'sku': '100023821194', 'state': '待收货'}, {'orderid': '236376522550', 'sku': ['100008885238', '100009254925'], 'state': '待收货'}]}
        return res_dict

    # 识别订单跟踪是否收货
    def discernOrderTrack(self, json_data: dict) -> bool:
        # 获取订单快递类型
        query = "$.floors[*].data.orderInfoMap.extTagList[0].value"
        express_types = jsonpath(json_data, query)
        if express_types:
            express_type = express_types.pop()
            print("express type -----> ", express_type)
            jsonstr = str(json_data)
            if eq(express_type, "京东快递"):
                # 京东快递识别处理
                if "已完成配送" in jsonstr:
                    return True
            else:
                # 普通快递、或其他渠道的快递
                if eq(express_type, "普通快递"):
                    # TODO 网络充值类一律视为已收货
                    if "已完成配送" in jsonstr:
                        return True
                else:
                    if "已完成配送" in jsonstr:
                        return True
            return False
        else:
            raise Exception(
                "express_types not get,jsonpath query:{}".format(repr(query)))
    # 请求 -> 所有订单列表
    def wait4DeliveryAll(self):
        page = 1
        orderdatas = []
        while True:
            waitOrderJson = self.wait4Delivery(page)
            if not waitOrderJson.get("orderListCount"):
                return orderdatas
            orderdata = self.extractWaitOrderList(waitOrderJson)
            orderdatas.extend(orderdata.get("data"))
            page += 1



# 测试待收货订单号第一页全部结果
def test_extractOrderList():
    from json import load
    with open("test/json/order-1.json", encoding='utf8') as f:
        jdcart = JDCartMonitor()
        print(jdcart.extractWaitOrderList(load(f)))


# 多进程启动购物车、待收货订单监控
def reflect_call(obj:JDCartMonitor):
    run_fun = getattr(obj,"run")
    print(run_fun)
    run_fun()
    
def process_launcher():
    from multiprocessing import Process
    orm_session = sessionmaker(engine)()
    # cookies = orm_session.query(Cookie).all()
    cookies = range(2)
    ps = []
    for cookie in cookies:
        c = cookie.compose_cookie()
        print(c)
        p = Process(target=reflect_call,args=(JDCartMonitor(cookies=c),))
        p.start()
        ps.append(p)

    for w in ps:
        w.join()