import datetime
import hashlib
import os
import webbrowser
from .MachineUtil import MachineUtil

class LicenseUtil:

    LICENSE_PATH = os.path.join(
        os.getenv("PROGRAMDATA"),
        "BanJin",
        "license.txt"
    )

    # 保存 license
    @staticmethod
    def save_license(license_str):
        dir_path = os.path.dirname(LicenseUtil.LICENSE_PATH)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(LicenseUtil.LICENSE_PATH, "w", encoding="utf-8") as f:
            f.write(license_str.strip())

    # 读取 license
    @staticmethod
    def load_license():
        if not os.path.exists(LicenseUtil.LICENSE_PATH):
            return None
        with open(LicenseUtil.LICENSE_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()

    # 获取指定产品 license
    @staticmethod
    def get_license(product):
        if not os.path.exists(LicenseUtil.LICENSE_PATH):
            return None
        with open(LicenseUtil.LICENSE_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith(product + "|"):
                return line.strip()
        return None


    # 保存或更新 license
    @staticmethod
    def save_or_update_license(new_license):
        product = new_license.split("|")[0]
        lines = []
        if os.path.exists(LicenseUtil.LICENSE_PATH):
            with open(LicenseUtil.LICENSE_PATH, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
        replaced = False
        for i in range(len(lines)):
            if lines[i].startswith(product + "|"):
                lines[i] = new_license
                replaced = True
                break
        if not replaced:
            lines.append(new_license)
        dir_path = os.path.dirname(LicenseUtil.LICENSE_PATH)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(LicenseUtil.LICENSE_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


    # 校验产品 license
    @staticmethod
    def validate_product(product):
        lic = LicenseUtil.get_license(product)
        if lic is None:
            return None
        local_machine = MachineUtil.get_machine_code(product)
        return LicenseUtil.check_license(lic, local_machine)


    # 核心校验
    @staticmethod
    def check_license(license_str, local_machine):
        arr = license_str.split("|")
        if len(arr) != 4:
            return None
        product = arr[0]
        expire = arr[1]
        machine = arr[2]
        sign = arr[3]
        # 检查 product
        if not local_machine.startswith(product + "-"):
            return None
        # 检查机器
        local_machine_part = local_machine[len(product) + 1:]
        if machine != local_machine_part:
            return None
        # 检查时间
        try:
            exp = datetime.datetime.strptime(expire, "%Y-%m-%d")
        except:
            return None
        if datetime.datetime.now().date() > exp.date():
            return None
        # 校验签名
        raw = f"{product}|{expire}|{machine}|Dikaer@2013"
        my_sign = LicenseUtil.get_md5(raw)[:4].upper()
        if my_sign == sign:
            return exp
        else:
            return None

    # MD5
    @staticmethod
    def get_md5(text):
        m = hashlib.md5()
        m.update(text.encode("utf-8"))
        return m.hexdigest().upper()

    # 打开浏览器
    @staticmethod
    def open_browser(url):
        webbrowser.open(url)

    # 字符串转 int
    @staticmethod
    def int_1(a):
        if not a:
            return 0
        try:
            return int(a.replace("￥", ""))
        except:
            return 0