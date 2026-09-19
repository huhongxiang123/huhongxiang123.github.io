#return 讲完就完事了，坚持一下伙伴们

def add(a,b):
    c = a+b
    print(f'你求的两个数的和是{c}')
    return c

def cheng(a,b):
    c = a*b
    print(f'你求的两个数的积是{c}')
    return c

c1 = add(107,113133131.2312)  #现在虽然能看到结果，但是程序里，没办法保存这个和
c2 = cheng(122,1213)
#如果程序，直接在函数里就结束了，那你不需要加return
#如果你想后续继续能使用这个函数的处理结果，需要加return

