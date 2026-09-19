# 数据监听
from DrissionPage import ChromiumPage
import jsonpath
import csv
#这里不需要修改任何的cookie内容就可以了

# 搜索内容
search = '相机'
# 创建浏览器对象
page = ChromiumPage()
# 开始监听请求网址
page.listen.start("https://h5api.m.goofish.com/h5/mtop.taobao.idlemtopsearch.pc.search/1.0/",method="POST")
# 打开网页
page.get(f"https://www.goofish.com/search?spm=a21ybx.home.searchHistory.1.4c053da60S4QYq&q={search}")
# 获取监听到的数据
res = page.listen.wait() # 等待数据产生
resdata = res.response.body # 提取数据

# 通过jsonpath---》跨层级找到excontent--->$..
exContent=jsonpath.jsonpath(resdata,'$..exContent')

#定义一个空列表用于存储数据
all_data=[]
for i in exContent:
    print(i)
    #提取地址
    try:
        area=i["area"]
        # 提取价格
        price=i["detailParams"]['soldPrice']
        # 提取标题
        title=i["detailParams"]['title'][:15]

        #每循环一次就添加一次
        all_data.append([title,area,price])
    except Exception as e:
        print(e)

"""
【保存数据】
"""
with open('闲鱼数据11.csv', "w", newline="", encoding="utf-8") as f:
    cf = csv.writer(f)
    # 表头
    cf.writerow(["商品","地址","价格"])
    # 要存的数据
    cf.writerows(all_data)







