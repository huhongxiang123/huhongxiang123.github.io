#爬文字，爬图片，爬音乐，爬视频。
#有限制的，我们也能找到了
#直接课的目的：1、解放双手，自动爬取  2、抢票，刷单，刷数据  3、重点听逻辑
#  pip install DrissionPage
# 导入我们安装好的包
import time
from DrissionPage import ChromiumPage

#创建一个谷歌浏览器的对象
page = ChromiumPage()  #现在page就是我新打开的浏览器了
#用浏览器，打开网址
page.get("https://www.baidu.com")
#接下来要在代码里输入刘亦菲
#注意这里也是找元素，但跟xpath有区别
#找id就通过 #id名
#找class就通过.class名
textarea = page.ele("#chat-textarea")
#找到了输入框，那我就输入内容呗
textarea.input('刘亦菲')
#找到百度一下的按钮 div[@id="chat-submit-button"]
button = page.ele("#chat-submit-button")
#点击这个按钮
button.click()

#搜索可能跟网络有关系，所以我们睡一会
time.sleep(2)

#找图片的这个按钮
page.ele('xpath://div[@id="s_tab_inner"]/a[2]').click()

#下载所有的刘亦菲图片 要下载多个图片，那么就用eles
#imgs就是没滑动之前的内容，如果想让他更多，那么就多滑动几次
# for i in range(5):
#     time.sleep(2)
#     page.scroll.to_bottom()

imgs = page.eles('xpath://div[@class="image-m9T9I img-hFPj_"]//img')
#要有列表，接下来要下载单张图片了
print(imgs)
#imgs是一个图片列表，img就是一张图片
for img in imgs:
    img.save('刘亦菲')

