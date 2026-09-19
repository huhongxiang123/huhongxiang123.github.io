#为什么要模拟浏览器呢？---如何瞒天过海
#人家都知道你是一个爬虫了 "User-Agent": "python-requests/2.34.2",
#下面就代表了，你是一个正常浏览器了
#User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
#不模拟，人家都知道你是一个非法程序了，就会屏蔽你，甚至拉到黑名单，你后续什么都爬不到了
import requests
kaiyangurl = 'http://httpbin.org/get'

#开始模拟浏览器
kaiyangheaders = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
}

#发起请求  需要加入请求头
response = requests.get(url=kaiyangurl,headers=kaiyangheaders)

#打印响应内容
print(response.text)