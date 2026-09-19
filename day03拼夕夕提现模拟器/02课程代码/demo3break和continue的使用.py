#break 会让循环终止。不管什么时候，执行到break，就会跳出循环
# for my_girlfriend in ['刘亦菲','高圆圆','古力娜扎','迪丽热巴']:
#     if my_girlfriend == '刘亦菲':
#         print('我们幸福的在一起！')
#         # break
#     elif my_girlfriend == '高圆圆':
#         # continue
#         print('虽然我也很爱，但是不选人妻')
#     else:
#         print('朋友~新疆的女孩漂亮的很！')
#
#break后面的语句是不会执行的 所以如果需要一定要执行的代码，不要放在break后面
#break的作用域很重要，就是缩进，跟break同一列的内容，后面不会执行到
# for num in range(1,10):
#     print(f'第{num}位好友已经帮我完成了助力！')
#     if num == 5:
#         print('✅️ 已集齐5位好友，满足提现条件！')
#         break
#     if num == 3:
#         print(f"❌ 第 {num} 位好友助力无效（非活跃用户），跳过本次助力")

#continue可以帮我们做内容筛选，筛选掉不要的东西
for i in range(1,10):
    if i%2 == 0:  #4除以2没有余数  3除以2余1
        continue
    print(i)