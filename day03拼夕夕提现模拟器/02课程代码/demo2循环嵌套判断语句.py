#循环当中嵌套判断语句
# for my_girlfriend in ['刘亦菲','高圆圆','古力娜扎','迪丽热巴']:
#     if my_girlfriend == '刘亦菲':
#         print('我们幸福的在一起！')
#     elif my_girlfriend == '高圆圆':
#         print('虽然我也很爱，但是不选人妻')
#     else:
#         print('朋友~新疆的女孩漂亮的很！')

for num in range(1,10):
    print(f'第{num}位好友已经帮我完成了助力！')
    if num == 5:
        print('✅️ 已集齐5位好友，满足提现条件！')
    if num == 3:
        print(f"❌ 第 {num} 位好友助力无效（非活跃用户），跳过本次助力")