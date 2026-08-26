import base64
import datetime
import re
import tkinter as tk
import webbrowser
import configparser
from tkinter import messagebox, ttk

from app.utils import MachineUtil, LicenseUtil

"""
"""


class VIPVideoPlayer:
    def __init__(self):
        # 初始化窗口
        self.root = tk.Tk()
        self.root.title("VIP视频播放器")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        key = 'banjin-vip-player@-2026'
        # 加密key（首次生成后固定）
        self.key = key;

        # 设置透明度（0完全透明）
        self.root.configure(bg='')  # 清空背景色
        self.root.wm_attributes("-alpha", 1.0)

        # 读取配置
        self.vip_lines = self.load_ini()
        # 创建界面组件
        self.create_widgets()

    def load_ini(self):
        """
        读取ini配置
        """
        config = configparser.ConfigParser()
        config.read("config.ini", encoding="utf-8")

        lines = {}

        if "VIP" in config:
            for i, key in enumerate(config["VIP"]):
                enc_url = config["VIP"][key]
                try:
                    real_url = self.decrypt_url(enc_url)
                    lines[f"VIP{i + 1}"] = real_url
                except Exception as e:
                    print("解析失败:", key, e)

        return lines

    def encrypt_url(self, text):
        key = self.key
        result = []

        for i, c in enumerate(text):
            k = key[i % len(key)]
            result.append(chr(ord(c) ^ ord(k)))

        return base64.b64encode(
            "".join(result).encode("utf-8")
        ).decode("utf-8")

    def decrypt_url(self, text):
        key = self.key
        raw = base64.b64decode(
            text.encode("utf-8")
        ).decode("utf-8")

        result = []

        for i, c in enumerate(raw):
            k = key[i % len(key)]
            result.append(chr(ord(c) ^ ord(k)))

        return "".join(result)

    def create_widgets(self):

        self.center_window(self.root, 580, 520)

        main = tk.Frame(self.root, bg="#f5f5f5")
        main.pack(fill="both", expand=True)

        container = tk.Frame(main, bg="#f5f5f5", padx=25, pady=20)
        container.pack(fill="both", expand=True)

        tk.Label(
            container,
            text="VIP视频播放器",
            font=("微软雅黑", 18, "bold"),
            bg="#f5f5f5"
        ).pack(pady=(0, 5))

        tk.Label(
            container,
            text="支持主流视频网站VIP解析，更多内容移步: 51banjin.top",
            font=("微软雅黑", 10),
            fg="#666",
            bg="#f5f5f5"
        ).pack(pady=(0, 20))
        # 输入框
        tk.Label(
            container,
            text="请输入视频地址：",
            font=("微软雅黑", 11),
            bg="#f5f5f5"
        ).pack(anchor="w")

        self.url_var = tk.StringVar()

        self.url_entry = tk.Entry(
            container,
            textvariable=self.url_var,
            font=("微软雅黑", 10)
        )
        self.url_entry.pack(fill="x", pady=8, ipady=5)

        # 线路
        tk.Label(
            container,
            text="选择解析线路：",
            font=("微软雅黑", 11),
            bg="#f5f5f5"
        ).pack(anchor="w", pady=(10, 0))

        self.vip_var = tk.StringVar()

        self.vip_combo = ttk.Combobox(
            container,
            textvariable=self.vip_var,
            state="readonly",
            height=8,
            values=list(self.vip_lines.keys())
        )

        if self.vip_lines:
            self.vip_combo.current(0)

        self.vip_combo.pack(fill="x", pady=8, ipady=3)

        # 按钮
        btn_frame = tk.Frame(container, bg="#f5f5f5")
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="播放视频",
            command=self.play_video,
            width=14,
            bg="#4CAF50",
            fg="white",
            font=("微软雅黑", 10)
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="获取注册码",
            command=self.register_code,
            width=14,
            bg="#009BFF",
            fg="white",
            font=("微软雅黑", 10)
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="清空链接",
            command=self.clear_url,
            width=14,
            bg="#f44336",
            fg="white",
            font=("微软雅黑", 10)
        ).pack(side="left", padx=10)

        # 提示
        self.tipLabel = tk.Label(
            container,
            text="仅供学习交流使用，"+self.update_register_status(),
            fg="red",
            bg="#f5f5f5",
            font=("微软雅黑", 9)
        );
        self.tipLabel.pack();
        # 网站区域
        link_frame = tk.LabelFrame(
            container,
            text="视频网站",
            font=("微软雅黑", 10),
            bg="#f5f5f5"
        )
        link_frame.pack(fill="x", pady=20)
        websites = [
            ("腾讯视频", "https://v.qq.com/"),
            ("爱奇艺", "https://www.iqiyi.com/"),
            ("优酷", "https://www.youku.com/"),
            ("B站", "https://www.bilibili.com/"),
            ("搜狐视频", "https://tv.sohu.com/"),
            ("咪咕视频", "https://www.miguvideo.com/"),
            ("西瓜视频", "https://www.ixigua.com/")
        ]
        row = 0
        col = 0
        for name, url in websites:
            btn = tk.Button(
                link_frame,
                text=name,
                width=10,
                command=lambda u=url: webbrowser.open(u)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col == 4:
                col = 0
                row += 1

    # 让窗体显示在中央，取消直接 geometry
    def center_window(self, win, width, height):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()

        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)

        win.geometry(f"{width}x{height}+{x}+{y}")

    def play_video(self):
        """播放视频"""
        exp_date = LicenseUtil.validate_product(MachineUtil.PRODUCT)  # 假设有方法获取注册有效期
        if exp_date is not None:
            if exp_date.date() <= datetime.datetime.now().date():
                messagebox.showerror("已过期","软件已过期，请先注册")
                self.open_register()
                return
        else:
            messagebox.showerror("未注册", "请前往半斤网站免费注册")
            return;

        video_url = self.url_var.get().strip()

        # 验证链接格式
        if not self.is_valid_url(video_url):
            messagebox.showerror("错误", "请输入有效的视频链接！\n链接应以 http:// 或 https:// 开头")
            return
        line_name = self.vip_var.get()
        if line_name not in self.vip_lines:
            messagebox.showerror("错误", "请选择解析线路")
            return
        parser_prefix = self.vip_lines[line_name]
        parser_url = parser_prefix + video_url

        # 使用解析源
        #parser_url = f"https://jx.xmflv.cc/?url={video_url}"
        #parser_url = f"https://tool.bitefu.net/video/?url={video_url}&type=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16"

        # 在浏览器中打开解析后的链接
        try:
            webbrowser.open(parser_url)
            messagebox.showinfo("提示", "正在为您播放视频...")
        except Exception as e:
            messagebox.showerror("错误", f"无法打开浏览器：{str(e)}")

    def update_register_status(self):
        exp_date = LicenseUtil.validate_product(MachineUtil.PRODUCT)  # 假设有方法获取注册有效期
        if exp_date is not None:
            if exp_date.date()<=datetime.datetime.now().date():
                return f"已过期请打开半斤网站免费授权，截止日期：{exp_date.strftime('%Y-%m-%d')}"
            else:
                return f"已注册，截止日期：{exp_date.strftime('%Y-%m-%d')}"
        else:
            return "未注册"

    def is_valid_url(self, url):
        """验证URL格式是否正确"""
        pattern = re.compile(
            r'^https?://'  # http:// 或 https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # 域名
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # 可选端口
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url is not None and pattern.search(url) is not None

    def clear_url(self):
        """清空输入框"""
        self.url_var.set("")

    def register_code(self):
        """设备注册"""
        win = tk.Toplevel(self.root)
        win.title("设备注册")
        self.center_window(win, 380, 220);
        win.transient(self.root)
        win.grab_set()
        win.focus_force();
        win.resizable(False, False)

        device_code = MachineUtil.get_machine_code(MachineUtil.PRODUCT);

        tk.Label(win, text="设备机器码", font=("微软雅黑", 12), justify="left", fg="#666",
            bg="#f5f5f5"
        ).pack(pady=(0, 5))

        dev = tk.Entry(win, font=("微软雅黑", 11), justify="center", width=130)
        dev.insert(0, device_code)
        dev.config(state="readonly")
        dev.pack(pady=10, ipadx=20)

        tk.Label(win, text="请输入注册码").pack()

        reg_var = tk.StringVar()
        self.url_entry = tk.Entry(
            win,
            textvariable=reg_var,
            font=("微软雅黑", 10)
        )
        self.url_entry.pack(fill="x", pady=8, ipady=5)

        def submit():
            code = reg_var.get().strip();
            if code == '':
                messagebox.showerror("失败", "请在邮件中或者半斤网站复制License");
            else:
                exp = LicenseUtil.check_license(code, MachineUtil.get_machine_code(MachineUtil.PRODUCT));
                if exp is not None:
                    if exp.date() <= datetime.datetime.now().date():
                        messagebox.showerror("失败", "注册码错误")
                    else:
                        LicenseUtil.save_or_update_license(code);
                        # 通知主窗体
                        messagebox.showinfo("成功", "注册成功")
                        # 这里需要更新主窗体的状态
                        self.tipLabel.config(
                            text="仅供学习交流使用，" + self.update_register_status()
                        )
                        win.destroy();

        def close():
            win.destroy()

        def hrefBanjin():
            webbrowser.open("https://51banjin.top")

        # 按钮
        btn_frame = tk.Frame(win, bg="#f5f5f5")
        btn_frame.pack(pady=10)
        tk.Button(
            win,
            text="前往半斤网站",
            command=hrefBanjin,
            width=14,
            bg="#4CAF50",
            fg="white",
            font=("微软雅黑", 10)
        ).pack(side="left", padx=10)
        tk.Button(
            win,
            text="注册",
            command=submit,
            width=14,
            bg="#4CAF50",
            fg="white",
            font=("微软雅黑", 10)
        ).pack(side="left", padx=10)

        tk.Button(
            win,
            text="关闭",
            command=close,
            width=14,
            bg="#f44336",
            fg="white",
            font=("微软雅黑", 10)
        ).pack(side="left", padx=10)

    def run(self):
        """运行应用"""
        self.root.resizable(False, False)
        self.root.mainloop()