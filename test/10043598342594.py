import requests

url = "http://api.m.jd.com/client.action"

querystring = {"functionId":"wareBusiness","clientVersion":"10.1.2","build":"89743","client":"android","d_brand":"Google","d_model":"Pixel3","osVersion":"9","screen":"2028*1080","partner":"au_jddcqj010","oaid":"","eid":"eidAf3bd8122abscDxd5CXEySKen KlU3FRiIA8XeohosqFme5YQ6ZmFVLBf9V8rr2lxQEp5tbXp3mSU7sHoF8C afWknk4dZdbTOJMQvlPU2qmX9udH","sdkVersion":"28","lang":"zh_CN","eu":"3353831323330393031393235383","fv":"23D2333623836346036663935383","uuid":"a8dfc48a8def7b4f","aid":"a8dfc48a8def7b4f","area":"15_1213_3038_0","networkType":"wifi","wifiBssid":"unknown","uts":"0f31TVRjBSspx2ZitN2ua13QZfhAntC5vKhhadjLR8wO3wx88aJNTw7wf8HYgCUhmQW5MG6GdpeDHWB40qGLB7xncizWeUTar2Y/LXcAiclHi6vTdCW6etCvnSzNILzYpwSRGU3+5HSkpOgK8Xpp/xPjGNz9+NVAjkdS6OWbJLcwsI+A72dtyO5QGvzfa+V8pyrPi6ct6vSYdaR7Tbq6xw==","uemps":"0-0","harmonyOs":"0","scval":"10043598342594","st":"1645086531082","sign":"6df9409cc428055f76fd7b3cd2e6de5a","sv":"102"}


payload = "body=%7B%22abTest800%22%3Atrue%2C%22avoidLive%22%3Afalse%2C%22brand%22%3A%22google%22%2C%22cityId%22%3A0%2C%22cpsNoTuan%22%3Anull%2C%22darkModelEnum%22%3A3%2C%22districtId%22%3A0%2C%22eventId%22%3A%22Shopcart_Productid%22%2C%22fromType%22%3A0%2C%22isDesCbc%22%3Atrue%2C%22latitude%22%3A%220.0%22%2C%22lego%22%3Atrue%2C%22longitude%22%3A%220.0%22%2C%22model%22%3A%22Pixel+3%22%2C%22ocrFlag%22%3Afalse%2C%22pluginVersion%22%3A101020%2C%22plusClickCount%22%3A0%2C%22plusLandedFatigue%22%3A0%2C%22provinceId%22%3A%220%22%2C%22skuId%22%3A%2210043598342594%22%2C%22source_type%22%3A%22shoppingCart_pack%22%2C%22source_value%22%3A%22%22%2C%22townId%22%3A0%2C%22uAddrId%22%3A%220%22%2C%22utmMedium%22%3Anull%7D&"
headers = {
    'cookie': 'pin=jd_70d9ec2acb99a;wskey=AAJiCkYtAEDhPMfGHhZvhU5t48qUHrtfzW6JvShFOQLA2GJMZLoVMLxQdgcDLj7fjuHfCkMJJG2qaeG3GvkB-H9lqqpOP_8u;whwswswws=yuNirsyci2_G3jD43XLRwYZupG4GUqBeqM91lbZmpsirfZZmGLIayQZNxsQJWas6Upj2QWi0EPbeMQ9BN-kJb4ayPy4jbv1VuBWqT_OWeTCQ;unionwsws={"devicefinger":"eidAf3bd8122abscDxd5CXEySKen+KlU3FRiIA8XeohosqFme5YQ6ZmFVLBf9V8rr2lxQEp5tbXp3mSU7sHoF8C+afWknk4dZdbTOJMQvlPU2qmX9udH","jmafinger":"yuNirsyci2_G3jD43XLRwYZupG4GUqBeqM91lbZmpsirfZZmGLIayQZNxsQJWas6Upj2QWi0EPbeMQ9BN-kJb4ayPy4jbv1VuBWqT_OWeTCQ"};',
    'user-agent': "okhttp/3.12.1;jdmall;android;version/10.1.2;build/89743;screen/1080x2028;os/9;network/wifi;",
    'jdc-backup': 'pin=jd_70d9ec2acb99a;wskey=AAJiCkYtAEDhPMfGHhZvhU5t48qUHrtfzW6JvShFOQLA2GJMZLoVMLxQdgcDLj7fjuHfCkMJJG2qaeG3GvkB-H9lqqpOP_8u;whwswswws=yuNirsyci2_G3jD43XLRwYZupG4GUqBeqM91lbZmpsirfZZmGLIayQZNxsQJWas6Upj2QWi0EPbeMQ9BN-kJb4ayPy4jbv1VuBWqT_OWeTCQ;unionwsws={"devicefinger":"eidAf3bd8122abscDxd5CXEySKen+KlU3FRiIA8XeohosqFme5YQ6ZmFVLBf9V8rr2lxQEp5tbXp3mSU7sHoF8C+afWknk4dZdbTOJMQvlPU2qmX9udH","jmafinger":"yuNirsyci2_G3jD43XLRwYZupG4GUqBeqM91lbZmpsirfZZmGLIayQZNxsQJWas6Upj2QWi0EPbeMQ9BN-kJb4ayPy4jbv1VuBWqT_OWeTCQ"};',
    'connection': "Keep-Alive",
    'host': "api.m.jd.com",
    'charset': "UTF-8",
    'accept-encoding': "br,gzip,deflate",
    'cache-control': "no-cache",
    'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)