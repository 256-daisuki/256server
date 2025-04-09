import requests
import json
from time import sleep

# list
links = [
    {"name": "activetk", "url": "https://www.activetk.jp"},
    {"name": "doremire", "url": "https://doremire-server.com/"},
    {"name": "keichankotaro", "url": "https://keichankotaro.com/"},
    {"name": "21emon", "url": "http://21emon.wjg.jp"},
    {"name": "tenohira", "url": "https://mcflurryoreo.github.io/"},
    {"name": "canon", "url": "https://sites.google.com/view/minecraft-canon-world"},
    {"name": "mozero", "url": "https://mozero.net"},
    {"name": "p-nsk", "url": "https://p-nsk.com"},
    {"name": "nanasi", "url": "https://nanasi-rasi.net/"},
    {"name": "koneru", "url": "https://koneruhome.com/"},
    {"name": "lolineko", "url": "https://lolineko3.net"},
    {"name": "szk", "url": "https://satsuki-blog.neocities.org"},
    {"name": "nazo", "url": "https://senpai114514.icu"},
    {"name": "kazemidori", "url": "https://nekokawa.net/"},
    {"name": "lifebooker", "url": "http://www.lifebookert935k.f5.si/"},
    {"name": "nextpatch", "url": "https://nextpatch.net"},
    {"name": "kisetsu", "url": "https://sites.google.com/view/kamera-room/%E3%83%9B%E3%83%BC%E3%83%A0"},
    {"name": "google", "url": "https://google.co.jp"},
    {"name": "ipsj", "url": "https://www.ipsj.or.jp/"},
    {"name": "dream-library", "url": "https://www.dream-library.org/"},
    {"name": "majinkz", "url": "https://majinkz.moe/"},
    {"name": "hassy", "url": "http://hassy1216.f5.si/"},
    {"name": "kaeru", "url": "https://www.kaerubasyo.com/"},
    {"name": "atshift", "url": "https://global.atserver186.jp/"},
    {"name": "linkserver", "url": "https://linkserver.jp/"},
]

# ステータスチェックと保存
def check_links():
    status_data = {}
    for link in links:
        try:
            response = requests.head(link["url"], timeout=5)
            status_code = response.status_code
            status_data[link["name"]] = "up" if 200 <= status_code < 400 else "down"
        except requests.RequestException:
            status_data[link["name"]] = "down"
    
    # JSONに情報をIN!
    with open("status.json", "w") as f:
        json.dump(status_data, f, indent=4)

if __name__ == "__main__":
    while True:
        check_links()
        sleep(600)  # 10分に一度更新する 
