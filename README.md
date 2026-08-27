# vipPlayer

一键解析播放 VIP 视频，支持 B 站、腾讯视频、爱奇艺、优酷、搜狐、咪咕、西瓜等主流 VIP 视频。

> 仅供学习交流使用，请勿用于商业用途。软件解析能力依赖第三方接口，接口失效时请前往 [半斤网站](https://51banjin.top) 获取最新授权或更换解析线路。

## 功能特性

- 🎬 **一键播放**：粘贴视频地址 → 选择解析线路 → 自动在浏览器中打开解析后的播放页面。
- 🌐 **多线路支持**：内置多条 VIP 解析线路，可在下拉框中切换，单条失效不影响整体使用。
- 📺 **常用网站导航**：界面内集成腾讯视频、爱奇艺、优酷、B 站、搜狐视频、咪咕视频、西瓜视频等常用站点快捷入口。
- 🔐 **设备授权管理**：基于本机硬件信息（磁盘序列号 / CPU ID / 内存容量）生成机器码，配吉 License 实现一机一码授权校验。
- ⚙️ **配置自生成**：提供 `make_ini.py` 脚本，可一键重新生成 `config.ini`，方便维护解析线路。

## 目录结构

```text
vipPlayer/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   └── VIPVideoPlayer.py   # 主程序：窗口界面、解析播放、设备注册逻辑
│   └── utils/
│       ├── __init__.py
│       ├── LicenseUtil.py      # License 校验、读写、签名工具
│       └── MachineUtil.py      # 机器码生成（磁盘 / CPU / 内存）
├── config.ini                  # 解析线路配置（加密存储，由 make_ini.py 生成）
├── make_ini.py                 # 配置生成脚本：维护解析线路
├── vip_player.py               # 程序入口
├── requirements.txt            # 依赖清单
├── LICENSE
└── README.md
```

## 环境要求

- 操作系统：Windows 7 及以上（机器码功能依赖 Windows API，其他系统会回退为通用标识）
- Python：>= 3.8（推荐 3.10 及以上）

## 安装

1. 克隆仓库

    ```bash
    git clone <仓库地址>
    cd vipPlayer
    ```

2. （推荐）创建虚拟环境

    ```bash
    python -m venv venv
    venv\Scripts\activate      # Windows
    # source venv/bin/activate # macOS / Linux
    ```

3. 安装依赖（本项目核心功能基于标准库，依赖为可选增强项）

    ```bash
    pip install -r requirements.txt
    ```

## 使用方式

### 直接运行

```bash
python vip_player.py
```

运行后会弹出软件窗口：

1. 在「请输入视频地址」输入框中粘贴 VIP 视频链接。
2. 在「选择解析线路」下拉框中选择一条线路。
3. 点击「播放视频」，软件会自动调用系统浏览器打开解析后的播放页面。
4. 如需清空输入，点击「清空链接」即可。

### 设备注册

- 点击「获取注册码」按钮，弹出注册窗口。
- 复制窗口中显示的「设备机器码」。
- 在半斤网站（[https://51banjin.top](https://51banjin.top)）免费获取对应产品的 License。
- 将 License 粘贴到「请输入注册码」输入框，点击「注册」完成授权。
- 授权信息保存在 `C:\ProgramData\BanJin\license.txt`，按产品区分，可一机多产品共存。

## 配置说明

`config.ini` 存放各条 VIP 解析线路，URL 经 XOR + Base64 加密存储，避免明文暴露：

```ini
[VIP]
vip1 = <加密后的解析线路1>
vip2 = <加密后的解析线路2>
...
```

如需新增或更换解析线路，请修改 `make_ini.py` 中的 `urls` 列表后执行：

```bash
python make_ini.py
```

脚本会自动重新生成 `config.ini`。

## 打包发布（可选）

使用 PyInstaller 打包成单文件 exe：

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --name vipPlayer vip_player.py
```

打包产物位于 `dist/` 目录下。

## 许可证

详见 [LICENSE](LICENSE)。

## 免责声明

本项目仅用于个人学习与技术交流，不存储、不传播任何视频内容，所有解析能力均由第三方公共接口提供，版权归原网站所有。使用本软件产生的一切后果由使用者自行承担，开发者不承担任何法律责任。请在合法合规的前提下使用。
