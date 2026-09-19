import requests

kaiyangurl = 'https://audio04.dmhmusic.com/71_53_T10062480746_128_4_1_0_sdk-cpm/cn/0105/M00/94/F5/ChR45GGfEKiAMwhJADAJ-QfVmQU129.mp3?xcode=6ac235e8baafadd811e7bf7770b24292dca79825'

kaiyangheaders = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
}
response = requests.get(url=kaiyangurl,headers=kaiyangheaders)

#下载歌曲
#要是文本:w 还要加上encoding
#要是音视频：wb
with open('天地龙鳞.mp3','wb') as f:
    f.write(response.content)
