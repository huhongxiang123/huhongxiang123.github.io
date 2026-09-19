# 【导入requests模块】
import requests
from lxml import etree

# 【定义url】
kaiyangurl = "https://bizhi1.com/"

# 【发请求】
response = requests.get(url=kaiyangurl)
# print(response.text)
#把刚才访问到的结果，转为树形结构
treeHtml = etree.HTML(response.text)

#查找img标签 全部找到img行不
# attachment-post-thumbnail size-post-thumbnail spc wp-post-image
# attachment-post-thumbnail size-post-thumbnail spc wp-post-image
# attachment-post-thumbnail size-post-thumbnail spc wp-post-image
#这是找到的所有的img
imgs = treeHtml.xpath('//img[@class="attachment-post-thumbnail size-post-thumbnail spc wp-post-image"]')
# img 就是列表当中的其中一张照片
for img in imgs:
    #img就是这个标签，里面放了有alt--图片名字。还有图片的地址 src

    #每张图片的地址
    src = img.xpath('./@src')[0]
    #每张图片的名字
    name = img.xpath('./@alt')[0]
    print(src)
    # #开始保存图片
    response = requests.get(url=src)
    with open(f'{name}.png','wb') as f:
        f.write(response.content)