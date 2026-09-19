import requests  #导入requests

# kaiyangurl = 'https://www.baidu.com'

kaiyangurl = 'https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png'
#开始模拟浏览器
kaiyangheaders = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
}

#发起请求
response = requests.get(url=kaiyangurl,headers=kaiyangheaders)
print(response.text)
#二进制的图片 音频 视频用wb(用resopnse.content)   文本的形式用w
#最常见的两种图片形式，jpg,png
# with open('kaiyang.png','wb') as f:
    # f.write(response.content)