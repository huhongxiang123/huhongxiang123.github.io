import tkinter as tk
from tkinter import ttk, filedialog
import pygame
from PIL import Image, ImageTk, ImageDraw
import os
import re
from mutagen.mp3 import MP3
import time


# ================== 工具函数 ==================
def make_round(img, size=180):
    """制作圆形图片（封面）"""
    # 确保图片是RGBA模式
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    img.putalpha(mask)
    return img


def make_disc(size=380):
    """制作黑胶唱片背景"""
    disc = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(disc)

    # 外圈 - 深灰色
    draw.ellipse((0, 0, size, size), fill="#2a2a2a")
    # 中圈 - 黑色
    draw.ellipse((15, 15, size - 15, size - 15), fill="#1a1a1a")
    # 内圈 - 深灰色
    draw.ellipse((35, 35, size - 35, size - 35), fill="#2a2a2a")
    # 中心点
    draw.ellipse((size // 2 - 10, size // 2 - 10, size // 2 + 10, size // 2 + 10), fill="#333")
    draw.ellipse((size // 2 - 4, size // 2 - 4, size // 2 + 4, size // 2 + 4), fill="#555")

    # 添加唱盘纹路
    for i in range(4, 18, 2):
        r = size // 2 - i * 6
        if r > 20:
            draw.ellipse((size // 2 - r, size // 2 - r, size // 2 + r, size // 2 + r),
                         outline="#252525", width=1)

    return disc


# ================== 播放器主类 ==================
class MusicPlayer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("网易云音乐 - 本地播放器")
        self.master.geometry("420x850")
        self.master.configure(bg="#f5f5f5")
        self.master.resizable(False, False)

        self.pack(fill="both", expand=True)

        pygame.mixer.init()

        self.music_path = ""
        self.cover_path = ""
        self.lyric_path = ""
        self.is_playing = False
        self.is_paused = False
        self.total_time = 0
        self.lyric_list = []
        self.current_line = -1
        self.angle = 0
        self.rotation_speed = 2
        self.rotating = False
        self.is_seeking = False
        self.rotation_animation_id = None
        self.current_cover_tk = None

        # 创建唱片和封面（统一尺寸）
        self.disc_size = 380
        self.cover_size = 200  # 调整为200，与唱片中心区域匹配

        self.disc = make_disc(self.disc_size)

        # 创建默认封面（更明显的红色封面）
        default_cover = Image.new("RGB", (self.cover_size, self.cover_size), "#d43c33")
        draw = ImageDraw.Draw(default_cover)
        # 绘制一个音乐图标
        draw.ellipse((self.cover_size // 4, self.cover_size // 4,
                      self.cover_size * 3 // 4, self.cover_size * 3 // 4),
                     outline="white", width=3)
        draw.text((self.cover_size // 2 - 15, self.cover_size // 2 - 10),
                  "♪", fill="white", font=None)

        self.cover_image = make_round(default_cover, self.cover_size)

        # 测试：直接显示封面图片
        self.test_label = None

        self.create_widgets()

        # 延迟更新，确保组件已创建
        self.master.after(100, self.update_display)

    def create_widgets(self):
        # 顶部标题栏
        title_bar = tk.Frame(self, bg="#d43c33", height=50)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)

        title_label = tk.Label(title_bar, text="本地音乐", font=("微软雅黑", 16, "bold"),
                               bg="#d43c33", fg="white")
        title_label.pack(pady=10)

        # 唱片容器
        disc_frame = tk.Frame(self, bg="#f5f5f5")
        disc_frame.pack(pady=20)

        # 唱片标签
        self.disc_lbl = tk.Label(disc_frame, bg="#f5f5f5")
        self.disc_lbl.pack()

        # 歌曲信息
        info_frame = tk.Frame(self, bg="#f5f5f5")
        info_frame.pack(fill="x", padx=20, pady=5)

        self.song_lbl = tk.Label(info_frame, text="未选择歌曲",
                                 font=("微软雅黑", 16, "bold"),
                                 bg="#f5f5f5", fg="#333")
        self.song_lbl.pack()

        # 歌词显示
        lyric_frame = tk.Frame(self, bg="#f5f5f5")
        lyric_frame.pack(fill="x", padx=20, pady=10)

        self.lyric_lbl = tk.Label(lyric_frame, text="等待播放...",
                                  font=("微软雅黑", 12),
                                  bg="#f5f5f5", fg="#666",
                                  wraplength=380, justify="center")
        self.lyric_lbl.pack()

        # 进度条
        progress_frame = tk.Frame(self, bg="#f5f5f5")
        progress_frame.pack(fill="x", padx=20, pady=10)

        # 自定义进度条样式
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TScale",
                        background="#f5f5f5",
                        troughcolor="#e0e0e0",
                        sliderlength=15,
                        sliderrelief="flat")

        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Scale(progress_frame, variable=self.progress_var,
                                  from_=0, to=100, style="TScale")
        self.progress.pack(fill="x")
        self.progress.bind("<ButtonPress-1>", self.start_seek)
        self.progress.bind("<ButtonRelease-1>", self.end_seek)

        # 时间显示
        time_frame = tk.Frame(progress_frame, bg="#f5f5f5")
        time_frame.pack(fill="x", pady=5)
        self.lb_now = tk.Label(time_frame, text="00:00",
                               font=("微软雅黑", 10), bg="#f5f5f5", fg="#999")
        self.lb_now.pack(side="left")
        self.lb_total = tk.Label(time_frame, text="00:00",
                                 font=("微软雅黑", 10), bg="#f5f5f5", fg="#999")
        self.lb_total.pack(side="right")

        # 播放按钮
        btn_frame = tk.Frame(self, bg="#f5f5f5")
        btn_frame.pack(pady=15)

        self.btn_play = tk.Button(
            btn_frame, text="▶", font=("Arial", 28), width=3, height=1,
            bg="#d43c33", fg="white", bd=0, cursor="hand2",
            activebackground="#b3352d", activeforeground="white",
            relief="flat", command=self.toggle_play
        )
        self.btn_play.pack()

        # 文件选择按钮
        file_frame = tk.Frame(self, bg="#f5f5f5")
        file_frame.pack(fill="x", padx=30, pady=20)

        btn_style = {
            "font": ("微软雅黑", 11),
            "bg": "white",
            "fg": "#333",
            "bd": 1,
            "relief": "solid",
            "cursor": "hand2",
            "activebackground": "#e0e0e0",
            "height": 1,
            "width": 10
        }

        music_btn = tk.Button(file_frame, text="🎵 音乐", command=self.select_music, **btn_style)
        music_btn.pack(side="left", padx=5, expand=True, fill="x")

        cover_btn = tk.Button(file_frame, text="🖼️ 封面", command=self.select_cover, **btn_style)
        cover_btn.pack(side="left", padx=5, expand=True, fill="x")

        lyric_btn = tk.Button(file_frame, text="📝 歌词", command=self.select_lyric, **btn_style)
        lyric_btn.pack(side="left", padx=5, expand=True, fill="x")

        tip_label = tk.Label(
            self,
            text="提示：选择音乐后，可选择封面和歌词文件",
            font=("微软雅黑", 9),
            bg="#f5f5f5",
            fg="#999"
        )
        tip_label.pack(pady=5)

    def update_display(self):
        """更新唱片显示 - 完全重写，确保显示正常"""
        try:
            # 创建唱片副本
            temp_disc = self.disc.copy()

            # 计算封面粘贴位置（居中）
            # 唱片380，封面200，偏移90
            offset = (self.disc_size - self.cover_size) // 2

            # 确保封面是RGBA模式
            if self.cover_image.mode != 'RGBA':
                cover_temp = self.cover_image.convert('RGBA')
            else:
                cover_temp = self.cover_image.copy()

            # 确保大小正确
            if cover_temp.size != (self.cover_size, self.cover_size):
                cover_temp = cover_temp.resize((self.cover_size, self.cover_size),
                                               Image.Resampling.LANCZOS)

            # 粘贴封面到唱片中心
            temp_disc.paste(cover_temp, (offset, offset), cover_temp)

            # 旋转唱片
            rotated = temp_disc.rotate(-self.angle, resample=Image.Resampling.BICUBIC, expand=False)

            # 转换为PhotoImage
            self.disc_tk = ImageTk.PhotoImage(rotated)
            self.disc_lbl.config(image=self.disc_tk, width=self.disc_size, height=self.disc_size)

        except Exception as e:
            print(f"更新显示错误: {e}")
            import traceback
            traceback.print_exc()

    # ================== 文件选择 ==================
    def select_music(self):
        f = filedialog.askopenfilename(filetypes=[("音频文件", "*.mp3 *.wav *.flac *.ogg")])
        if f:
            self.music_path = f
            song_name = os.path.splitext(os.path.basename(f))[0]
            self.song_lbl.config(text=song_name)
            self.get_length()

            # 尝试自动加载同名的封面和歌词
            base_path = os.path.splitext(f)[0]
            if os.path.exists(base_path + ".jpg"):
                self.select_cover_file(base_path + ".jpg")
            elif os.path.exists(base_path + ".png"):
                self.select_cover_file(base_path + ".png")

            if os.path.exists(base_path + ".lrc"):
                self.select_lyric_file(base_path + ".lrc")

            self.lyric_lbl.config(text="已选择音乐，点击播放")

    def select_cover(self):
        f = filedialog.askopenfilename(filetypes=[("图片文件", "*.jpg *.png *.jpeg *.webp")])
        if f:
            self.select_cover_file(f)

    def select_cover_file(self, file_path):
        self.cover_path = file_path
        try:
            img = Image.open(file_path).convert("RGB")
            # 调整封面大小
            img = img.resize((self.cover_size, self.cover_size), Image.Resampling.LANCZOS)
            self.cover_image = make_round(img, self.cover_size)
            self.update_display()
            self.lyric_lbl.config(text="封面已更新")
        except Exception as e:
            print(f"加载封面失败: {e}")
            self.lyric_lbl.config(text="封面加载失败")

    def select_lyric(self):
        f = filedialog.askopenfilename(filetypes=[("歌词文件", "*.lrc")])
        if f:
            self.select_lyric_file(f)

    def select_lyric_file(self, file_path):
        self.lyric_path = file_path
        self.load_lyric()

    # ================== 歌词加载 ==================
    def load_lyric(self):
        self.lyric_list.clear()

        # 尝试多种编码
        for enc in ["utf-8", "gbk", "gb2312"]:
            try:
                with open(self.lyric_path, encoding=enc) as f:
                    lines = f.readlines()
                break
            except:
                continue
        else:
            self.lyric_lbl.config(text="歌词加载失败")
            return

        pat = re.compile(r"\[(\d+):(\d+\.?\d*)\](.*)")

        for line in lines:
            m = pat.match(line.strip())
            if m:
                minutes = int(m.group(1))
                seconds = float(m.group(2))
                time_stamp = minutes * 60 + seconds
                lyric_text = m.group(3).strip()

                if lyric_text:
                    self.lyric_list.append([time_stamp, lyric_text])

        # 按时间排序
        self.lyric_list.sort(key=lambda x: x[0])

        if self.lyric_list:
            self.lyric_lbl.config(text=f"歌词已加载 ({len(self.lyric_list)}行)")
            self.current_line = -1
        else:
            self.lyric_lbl.config(text="无有效歌词")

    # ================== 歌曲时长 ==================
    def get_length(self):
        try:
            if self.music_path.endswith(".mp3"):
                audio = MP3(self.music_path)
                self.total_time = audio.info.length
            else:
                sound = pygame.mixer.Sound(self.music_path)
                self.total_time = sound.get_length()

            minutes = int(self.total_time // 60)
            seconds = int(self.total_time % 60)
            self.lb_total.config(text=f"{minutes:02d}:{seconds:02d}")
        except Exception as e:
            print(f"获取时长失败: {e}")
            self.total_time = 0

    # ================== 播放控制 ==================
    def toggle_play(self):
        if not self.music_path:
            self.select_music()
            if not self.music_path:
                return

        if not self.is_playing:
            # 开始播放
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            self.btn_play.config(text="⏸")
            self.start_rotation()
            self.update_all()
        else:
            if self.is_paused:
                # 继续播放
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.btn_play.config(text="⏸")
                self.start_rotation()
            else:
                # 暂停播放
                pygame.mixer.music.pause()
                self.is_paused = True
                self.btn_play.config(text="▶")
                self.stop_rotation()

    # ================== 唱片旋转 ==================
    def start_rotation(self):
        if not self.rotating:
            self.rotating = True
            self.rotate_loop()

    def stop_rotation(self):
        self.rotating = False
        if self.rotation_animation_id:
            self.master.after_cancel(self.rotation_animation_id)
            self.rotation_animation_id = None

    def rotate_loop(self):
        if not self.rotating:
            return

        self.angle = (self.angle + self.rotation_speed) % 360
        self.update_display()
        self.rotation_animation_id = self.master.after(30, self.rotate_loop)

    # ================== 进度条控制 ==================
    def start_seek(self, event):
        self.is_seeking = True
        if self.rotating:
            self.stop_rotation()

    def end_seek(self, event):
        self.is_seeking = False
        if self.total_time > 0:
            val = self.progress_var.get()
            target = val / 100 * self.total_time
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(target)

            if self.is_playing and not self.is_paused:
                self.start_rotation()

    # ================== 实时更新 ==================
    def update_all(self):
        if not self.is_playing or self.is_paused:
            self.master.after(500, self.update_all)
            return

        try:
            # 获取当前播放位置
            current_pos = pygame.mixer.music.get_pos() / 1000.0

            if current_pos < 0:
                current_pos = 0

            # 更新时间显示
            minutes = int(current_pos // 60)
            seconds = int(current_pos % 60)
            self.lb_now.config(text=f"{minutes:02d}:{seconds:02d}")

            # 更新进度条
            if not self.is_seeking and self.total_time > 0:
                progress_percent = (current_pos / self.total_time) * 100
                self.progress_var.set(progress_percent)

            # 更新歌词显示
            if self.lyric_list:
                for i, (time_stamp, lyric) in enumerate(self.lyric_list):
                    if current_pos >= time_stamp - 0.2:
                        if i != self.current_line:
                            self.current_line = i
                            self.lyric_lbl.config(text=lyric, fg="#d43c33")
                    else:
                        break

        except Exception as e:
            pass

        # 继续更新
        if pygame.mixer.music.get_busy():
            self.master.after(100, self.update_all)
        else:
            # 播放完成
            self.is_playing = False
            self.is_paused = False
            self.btn_play.config(text="▶")
            self.stop_rotation()
            self.progress_var.set(0)
            self.lb_now.config(text="00:00")
            self.lyric_lbl.config(text="播放完成", fg="#666")

    def on_closing(self):
        """关闭窗口时的清理工作"""
        self.stop_rotation()
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    # 绑定关闭事件
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()