import requests
import webbrowser
import os
import time

# 【定义请求地址】
# 其余静态网站链接：
# 复古游戏厅 ： https://www.yikm.net/#google_vignette
# 百度首页： https://www.baidu.com/
# 美女网站：https://www.xiangsn.com/
qqurl = "https://www.xiangsn.com/"

# 【伪装请求头】User-Agent 相当于你进门时亮出一张 "我是浏览器" 的身份证。
qqheaders = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'connection': 'keep-alive',
    'upgrade-insecure-requests': '1'
}

print("🔄 正在请求该网页页面...")

# 【发送GET请求】
try:
    response = requests.get(url=qqurl, headers=qqheaders, timeout=10)
    response.raise_for_status()  # 检查请求是否成功

    # 【设置编码】
    response.encoding = "utf-8"

    # 【查看状态】
    print(f"✅ 请求成功！状态码: {response.status_code}")

    # 【输出源码长度】
    print(f"📄 页面源码长度: {len(response.text)} 字符")

except requests.exceptions.RequestException as e:
    print(f"❌ 请求失败: {e}")
    exit()

# 【处理相对路径资源】为了让页面完整显示，需要修改资源路径
html_content = response.text

# 替换资源路径为绝对路径（百度CDN资源）
html_content = html_content.replace('src="//', 'src="https://')
html_content = html_content.replace('href="//', 'href="https://')

# 添加一个简单的样式修复，让页面更好看
style_fix = '''
<style>
    body { 
        font-family: Arial, sans-serif; 
        margin: 0; 
        padding: 0;
        background: #f0f0f0;
    }
    #wrapper { 
        max-width: 1200px; 
        margin: 0 auto; 
        background: white;
        min-height: 100vh;
    }
    img { 
        max-width: 100%; 
        height: auto;
    }
</style>
'''

# 在head标签中插入样式修复
html_content = html_content.replace('</head>', f'{style_fix}</head>')

# 【保存到文件】存成HTML文件
filename = "我的网页.html"
try:
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(f"💾 页面已保存为: {filename}")
except Exception as e:
    print(f"❌ 保存文件失败: {e}")
    exit()

# 【自动打开浏览器】
print("🌐 正在浏览器中打开页面...")
time.sleep(0.5)  # 稍微等待一下

# 获取文件的绝对路径
file_path = os.path.abspath(filename)
# 在浏览器中打开
webbrowser.open(f'file://{file_path}')

print("=" * 50)
print("✨ 操作完成！")
print(f"📁 文件位置: {file_path}")
print("💡 提示：如果页面显示不完整，是因为百度页面依赖外部资源")
print("💡 建议：你可以尝试访问：https://www.baidu.com 查看完整页面")
print("=" * 50)

"""
【问题解答】
Q: 保存文件时，后缀名是否与文件类型相关？
A: 是的！.html 文件就是网页文件，浏览器能识别并渲染它。
   我们保存为 .html 格式，浏览器就能正确解析HTML标签。

Q: 图片等资源该如何采集？
A: 图片采集需要额外步骤：
   1. 解析HTML找到所有图片标签 <img src="...">
   2. 使用 requests.get() 下载图片二进制数据
   3. 以 'wb' 模式保存为 .jpg/.png 等格式
   示例：
   img_data = requests.get(img_url).content
   with open('image.jpg', 'wb') as f:
       f.write(img_data)
"""

# 如果需要采集图片，可以运行下面的代码（已注释）
"""
# 【图片采集示例】
import re
from urllib.parse import urljoin

# 提取所有图片URL
img_urls = re.findall(r'<img[^>]+src=["\'](.*?)["\']', html_content)

# 创建图片文件夹
os.makedirs('images', exist_ok=True)

for i, img_url in enumerate(img_urls[:5]):  # 只下载前5张
    if img_url.startswith('//'):
        img_url = 'https:' + img_url

    try:
        img_data = requests.get(img_url, headers=qqheaders, timeout=5).content
        with open(f'images/image_{i+1}.jpg', 'wb') as f:
            f.write(img_data)
        print(f'✅ 下载图片 {i+1}: {img_url}')
    except Exception as e:
        print(f'❌ 下载图片 {i+1} 失败: {e}')
"""

print("\n📌 记住：写爬虫时加上 User-Agent 是基本操作！")