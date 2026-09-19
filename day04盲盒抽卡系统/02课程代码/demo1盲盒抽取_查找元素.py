#利用之前的内容，怎么存储这些角色呢？
# haizei = '娜美'
# huoying = '鸣人'
# xianjian = '刘亦菲'
#
# #列表---存储一组数据的结构 [1,2,3]
# roles = ['娜美','鸣人','刘亦菲']

#操作这里的数据--增删改查
roles = ["路飞-ssr","哥斯拉-ssr","王林-ssr","陈平安-ssr","古月方源-sr",'R-娜美', 'R-沙僧', 'R-猪八戒']
            #0          1          2           3           4          5       6         7
#要从这里面找出一条数据---查 通过索引/下标来找的[0]
#如果说找第几个元素，就把索引-1
# roles[1]
# print(roles[-1]) #下标越界

# print()
import random
#通过随机的下标去获取一个元素
# num = random.randint(0,len(roles)-1)
# print(roles[num])
#直接从列表中去选择一个元素
# role = random.choice(roles)
# print(f'恭喜大佬抽中了超稀有级英雄{role}!!!!')
import time
num = int(input('请输入要抽卡的次数：')) #输入内容是 '9' -->9
for i in range(num):
    role = random.choice(roles)
    print(f'恭喜大佬抽中了超稀有级英雄{role}!!!!')
    time.sleep(1)


#int只能把 '9'-->9
#float 把 '9.1'-->9.1
