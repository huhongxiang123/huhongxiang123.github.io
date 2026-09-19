# 存储不同账号的cookie值，轮流使用不同账号的cookie来做自动化信息抓取
import json
import os.path

from DrissionPage import ChromiumPage
# 创建浏览器窗口
page = ChromiumPage()
# 使用这个新的浏览器窗口打开url地址
page.get("https://www.zhihu.com/hot")
# 清除之前的cookie
page.set.cookies.clear()
# 刷新一下页面
page.refresh()
print("请先进行手动登录一次~")
input("登录成功请按下回车~")
# 这时候cookie一定是最新的
ck = page.cookies().as_str() # 固定写法 获取cookie
print(ck)
# 拿到最新的cookie之后，我们需要把cookie存在本地文件当中
cfile = "cuncookies.json"
if os.path.exists(cfile):
    # 如果这个文件存在的话 -- 你已经至少存过一次了,那么我需要做的是把这个数据给读出来
    with open("cuncookies.json","r") as f:
        cklist = json.load(f)
else:
    # 第一次运行，没有保存过cookie，准备一个容器来装你的cookie
    cklist = []

# 除了第一次，后续的每一次都需要存到列表当中
cklist.append(ck)
# 我们就需要把这个在内存当中的存了cookie的列表，保存到本地
with open("cuncookies.json","w") as f:
    json.dump(cklist,f,indent=4)