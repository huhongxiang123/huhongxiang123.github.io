vip = 5000
def my_friend():
    global vip
    #精品spa
    vip-= 150
    #精品足道
    vip-= 200

my_friend()
#我在外面急得直跺脚，却不知道他消费了多少
print(vip)