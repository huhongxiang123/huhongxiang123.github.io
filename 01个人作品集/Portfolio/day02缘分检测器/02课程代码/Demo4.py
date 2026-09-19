import random

print("===== 今日星座运势 =====")
star = input("请输入你的星座：")
num = random.randint(1, 3)
# lucy_number = random.randint(1,100)
lucy_number = random.choice([6,66,88,99])
print(f'今日的幸运数字是{lucy_number}')
print("\n今日运势：")
if star == "白羊座":
    if num == 1:
        print("运势很好，做事一帆风顺，心情格外舒畅")
    elif num == 2:
        print("运势不错，身边会遇到开心的小事")
    elif num == 3:
        print("运势平平，按部就班度过一天就好")

elif star == "金牛座":
    if num == 1:
        print("运势很好，付出的努力很快会有回报")
    elif num == 2:
        print("运势不错，人际关系和谐融洽")
    elif num == 3:
        print("运势平平，适合静下心做好手头事")

elif star == "双子座":
    if num == 1:
        print("运势很好，头脑灵活，学习效率超高")
    elif num == 2:
        print("运势不错，容易收获新想法、新灵感")
    elif num == 3:
        print("运势平平，状态平稳，不必急于求成")

elif star == "巨蟹座":
    if num == 1:
        print("运势很好，身边充满温暖，幸福感满满")
    elif num == 2:
        print("运势不错，待人友善，相处十分轻松")
    elif num == 3:
        print("运势平平，放平心态享受日常")

elif star == "狮子座":
    if num == 1:
        print("运势很好，自信满满，容易得到他人认可")
    elif num == 2:
        print("运势不错，行动力强，做事得心应手")
    elif num == 3:
        print("运势平平，低调做事更稳妥")

elif star == "处女座":
    if num == 1:
        print("运势很好，心思缜密，做事很少出错")
    elif num == 2:
        print("运势不错，细节把控到位，收获好评")
    elif num == 3:
        print("运势平平，不用纠结小细节")

elif star == "天秤座":
    if num == 1:
        print("运势很好，人缘极佳，沟通十分顺利")
    elif num == 2:
        print("运势不错，心态从容，遇事不慌乱")
    elif num == 3:
        print("运势平平，简单生活也有小快乐")

elif star == "天蝎座":
    if num == 1:
        print("运势很好，专注力拉满，目标容易达成")
    elif num == 2:
        print("运势不错，洞察力强，能看清问题本质")
    elif num == 3:
        print("运势平平，养精蓄锐，等待合适时机")

elif star == "射手座":
    if num == 1:
        print("运势很好，活力四射，适合放松与探索")
    elif num == 2:
        print("运势不错，心态乐观，处处有惊喜")
    elif num == 3:
        print("运势平平，稳步前行即可")

elif star == "摩羯座":
    if num == 1:
        print("运势很好，踏实努力，离目标越来越近")
    elif num == 2:
        print("运势不错，坚持付出，慢慢看到成果")
    elif num == 3:
        print("运势平平，积累沉淀，厚积薄发")

elif star == "水瓶座":
    if num == 1:
        print("运势很好，创意十足，想法与众不同")
    elif num == 2:
        print("运势不错，思维开阔，接触新鲜事物")
    elif num == 3:
        print("运势平平，自在随心就好")

elif star == "双鱼座":
    if num == 1:
        print("运势很好，温柔善良，身边贵人相伴")
    elif num == 2:
        print("运势不错，心情柔软，生活充满暖意")
    elif num == 3:
        print("运势平平，安稳度日也是一种幸福")
# elif star == '天平座':
#     print('您想输入的可能是天秤座呢？')

#当用户输入了一些，你意想不到的结果的时候，else帮你处理这些额外情况
else:
    print('您输入的星座可能有误，请检查后重新输入')