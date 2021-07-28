import json
import urllib.request


client_id = "KR2SGiYgWfN7l79DeNU8" # 개발자센터에서 발급받은 Client ID 값
client_secret = open("secret.txt", "r").read() # 개발자센터에서 발급받은 Client Secret 값

encText = urllib.parse.quote("아이폰")
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText
url = "https://openapi.naver.com/v1/search/news.json?query=" + encText


request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)

response = urllib.request.urlopen(request)
rescode = response.getcode()

if(rescode==200):
    response_body = response.read()
    # print(response_body.decode('utf-8'))
    data = response_body.decode('utf-8')
    json_data = json.loads(data)
    for item in json_data["items"]:
        print(item["pubDate"] + " : " + item["title"])
else:
    print("Error Code:" + rescode)
