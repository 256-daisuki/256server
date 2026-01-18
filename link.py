#!/usr/bin/env python3
import requests
import json
from time import sleep

# list
links = [
    {"name": "activetk", "url": "https://www.activetk.jp"},
    {"name": "doremire", "url": "https://doremire-server.com/"},
    {"name": "keichankotaro", "url": "https://keichankotaro.com/"},
    {"name": "21emon", "url": "http://21emon.wjg.jp"},
    {"name": "tenohira", "url": "https://iamonlyyour-model.net/"},
    {"name": "canon", "url": "https://canonslod.sakura.ne.jp/"},
    {"name": "mozero", "url": "https://mozero.xyz/"},
    {"name": "p-nsk", "url": "https://p-nsk.com/"},
    {"name": "nanasi", "url": "https://nanasi-rasi.net/"},
    {"name": "koneru", "url": "https://koneruhome.com/"},
    {"name": "lolineko", "url": "https://lolineko3.net"},
    {"name": "szk", "url": "http://ramuneserver323.f5.si/"},
    {"name": "nazo", "url": "https://senpai114514.icu"},
    {"name": "kazemidori", "url": "https://nekokawa.net/"},
    {"name": "lifebooker", "url": "http://www.lifebookert935k.f5.si/"},
    {"name": "nextpatch", "url": "https://nextpatch.net"},
    {"name": "kisetsu", "url": "https://sites.google.com/view/kamera-room/%E3%83%9B%E3%83%BC%E3%83%A0"},
    {"name": "google", "url": "https://google.co.jp"},
    {"name": "ipsj", "url": "https://www.ipsj.or.jp/"},
    {"name": "dream-library", "url": "https://scitech.or.jp/micommuseum/"},
    {"name": "majinkz", "url": "https://majinkz.moe/"},
    {"name": "hassy", "url": "http://hassy1216.f5.si/"},
    {"name": "kaeru", "url": "https://www.kaerubasyo.com/"},
    {"name": "atshift", "url": "https://global.atserver186.jp/"},
    {"name": "linkserver", "url": "https://linkserver.jp/"},
    {"name": "t3tra", "url": "https://t3tra.dev/"},
    {"name": "kinoemon", "url": "https://kinoemon.com/"},
    {"name": "ayane", "url": "https://ayane0857.net/"},
    {"name": "shihiro", "url": "https://shihiro.com/"},
    {"name": "wsn0672", "url": "https://wsn0672.org/"},
    {"name": "yuito", "url": "https://www.yuito-it.jp/ja"},
    {"name": "koko", "url": "https://kotetsu.dev/"},
    {"name": "kokorine", "url": "https://koko2rine.com/"},
    {"name": "dragon_scratch", "url": "https://drsb.f5.si/"}
]

# ステータスチェックと保存
def check_links():
    status_data = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }  # ← 追加: ブラウザっぽいUser-Agentでボット判定を回避
    for link in links:
        try:
            response = requests.get(link["url"], timeout=30, headers=headers, allow_redirects=True)  # ← 変更: HEAD→GETに、timeout30秒に、allow_redirects追加
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
        sleep(3600)  # 60分に一度更新する 