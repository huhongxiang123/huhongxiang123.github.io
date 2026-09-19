#https://music.taihe.com/player
import requests

kaiyangurl = 'https://music.taihe.com/player'

kaiyangheaders = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
}

response = requests.get(url=kaiyangurl,headers=kaiyangheaders)

with open('kaiyangyun.html','w',encoding='utf-8') as f:
    f.write(response.text)

#网站分为两种：
#1、静态网站--像百度一样，把网站内容全都给我了，我直接可以看到所有的东西。就可以用xpath从中提取内容就行了
#2、动态网站--像刚才看到的音乐/视频网站一样，把后面的内容都隐藏了，无法直接获取

#动态网站可以反扒---但爬虫是只要在浏览器上能够访问到，我们就可以拿到的内容