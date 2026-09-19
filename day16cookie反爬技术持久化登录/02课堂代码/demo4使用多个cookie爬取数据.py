# 存储不同账号的cookie值，轮流使用不同账号的cookie来做自动化信息抓取
import json
import os.path
from DrissionPage import ChromiumPage
# 创建浏览器窗口
page = ChromiumPage()
# 使用这个新的浏览器窗口打开url地址
page.get("https://www.zhihu.com/hot")
# 读取本地保存的cookie
with open("cuncookies.json","r") as f:
    data = json.load(f)
# [cookie1,cookie2,cookie2]
print("data",len(data))
count = 1
for ck in data:
    print(f"当前使用第{count}个cookie{ck}")
    count = count + 1 # 每循环一次就让数字+1，这样的话我们能够知道是第几次循环 count = count + 1
    # 清除之前的数据
    page.set.cookies.clear()
    # 使用当前的这个cookie
    page.set.cookies(ck)
    # 刷新页面
    page.refresh()
    # 等待一下时间
    page.wait(1,5)
    # 验证是否通过这个cookie登录成功，查看是否有 Avatar AppHeader-profileAvatar css-d9tvwx 元素
    img = page.ele(".Avatar AppHeader-profileAvatar css-d9tvwx")
    if img:
        print("登录成功")
        # 获取热榜信息
        hotele = page.eles('x://section[@class="HotItem"]')
        # print("热榜元素", hotele)
        # 循环找到的所有热点元素
        for i in hotele:
            # url 热度信息筛选>200万 标题
            redu = i.ele('@class:HotItem-metrics').text  # 469 万热度       分享
            # print("每个热点的热度值",redu)
            # 字符串处理
            redu = redu.split(" ")[0]
            # print("处理之后的热度",redu)
            # 判断热度是否大于200
            if int(redu) > 200:
                # 那么我就认为当前这个信息热度高，我需要这个信息
                title = i.ele(".HotItem-title").text
                aurl = i.ele("x:.//a/@href")
                print(title, aurl)
    else:
        print("当前cookie已失效，使用下一个cookie继续")
