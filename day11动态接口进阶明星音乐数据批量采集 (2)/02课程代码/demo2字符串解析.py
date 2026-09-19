#我们发现网站爬下来的东西有很多空格怎么办呢？

# str = '       开阳老师很帅         '
# str1 = str.strip() #可以帮我们把里面的空格去掉
# print(str)
#字符串的切割
str = '开阳老师，讲课很好，人很帅，非常优秀，嗓音奇特'
str1 = str.split('，')  #切割内容的意思
print(str1[1])

str = '"mp3_id":4195,"play_id":"eyJpdiI6IkVHOHdTTk9IYThCTm95SlpudjhpOHc9PSIsInZhbHVlIjoidmNhTkhTeVNHcVpyR09UZWZ4anVndEhNSUN4VXIweHRZa2E3bm5sR3BKYmJ4bVhHVVNQbFhVdklJS1hITTZLVFNTeGlnZWY2d3pNUTNkTmVIS291OGc9PSIsIm1hYyI6IjUxZmUyZTIzNGVmMTcxYjZiOWM4ZmFiOGFlM2RmNzU3Y2VhYzFiMDg3NjA0ODk1NjY2MGI0YzljMDVhNzI1MzMiLCJ0YWciOiIifQ=="'
str1 = str.split('"play_id":')[1]
print(str1)

str = '\\u022 zhangsan \\u022 '
str1 = str.replace('\\u022','"')
print(str1)