#你已经学会了 用一个B站链接--找到视频/音频-合并在一起---下载下来
#加上自动化以后，所有的视频，不需要一个个粘贴地址，可以下载他的所有视频内容

import time
from DrissionPage import ChromiumPage
import b站单视频下载
#创建一个谷歌浏览器的对象
page = ChromiumPage()  #现在page就是我新打开的浏览器了
#用浏览器，打开网址
page.get("https://www.bilibili.com/")
#为什么要睡一会？？
time.sleep(1)
#有id的时候，就用ele("#chat-textarea")
page.ele('xpath://input[@class="nav-search-input"]').input('刘亦菲')
#点击搜索按钮
page.ele('xpath://div[@class="nav-search-btn"]').click()
#获取最新打开的标签页
newPage = page.latest_tab
time.sleep(2)
#点击最多播放---搜实时热搜就最新发布。不想踩坑--搜最多播放
#要找的是一组元素，所以不要忘了是写eles
newPage.eles('xpath://div[@class="search-condition-row"]/button')[1].click()
time.sleep(2)

#找到所有的链接 找到所有的能播放视频的链接地址，这里只找3个
videoUrls = newPage.eles('xpath://div[@class="bili-video-card__wrap"]/a')
#videoUrl就是每一个视频的链接地址
for video in videoUrls[0:3]:
    #提取里面的纯粹的url
    videoUrl = video.attr('href')
    #在新的标签页打开视频（不覆盖上个界面）
    videoTab = page.new_tab(videoUrl)
    time.sleep(2)
    #把这个界面的内容，传递给我们的之前学习过的下载视频的地方就好了
    b站单视频下载.downloadVideo(videoTab.html)
    #下载完，睡一会
    time.sleep(1)
    #关闭这个网页
    videoTab.close()


