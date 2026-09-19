# pyecharts是python绘制图表的库
# 需要先安装 pip install pyecharts -i https://mirrors.aliyun.com/pypi/simple/

from pyecharts.charts import Bar,Line

bar = Bar()
bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
bar.add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
# render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
# 也可以传入路径参数，如 bar.render("mycharts.html")
bar.render('商品销售.html')

line = Line()
line.add_xaxis(["披萨", "汉堡", "薯条", "烤鸭", "寿司", "咖喱"])
line.add_yaxis("商家A", [15, 220, 26, 10, 75, 90])
# render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
# 也可以传入路径参数，如 bar.render("mycharts.html")
line.render('商品销售1.html')