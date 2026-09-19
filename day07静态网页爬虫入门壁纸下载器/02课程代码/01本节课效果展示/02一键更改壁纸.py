import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import ctypes
from ctypes import wintypes
from PIL import Image, ImageTk
import os
import io

# 全局变量
selected_image_path = ""
screen_width = ctypes.windll.user32.GetSystemMetrics(0)
screen_height = ctypes.windll.user32.GetSystemMetrics(1)

# 系统API常量
SPI_SETDESKWALLPAPER = 0x0014
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

# GUI 视觉配置
APP_WIDTH = 900
APP_HEIGHT = 650
PREVIEW_WIDTH = 520
PREVIEW_HEIGHT = 330

COLOR_BG = "#070B18"
COLOR_PANEL = "#10172A"
COLOR_PANEL_2 = "#111C35"
COLOR_CARD = "#121B33"
COLOR_CARD_DARK = "#08111F"
COLOR_BORDER = "#263B70"
COLOR_TEXT = "#EAF2FF"
COLOR_MUTED = "#8EA4C8"
COLOR_NEON = "#36D8FF"
COLOR_PURPLE = "#8B5CF6"
COLOR_SUCCESS = "#28E7A8"
COLOR_WARNING = "#FFD166"
COLOR_DANGER = "#FF5C8A"

root = None
path_label = None
preview_label = None
status_label = None
file_meta_label = None
preview_title_label = None


def prepare_wallpaper(img_path, target_width, target_height):
    """处理图片：缩放并填充到屏幕大小"""
    try:
        # 打开图片
        img = Image.open(img_path)
        # 计算缩放比例（保持宽高比，完全覆盖屏幕）
        img_ratio = img.width / img.height
        screen_ratio = target_width / target_height
        
        if img_ratio > screen_ratio:
            # 图片更宽，按高度缩放
            new_height = target_height
            new_width = int(new_height * img_ratio)
        else:
            # 图片更高，按宽度缩放
            new_width = target_width
            new_height = int(new_width / img_ratio)
        
        # 缩放图片
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        # 创建新画布（屏幕大小）并居中粘贴
        canvas = Image.new('RGB', (target_width, target_height), (0, 0, 0))
        x = (target_width - new_width) // 2
        y = (target_height - new_height) // 2
        canvas.paste(img_resized, (x, y))
        
        # 保存到临时文件
        temp_path = os.path.join(os.environ['TEMP'], 'temp_wallpaper.jpg')
        canvas.save(temp_path, quality=95)
        return temp_path
    except Exception as e:
        raise Exception(f"图片处理失败：{e}")


def truncate_text(text, max_len=42):
    """过长文件名截断，避免撑坏界面"""
    if not text:
        return ""
    return text if len(text) <= max_len else text[:max_len - 3] + "..."


def center_window(window, width=None, height=None, parent=None):
    """窗口居中显示"""
    window.update_idletasks()
    if width is None:
        width = window.winfo_width()
    if height is None:
        height = window.winfo_height()

    if parent:
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - width) // 2
        y = parent.winfo_y() + (parent.winfo_height() - height) // 2
    else:
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def hex_to_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb


def draw_gradient(canvas, width, height, start_color, end_color):
    """Canvas 绘制横向渐变背景"""
    start = hex_to_rgb(start_color)
    end = hex_to_rgb(end_color)
    steps = max(width, 1)
    for i in range(steps):
        ratio = i / steps
        r = int(start[0] + (end[0] - start[0]) * ratio)
        g = int(start[1] + (end[1] - start[1]) * ratio)
        b = int(start[2] + (end[2] - start[2]) * ratio)
        canvas.create_line(i, 0, i, height, fill=rgb_to_hex((r, g, b)))


def create_header(parent):
    """顶部科技感横幅"""
    header = tk.Canvas(parent, width=APP_WIDTH, height=132, highlightthickness=0, bd=0)
    header.pack(fill="x")
    draw_gradient(header, APP_WIDTH, 132, "#101B3F", "#32145F")

    # 科技感装饰线条
    header.create_line(24, 108, 245, 108, fill=COLOR_NEON, width=2)
    header.create_line(245, 108, 285, 88, fill=COLOR_NEON, width=2)
    header.create_line(650, 26, 840, 26, fill="#7C3AED", width=2)
    header.create_oval(782, 52, 850, 120, outline="#36D8FF", width=2)
    header.create_oval(802, 72, 834, 104, outline="#8B5CF6", width=2)
    header.create_text(
        36, 38,
        text="Wallpaper Studio",
        anchor="w",
        fill="#FFFFFF",
        font=("微软雅黑", 27, "bold")
    )
    header.create_text(
        38, 78,
        text="炫彩壁纸控制台 · 一键更换你的桌面背景",
        anchor="w",
        fill="#B7CAFF",
        font=("微软雅黑", 12)
    )
    header.create_text(
        844, 36,
        text="SCREEN",
        anchor="e",
        fill="#90F7FF",
        font=("微软雅黑", 9, "bold")
    )
    header.create_text(
        844, 62,
        text=f"{screen_width} × {screen_height}",
        anchor="e",
        fill="#FFFFFF",
        font=("Consolas", 18, "bold")
    )
    header.create_text(
        844, 88,
        text="自动缩放 · 裁剪 · 填充",
        anchor="e",
        fill="#B7CAFF",
        font=("微软雅黑", 9)
    )
    return header


