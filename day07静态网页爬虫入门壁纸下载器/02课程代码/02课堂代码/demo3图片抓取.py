import requests
kaiyangurl = 'https://pic.rmb.bdstatic.com/bjh/bc14bf22a68/251227/f247085878e4b6119cb225c36275c3b6.jpeg'

#开始模拟浏览器
kaiyangheaders = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
}

#发起请求  需要加入请求头
response = requests.get(url=kaiyangurl,headers=kaiyangheaders)
#图片不能用文本的方式显示
#content是只要是二进制的内容，都需要。音频视频图片，都需要用content
# print(response.text)
#保存图片，就可以了
# w 是写入的意思，但是只能写入字符串
# wb 想写入图片，音频，视频，wb
#当你要显示文本的时候需要写encoding='utf-8'
with open('刘亦菲.jpg','wb') as f:
    f.write(response.content)



