import requests
import os
import re
import datetime
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from moviepy import VideoFileClip, AudioFileClip

# 请求头信息（实际使用时建议从配置文件读取或动态获取）
BILI_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    'cookie': '''buvid3=EB6F3D66-02F6-11A6-5AD2-50337DEDD7B788344infoc; b_nut=1766832788; _uuid=1AB75B10E-61010B-CB9E-10BBF-EC38D98B10E8291813infoc; CURRENT_QUALITY=0; buvid4=1316E840-BF64-FB88-F6D1-97DF80B6E05589402-025122718-XcBN+471fX7r4X5IUw1rrw%3D%3D; buvid_fp=2d5789b5aa80e57c3bd646e797799d47; rpdid=|(k))JRRJYkJ0J'u~YY)Jk~)m; theme-tip-show=SHOWED; SESSDATA=6fe7e711%2C1787821956%2C9264b%2A22CjAlNax74efVMOMZ8lQvHTINGKBerLFON2kwrtDILJNyMyjgG-LLaGxisefHgKDTrqESVlgyUnI4RVF4WEM5U1FLZnZveTkxX19DdXoyWmE0VlhaUkNiRnFCV1N5Q2dsZC1kaXlUWVJfZnV1amR3elBqWElHaXhVanVTSVFNdG9IZm83dkRoMzZRIIEC; bili_jct=aa75cd38ade88bdefb4b89d7a260eb5d; DedeUserID=3691012830529795; DedeUserID__ckMd5=a31892cffe47164b; theme-avatar-tip-show=SHOWED; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzI4NzQ0NTQsImlhdCI6MTc3MjYxNTE5NCwicGx0IjotMX0.wX4FCQ1wTIDotsjgIdiGzSb3RSZWINs1TSJsyXJbL1k; bili_ticket_expires=1772874394; home_feed_column=5; bmg_af_switch=1; bmg_src_def_domain=i2.hdslb.com; browser_resolution=1536-735; sid=5o5hgk33; bp_t_offset_3691012830529795=1175905940487012352; CURRENT_FNVAL=4048; b_lsid=FEAAE934_19CB8C8427B''',
    'referer': 'https://www.bilibili.com/'
}


def extract_bv_from_url(url):
    """从完整的B站视频链接中提取BV号"""
    # 匹配模式：/video/BV1xxxxxx/
    pattern = r'/video/(BV[a-zA-Z0-9]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    # 如果直接传入的是BV号，也支持
    if re.match(r'^BV[a-zA-Z0-9]+$', url.strip()):
        return url.strip()
    return None


def send_url(bili_url, headers):
    """
    发送请求获取视频和音频的直链
    :param bili_url: 视频页面URL
    :param headers: 请求头
    :return: 视频直链, 音频直链
    """
    response = requests.get(url=bili_url, headers=headers)
    response.raise_for_status()
    # 匹配画面链接、音频链接
    rule = r'"baseUrl":"(.+?)"'
    result = re.findall(rule, response.text)
    if len(result) < 2:
        raise Exception("未找到视频/音频链接，可能是页面结构变化或请求被拦截")
    video_url = result[0]
    audio_url = result[-1]
    return video_url, audio_url


def download_file(url, headers, filepath, progress_callback=None):
    """
    下载文件，支持进度回调
    :param url: 文件URL
    :param headers: 请求头
    :param filepath: 保存路径
    :param progress_callback: 进度回调函数，接收已下载字节和总字节
    """
    response = requests.get(url=url, headers=headers, stream=True, timeout=(10, 30))
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if progress_callback and total_size > 0:
                    progress_callback(downloaded, total_size)
    return total_size


def merge_video(video_path, audio_path, output_dir=None):
    """
    合并视频和音频
    :param video_path: 视频文件路径
    :param audio_path: 音频文件路径
    :param output_dir: 输出目录，默认为当前目录下的videos文件夹
    :return: 最终视频文件路径
    """
    if output_dir is None:
        output_dir = 'videos'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"bili_video_{timestamp}.mp4"
    output_path = os.path.join(output_dir, output_filename)

    # 使用moviepy合成
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    final_video = video.with_audio(audio)
    final_video.write_videofile(output_path, logger=None, verbose=False)

    # 释放资源
    video.close()
    audio.close()

    # 删除临时文件
    os.remove(video_path)
    os.remove(audio_path)

    return output_path


class BiliDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("B站视频下载器")
        self.root.geometry("700x550")
        self.root.resizable(True, True)

        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')

        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 输入区域
        input_frame = ttk.LabelFrame(main_frame, text="视频链接或BV号", padding="5")
        input_frame.pack(fill=tk.X, pady=5)

        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(input_frame, textvariable=self.url_var, font=('Arial', 10))
        url_entry.pack(fill=tk.X, padx=5, pady=5)

        # 按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        self.download_btn = ttk.Button(btn_frame, text="下载视频", command=self.start_download_video)
        self.download_btn.pack(side=tk.LEFT, padx=5)

        self.audio_btn = ttk.Button(btn_frame, text="仅下载音频", command=self.start_download_audio)
        self.audio_btn.pack(side=tk.LEFT, padx=5)

        self.batch_btn = ttk.Button(btn_frame, text="批量下载(BV列表)", command=self.open_batch_window)
        self.batch_btn.pack(side=tk.LEFT, padx=5)

        # 输出目录选择
        dir_frame = ttk.Frame(main_frame)
        dir_frame.pack(fill=tk.X, pady=5)

        ttk.Label(dir_frame, text="保存目录:").pack(side=tk.LEFT, padx=5)
        self.output_dir_var = tk.StringVar(value="videos")
        dir_entry = ttk.Entry(dir_frame, textvariable=self.output_dir_var)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(dir_frame, text="浏览", command=self.select_output_dir).pack(side=tk.LEFT, padx=5)

        # 进度条区域
        progress_frame = ttk.LabelFrame(main_frame, text="下载进度", padding="5")
        progress_frame.pack(fill=tk.X, pady=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)

        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        status_label.pack(anchor=tk.W, padx=5, pady=2)

        # 日志区域
        log_frame = ttk.LabelFrame(main_frame, text="下载日志", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.log_text = tk.Text(log_frame, height=12, wrap=tk.WORD, font=('Consolas', 9))
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 禁用下载按钮状态管理
        self.is_downloading = False

    def log(self, message):
        """在日志区域添加消息"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def select_output_dir(self):
        """选择输出目录"""
        directory = filedialog.askdirectory(title="选择保存目录")
        if directory:
            self.output_dir_var.set(directory)

    def update_progress(self, current, total, phase=""):
        """更新进度条"""
        if total > 0:
            percent = (current / total) * 100
            self.progress_var.set(percent)
            self.status_var.set(f"{phase} {current / 1024 / 1024:.1f}MB / {total / 1024 / 1024:.1f}MB ({percent:.1f}%)")
        self.root.update_idletasks()

    def reset_ui_state(self):
        """重置UI状态"""
        self.is_downloading = False
        self.download_btn.config(state=tk.NORMAL)
        self.audio_btn.config(state=tk.NORMAL)
        self.batch_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        self.status_var.set("就绪")

    def start_download_video(self):
        """开始下载视频（合并音视频）"""
        if self.is_downloading:
            messagebox.showwarning("提示", "正在下载中，请稍后...")
            return

        url_or_bv = self.url_var.get().strip()
        if not url_or_bv:
            messagebox.showerror("错误", "请输入视频链接或BV号")
            return

        bv = extract_bv_from_url(url_or_bv)
        if not bv:
            messagebox.showerror("错误", "无法识别视频链接或BV号，请检查输入格式")
            return

        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED)
        self.audio_btn.config(state=tk.DISABLED)
        self.batch_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)

        thread = threading.Thread(target=self.download_video_task, args=(bv, False), daemon=True)
        thread.start()

    def start_download_audio(self):
        """开始仅下载音频"""
        if self.is_downloading:
            messagebox.showwarning("提示", "正在下载中，请稍后...")
            return

        url_or_bv = self.url_var.get().strip()
        if not url_or_bv:
            messagebox.showerror("错误", "请输入视频链接或BV号")
            return

        bv = extract_bv_from_url(url_or_bv)
        if not bv:
            messagebox.showerror("错误", "无法识别视频链接或BV号，请检查输入格式")
            return

        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED)
        self.audio_btn.config(state=tk.DISABLED)
        self.batch_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)

        thread = threading.Thread(target=self.download_audio_only_task, args=(bv,), daemon=True)
        thread.start()

    def download_video_task(self, bv, is_batch=False, batch_callback=None):
        """下载视频并合成的任务"""
        try:
            b_url = f'https://www.bilibili.com/video/{bv}/'
            self.log(f"开始处理视频: {bv}")

            # 获取直链
            self.status_var.set("正在获取视频信息...")
            v_url, a_url = send_url(b_url, BILI_HEADERS)
            self.log("成功获取视频和音频直链")

            # 临时文件路径
            temp_dir = "temp_downloads"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            v_path = os.path.join(temp_dir, f"{bv}_video.mp4")
            a_path = os.path.join(temp_dir, f"{bv}_audio.mp3")

            # 下载视频
            self.status_var.set("正在下载视频...")
            self.log("开始下载视频流...")
            download_file(v_url, BILI_HEADERS, v_path,
                          lambda cur, total: self.update_progress(cur, total, "下载视频:"))
            self.log(f"视频下载完成")

            # 下载音频
            self.status_var.set("正在下载音频...")
            self.log("开始下载音频流...")
            download_file(a_url, BILI_HEADERS, a_path,
                          lambda cur, total: self.update_progress(cur, total, "下载音频:"))
            self.log(f"音频下载完成")

            # 合成
            self.status_var.set("正在合成视频...")
            self.log("正在合成视频和音频...")
            output_dir = self.output_dir_var.get()
            output_path = merge_video(v_path, a_path, output_dir)
            self.log(f"合成完成！视频保存至: {output_path}")

            if not is_batch:
                messagebox.showinfo("完成", f"视频下载并合成完成！\n保存位置: {output_path}")
            else:
                if batch_callback:
                    batch_callback(True, bv, output_path)

            self.status_var.set("下载完成")

        except Exception as e:
            error_msg = f"下载失败: {str(e)}"
            self.log(f"错误: {error_msg}")
            if not is_batch:
                messagebox.showerror("错误", error_msg)
            else:
                if batch_callback:
                    batch_callback(False, bv, error_msg)
        finally:
            if not is_batch:
                self.reset_ui_state()

    def download_audio_only_task(self, bv):
        """仅下载音频的任务"""
        try:
            b_url = f'https://www.bilibili.com/video/{bv}/'
            self.log(f"开始提取音频: {bv}")

            # 获取直链
            self.status_var.set("正在获取音频信息...")
            _, a_url = send_url(b_url, BILI_HEADERS)
            self.log("成功获取音频直链")

            # 保存路径
            output_dir = self.output_dir_var.get()
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_filename = f"bili_audio_{bv}_{timestamp}.mp3"
            audio_path = os.path.join(output_dir, audio_filename)

            # 下载音频
            self.status_var.set("正在下载音频...")
            self.log("开始下载音频...")
            download_file(a_url, BILI_HEADERS, audio_path,
                          lambda cur, total: self.update_progress(cur, total, "下载音频:"))
            self.log(f"音频下载完成！保存至: {audio_path}")

            messagebox.showinfo("完成", f"音频下载完成！\n保存位置: {audio_path}")
            self.status_var.set("下载完成")

        except Exception as e:
            error_msg = f"下载失败: {str(e)}"
            self.log(f"错误: {error_msg}")
            messagebox.showerror("错误", error_msg)
        finally:
            self.reset_ui_state()

    def open_batch_window(self):
        """打开批量下载窗口"""
        batch_window = tk.Toplevel(self.root)
        batch_window.title("批量下载 - 输入BV号列表")
        batch_window.geometry("500x400")
        batch_window.transient(self.root)

        frame = ttk.Frame(batch_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="每行一个BV号或完整视频链接").pack(anchor=tk.W)
        text_area = tk.Text(frame, height=15, font=('Consolas', 10))
        text_area.pack(fill=tk.BOTH, expand=True, pady=5)

        # 预设一些示例
        text_area.insert(tk.END, "BV1BdARz5EJp\nBV1CufaBkEJK\nBV12GASzuEHy")

        def start_batch():
            content = text_area.get("1.0", tk.END).strip()
            if not content:
                messagebox.showwarning("警告", "请输入BV号列表")
                return

            lines = [line.strip() for line in content.split('\n') if line.strip()]
            bv_list = []
            for line in lines:
                bv = extract_bv_from_url(line)
                if bv:
                    bv_list.append(bv)
                else:
                    messagebox.showerror("错误", f"无法识别: {line}\n请确保每行是BV号或完整的B站视频链接")
                    return

            if not bv_list:
                messagebox.showerror("错误", "没有有效的BV号")
                return

            batch_window.destroy()
            self.start_batch_download(bv_list)

        ttk.Button(frame, text="开始批量下载", command=start_batch).pack(pady=10)

    def start_batch_download(self, bv_list):
        """开始批量下载"""
        if self.is_downloading:
            messagebox.showwarning("提示", "正在下载中，请稍后...")
            return

        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED)
        self.audio_btn.config(state=tk.DISABLED)
        self.batch_btn.config(state=tk.DISABLED)

        self.log(f"开始批量下载，共 {len(bv_list)} 个视频")

        def batch_task():
            success_count = 0
            fail_list = []

            for idx, bv in enumerate(bv_list, 1):
                self.log(f"\n===== 开始下载第 {idx}/{len(bv_list)} 个: {bv} =====")

                def callback(success, bv_id, msg):
                    nonlocal success_count
                    if success:
                        success_count += 1
                        self.log(f"✓ {bv_id} 下载成功 -> {msg}")
                    else:
                        fail_list.append((bv_id, msg))
                        self.log(f"✗ {bv_id} 下载失败: {msg}")

                # 下载单个视频（同步方式）
                try:
                    b_url = f'https://www.bilibili.com/video/{bv}/'
                    self.root.after(0, lambda: self.status_var.set(f"正在处理: {bv}"))
                    v_url, a_url = send_url(b_url, BILI_HEADERS)

                    temp_dir = "temp_downloads"
                    if not os.path.exists(temp_dir):
                        os.makedirs(temp_dir)
                    v_path = os.path.join(temp_dir, f"{bv}_video.mp4")
                    a_path = os.path.join(temp_dir, f"{bv}_audio.mp3")

                    self.root.after(0, lambda: self.log(f"下载视频流: {bv}"))
                    download_file(v_url, BILI_HEADERS, v_path)

                    self.root.after(0, lambda: self.log(f"下载音频流: {bv}"))
                    download_file(a_url, BILI_HEADERS, a_path)

                    self.root.after(0, lambda: self.log(f"合成视频: {bv}"))
                    output_dir = self.output_dir_var.get()
                    output_path = merge_video(v_path, a_path, output_dir)

                    callback(True, bv, output_path)
                except Exception as e:
                    callback(False, bv, str(e))

            # 批量下载完成
            self.root.after(0, lambda: self.log(f"\n批量下载完成！成功: {success_count}, 失败: {len(fail_list)}"))
            if fail_list:
                self.root.after(0, lambda: self.log("失败列表:"))
                for bv, err in fail_list:
                    self.root.after(0, lambda b=bv, e=err: self.log(f"  {b}: {e}"))

            self.root.after(0, lambda: messagebox.showinfo("批量下载完成",
                                                           f"成功: {success_count}\n失败: {len(fail_list)}\n详情请查看日志"))
            self.root.after(0, self.reset_ui_state)

        thread = threading.Thread(target=batch_task, daemon=True)
        thread.start()


def main():
    root = tk.Tk()
    app = BiliDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()