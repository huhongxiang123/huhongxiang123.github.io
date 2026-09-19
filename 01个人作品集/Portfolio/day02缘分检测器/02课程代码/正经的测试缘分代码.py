import datetime

# 基础命理常量
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
TG_WUXING = ["木", "木", "火", "火", "土", "土", "金", "金", "水", "水"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
DZ_WUXING = ["水", "土", "木", "木", "土", "火", "火", "土", "金", "金", "土", "水"]
SHENG_XIAO = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

# 生肖相合相冲规则
LIU_HE = {"鼠": "牛", "牛": "鼠", "虎": "猪", "猪": "虎", "兔": "狗", "狗": "兔",
          "龙": "鸡", "鸡": "龙", "蛇": "猴", "猴": "蛇", "马": "羊", "羊": "马"}
XIANG_CHONG = {"鼠": "马", "牛": "羊", "虎": "猴", "兔": "鸡", "龙": "狗", "蛇": "猪",
               "马": "鼠", "羊": "牛", "猴": "虎", "鸡": "兔", "狗": "龙", "猪": "蛇"}
WUXING_SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
WUXING_KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

# 简易公历年份推算年柱、生肖
def get_year_info(solar_year):
    tg_idx = (solar_year - 4) % 10
    dz_idx = (solar_year - 4) % 12
    return f"{TIAN_GAN[tg_idx]}{DI_ZHI[dz_idx]}", SHENG_XIAO[dz_idx]

# 简易日柱推算（娱乐简化算法）
def get_day_pillar(y, m, d):
    base = y * 365 + m * 30 + d
    tg = TIAN_GAN[base % 10]
    dz = DI_ZHI[base % 12]
    return tg + dz

# 提取八字五行统计
def count_wuxing(bazi):
    cnt = {"金":0,"木":0,"水":0,"火":0,"土":0}
    for c in bazi:
        if c in TIAN_GAN:
            idx = TIAN_GAN.index(c)
            cnt[TG_WUXING[idx]] += 1
        else:
            idx = DI_ZHI.index(c)
            cnt[DZ_WUXING[idx]] += 1
    return cnt

# 计算匹配分数
def calc_score(sx1, wu1, sx2, wu2):
    score = 50
    # 生肖加分减分
    if LIU_HE[sx1] == sx2:
        score += 20
    if XIANG_CHONG[sx1] == sx2:
        score -= 15
    # 五行互补加分
    for w in wu1:
        if wu1[w]==0 and wu2[w]>=2:
            score +=6
        if wu2[w]==0 and wu1[w]>=2:
            score +=6
    return max(0, min(100, score))

# 分数解读
def score_text(s):
    if s >=85: return "天作之合，良缘佳配"
    elif s>=70: return "上等婚配，相处融洽"
    elif s>=55: return "中等婚配，需要互相包容"
    elif s>=35: return "下等婚配，容易产生矛盾"
    else: return "匹配度极低，多忍让磨合"

if __name__ == "__main__":
    print("====八字婚配匹配工具（无依赖版·仅供娱乐）====")
    # 输入1
    n1 = input("第一人姓名：")
    y1 = int(input(f"{n1}出生公历年份："))
    m1 = int(input(f"{n1}出生公历月份："))
    d1 = int(input(f"{n1}出生公历日期："))
    # 输入2
    n2 = input("\n第二人姓名：")
    y2 = int(input(f"{n2}出生公历年份："))
    m2 = int(input(f"{n2}出生公历月份："))
    d2 = int(input(f"{n2}出生公历日期："))

    # 计算信息
    bazi1, sx1 = get_year_info(y1)
    bazi1 += get_day_pillar(y1,m1,d1)
    wu1 = count_wuxing(bazi1)

    bazi2, sx2 = get_year_info(y2)
    bazi2 += get_day_pillar(y2,m2,d2)
    wu2 = count_wuxing(bazi2)

    score = calc_score(sx1,wu1,sx2,wu2)
    desc = score_text(score)

    # 输出结果
    print("\n========测算结果========")
    print(f"【{n1}】生肖：{sx1} 八字：{bazi1} 五行：{wu1}")
    print(f"【{n2}】生肖：{sx2} 八字：{bazi2} 五行：{wu2}")
    print(f"\n婚配匹配度：{score}分 / 100")
    print(f"解读：{desc}")
    print("\n⚠️ 民俗娱乐，无科学参考价值")