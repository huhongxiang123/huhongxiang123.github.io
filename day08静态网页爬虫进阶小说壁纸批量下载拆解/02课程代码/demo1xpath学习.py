#这些内容就相当于，之前的response.text
#现在教你，怎么把这里面的你想要的内容摘取出来
data = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>
      🌟 开阳追星·圆满结局 刘亦菲
    </h1>
    <h1>
      🌟 开阳老师讲的yyds
    </h1>
    <span id="date-tag1">✦ 今日是第一天圆梦日</span>
    <span id="date-tag2">✦ 今日是第二天圆梦日</span>
    <span id="date-tag3">✦ 今日是第三天圆梦日</span>
 <div class="items-list">
        <div class="list-col">
            <img id="liuyifei" src="https://b0.bdstatic.com/ugc/4CLqr8P4742qCOMs2qPkDQ8fb151782cb3d891d3b1c41dadddb62e.jpg" alt="刘亦菲穿白色礼服走红毯，像仙女下凡一样优雅" class="img-item">
            <img src="https://https://img2.baidu.com/it/u=1649680162,2969906997&fm=253&app=138&f=JPEG?w=800&h=1067" alt="神仙姐姐刘亦菲回眸一笑，开阳的心都要融化了" class="img-item">
        </div>
        <div class="list-col">
            <img src="https://pic.rmb.bdstatic.com/bjh/bc1f429a5ed/251022/6c98906fa154bc5cac47aca6f7c79402.jpeg" alt="开阳拿着刘亦菲的海报，在人群中激动地挥舞" class="img-item">
            <img src="https://pic.rmb.bdstatic.com/bjh/bc1f429a5ed/251022/7e49128f2519566fe0a6740afbd3a886.jpeg" alt="开阳终于见到刘亦菲本人，开心得合不拢嘴" class="img-item">
        </div>
        <div class="list-col">
            <img src="https://https://pic.rmb.bdstatic.com/bjh/3f119bdb648e/250825/08975f93e2ef855b7152c3b03a4ddfdf.jpeg" alt="刘亦菲的粉丝们举着灯牌应援，场面十分壮观" class="img-item">
            <img src="https://b0.bdstatic.com/ugc/personal_page_creator/yFe2JCSPp8dPuBzIw38g1Q55f7caf4b37791bc21be94f6af0b2ce2.jpg" alt="开阳拿着签名本排队，等待刘亦菲的珍贵签名" class="img-item">
        </div>
        <div class="list-col">
            <img src="https://nimg.ws.126.net/?url=http%3A%2F%2Fdingyue.ws.126.net%2F2026%2F0318%2F709fd3e4j00tc36ap02ffd0014001o1m.jpg&thumbnail=660x2147483647&quality=80&type=jpg" alt="刘亦菲在舞台上挥手，开阳在台下感动得流泪" class="img-item">
            <img src="https://img0.baidu.com/it/u=3840064614,1788386143&fm=253&fmt=auto&app=120&f=JPEG?w=500&h=930" alt="开阳举着手机疯狂拍照，记录见到偶像的每一刻" class="img-item">
        </div>

    </div>
</body>
</html>
"""
#导入lxml库 pip install lxml

# import lxml
#从哪个库里面，去导入其中的一个小功能。用的是import 后面的东西
from lxml import etree

#原本data比较乱，不方便找
#把原本的字符串，变成一个树形结构
htmltree = etree.HTML(data)
'''
      👴 html (老祖宗)
        /        \
    head        body (儿子)
   /            /    |    \
meta    title  div   div (孙子)
                 /   |   \
               img  img  img (曾孙)
'''
# print(type(htmltree))
#具体的语法，开始找内容了  这里面就是一层一层的进入去查找内容
# biaobai = htmltree.xpath('/html/body/h1')
# print(biaobai)

#教你一个简单的方式  这个是从任意节点开始找  //是找到整个网页中的所有该标签
#因为全篇可能不止一个h1标签，或者Img标签，所以xpath找到的是一组数据
# biaobai = htmltree.xpath('//h1/text()')
# print(biaobai[1])

#教你利用id去找东西
#接着我要在这一组数据里去找到id叫某个名字的人
#这里面外面的单引号，表示的是字符串，里面的双引号，表示引用这个id
# biaobai = htmltree.xpath('//span[@id="date-tag1"]/text()')
# print(biaobai[0])

#找到id="liuyifei"的img图像  现在找的不是一个文本了 是他的src
#img里有id class alt src  但是我们只要src就是链接地址
#id这个编号，只有一个
# biaobai = htmltree.xpath('//img[@id="liuyifei"]/@src')
# print(biaobai[0])

#怎么批量爬取 通过同一个class名字爬取
#class有一堆重名的
# biaobai = htmltree.xpath('//img[@class="img-item"]/@src')
biaobai = htmltree.xpath('//div[@class="list-col"]/img/@src')
for i in biaobai:
    print(i)

#总结
# /爷爷/爸爸/孩子
#//整个html当中找到所有
#@id=名字（全html就一个）  @class=名字（一组数据）
#xpath找到的是列表，可以循环找到所有内容
#提取标签的问题 /text()
#提取标签的树形 @src @alt