def make_card(parent, bg=COLOR_CARD, border=COLOR_BORDER, padx=14, pady=14):
    """卡片式容器"""
    outer = tk.Frame(parent, bg=border)
    inner = tk.Frame(outer, bg=bg)
    inner.pack(fill="both", expand=True, padx=1, pady=1)
    inner.configure(padx=padx, pady=pady)
    return outer, inner


def create_neon_button(parent, text, command, bg, hover_bg, fg="#FFFFFF", width=20, height=2):
    """带鼠标悬停效果的高级按钮"""
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=hover_bg,
        activeforeground="#FFFFFF",
        relief="flat",
        bd=0,
        width=width,
        height=height,
        cursor="hand2",
        font=("微软雅黑", 10, "bold")
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


def make_step(parent, number, title, detail):
    """左侧流程步骤"""
    row = tk.Frame(parent, bg=COLOR_CARD)
    row.pack(fill="x", pady=7)

    badge = tk.Label(
        row,
        text=str(number),
        width=3,
        height=1,
        bg=COLOR_PURPLE if number < 3 else COLOR_NEON,
        fg="#FFFFFF" if number < 3 else "#06101F",
        font=("Consolas", 12, "bold")
    )
    badge.pack(side="left", padx=(0, 10))

    text_box = tk.Frame(row, bg=COLOR_CARD)
    text_box.pack(side="left", fill="x", expand=True)
    tk.Label(text_box, text=title, bg=COLOR_CARD, fg=COLOR_TEXT, font=("微软雅黑", 10, "bold"), anchor="w").pack(fill="x")
    tk.Label(text_box, text=detail, bg=COLOR_CARD, fg=COLOR_MUTED, font=("微软雅黑", 8), anchor="w").pack(fill="x", pady=(2, 0))


def set_status(text, color=COLOR_MUTED):
    """底部状态文案"""
    if status_label:
        status_label.config(text=text, fg=color)


def update_selected_file_display(file_path, prefix="已选择"):
    """刷新当前选择图片名称与基础信息"""
    if not file_path:
        if path_label:
            path_label.config(text="未选择图片")
        if file_meta_label:
            file_meta_label.config(text="等待选择本地图片，或粘贴真实在线图片链接。")
        return

    file_name = os.path.basename(file_path)
    short_name = truncate_text(file_name, 46)
    if path_label:
        path_label.config(text=f"{prefix}：{short_name}")

    try:
        img = Image.open(file_path)
        meta = f"图片尺寸：{img.width} × {img.height}｜适配目标：{screen_width} × {screen_height}"
    except Exception:
        meta = f"文件位置：{truncate_text(file_path, 56)}"

    if file_meta_label:
        file_meta_label.config(text=meta)


def set_wallpaper():
    """设置壁纸"""
    global selected_image_path
    
    if not selected_image_path or not os.path.exists(selected_image_path):
        set_status("请先选择一张有效图片，再点击设置壁纸。", COLOR_WARNING)
        messagebox.showwarning("警告", "请先选择有效的图片文件！")
        return
    
    try:
        set_status("正在处理图片并调用 Windows 系统接口设置壁纸...", COLOR_NEON)
        root.update_idletasks()

        # 处理图片
        processed_path = prepare_wallpaper(selected_image_path, screen_width, screen_height)
        
        # 调用系统API设置壁纸
        user32 = ctypes.WinDLL("user32", use_last_error=True)
        user32.SystemParametersInfoW.restype = wintypes.BOOL
        user32.SystemParametersInfoW.argtypes = [
            wintypes.UINT, wintypes.UINT, wintypes.LPCWSTR, wintypes.UINT
        ]
        
        success = user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, processed_path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )
        
        # 删除临时文件
        if os.path.exists(processed_path):
            os.remove(processed_path)
        
        if success:
            set_status("壁纸设置成功：图片已自动适配当前屏幕。", COLOR_SUCCESS)
            messagebox.showinfo("成功", "壁纸设置成功！（已自适应屏幕大小）")
        else:
            error_code = ctypes.get_last_error()
            set_status(f"壁纸设置失败，Windows 错误码：{error_code}", COLOR_DANGER)
            messagebox.showerror("失败", f"壁纸设置失败，错误码：{error_code}")
            
    except Exception as e:
        set_status(f"处理失败：{str(e)}", COLOR_DANGER)
        messagebox.showerror("错误", f"处理失败：{str(e)}")


