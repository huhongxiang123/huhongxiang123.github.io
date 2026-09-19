import pandas

df = pandas.read_csv('各院校历年数据采集.csv')

#拿到了数据，先瞅瞅，看看里面有没有用户偷懒 没有输入的内容 就是空值
#数据清洗--把一些异常的内容或者空的内容去掉
new_df = df[df['外语'] != '--']
new_df = df[df['总分'] != '--']
new_df = df[df['政治'] != '--']
new_df = df[df['专业课一'] != '--']
new_df = df[df['专业课二'] != '--']
new_df = df[df['录取年份'] == 2026]

# new_df["专业课一"] = new_df["专业课一"].astype(int)
# new_df["政治"] = new_df["政治"].astype(int)
#new_df.info() 对于每一列的内容描述

#接下来做数据分析
#老师我很牛逼，我就想看看什么专业最难考，分数最高！！  False是降序排列， True是升序排列
zydata = new_df.groupby('专业')['总分'].max().sort_values(ascending=False).head(10).reset_index(name='最高总分')
print('=============专业最高分TOP10==============')
print(zydata)

#老师，什么专业最火啊？学的人最多啊？这是考研数据，考研的材料的人多，说明啥？说明本科不好找工作
#材料工程本科生考研比例显著高于计算机、电气、自动化等热门工科
#size() 获取这一列的个数
zycount = new_df.groupby('专业').size().sort_values(ascending=False).head(10).reset_index(name='数量')
print('=============专业人数最多TOP10==============')
print(zycount)

#老师我想更容易被录取，找一些招生人数多的学校，更好考
school_count = new_df.groupby('学校').size().sort_values(ascending=False).head(10).reset_index(name='招生人数')
print('=============学校招生人数最多TOP10==============')
print(school_count)
"""
==================================================
第九步：统计专业招生数量和平均录取分。
==================================================
"""
# agg多指标统计：一次完成多个统计任务
# count统计数量，mean计算平均值，max取最大值，min取最小值
# 可以同时分析专业热度和录取难度
# 按专业统计招生数量和平均分

zy_data = new_df.groupby("专业").agg(
    招生数量=("专业","count"),
    最高分=("总分","max")
).sort_values(by="招生数量",ascending=False).head(10).reset_index()
# 平均分保留一位小数

print("================专业招生数量和平均分===================")
print(zy_data)
