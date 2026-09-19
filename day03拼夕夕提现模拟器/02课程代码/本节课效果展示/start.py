import json
import http.server
import socketserver
import webbrowser
import os
import threading
import time
import urllib.parse

# 角色列表 - 只需修改这里
ssr_characters = ["原神-钟离", "原神-雷电将军", "海贼王-路飞", "海贼王-香克斯", "火影忍者-鸣人", "火影忍者-宇智波斑", "龙珠-孙悟空(超级赛亚人)", "龙珠-贝吉塔", "游戏王-武藤游戏", "鬼灭之刃-灶门炭治郎"]
sr_characters = ["原神-胡桃", "原神-甘雨", "海贼王-索隆", "海贼王-山治", "火影忍者-佐助", "火影忍者-卡卡西", "龙珠-孙悟饭", "龙珠-比克", "游戏王-海马濑人", "鬼灭之刃-祢豆子"]
r_characters = ["原神-香菱", "原神-芭芭拉", "海贼王-乌索普", "海贼王-娜美", "火影忍者-小樱", "火影忍者-鹿丸", "龙珠-克林", "龙珠-龟仙人", "游戏王-城之内克也", "鬼灭之刃-我妻善逸"]

# 创建images目录
if not os.path.exists('images'):
    os.makedirs('images')

# 获取角色图片路径
def get_character_image(name):
    formats = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
    for fmt in formats:
        if os.path.exists(f'images/{name}{fmt}'):
            return f'images/{name}{fmt}'
        if os.path.exists(f'images/{name.split("-")[-1]}{fmt}'):
            return f'images/{name.split("-")[-1]}{fmt}'
    return f'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={urllib.parse.quote(name)} geometric design portrait&image_size=portrait_4_3'

# 生成角色池
character_pool = {
    "SSR": [{"name": name, "image": get_character_image(name)} for name in ssr_characters],
    "SR": [{"name": name, "image": get_character_image(name)} for name in sr_characters],
    "R": [{"name": name, "image": get_character_image(name)} for name in r_characters]
}

# 保存为JSON
with open("characters.json", "w", encoding="utf-8") as f:
    json.dump(character_pool, f, ensure_ascii=False, indent=4)

# 启动服务器
PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

def start_server():
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        httpd.serve_forever()

# 启动服务器线程
threading.Thread(target=start_server, daemon=True).start()
time.sleep(1)

# 打开浏览器
webbrowser.open(f'http://localhost:{PORT}')
webbrowser.open(f'http://localhost:{PORT}/all_characters.html')

print("✅ 盲盒抽取器已启动！")
print(f"🚀 访问地址: http://localhost:{PORT}")
print("💡 修改角色列表后重新运行即可更新")

# 保持运行
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n👋 服务器已停止")