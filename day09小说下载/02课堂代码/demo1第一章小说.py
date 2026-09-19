import requests
from lxml import etree

#要爬取的网址内容  先爬一章练练手
kaiyangurl = 'https://www.diandingnnn.cc/ddk92482/73219338.html'

kaiyangheaders = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
}

#发送请求
response = requests.get(url=kaiyangurl,headers=kaiyangheaders)
# print(response.text)

#接着要从里面去摘取内容了
#把这个网站的内容，转为一棵可以爬下来的树
data = etree.HTML(response.text)

#我们要的是小说标题，还有小说的内容（文本）
#获取标签中间的文本用text()  <p>文本1<p/>  <span>文本1<span/>    <h1>文本1<h1/>
biaoti = data.xpath('//h1/text()')
# print(biaoti[0])

zhengwen = data.xpath('//div[@id="content"]/text()')
print(zhengwen)

#接着我们只需要把列表里的内容，一行一行的提取出来就行了
#w会写入一个内容，但会替换掉之前的内容
#a保存之前的内容，接着再追加一个新的内容 append
for hang in zhengwen:
    # print(hang,'===========')
    with open(f'{biaoti[0]}.txt','a',encoding='utf-8') as f:
        f.write('  '+hang+'\n')
        # f.write('\n')