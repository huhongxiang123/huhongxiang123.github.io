import ctypes
import io
import os
import tempfile
import threading
import tkinter as tk
from ctypes import wintypes
from pathlib import Path
from tkinter import filedialog, messagebox

import requests
from PIL import Image, ImageDraw, ImageTk


BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "imgs"

SPI_SETDESKWALLPAPER = 0x0014
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, bg, fg, hover_bg=None, width=None, height=40, radius=18):
        width = width or max(92, len(text) * 18 + 30)
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent.cget("bg"),
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )
        self.text = text
        self.command = command
        self.fill = bg
        self.hover_fill = hover_bg or bg
        self.fg = fg
        self.radius = radius
        self.width_value = width
        self.height_value = height
        self.draw(self.fill)
        self.bind("<Enter>", lambda event: self.draw(self.hover_fill))
        self.bind("<Leave>", lambda event: self.draw(self.fill))
        self.bind("<Button-1>", lambda event: self.command())

    def draw(self, fill):
        self.delete("all")
        self.create_round_rect(
            1,
            1,
            self.width_value - 1,
            self.height_value - 1,
            self.radius,
            fill=fill,
            outline=fill,
        )
        self.create_text(
            self.width_value / 2,
            self.height_value / 2,
            text=self.text,
            fill=self.fg,
            font=("Microsoft YaHei", 10, "bold"),
        )

    def create_round_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)


class WallpaperApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("壁纸更换工具")
        self.root.geometry("1120x760")
        self.root.minsize(980, 680)
        self.root.configure(bg="#edf3f8")

        self.screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        self.screen_height = ctypes.windll.user32.GetSystemMetrics(1)

        self.selected_image_path = ""
        self.preview_image = None
        self.preview_photo = None
        self.gallery_photos = []
        self.gallery_items = []
        self.gallery_paths = []
        self.temp_files = []
        self.url_var = tk.StringVar()
        self.status_var = tk.StringVar(value="请选择一张图片，或从素材图库中挑选。")
        self.file_var = tk.StringVar(value="暂无")
        self.size_var = tk.StringVar(value="暂无")

        self.build_ui()
        self.center_window()
        self.load_gallery()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_ui(self):
        header = tk.Frame(self.root, bg="#edf3f8")
        header.pack(fill="x", padx=26, pady=(22, 14))

        logo = tk.Label(
            header,
            text="WP",
            width=4,
            height=2,
            fg="white",
            bg="#1d4ed8",
            font=("Segoe UI", 14, "bold"),
        )
        logo.pack(side="left")

        title_box = tk.Frame(header, bg="#edf3f8")
        title_box.pack(side="left", padx=14)
        tk.Label(
            title_box,
            text="壁纸更换工具",
            fg="#172033",
            bg="#edf3f8",
            font=("Microsoft YaHei", 24, "bold"),
        ).pack(anchor="w")
        tk.Label(
            title_box,
            text="选择图片、预览桌面效果，并一键设置为当前系统壁纸",
            fg="#667085",
            bg="#edf3f8",
            font=("Microsoft YaHei", 10),
        ).pack(anchor="w", pady=(4, 0))

        screen_text = f"当前屏幕：{self.screen_width} × {self.screen_height}"
        tk.Label(
            header,
            text=screen_text,
            fg="#344054",
            bg="#ffffff",
            padx=16,
            pady=10,
            font=("Microsoft YaHei", 10),
            relief="flat",
        ).pack(side="right")

        main = tk.Frame(self.root, bg="#edf3f8")
        main.pack(fill="both", expand=True, padx=26, pady=(0, 24))
        main.grid_columnconfigure(0, minsize=390)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        self.left_panel = self.card(main)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 18))

        self.right_panel = self.card(main)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)

        self.build_controls()
        self.build_preview()

    def build_controls(self):
        tk.Label(
            self.left_panel,
            text="导入图片",
            fg="#172033",
            bg="white",
            font=("Microsoft YaHei", 14, "bold"),
        ).pack(anchor="w", padx=18, pady=(18, 12))

        upload = tk.Frame(self.left_panel, bg="#f4f8ff", highlightthickness=1, highlightbackground="#c7d7fe")
        upload.pack(fill="x", padx=18)
        tk.Label(upload, text="+", fg="#1d4ed8", bg="#f4f8ff", font=("Segoe UI", 30, "bold")).pack(pady=(12, 0))
        tk.Label(
            upload,
            text="选择一张本地图片",
            fg="#172033",
            bg="#f4f8ff",
            font=("Microsoft YaHei", 12, "bold"),
        ).pack()
        tk.Label(
            upload,
            text="支持 jpg、png、bmp、gif、webp 等格式",
            fg="#667085",
            bg="#f4f8ff",
            font=("Microsoft YaHei", 9),
        ).pack(pady=(4, 10))
        self.button(upload, "选择本地图片", self.select_image, "#1d4ed8", "white").pack(pady=(0, 14))

        url_box = tk.Frame(self.left_panel, bg="white")
        url_box.pack(fill="x", padx=18, pady=(18, 0))
        tk.Label(
            url_box,
            text="网络图片地址",
            fg="#344054",
            bg="white",
            font=("Microsoft YaHei", 10, "bold"),
        ).pack(anchor="w", pady=(0, 8))
        url_row = tk.Frame(url_box, bg="white")
        url_row.pack(fill="x")
        entry = tk.Entry(
            url_row,
            textvariable=self.url_var,
            relief="flat",
            bg="#f8fafc",
            fg="#172033",
            insertbackground="#172033",
            font=("Microsoft YaHei", 10),
        )
        entry.pack(side="left", fill="x", expand=True, ipady=10)
        self.button(url_row, "导入", self.download_online_image, "#e8eef7", "#274060").pack(side="left", padx=(8, 0))
        tk.Label(
            url_box,
            text='图片地址需要在图片上点击鼠标右键，选择“复制图片地址”（或“复制图像链接”），再粘贴过来就可以了啦！',
            fg="#667085",
            bg="white",
            font=("Microsoft YaHei", 9),
            wraplength=320,
            justify="left",
        ).pack(anchor="w", pady=(8, 0))

        option_box = tk.Frame(self.left_panel, bg="white")
        option_box.pack(fill="x", padx=18, pady=(16, 0))
        tk.Label(
            option_box,
            text="适配方式",
            fg="#344054",
            bg="white",
            font=("Microsoft YaHei", 10, "bold"),
        ).pack(anchor="w")
        tk.Label(
            option_box,
            text="铺满裁剪",
            fg="#0f9f6e",
            bg="white",
            font=("Microsoft YaHei", 10, "bold"),
        ).pack(anchor="w", pady=(8, 0))
        tk.Label(
            option_box,
            text="图片会自动裁剪到屏幕比例，保证壁纸铺满整个桌面。",
            fg="#667085",
            bg="white",
            font=("Microsoft YaHei", 9),
            wraplength=320,
            justify="left",
        ).pack(anchor="w", pady=(5, 0))

        info = tk.Frame(self.left_panel, bg="white")
        info.pack(fill="x", padx=18, pady=(18, 0))
        self.info_box(info, "已选图片", self.file_var).pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.info_box(info, "原图尺寸", self.size_var).pack(side="left", fill="x", expand=True)


    def build_preview(self):
        top = tk.Frame(self.right_panel, bg="white")
        top.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 10))
        top.grid_columnconfigure(0, weight=1)

        tk.Label(
            top,
            text="桌面预览",
            fg="#172033",
            bg="white",
            font=("Microsoft YaHei", 16, "bold"),
        ).grid(row=0, column=0, sticky="w")

        action = tk.Frame(top, bg="white")
        action.grid(row=0, column=1, sticky="e")
        self.button(action, "设为桌面壁纸", self.set_wallpaper, "#0f9f6e", "white").pack(side="left", padx=(0, 8))
        self.button(action, "清空", self.clear_image, "#e8eef7", "#274060").pack(side="left")

        preview_wrap = tk.Frame(self.right_panel, bg="white")
        preview_wrap.grid(row=1, column=0, sticky="nsew", padx=18, pady=(4, 12))
        preview_wrap.grid_columnconfigure(0, weight=1)
        preview_wrap.grid_rowconfigure(0, weight=1)

        self.preview_canvas = tk.Canvas(
            preview_wrap,
            bg="#111827",
            highlightthickness=10,
            highlightbackground="#172033",
            relief="flat",
        )
        self.preview_canvas.grid(row=0, column=0, sticky="nsew")
        self.preview_canvas.bind("<Configure>", lambda event: self.render_preview())

        gallery_panel = tk.Frame(self.right_panel, bg="white")
        gallery_panel.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 12))
        gallery_panel.grid_columnconfigure(0, weight=1)

        tk.Label(
            gallery_panel,
            text="素材图库",
            fg="#172033",
            bg="white",
            font=("Microsoft YaHei", 13, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        gallery_body = tk.Frame(gallery_panel, bg="white")
        gallery_body.grid(row=1, column=0, sticky="ew")
        gallery_body.grid_columnconfigure(0, weight=1)

        self.gallery_canvas = tk.Canvas(
            gallery_body,
            bg="white",
            highlightthickness=0,
            bd=0,
            height=144,
            cursor="hand2",
        )
        self.gallery_scrollbar = tk.Scrollbar(
            gallery_body,
            orient="vertical",
            command=self.gallery_canvas.yview,
            relief="flat",
        )
        self.gallery_canvas.configure(yscrollcommand=self.gallery_scrollbar.set)
        self.gallery_canvas.grid(row=0, column=0, sticky="ew")
        self.gallery_scrollbar.grid(row=0, column=1, sticky="ns", padx=(6, 0))
        self.gallery_canvas.bind("<Configure>", lambda event: self.render_gallery())
        self.gallery_canvas.bind("<Enter>", self.bind_gallery_wheel)
        self.gallery_canvas.bind("<Leave>", self.unbind_gallery_wheel)
        self.gallery_canvas.bind("<Button-1>", self.on_gallery_click)

        bottom = tk.Frame(self.right_panel, bg="white")
        bottom.grid(row=3, column=0, sticky="ew", padx=18, pady=(0, 18))
        tk.Label(
            bottom,
            textvariable=self.status_var,
            fg="#667085",
            bg="white",
            anchor="w",
            font=("Microsoft YaHei", 10),
        ).pack(side="left", fill="x", expand=True)

    def card(self, parent):
        return tk.Frame(parent, bg="white", highlightthickness=1, highlightbackground="#d8e0ea")

    def button(self, parent, text, command, bg, fg):
        hover = {
            "#1d4ed8": "#1e40af",
            "#0f9f6e": "#0b8f63",
            "#e8eef7": "#dbe5f1",
        }.get(bg, bg)
        return RoundedButton(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            hover_bg=hover,
            radius=18,
        )

    def info_box(self, parent, label, variable):
        box = tk.Frame(parent, bg="#f8fafc", padx=12, pady=10)
        tk.Label(box, text=label, fg="#667085", bg="#f8fafc", font=("Microsoft YaHei", 8)).pack(anchor="w")
        tk.Label(
            box,
            textvariable=variable,
            fg="#172033",
            bg="#f8fafc",
            font=("Microsoft YaHei", 10, "bold"),
            wraplength=120,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))
        return box

    def update_gallery_scroll(self, event=None):
        self.gallery_canvas.configure(scrollregion=self.gallery_canvas.bbox("all"))

    def bind_gallery_wheel(self, event=None):
        self.root.bind_all("<MouseWheel>", self.on_gallery_wheel)

    def unbind_gallery_wheel(self, event=None):
        self.root.unbind_all("<MouseWheel>")

    def on_gallery_wheel(self, event):
        self.gallery_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_gallery_click(self, event):
        x = self.gallery_canvas.canvasx(event.x)
        y = self.gallery_canvas.canvasy(event.y)
        for item in self.gallery_items:
            x1, y1, x2, y2 = item["bounds"]
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.use_image(item["path"])
                return

    def load_gallery(self):
        if not IMG_DIR.exists():
            self.gallery_paths = []
            self.render_gallery("未找到 imgs 素材文件夹")
            return

        self.gallery_paths = [
            path for path in IMG_DIR.iterdir()
            if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tiff"}
        ][:12]

        if self.gallery_paths:
            self.use_image(self.gallery_paths[0])

        self.root.after(100, self.render_gallery)

    def render_gallery(self, empty_text=None):
        if not hasattr(self, "gallery_canvas"):
            return

        width = self.gallery_canvas.winfo_width()
        if width <= 1:
            self.root.after(100, self.render_gallery)
            return

        self.gallery_canvas.delete("all")
        self.gallery_photos.clear()
        self.gallery_items.clear()

        if not self.gallery_paths:
            self.gallery_canvas.create_text(
                12,
                24,
                anchor="w",
                text=empty_text or "imgs 文件夹里没有可展示的图片",
                fill="#667085",
                font=("Microsoft YaHei", 10),
            )
            self.gallery_canvas.configure(scrollregion=self.gallery_canvas.bbox("all"))
            return

        thumb_width = 104
        thumb_height = 64
        gap = 10
        columns = max(1, (width - 8) // (thumb_width + gap))

        for index, path in enumerate(self.gallery_paths):
            column = index % columns
            row = index // columns
            x = column * (thumb_width + gap)
            y = row * (thumb_height + gap)

            thumb = self.make_thumbnail(path, thumb_width, thumb_height)
            self.gallery_photos.append(thumb)
            self.gallery_canvas.create_image(x, y, image=thumb, anchor="nw")
            self.gallery_items.append(
                {
                    "path": path,
                    "bounds": (x, y, x + thumb_width, y + thumb_height),
                }
            )

        self.gallery_canvas.configure(scrollregion=self.gallery_canvas.bbox("all"))

    def make_thumbnail(self, path, width, height):
        img = Image.open(path).convert("RGB")
        img_ratio = img.width / img.height
        target_ratio = width / height
        if img_ratio > target_ratio:
            new_height = height
            new_width = int(height * img_ratio)
        else:
            new_width = width
            new_height = int(width / img_ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        x = (new_width - width) // 2
        y = (new_height - height) // 2
        img = img.crop((x, y, x + width, y + height))
        img = img.convert("RGBA")
        img.putalpha(self.rounded_mask(width, height, 10))
        return ImageTk.PhotoImage(img)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="选择壁纸图片",
            initialdir=os.path.expanduser("~"),
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.webp *.tiff"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("所有文件", "*.*"),
            ],
        )
        if file_path:
            self.use_image(file_path)

    def download_online_image(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("提示", "请先输入图片 URL。")
            return

        self.status_var.set("正在下载网络图片...")
        self.run_async(lambda: self.fetch_image(url), self.use_image, "图片下载失败")

    def fetch_image(self, url):
        headers = {
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        Image.open(io.BytesIO(response.content)).verify()
        suffix = Path(url.split("?")[0]).suffix or ".jpg"
        fd, temp_path = tempfile.mkstemp(prefix="online_wallpaper_", suffix=suffix)
        with os.fdopen(fd, "wb") as file:
            file.write(response.content)
        self.temp_files.append(temp_path)
        return temp_path

    def use_image(self, path):
        try:
            path = str(path)
            img = Image.open(path).convert("RGB")
            self.selected_image_path = path
            self.preview_image = img
            self.file_var.set(Path(path).name)
            self.size_var.set(f"{img.width} × {img.height}")
            self.status_var.set("图片已载入，可以设置为桌面壁纸。")
            self.render_preview()
        except Exception as exc:
            messagebox.showerror("错误", f"图片加载失败：{exc}")
            self.status_var.set("图片加载失败。")

    def clear_image(self):
        self.selected_image_path = ""
        self.preview_image = None
        self.preview_photo = None
        self.file_var.set("暂无")
        self.size_var.set("暂无")
        self.status_var.set("请选择一张图片，或从素材图库中挑选。")
        self.render_preview()

    def render_preview(self):
        if not hasattr(self, "preview_canvas"):
            return

        canvas = self.preview_canvas
        width = max(canvas.winfo_width(), 320)
        height = max(canvas.winfo_height(), 180)
        canvas.delete("all")

        if self.preview_image is None:
            canvas.create_text(
                width / 2,
                height / 2 - 14,
                text="还没有选择图片",
                fill="#ffffff",
                font=("Microsoft YaHei", 20, "bold"),
            )
            canvas.create_text(
                width / 2,
                height / 2 + 22,
                text="导入图片后会在这里看到桌面预览",
                fill="#aab4c3",
                font=("Microsoft YaHei", 11),
            )
            return

        preview = self.compose_preview(width, height)
        self.preview_photo = ImageTk.PhotoImage(preview)
        canvas.create_image(width / 2, height / 2, image=self.preview_photo)

    def compose_preview(self, width, height):
        img = self.preview_image
        img_ratio = img.width / img.height
        target_ratio = width / height

        bg = Image.new("RGB", (width, height), (15, 23, 42))
        if img_ratio > target_ratio:
            new_height = height
            new_width = int(height * img_ratio)
        else:
            new_width = width
            new_height = int(width / img_ratio)

        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        x = (width - new_width) // 2
        y = (height - new_height) // 2
        bg.paste(resized, (x, y))
        return bg

    def set_wallpaper(self):
        if not self.selected_image_path or not os.path.exists(self.selected_image_path):
            messagebox.showwarning("提示", "请先选择一张有效图片。")
            return

        self.status_var.set("正在处理图片并设置桌面壁纸...")
        self.run_async(self.apply_wallpaper, self.on_wallpaper_done, "壁纸设置失败")

    def apply_wallpaper(self):
        processed_path = self.prepare_wallpaper(
            self.selected_image_path,
            self.screen_width,
            self.screen_height,
        )

        user32 = ctypes.WinDLL("user32", use_last_error=True)
        user32.SystemParametersInfoW.restype = wintypes.BOOL
        user32.SystemParametersInfoW.argtypes = [
            wintypes.UINT,
            wintypes.UINT,
            wintypes.LPCWSTR,
            wintypes.UINT,
        ]

        success = user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            processed_path,
            SPIF_UPDATEINIFILE | SPIF_SENDCHANGE,
        )

        if not success:
            error_code = ctypes.get_last_error()
            raise RuntimeError(f"系统 API 返回失败，错误码：{error_code}")

        return processed_path

    def prepare_wallpaper(self, img_path, target_width, target_height):
        img = Image.open(img_path).convert("RGB")
        img_ratio = img.width / img.height
        screen_ratio = target_width / target_height

        canvas = Image.new("RGB", (target_width, target_height), (15, 23, 42))
        if img_ratio > screen_ratio:
            new_height = target_height
            new_width = int(new_height * img_ratio)
        else:
            new_width = target_width
            new_height = int(new_width / img_ratio)

        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        x = (target_width - new_width) // 2
        y = (target_height - new_height) // 2
        canvas.paste(resized, (x, y))

        output_path = os.path.join(tempfile.gettempdir(), "current_wallpaper_from_python.jpg")
        canvas.save(output_path, quality=95)
        return output_path

    def rounded_mask(self, width, height, radius):
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        radius = max(0, min(int(radius), min(width, height) // 2))
        draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=radius, fill=255)
        return mask

    def on_wallpaper_done(self, output_path):
        self.status_var.set("壁纸设置成功。")
        messagebox.showinfo("成功", f"壁纸设置成功！\n已按屏幕尺寸生成：{output_path}")

    def run_async(self, work, on_success, error_title):
        def runner():
            try:
                result = work()
                self.root.after(0, lambda: on_success(result))
            except Exception as exc:
                self.root.after(0, lambda error=exc: self.show_error(error_title, error))

        threading.Thread(target=runner, daemon=True).start()

    def show_error(self, title, exc):
        self.status_var.set(title)
        messagebox.showerror("错误", f"{title}：{exc}")

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def on_close(self):
        for path in self.temp_files:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except OSError:
                pass
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    WallpaperApp().run()
