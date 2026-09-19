# pip install 包名(requests)  就可以安装这个第三方包了  --万能钥匙，基本所有的功能，机器学习，人脸识别，语音识别，NLP
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple 包名
# 这是一个第三方的库，需要安装---不能够直接import 使用    按照需求去安装就可以了

#验证一下是否安好了
# No module named 'requests' 这种错误，就是包，没有安装的意思
import requests

#接着要去定义网址
#当你用这样的网址的时候

url = 'http://httpbin.org/get'

#发送请求  import 以后 就可以使用这个库里的所有功能了，通过.的方式使用
response = requests.get(url)

#响应  解析这里面都返回了个啥给我啊？
#想看看 response里还有啥？？text文本的意思
response.encoding = 'utf-8'
print('请求结果',response.text)

#这样虽然能够访问到一些界面内容，