def select_image():
    """选择本地图片"""
    global selected_image_path
    file_types = [
        ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp"),
        ("JPEG", "*.jpg *.jpeg"),
        ("PNG", "*.png"),
        ("WEBP", "*.webp"),
        ("所有文件", "*.*")
    ]
    
    file_path = filedialog.askopenfilename(
        title="选择壁纸图片",
        filetypes=file_types,
        initialdir=os.path.expanduser("~")
    )
    
    if file_path:
        selected_image_path = file_path
        update_selected_file_display(file_path, "已选择")
        set_status("本地图片已载入，请确认预览效果后点击“设置为壁纸”。", COLOR_SUCCESS)
        # 预览图片
        show_image_preview(file_path)


def show_image_preview(file_path):
    """显示图片预览"""
    try:
        # 打开图片并调整大小以适应预览框
        img = Image.open(file_path)
        # 调整预览图大小（保持宽高比）
        preview_width = PREVIEW_WIDTH
        preview_height = PREVIEW_HEIGHT
        
        # 计算缩放比例
        img_ratio = img.width / img.height
        preview_ratio = preview_width / preview_height
        
        if img_ratio > preview_ratio:
            new_width = preview_width
            new_height = int(new_width / img_ratio)
        else:
            new_height = preview_height
            new_width = int(new_height * img_ratio)
        
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img_resized)
        
        # 更新预览标签
        preview_label.config(image=photo, text="", bg=COLOR_CARD_DARK)
        preview_label.image = photo  # 保持引用

        if preview_title_label:
            preview_title_label.config(text="📺 当前预览 · 已载入")
        update_selected_file_display(file_path, "已选择")
        
    except Exception as e:
        preview_label.config(text=f"预览加载失败：{str(e)}", image="", fg=COLOR_DANGER, bg=COLOR_CARD_DARK)
        preview_label.image = None
        set_status(f"预览加载失败：{str(e)}", COLOR_DANGER)


