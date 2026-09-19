#接着我们就要学会保存内容了，csv

import csv

import csv
ldata = [ ]
ldata.append(['鲁班','3','男'])
ldata.append(['兰陵王','13','男'])
ldata.append(['后裔','23','男'])
# 将上面数据通过with  open写入到csv文件
with open("测试.csv","w",newline="",encoding="utf-8") as f:
    # 写csv的语法
    # 1.创建一个csv对象文件，才能语法吧数据写入
    cf = csv.writer(f)
    cf.writerow(['姓名','年龄','性别'])
    cf.writerows(ldata)