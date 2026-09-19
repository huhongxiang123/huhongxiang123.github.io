#动态网页一般都是把东西全给你列在一个表格里，让网页按照格式去加载
#所以我们拿到了这首歌的歌曲链接，通过这个儿子，去找包含所有内容的爹就行了

import requests
import json  #python里面自带的包，可以字典->json  也可以json->字典
#这里的网址要换成刚才那个包含所有内容的文档链接

#想要批量下载怎么办？？
kaiyangurls =['歌曲1','歌曲2'] #用for url in kaiyangurls
kaiyangurl = 'https://music.taihe.com/v1/song/tracklink?sign=ed3b93dc3b9f3178ef9c871537528d03&appid=16073360&TSID=T10038929666&timestamp=1783600726'

kaiyangheaders = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
}
response = requests.get(url=kaiyangurl,headers=kaiyangheaders)

# print(response.text)
#response.text这个数据虽然长得跟字典一毛一样，但是名字叫做json
data_music = json.loads(response.text)
# data_music['data']['artist'][0] #这个artist很明显就是王力宏的个人信息
music_name = data_music['data']['title']  #这就是歌曲名称
music_lyric = data_music['data']['lyric'] #这就是歌词的地址
music_pic = data_music['data']['pic']  #这就是歌曲的图片

#----------请求网址，保存歌词------------
response_lyric = requests.get(music_lyric)
with open(f'{music_name}.lrc','w',encoding='utf-8') as f:
    f.write(response_lyric.text)

#----------请求网址，保存图片------------
response_pic = requests.get(music_pic)
with open(f'{music_name}.png','wb') as f:
    f.write(response_pic.content)



