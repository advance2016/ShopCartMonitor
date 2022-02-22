import requests

url = "http://api.m.jd.com/client.action"

querystring = {"functionId":"cart","clientVersion":"10.1.2","build":"89743","client":"android","d_brand":"Google","d_model":"Pixel3","osVersion":"9","screen":"2028*1080","partner":"au_jddcqj010","oaid":"","eid":"eidA3683812337s1sJTwGtEvRnShhTRuZcwwQbCU8Zm1vvezHOW97ARksEpJRsVj6c1EhG00i9g1csVXaQb pizpyF/QYUXYvrqpzBmXtf3RJS0G23ZZ","sdkVersion":"28","lang":"zh_CN","eu":"3353831323330393031393235383","fv":"23D2333623836346036663935383","uuid":"a8dfc48a8def7b4f","aid":"a8dfc48a8def7b4f","networkType":"wifi","wifiBssid":"unknown","uts":"0f31TVRjBSvoFB9T2pZwlRNwdkBbq8pt+f7VJQIU+TidTwvvhlRKXIsoR3NP11HXOxTB+/7BVGjRRxcPXY2ZazAv5lOq1MRbjhbX0HewgSlqHXedaPBxxggnpS5VhoPXn+N1Cxy9uSBE1wF5OsvF1Scu1ZZ4Dm5/yHvqTm/p1ut9uQ0flmVyN5BdoFszm4iEG86iw6hgNmtVIHWs7DafQg==","uemps":"0-0","harmonyOs":"0","st":"1644826678093","sign":"c864d09040c8d755556c6ca496a2bd4c","sv":"122"}

payload = "body=%7B%22addressId%22%3A%220%22%2C%22appleCare%22%3A0%2C%22businessId%22%3A%22%22%2C%22cartBundleVersion%22%3A%2210120%22%2C%22cartRequestType%22%3A12%2C%22cartuuid%22%3A%2216633281-e33a-4c28-a2e0-c4d107b570e2%22%2C%22coord_type%22%3A%22%22%2C%22cvhv%22%3A%22213724367249618%22%2C%22hitNewUIStatus%22%3A1%2C%22homeWishListUserFlag%22%3A%222%22%2C%22latitude%22%3A%2230.199258%22%2C%22longitude%22%3A%22120.231404%22%2C%22mqTriggerStatus%22%3A%220%22%2C%22showPlusEntry%22%3A%222%22%2C%22syntype%22%3A%221%22%2C%22updateTag%22%3Afalse%2C%22userType%22%3A%221%22%7D&"
headers = {
    'cookie': 'pin=jd_70d9ec2acb99a;wskey=AAJiCcJLAEBHyuNO-45nknVjG3eDDFgULn_4b3RTEuEsy7JLwtbDAYFIZJx_Rwqa-0nVjbMJYKOPV7hhxQuOdqHJvKa2MloA;whwswswws=yuNirsyci2_G3jD43XLRwYZupG4GUqBeqM91lbZmpsirfZZmGLIayQZNxsQJWas6UxqkbpK7UthZriC0i-dyfTxt0gCL6Haky9dJJPyjVOOM;unionwsws={"devicefinger":"eidA3683812337s1sJTwGtEvRnShhTRuZcwwQbCU8Zm1vvezHOW97ARksEpJRsVj6c1EhG00i9g1csVXaQb+pizpyF\/QYUXYvrqpzBmXtf3RJS0G23ZZ","jmafinger":"yuNirsyci2_G3jD43XLRwYZupG4GUqBeqM91lbZmpsirfZZmGLIayQZNxsQJWas6UxqkbpK7UthZriC0i-dyfTxt0gCL6Haky9dJJPyjVOOM"};',
    'user-agent': "okhttp/3.12.1;jdmall;android;version/10.1.2;build/89743;screen/1080x2028;os/9;network/wifi;",
    'jdc-backup': 'pin=jd_70d9ec2acb99a;wskey=AAJiCcJLAEBHyuNO-45nknVjG3eDDFgULn_4b3RTEuEsy7JLwtbDAYFIZJx_Rwqa-0nVjbMJYKOPV7hhxQuOdqHJvKa2MloA;whwswswws=yuNirsyci2_G3jD43XLRwYZupG4GUqBeqM91lbZmpsirfZZmGLIayQZNxsQJWas6UxqkbpK7UthZriC0i-dyfTxt0gCL6Haky9dJJPyjVOOM;unionwsws={"devicefinger":"eidA3683812337s1sJTwGtEvRnShhTRuZcwwQbCU8Zm1vvezHOW97ARksEpJRsVj6c1EhG00i9g1csVXaQb+pizpyF\/QYUXYvrqpzBmXtf3RJS0G23ZZ","jmafinger":"yuNirsyci2_G3jD43XLRwYZupG4GUqBeqM91lbZmpsirfZZmGLIayQZNxsQJWas6UxqkbpK7UthZriC0i-dyfTxt0gCL6Haky9dJJPyjVOOM"};',
    'host': "api.m.jd.com",
    'charset': "UTF-8",
    'accept-encoding': "br,gzip,deflate",
    'cache-control': "no-cache",
    'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
    'connection': "keep-alive"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.content)