def download_online_image():
    """下载网络图片（保留原功能）"""
    def download_image():
        url = url_entry.get().strip()
        if not url:
            popup_status.config(text="请输入图片 URL。", fg=COLOR_WARNING)
            messagebox.showwarning("警告", "请输入图片URL！", parent=download_window)
            return
        
        try:
            popup_status.config(text="正在下载并校验图片内容...", fg=COLOR_NEON)
            download_btn.config(text="下载中...", state="disabled", bg="#254D7A")
            download_window.update_idletasks()

            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
            }
            res = requests.get(url=url, headers=headers, timeout=10)
            res.raise_for_status()

            # 校验是否为可打开的图片，避免把网页地址误保存成图片
            try:
                img_bytes = io.BytesIO(res.content)
                with Image.open(img_bytes) as img:
                    img.verify()
            except Exception as verify_error:
                raise Exception(
                    "当前链接没有直接返回图片内容。请填写真实图片地址，"
                    "例如以 .jpg / .png / .jpeg / .webp 结尾，或浏览器打开后只显示图片本身的地址。"
                ) from verify_error
            
            # 保存临时文件
            temp_file = os.path.join(os.environ['TEMP'], 'online_wallpaper.jpg')
            with open(temp_file, 'wb') as f:
                f.write(res.content)
            
            global selected_image_path
            selected_image_path = temp_file
            update_selected_file_display(temp_file, "已下载")
            show_image_preview(temp_file)
            set_status("网络图片下载成功，已自动刷新预览。", COLOR_SUCCESS)
            
            download_window.destroy()
            messagebox.showinfo("成功", "图片下载成功！", parent=root)
            
        except Exception as e:
            popup_status.config(text=f"下载失败：{str(e)}", fg=COLOR_DANGER)
            download_btn.config(text="重新下载", state="normal", bg="#0EA5E9")
            messagebox.showerror("错误", f"下载失败：{str(e)}", parent=download_window)
    
    # 创建下载窗口
    download_window = tk.Toplevel(root)
    download_window.title("下载网络图片")
    download_window.geometry("620x300")
    download_window.configure(bg=COLOR_BG)
    download_window.resizable(False, False)
    download_window.transient(root)
    download_window.grab_set()

    top = tk.Canvas(download_window, width=620, height=82, highlightthickness=0, bd=0)
    top.pack(fill="x")
    draw_gradient(top, 620, 82, "#172554", "#581C87")
    top.create_text(28, 28, text="🌐 下载网络图片", anchor="w", fill="#FFFFFF", font=("微软雅黑", 18, "bold"))
    top.create_text(30, 57, text="粘贴真实在线图片链接，下载后自动刷新预览", anchor="w", fill="#C7D2FE", font=("微软雅黑", 10))

    body = tk.Frame(download_window, bg=COLOR_BG, padx=26, pady=18)
    body.pack(fill="both", expand=True)

    tip = (
        "请输入图片真实在线链接，必须是以 .jpg / .png / .jpeg / .webp 等结尾，\n"
        "或能直接返回图片内容的地址，不要填网页地址。"
    )
    tk.Label(body, text=tip, bg=COLOR_BG, fg=COLOR_MUTED, justify="left", font=("微软雅黑", 9)).pack(anchor="w")

    entry_box = tk.Frame(body, bg=COLOR_BORDER)
    entry_box.pack(fill="x", pady=(14, 10))
    url_entry = tk.Entry(
        entry_box,
        bg="#0B1222",
        fg=COLOR_TEXT,
        insertbackground=COLOR_NEON,
        relief="flat",
        font=("微软雅黑", 11)
    )
    url_entry.pack(fill="x", ipady=10, padx=1, pady=1)
    url_entry.focus_set()

    action_row = tk.Frame(body, bg=COLOR_BG)
    action_row.pack(fill="x", pady=(4, 0))

    popup_status = tk.Label(action_row, text="等待输入图片地址。", bg=COLOR_BG, fg=COLOR_MUTED, font=("微软雅黑", 9), anchor="w")
    popup_status.pack(side="left", fill="x", expand=True)

    cancel_btn = create_neon_button(action_row, "取消", download_window.destroy, "#334155", "#475569", width=8, height=1)
    cancel_btn.pack(side="right", padx=(8, 0), ipady=3)

    download_btn = create_neon_button(action_row, "开始下载", download_image, "#0EA5E9", "#22D3EE", fg="#06101F", width=10, height=1)
    download_btn.pack(side="right", ipady=3)

    download_window.bind("<Return>", lambda event: download_image())
    center_window(download_window, 620, 300, root)


