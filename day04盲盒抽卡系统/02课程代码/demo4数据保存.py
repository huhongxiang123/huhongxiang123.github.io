#轻量级的讲一下数据的保存
#encoding="utf-8" 是固定格式，编码
#'w'是写入的意思
with open('hero.txt','w',encoding="utf-8") as f:
    f.write('陈平安真帅')

#'r'是读取的意思
# with open('震惊.txt','r',encoding="utf-8") as f:
#     print(f.read())

#扩展内容 append是追加的意思， a能够把内容追加到原本的后面
with open('hero.txt','a',encoding="utf-8") as f:
    f.write('天道崩塌')

with open('hero.txt','a',encoding="utf-8") as f:
    f.write('唯有一剑')