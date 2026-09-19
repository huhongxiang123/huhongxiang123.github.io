import jsonpath  # 需要安装：pip install jsonpath
resdata = {
    "data":{
        "saleList":[
            {"isStore":0,
             "madelList":[{"title":"沙床","price":16.9}]
             },
            {
               "isStore":1,
                "madelList":[{"title":"明珠","price":20}]
            }
        ]
    }
}
#使用这个功能，第一个参数，是我要查找的数据  第二个参数就是规则：..就是从全篇里面去找这个内容
#$ 先确保是英文模式，然后shift+4
titles = jsonpath.jsonpath(resdata,'$..title')
prices =  jsonpath.jsonpath(resdata,'$..price')
print(prices)