def create_gui():
    """创建GUI界面"""
    global root, path_label, preview_label, status_label, file_meta_label, preview_title_label
    
    # 主窗口
    root = tk.Tk()
    root.title("Wallpaper Studio｜炫彩壁纸控制台")
    root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
    root.configure(bg=COLOR_BG)
    root.resizable(False, False)
    
    # 设置样式
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TFrame", background=COLOR_BG)
    style.configure("TLabel", background=COLOR_BG, foreground=COLOR_TEXT, font=("微软雅黑", 10))
    style.configure("TEntry", fieldbackground="#0B1222", foreground=COLOR_TEXT, insertcolor=COLOR_NEON)

    # 顶部产品横幅
    create_header(root)

    # 主体区域
    main = tk.Frame(root, bg=COLOR_BG, padx=24, pady=18)
    main.pack(fill="both", expand=True)

    # 左侧控制卡片
    left_outer, left = make_card(main, bg=COLOR_CARD, border="#223763", padx=16, pady=16)
    left_outer.pack(side="left", fill="y", padx=(0, 18))
    left_outer.configure(width=278, height=456)
    left_outer.pack_propagate(False)

    tk.Label(left, text="🧭 操作路径", bg=COLOR_CARD, fg=COLOR_TEXT, font=("微软雅黑", 15, "bold"), anchor="w").pack(fill="x")
    tk.Label(left, text="三步完成桌面壁纸更换", bg=COLOR_CARD, fg=COLOR_MUTED, font=("微软雅黑", 9), anchor="w").pack(fill="x", pady=(4, 12))

    make_step(left, 1, "选择图片", "本地上传或网络下载")
    make_step(left, 2, "预览效果", "自动居中显示预览图")
    make_step(left, 3, "一键设置", "按屏幕分辨率自适应填充")

    divider = tk.Frame(left, bg="#24375F", height=1)
    divider.pack(fill="x", pady=14)

    select_btn = create_neon_button(left, "🖼 选择本地图片", select_image, "#2563EB", "#38BDF8", width=22, height=2)
    select_btn.pack(fill="x", pady=(0, 10), ipady=2)

    download_btn = create_neon_button(left, "🌐 下载网络图片", download_online_image, "#6D28D9", "#A855F7", width=22, height=2)
    download_btn.pack(fill="x", pady=(0, 10), ipady=2)

    tk.Label(left, text="🧩 屏幕适配", bg=COLOR_CARD, fg=COLOR_TEXT, font=("微软雅黑", 11, "bold"), anchor="w").pack(fill="x", pady=(8, 4))
    tk.Label(
        left,
        text=f"当前屏幕分辨率：{screen_width} × {screen_height}\n设置时会自动缩放、裁剪、填充。",
        bg=COLOR_CARD,
        fg=COLOR_MUTED,
        justify="left",
        font=("微软雅黑", 9)
    ).pack(fill="x")

    # 右侧预览卡片
    right = tk.Frame(main, bg=COLOR_BG)
    right.pack(side="left", fill="both", expand=True)

    preview_outer, preview_card = make_card(right, bg=COLOR_PANEL, border="#2B4D86", padx=16, pady=14)
    preview_outer.pack(fill="both", expand=True)

    title_row = tk.Frame(preview_card, bg=COLOR_PANEL)
    title_row.pack(fill="x")
    preview_title_label = tk.Label(title_row, text="📺 当前预览", bg=COLOR_PANEL, fg=COLOR_TEXT, font=("微软雅黑", 15, "bold"), anchor="w")
    preview_title_label.pack(side="left")
    tk.Label(
        title_row,
        text="Wallpaper Preview Monitor",
        bg=COLOR_PANEL,
        fg=COLOR_MUTED,
        font=("Consolas", 9),
        anchor="e"
    ).pack(side="right")

    screen_frame = tk.Frame(preview_card, bg=COLOR_NEON)
    screen_frame.pack(fill="both", expand=True, pady=(14, 12))

    screen_inner = tk.Frame(screen_frame, bg=COLOR_CARD_DARK)
    screen_inner.pack(fill="both", expand=True, padx=2, pady=2)
    screen_inner.pack_propagate(False)

    preview_label = tk.Label(
        screen_inner,
        text="等待选择壁纸\n\n🖼 选择本地图片  或  🌐 下载网络图片\n\n预览区会自动保持比例并居中显示",
        bg=COLOR_CARD_DARK,
        fg=COLOR_MUTED,
        justify="center",
        anchor="center",
        font=("微软雅黑", 12)
    )
    preview_label.pack(fill="both", expand=True, padx=10, pady=10)

    info_outer, info_card = make_card(preview_card, bg=COLOR_CARD_DARK, border="#233B6A", padx=12, pady=10)
    info_outer.pack(fill="x")

    path_label = tk.Label(info_card, text="未选择图片", bg=COLOR_CARD_DARK, fg=COLOR_TEXT, font=("微软雅黑", 11, "bold"), anchor="w")
    path_label.pack(fill="x")
    file_meta_label = tk.Label(
        info_card,
        text="等待选择本地图片，或粘贴真实在线图片链接。",
        bg=COLOR_CARD_DARK,
        fg=COLOR_MUTED,
        font=("微软雅黑", 9),
        anchor="w"
    )
    file_meta_label.pack(fill="x", pady=(5, 0))

    action_bar = tk.Frame(right, bg=COLOR_BG, pady=14)
    action_bar.pack(fill="x")

    status_label = tk.Label(
        action_bar,
        text="准备就绪：请选择图片开始。",
        bg=COLOR_BG,
        fg=COLOR_MUTED,
        font=("微软雅黑", 10),
        anchor="w"
    )
    status_label.pack(side="left", fill="x", expand=True)

    set_btn = create_neon_button(action_bar, "🚀 设置为壁纸", set_wallpaper, "#00D4FF", "#67E8F9", fg="#06101F", width=17, height=2)
    set_btn.pack(side="right", ipady=3)

    # 底部轻量说明
    footer = tk.Frame(root, bg=COLOR_BG, height=28)
    footer.pack(fill="x", side="bottom")
    tk.Label(
        footer,
        text="提示：网络图片请填写真实图片链接，不要填写网页地址。支持 jpg / png / jpeg / webp 等常见格式。",
        bg=COLOR_BG,
        fg="#61708F",
        font=("微软雅黑", 8)
    ).pack(pady=(0, 6))
    
    # 居中显示窗口
    center_window(root, APP_WIDTH, APP_HEIGHT)
    
    # 运行主循环
    root.mainloop()


if __name__ == "__main__":
    # 检查PIL是否支持JPEG
    try:
        Image.open(io.BytesIO(b'\xff\xd8\xff\xd9'))
    except:
        pass
    
    create_gui()
