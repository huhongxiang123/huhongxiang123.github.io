#requests 和 DrissionPage
#reuqests什么时候用？？
#1、不需要打开浏览器
#2、小网站用requests 豆瓣、新闻类型、简单的音乐
#3、requests直接请求就可以了 效率高
#4、做不了突破验证码
#5、用requests突破不了逆向 逆向很难破解


#DrissionPage什么时候用？
#1、需要打开浏览器
#2、大厂用DrissionPage  小红书、闲鱼、淘宝、京东
#3、经常需要等待界面加载，浪费的时间长
#4、可以突破验证码的
#5.可以突破逆向的限制

# cookie会过期的问题？
# 今天的内容，理解性为主；今天的内容，会讲一种逆向的requests的方式，再讲简单的DrissionPage



import requests
import jsonpath
import csv,time

t = str(int(time.time()*1000))
print(t)
kaiyang_url = "https://h5api.m.goofish.com/h5/mtop.taobao.idlemtopsearch.pc.search/1.0/?jsv=2.7.2&appKey=34839810&t=1785239450933&sign=1ea261f45f6f433281e8088f7cecd712&v=1.0&type=originaljson&accountSite=xianyu&dataType=json&timeout=20000&api=mtop.taobao.idlemtopsearch.pc.search&sessionOption=AutoLoginOnly&spm_cnt=a21ybx.search.0.0&spm_pre=a21ybx.search.searchInput.0"
kaiyang_headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "cookie":"t=6fef2309be7192ce1b7f316a0361cc46; cna=Cj3qInp5H3gBASQOA5kOQ5at; tracknick=%E5%AD%99%E9%A2%96suny; unb=667262785; havana_lgc2_77=eyJoaWQiOjY2NzI2Mjc4NSwic2ciOiJlZmZiMjdjNmMzYTQ5YTE3Zjc5ZGE4ZTJmNTk4ZjA2MSIsInNpdGUiOjc3LCJ0b2tlbiI6IjFfZl9sSWpxUXY2UWc5RlhYUHlPMzV3In0; _hvn_lgc_=77; havana_lgc_exp=1787731626538; xlly_s=1; cookie2=1d2da4c8aaf5935edf074d3d973dd557; mtop_partitioned_detect=1; _m_h5_tk=f367c39421be01aa446b45d284ba96b0_1785247373395; _m_h5_tk_enc=32d77ddeaffb43d5d45432644df64088; _samesite_flag_=true; _tb_token_=ee3b68e304353; sgcookie=E100lGsnlSA9077kORioyJWMnzZ2DNcua4kFPfG4ZO9G9rJwwRrNE9ZzAzEvnVrL9Lrd%2BVH1GZyO14QE%2FTKfYtrVJxRNODrNBdp%2BdAsH94JIo2Q%3D; csg=12c31ed3; sdkSilent=1785324774676; tfstk=gbCspe26Ncm1v5zTDczUO_UcJ5dXfyPrlqTArZhZkCdtDmQJYG-w_rVXDGxF_h7w6nhf0Z5N0s_mGEQAmPx4SJ7GSIAY4uRbaNbgSzHlUkRYkwd2lDbVC0_GSIAx8mePpN2fj8-HkIIv9pLMyIHx6fUB9ELWMfpx6vnpxEdvMKKY9vLMzfhx6fUCJHYvMnIvByOpxEdvDidxZegWlRtG5rSt2waqDq7MAjhAOeEDVNamOE5B5dtRW1GxMyY6C3Q9All6gevdoK1moj9fWTjDyGnT4dbAdMT6GWk9ww6AVefTacThQwQyvag-wNA6lLdvdqhARCxXp1R8wDThpNWAsGgjMFfNaKtkdrhD3BCyeTIsozbp6EIDEsroshQAr_XyNWk9ww6AVtsybb-WMzHjRLcXR3zQRxDc8rdWZbwMj-v9-F9URyiOn0cxg24QRcBDBeY6YyaIXtf..",
    "referer":"https://www.goofish.com/search?q=%E8%85%BE%E8%AE%AF%E8%A7%86%E9%A2%911%E5%A4%A9&spm=a21ybx.search.searchInput.0"
}
#post请求比较特殊，必须要带参数请求才能拿到数据，否则就是非法请求
data = {
    "data":'{"pageNumber":1,"keyword":"笔记本电脑","fromFilter":false,"rowsPerPage":30,"sortValue":"","sortField":"","customDistance":"","gps":"","propValueStr":{},"customGps":"","searchReqFromPage":"pcSearch","extraFilterValue":"{}","userPositionJson":"{}"}'
}

response = requests.post(url=kaiyang_url,headers=kaiyang_headers,data=data)
resdata = response.json()  #这是字符串的格式 #转为json格式的内容
#接下来我们从这一大堆数据中，找出我们需要的名字，价格
exContent = jsonpath.jsonpath(resdata,'$..exContent')
all_data = []
for i in exContent:
    print(i)
    #提取地址
    try:
        area = i['area']
        #提取价格
        price = i['detailParams']['soldPrice']
        #提取标题
        title = i['detailParams']['title'][:15]
        all_data.append([area, price, title])
    except:
        pass
    #每循环一次就保存这一组内容

#保存数据
with open('笔记本电脑.csv','w',newline="",encoding='utf-8') as f:
    cf=csv.writer(f)
    #写一个表头
    cf.writerow(['商品名称','地址','价格'])
    cf.writerows(all_data)



