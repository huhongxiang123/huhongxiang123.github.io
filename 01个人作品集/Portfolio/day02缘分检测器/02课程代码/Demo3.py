import random  #random就是随机的意思

boy_name = input('请输入您的姓名:')
girl_name = input('请输入您要测试人的姓名:')
yuanfen = random.randint(60,100)#帮我们生成一个1~100之间的随机数据

print(yuanfen)
#测试一下，两个人的缘分值
if yuanfen>80:
    print('天生一对，早点在一起，早生贵子！')
elif yuanfen>60:
    print('千里姻缘一线牵')
elif yuanfen>40:
    print('你们缘分差点意思啊，继续努努力')
else:
    print('你们不合适，快点散了吧！')

#布尔值可以分为两种情况：
# 2>1 2!=1+1   ==  !=
#'高圆圆'=='刘亦菲'
# 红线证明有语法错误
# if '高圆圆'!='刘亦菲': #如果这里成立
#     print('的确长得不一样')       #执行下面的语句


