import requests

url = "https://api.m.jd.com/client.action"

querystring = {"functionId":"orderTrackBusiness","clientVersion":"10.1.2","build":"89743","client":"android","d_brand":"Google","d_model":"Pixel3","osVersion":"9","screen":"2028*1080","partner":"au_jddcqj010","oaid":"","eid":"eidAd0c08122c3s6QG1L7AORS7Kh0aKLdhclPEBtTWrtm3 grbZCKZw7L2q8RHX4bxCsjndpfuCYaOwvBEz5tbGbmy6bsIUgqAfzH/ED1IpUz4qVtxVI","sdkVersion":"28","lang":"zh_CN","uuid":"5de1feb3343360ff","aid":"5de1feb3343360ff","networkType":"wifi","uts":"0f31TVRjBSspx2ZitN2ua13QZfhAntC5vKhhadjLR8wO3wx88aJNTw7wf8HYgCUhmQW5MG6GdpeDHWB40qGLB7xncizWeUTar2Y/LXcAiclHi6vTdCW6etCvnSzNILzYpwSRGU3+5HSkpOgK8Xpp/xPjGNz9+NVAjkdS6OWbJLcwsI+A72dtyO5QGvzfa+V8pyrPi6ct6vSYdaR7Tbq6xw==","uemps":"0-0","harmonyOs":"0","st":"1645175560692","sign":"3b4439b2d01b28417c48567308be86e4","sv":"122"}

payload = "body=%7B%22bigTrack%22%3A%221%22%2C%22orderId%22%3A%22239199533095%22%2C%22packageCode%22%3A%22%22%2C%22plugin_version%22%3A101002%2C%22showMap%22%3A%220%22%7D&"
headers = {
    'cookie': 'pin=432522ZMD168;wskey=AAJiD15ZAEDkTd8SYwYyQn1rwo3lIRTL0WajPVRtSMABrXQONPJ-UfT3M-dFIdpnkXPV7C2DzXPTB1aCWyjPQ1Z8kWWUEH2U;whwswswws=fuNirsyci2_G3jD43XLRwYQR7QNMfsN7i8VSiDZQUw_IWektzah5Si6WtfvUB53pmcPSfW2s1_ZRiYqvKjElKLlT5BiVyXR-jBqukMQ8a_zQ;unionwsws={"devicefinger":"eidAd0c08122c3s6QG1L7AORS7Kh0aKLdhclPEBtTWrtm3+grbZCKZw7L2q8RHX4bxCsjndpfuCYaOwvBEz5tbGbmy6bsIUgqAfzH\/ED1IpUz4qVtxVI","jmafinger":"fuNirsyci2_G3jD43XLRwYQR7QNMfsN7i8VSiDZQUw_IWektzah5Si6WtfvUB53pmcPSfW2s1_ZRiYqvKjElKLlT5BiVyXR-jBqukMQ8a_zQ"};',
    'user-agent': "okhttp/3.12.1;jdmall;android;version/10.1.2;build/89743;screen/1080x2028;os/9;network/wifi;",
    'jdc-backup': 'pin=432522ZMD168;wskey=AAJiD15ZAEDkTd8SYwYyQn1rwo3lIRTL0WajPVRtSMABrXQONPJ-UfT3M-dFIdpnkXPV7C2DzXPTB1aCWyjPQ1Z8kWWUEH2U;whwswswws=fuNirsyci2_G3jD43XLRwYQR7QNMfsN7i8VSiDZQUw_IWektzah5Si6WtfvUB53pmcPSfW2s1_ZRiYqvKjElKLlT5BiVyXR-jBqukMQ8a_zQ;unionwsws={"devicefinger":"eidAd0c08122c3s6QG1L7AORS7Kh0aKLdhclPEBtTWrtm3+grbZCKZw7L2q8RHX4bxCsjndpfuCYaOwvBEz5tbGbmy6bsIUgqAfzH\/ED1IpUz4qVtxVI","jmafinger":"fuNirsyci2_G3jD43XLRwYQR7QNMfsN7i8VSiDZQUw_IWektzah5Si6WtfvUB53pmcPSfW2s1_ZRiYqvKjElKLlT5BiVyXR-jBqukMQ8a_zQ"};',
    'host': "api.m.jd.com",
    'charset': "UTF-8",
    'cache-control': "no-cache",
    'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)