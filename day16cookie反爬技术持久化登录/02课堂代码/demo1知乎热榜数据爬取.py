from DrissionPage import ChromiumPage
# 创建浏览器窗口
page = ChromiumPage()
# 使用这个新的浏览器窗口打开url地址
page.get("https://www.zhihu.com/hot")
# 获取热榜信息
hotele = page.eles('x://section[@class="HotItem"]')
print("热榜元素",hotele)
# 循环找到的所有热点元素
for i in hotele:
    # url 热度信息筛选>200万 标题
    redu = i.ele('@class:HotItem-metrics').text # 469 万热度       分享
    # print("每个热点的热度值",redu)
    # 字符串处理
    redu = redu.split(" ")[0]
    # print("处理之后的热度",redu)
    # 判断热度是否大于200
    if int(redu) > 200:
        # 那么我就认为当前这个信息热度高，我需要这个信息
        title = i.ele(".HotItem-title").text
        aurl = i.ele("x:.//a/@href")
        print(title,aurl)

# cookie 他是会自动更新的 ，我们肯定是不能指望手动去复制cookie的