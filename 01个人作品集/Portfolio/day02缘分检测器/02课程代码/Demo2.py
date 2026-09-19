#缘分测试不能太假，要有一定的随机性

import random  #random就是随机的意思

# boy_name = input('请输入您的姓名:')
# girl_name = input('请输入您要测试人的姓名:')
yuanfen = random.randint(1,100)#帮我们生成一个1~100之间的随机数据
yuanfen = '古力娜扎'
#if判断语句
if yuanfen == '刘亦菲':
    print('和刘亦菲幸福的在一起')
# if yuanfen == '高圆圆':
#     print('和高圆圆幸福的在一起')
elif yuanfen =='古力娜扎':
    print('和古力娜扎幸福的在一起')
elif yuanfen =='高圆圆':
    print('和高圆圆幸福的在一起')
else:
    print('其他人我谁都不考虑')


#当你只有唯一选择，其他都不考虑的时候，就用if else
#当你有其他很多备选方案要比对的时候，就用if/elif/elif../else