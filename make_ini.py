import base64
import configparser

KEY = "banjin-vip-player@-2026"

def encrypt(text):
    result = []

    for i, c in enumerate(text):
        k = KEY[i % len(KEY)]
        result.append(chr(ord(c) ^ ord(k)))
    return base64.b64encode("".join(result).encode("utf-8")).decode("utf-8")

urls = [
    "https://jx.xmflv.cc/?url=",
    "https://tool.bitefu.net/video/?type=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16&url=",
    "https://www.ckplayer.vip/jiexi/?url=",
    "https://jx.playerjy.com/?url="
]

config = configparser.ConfigParser()
config["VIP"] = {}

for i, url in enumerate(urls):
    enc = encrypt(url)
    config["VIP"][f"VIP{i+1}"] = enc

with open("config.ini", "w", encoding="utf-8") as f:
    config.write(f)

print("生成完成")