import requests

url = "https://api.m.jd.com/client.action"

querystring = {"functionId":"wait4Delivery","clientVersion":"10.1.2","build":"89743","client":"android","d_brand":"Google","d_model":"Pixel3","osVersion":"9","screen":"2028*1080","partner":"au_jddcqj010","oaid":"","eid":"eidAd0c08122c3s6QG1L7AORS7Kh0aKLdhclPEBtTWrtm3 grbZCKZw7L2q8RHX4bxCsjndpfuCYaOwvBEz5tbGbmy6bsIUgqAfzH/ED1IpUz4qVtxVI","sdkVersion":"28","lang":"zh_CN","uuid":"5de1feb3343360ff","aid":"5de1feb3343360ff","area":"15_1213_3038_59931","networkType":"wifi","wifiBssid":"e34dcfaa4b294b9bc5252c831e48fd87","uts":"0f31TVRjBSsqndu4/jgUPz6uymy50MQJgKD9MPeBMiHlC6TOSr2LRJapxK0f5hWlcyjHLHYMGVHYlnwZngaA0/4kqAmhhpHlcLOYO9CEd3pQsQJZps9y3WShOjeA/OhbC1D54tOR9fYL+B6O7pCDbUeH/vkGq39MCZI0l6anmTQnHQqOX47SlCkga/kHtE1KrTVqZHnMs+zbrIgeYckoFA==","uemps":"0-0","harmonyOs":"0","st":"1645176491951","sign":"e47b1f19657365c3c252a292256d5260","sv":"120"}

payload = "body=%7B%22deis%22%3A%22dy%22%2C%22phcre%22%3A%22v%22%2C%22newUiSwitch%22%3A%221%22%2C%22page%22%3A%221%22%2C%22pagesize%22%3A%2210%22%2C%22pass%22%3A%22%7B%5C%22datas%5C%22%3A%7B%7D%2C%5C%22sig%5C%22%3A%5C%22FA3A301B75%5C%22%2C%5C%22timestamp%5C%22%3A1645175686014%2C%5C%22uuid%5C%22%3A%5C%221592a949-5199-41dc-b964-6c187b9fbc6c%5C%22%7D%22%2C%22plugin_version%22%3A101002%7D&"
headers = {
    'cookie': 'pin=432522ZMD168;wskey=AAJiD15ZAEDkTd8SYwYyQn1rwo3lIRTL0WajPVRtSMABrXQONPJ-UfT3M-dFIdpnkXPV7C2DzXPTB1aCWyjPQ1Z8kWWUEH2U;whwswswws=fuNirsyci2_G3jD43XLRwYQR7QNMfsN7i8VSiDZQUw_IWektzah5Si6WtfvUB53pmcPSfW2s1_ZRiYqvKjElKLlT5BiVyXR-jBqukMQ8a_zQ;unionwsws={"devicefinger":"eidAd0c08122c3s6QG1L7AORS7Kh0aKLdhclPEBtTWrtm3+grbZCKZw7L2q8RHX4bxCsjndpfuCYaOwvBEz5tbGbmy6bsIUgqAfzH\/ED1IpUz4qVtxVI","jmafinger":"fuNirsyci2_G3jD43XLRwYQR7QNMfsN7i8VSiDZQUw_IWektzah5Si6WtfvUB53pmcPSfW2s1_ZRiYqvKjElKLlT5BiVyXR-jBqukMQ8a_zQ"};',
    'user-agent': "okhttp/3.12.1;jdmall;android;version/10.1.2;build/89743;screen/1080x2028;os/9;network/wifi;",
    'charset': "UTF-8",
    'jdc-backup': 'pin=432522ZMD168;wskey=AAJiD15ZAEDkTd8SYwYyQn1rwo3lIRTL0WajPVRtSMABrXQONPJ-UfT3M-dFIdpnkXPV7C2DzXPTB1aCWyjPQ1Z8kWWUEH2U;whwswswws=fuNirsyci2_G3jD43XLRwYQR7QNMfsN7i8VSiDZQUw_IWektzah5Si6WtfvUB53pmcPSfW2s1_ZRiYqvKjElKLlT5BiVyXR-jBqukMQ8a_zQ;unionwsws={"devicefinger":"eidAd0c08122c3s6QG1L7AORS7Kh0aKLdhclPEBtTWrtm3+grbZCKZw7L2q8RHX4bxCsjndpfuCYaOwvBEz5tbGbmy6bsIUgqAfzH\/ED1IpUz4qVtxVI","jmafinger":"fuNirsyci2_G3jD43XLRwYQR7QNMfsN7i8VSiDZQUw_IWektzah5Si6WtfvUB53pmcPSfW2s1_ZRiYqvKjElKLlT5BiVyXR-jBqukMQ8a_zQ"};',
    'cache-control': "no-cache",
    'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
    'host': "api.m.jd.com"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)
