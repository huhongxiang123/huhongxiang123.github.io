from DrissionPage import ChromiumPage

#创建浏览器实例
page = ChromiumPage()

#DrissionPage 可以自动保存cookie，因为他本身就是一个浏览器
#只要登录一次，就可以把cookie保存到浏览器上，不需要经常的设置cookie
page.get('https://item.jd.com/100359969926.html')

# #清除一下网页的cookie
# page.set.cookies.clear()
# page.wait(5)
#
# #刷新界面
# page.refresh()

"""
一个cookie数据对应一个账号
当采集数据频率过于频繁时，一个账号一直访问同一个网站触发反爬的概率会大大增加
解决方案：使用多个cookie，轮流访问
-->demo3获取多个cookie
"""
