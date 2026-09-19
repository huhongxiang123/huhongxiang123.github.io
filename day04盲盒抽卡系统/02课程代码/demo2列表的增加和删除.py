roles = ["路飞-ssr", "哥斯拉-ssr", "王林-ssr", "陈平安-ssr", "古月方源-sr", 'R-娜美', 'R-沙僧', 'R-猪八戒']
            # 0          1          2           3           4          5       6         7

# girls = ['娜美','路飞','雏田','刘亦菲']
# #在列表的末尾追加一个元素 必须前面是一个列表才可以通过.去找到其中的方法
# girls.append('路飞')
# # girls.insert(1,'索隆')
# print(girls)

#系统的卡库中抽到的卡片，怎么把他保存到我自己的卡库中呢？？？

# my_roles = []
import random
# num = int(input('请输入你要抽卡的次数:'))
# for i in range(num):
#     role = random.choice(roles)
#     print(f'恭喜您抽中了{role}!!!')
#     my_roles.append(role)
# print(my_roles)

# girls = ['娜美','路飞','雏田','刘亦菲']
# #在列表的末尾追加一个元素 必须前面是一个列表才可以通过.去找到其中的方法
# girls[1] = '路飞-尼卡觉醒状态'
# print(girls)


# girls = ['娜美','路飞','路飞','路飞','雏田','刘亦菲']
#主要的删除方式
# del girls[3]
# girls.pop(0)
# girls.remove('路飞') #1.容易打错字  2.只能删除第一个元素
# print(girls)

for i in range(8):
    role = random.choice(roles)
    roles.remove(role)
    print(f'恭喜您抽中了{role}!!!')
    print(roles)

