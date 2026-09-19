"""
这个文件估计没时间讲了
"""
import random
import time

# 基础抽卡池，共5张
heros = [
    {"名字":"刻晴", "稀有度":"5星", "属性":"雷系"},
    {"名字":"芭芭拉", "稀有度":"4星", "属性":"水系"},
    {"名字":"安柏", "稀有度":"4星", "属性":"火系"},
    {"名字":"丽莎", "稀有度":"4星", "属性":"雷系"},
    {"名字":"香菱", "稀有度":"4星", "属性":"火系"}
]

# 根据会员等级, 生成不同的抽卡池
def get_heros(vip_level):
    """
    :param vip_level: 会员等级
    :return: 该会员得到的 抽卡池
    """
    add_hero = {"名字":"刻晴", "稀有度":"5星", "属性":"雷系"}
    if vip_level == 1:
        # vip1: 增加1张'5星-刻晴'
        candidate = heros + [add_hero]
    elif vip_level == 2:
        # vip2：增加3张'5星-刻晴'
        candidate = heros + [add_hero] * 3
        # vip2：增加5张'5星-刻晴'
    elif vip_level == 3:
        candidate = heros + [add_hero] * 5
    else:
        # 其余不变
        candidate = heros

    return candidate

# 抽卡并保存数据到本地
def chouka(counts, cards, filename="盲盒抽卡记录.txt"):
    """
    :param counts: 抽卡次数
    :param cards: 卡片盲盒
    """
    length = len(cards)
    # 设置连抽次数
    for i in range(counts):
        index = random.randint(0, length - 1)
        hero = cards[index]
        print(f"恭喜您抽中{hero['稀有度']}级别英雄{hero['名字']}！！！")
        # 将抽到的卡片数据保存起来
        with open(filename, 'a', encoding='utf-8') as f:
            record = f'{hero["稀有度"]} - {hero["名字"]} | 属性: {hero["属性"]}'
            f.write(record)
            f.write('\n')
        print(f'抽卡记录已保存到{filename}')
        time.sleep(1)


# 获取vip3的卡片盲盒
cards = get_heros(3)
# 抽卡并保存
chouka(5, cards)