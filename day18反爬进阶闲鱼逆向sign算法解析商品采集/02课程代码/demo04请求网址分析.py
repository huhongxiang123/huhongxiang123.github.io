#这个是笔记本电脑的URL
import hashlib
import time
#逆向
#

#时间戳，就是1970年1月1日到现在的
#这就能获取到当前时间


#10eebb70eb8edc65b446b这个参数，是通过加密产生的一个复杂的参数
#在哪儿找？
#js的文件里去找---一定有一个js文件，是对这个参数进行加密的
'''

c6dffe4f6267787ad605ba95df0411e3
110eebb70eb8edc65b446bedd32e29bb
if (d.H5Request === !0) {
            var g = "//" + (d.prefix ? d.prefix + "." : "") + (d.subDomain ? d.subDomain + "." : "") + d.mainDomain + "/h5/" + c.api.toLowerCase() + "/" + c.v.toLowerCase() + "/"
              , h = c.appKey || ("waptest" === d.subDomain ? "4272" : "12574478")
              , j = (new Date).getTime()
              , k = i(d.token + "&" + j + "&" + h + "&" + c.data)
              , l = {
                jsv: A,
                appKey: h,
                t: j,
                sign: k
            }
'''

#获取到token
d_token = 'f367c39421be01aa446b45d284ba96b0'
h='34839810'
c_data = '{"pageNumber":1,"keyword":"相机","fromFilter":false,"rowsPerPage":30,"sortValue":"","sortField":"","customDistance":"","gps":"","propValueStr":{},"customGps":"","searchReqFromPage":"pcSearch","extraFilterValue":"{}","userPositionJson":"{}"}'
j = str(int(time.time()*1000))
sign = f"{d_token}&{j}&{h}&{c_data}"

md5=hashlib.md5()
#【2.统一编码格式】
md5.update(sign.encode('utf-8'))
#【3.开始加密】
new_sign=md5.hexdigest()
#【查看数据】
print(new_sign)
