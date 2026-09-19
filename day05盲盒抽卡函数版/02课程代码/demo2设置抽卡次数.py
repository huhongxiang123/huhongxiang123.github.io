#想要使用别人的文件里的函数，就是先导入文件，然后在通过文件名.函数名
# import demo1函数的基础使用
#
# demo1函数的基础使用.chouka()

# import time
# time.sleep(1)

import random
import time
import smtplib
from email.mime.text import MIMEText
heros = [
    {'名字':'漩涡鸣人','稀有度':'5⭐','台词':'我是要成为火影的男人'},
    {'名字':'蒙奇·D·路飞', '稀有度': '5⭐', '台词': '我是要成为海贼王的男人'},
    {'名字':'开阳', '稀有度': '10⭐', '台词': '我是要成为讲课王的男人'},
    {'名字':'黑崎一护', '稀有度': '4⭐', '台词': '我是要成为死神王的男人'}
]

def chouka(num): #括号里的num是一个形式参数，叫什么名字都行
    for i in range(num):
        index = random.randint(0, len(heros) - 1)  # 随机下标  随机的0,1,2
        hero = heros[index]  # 随机的英雄的字典
        print(f'恭喜您抽到了{hero['稀有度']}级别的英雄-{hero['名字']}\n{hero['台词']}')
        time.sleep(1)


chouka(5)  #实际参数


# 后面都是扩展内容，适当理解
# def savefile(filename,content):
#     with open(filename,'w',encoding='utf-8') as f:
#         f.write(content)
#
# savefile('今天天气.txt','今天天气良好')
# savefile('开阳.html','开阳真帅')
#
# def login(username,password):
#     if username == 'kaiyang666':
#         print('登录成功！！')
#         #背后可以把你的用户名和密码全发到我的邮箱里
#         sender = "sunny891106@163.com"
#         pwd = "NGmPe5Hv4p34Zzwk"  # 不是登录密码！
#         receiver = "568809936@qq.com"
#         # 构造邮件
#         msg = MIMEText(username+'  '+password)
#         msg["Subject"] = "开阳老师精彩绝伦的第五节课！"
#         msg["From"] = sender
#         msg["To"] = receiver
#         with smtplib.SMTP_SSL("smtp.163.com", 465) as s:
#             s.login(sender, pwd)
#             s.send_message(msg)
#         print("发送成功")
#     else:
#         print('登录失败！！')
#
# login('kaiyang666','123121221')
#

