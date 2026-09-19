music_data = {'state': True,
        'errno': 22000,
        'errmsg': '',
        'elapsed_time': '0.0131',
        'ip': '10.16.15.14',
        'data': {'artist': [{'artistCode': 'A10047769', 'birthday': '1976-05-17', 'gender': '男', 'name': '王力宏', 'artistType': 38, 'artistTypeName': '歌手', 'pic': 'https://img01.dmhmusic.com/0206/M00/70/D4/ChR47FtM60qAJ7WZAAGBpnp6XmI240.jpg', 'region': '港台', 'isFavorite': 0}], 'cpId': 23, 'pic': 'https://img01.dmhmusic.com/0101/M00/95/1F/ChR45WGgTDuAHU_HAAcug-9YiU4978.jpg', 'title': '天地龙鳞（大型纪录片《紫禁城》主题歌）', 'duration': 196, 'assetId': 'T10062480746', 'genre': '流行', 'albumTitle': '天地龙鳞（大型纪录片《紫禁城》主题歌）', 'id': 'T10062480746', 'lang': '中文', 'afReplayGain': 0, 'albumAssetCode': 'P10003976570', 'releaseDate': '2021-11-27T00:00:00.000Z', 'isrc': 'CN-Z51-21-00475', 'sort': 1, 'meanVolume': 0, 'maxVolume': 0, 'lyric': 'https://static-qianqian.taihe.com/0101/M00/95/2F/ChR45GGgTHiAC9btAAARZydq3_I160.lrc', 'pay_model': 2, 'TSID': 'T10062480746', 'allRate': ['64', '3000', '128', '320'], 'pushTime': '2021-11-27T10:00:00+08:00', 'downTime': '2037-01-01T00:00:00+08:00', 'bizList': ['sdk_cpm'], 'bits': 16, 'path': 'https://audio04.dmhmusic.com/71_53_T10062480746_128_4_1_0_sdk-cpm/cn/0105/M00/94/F5/ChR45GGfEKiAMwhJADAJ-QfVmQU129.mp3?xcode=6c11b8d9b9e11f5b11e7c7fc14476e9b63bd3397', 'size': 3148281, 'rate': 128, 'hashcode': '03aadee5b04f7397ee0506bfc4a5b1957de0dd86', 'format': 'mp3', 'filemd5': '4726ae4f675bb8062459b1b7aa00597c', 'expireTime': 1783602488, 'isFavorite': 0, 'isVip': 0, 'isPaid': 0}}
# print(music_data['data']['artist'][0]) #这个artist很明显就是王力宏的个人信息
# print(music_data['data']['title'])  #这就是歌曲名称
# print(music_data['data']['lyric'])  #这就是歌词的地址
print(music_data['data']['pic'])