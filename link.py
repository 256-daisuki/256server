#!/usr/bin/env python3
"""Check linked sites and write their status for the top page."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_DIR = Path(__file__).resolve().parent
STATUS_PATH = BASE_DIR / "status.json"

CHECK_INTERVAL_SECONDS = 60 * 60
REQUEST_TIMEOUT_SECONDS = 15
MAX_WORKERS = 8

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0 Safari/537.36"
)

LINKS = [
    {"name": "activetk", "url": "https://www.activetk.jp"},
    {"name": "doremire", "url": "https://doremire-server.com/"},
    {"name": "keichankotaro", "url": "https://keichankotaro.com/"},
    {"name": "21emon", "url": "https://isami.moe/"},
    {"name": "tenohira", "url": "https://iamonlyyour-model.net/"},
    {"name": "canon", "url": "https://canonslod.sakura.ne.jp/"},
    {"name": "mozero", "url": "https://mozero.xyz/"},
    {"name": "p-nsk", "url": "https://p-nsk.com/"},
    {"name": "nanasi", "url": "https://nanasi-rasi.net/"},
    {"name": "koneru", "url": "https://koneruhome.com/"},
    {"name": "lolineko", "url": "https://lolineko3.net"},
    {"name": "szk", "url": "http://ramuneserver.net/"},
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
    {"name": "wsn0672", "url": "https://wsn0672.jp/"},
    {"name": "yuito", "url": "https://www.yuito-it.jp/ja"},
    {"name": "koko", "url": "https://kotetsu.dev/"},
    {"name": "kokorine", "url": "https://koko2rine.com/"},
    {"name": "dragon_scratch", "url": "https://drsb.f5.si/"},
    {"name": "same", "url": "https://tadanosame.com/"},
    {"name": "chikunizaki", "url": "https://157.f5.si/"},
    {"name": "371tti", "url": "https://371tti.net/"},
    {"name": "ruth", "url": "https://www.ruthoyen.com/"},
    {"name": "koneru", "url": "https://coneruserver.xyz/"},
    {"name": "gigaonion", "url": "https://gigaonion.com"},
]


def is_success_status(status_code: int) -> bool:
    return 200 <= status_code < 400


def check_link(link: dict[str, str], timeout: int = REQUEST_TIMEOUT_SECONDS) -> tuple[str, str]:
    request = Request(link["url"], headers={"User-Agent": USER_AGENT})

    try:
        with urlopen(request, timeout=timeout) as response:
            status_code = response.getcode()
    except HTTPError as error:
        status_code = error.code
    except (TimeoutError, URLError, OSError):
        return link["name"], "down"

    return link["name"], "up" if is_success_status(status_code) else "down"


def check_links(links: Iterable[dict[str, str]] = LINKS) -> dict[str, str]:
    status_data: dict[str, str] = {}

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(check_link, link) for link in links]
        for future in as_completed(futures):
            name, status = future.result()
            status_data[name] = status

    return dict(sorted(status_data.items()))


def write_status(status_data: dict[str, str], path: Path = STATUS_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        delete=False,
        newline="\n",
    ) as temp_file:
        json.dump(status_data, temp_file, ensure_ascii=False, indent=4)
        temp_file.write("\n")
        temp_path = Path(temp_file.name)

    os.replace(temp_path, path)
    os.chmod(path, 0o644)


def run_once() -> dict[str, str]:
    status_data = check_links()
    write_status(status_data)
    return status_data


def main() -> None:
    parser = argparse.ArgumentParser(description="Check linked sites and update status.json.")
    parser.add_argument("--once", action="store_true", help="run one check and exit")
    parser.add_argument("--interval", type=int, default=CHECK_INTERVAL_SECONDS, help="seconds between checks")
    args = parser.parse_args()

    while True:
        run_once()
        if args.once:
            return
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
