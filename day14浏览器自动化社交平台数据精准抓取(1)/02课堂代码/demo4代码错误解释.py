money = '50'
try:
    if 20/money :
        print('有钱')
    else:
        print('没钱')
except Exception as e:
    print('程序报错了，错误的原因是',e)

print('后面的代码可能不会运行')