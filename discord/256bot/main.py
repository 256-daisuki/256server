import discord
import random
import requests
import subprocess
import re
import os
import math
import aiohttp
import asyncio
from aiohttp import ClientSession, ClientResponseError
import json
from datetime import datetime
import time
import pytz
import psutil
from enum import Enum
import logging
from discord import app_commands
from discord.ext import commands
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from PIL import Image, ImageOps
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

bot = commands.Bot(command_prefix='/', intents=intents)

browser = None

@client.event
async def on_ready():
    logging.info(" ____  ____   __   _           _")
    logging.info("|___ \| ___| / /_ | |__   ___ | |_")
    logging.info("  __) |___ \| '_ \| '_ \ / _ \| __|")
    logging.info(" / __/ ___) | (_) | |_) | (_) | |_")
    logging.info("|_____|____/ \___/|_.__/ \___/ \__|")


    logging.info(f'Logged in as {client.user} (ID: {client.user.id})')
    logging.info('------')

    # 認識しているサーバーをlist型で取得し、その要素の数を 変数:guild_count に格納しています。
    guild_count = len(client.guilds)
    # 関数:lenは、引数に指定したオブジェクトの長さや要素の数を取得します。
    
    game = discord.Game(f'{guild_count} サーバー数の人たちを監視中')
    # game = discord.Game(f'お前らを監視中')
    # f文字列(フォーマット済み文字列リテラル)は、Python3.6からの機能です。
    
    # BOTのステータスを変更する
    await client.change_presence(status=discord.Status.online, activity=game)
    # パラメーターの status でステータス状況(オンライン, 退席中など)を変更できます。

    logging.info("sterted!")
    await tree.sync()#スラッシュコマンドを同期

# メッセージを受信した時に呼ばれる
@client.event
async def handle_commands(message):
    # 自分のメッセージを無効
    if message.author == client.user:
        return

    # shellコマンド
    if message.content.startswith('$'):
        allowed_users = [891521181990129675, 997588139235360958, 664814874328563712]  # 許可するユーザーのIDリスト
        if message.author.id in allowed_users:

            cmd = message.content[2:]
            current_directory = os.getcwd()
            command_with_prompt = f'discord@256server:{current_directory}$ {cmd}\n'

            # カレントディレクトリを変更してからコマンドを実行
            if cmd.startswith("cd "):  # コマンドが「cd 」で始まる場合
                new_directory = cmd[3:].strip()
                os.chdir(new_directory)
                current_directory = os.getcwd()
                response = f'```discord@256server:{current_directory}$ cd {new_directory}```'
            else:
                # カレントディレクトリを保持したままコマンドを実行
                result = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True, cwd=current_directory
                )
                stdout, stderr = result.communicate()
                output = stdout.decode() + stderr.decode()
                response = f'```{command_with_prompt}{output}```'
                
            await message.channel.send(response)
        else:
            await message.channel.send('許してぇてぇ')
    if message.content.startswith('/send_message'):
        allowed_users = [891521181990129675, 997588139235360958, 1110918238327545886]  # 許可するユーザーのIDリスト
        if message.author.id in allowed_users:
            # コマンドの内容を取得
            content = message.content.split()
            # コマンドの引数が足りない場合はエラーメッセージを送信
            if len(content) < 3:
                await message.channel.send("コマンドの引数が不足しています。")
                return
            # チャンネルのURLとメッセージを取得
            channel_url = content[1]
            message_content = ' '.join(content[2:])
            # チャンネルのURLからチャンネルを取得
            channel = client.get_channel(int(channel_url.split('/')[-1]))
            if channel is None:
                await message.channel.send("指定されたチャンネルが見つかりませんでした。")
                return
            # メッセージを送信
            await channel.send(message_content)
        else:
            await message.channel.send('許してぇてぇ')

@client.event
async def on_message_edit(before, after):
    # メッセージがBOTのIDによって編集された場合
    if after.author.id == 949479338275913799 and before.content != after.content:
        if len(after.attachments) > 0:
            # メッセージに添付された画像を保存
            for attachment in after.attachments:
                image_url = attachment.url
                image_filename = attachment.filename

                # 画像を保存
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url) as response:
                        if response.status == 200:
                            image_data = await response.read()
                            with open(f'/home/discord/python/saved_images/{image_filename}', 'wb') as image_file:
                                image_file.write(image_data)
        else:
            # 画像が削除された場合の処理
            await after.channel.send('🚨 削除を検知しました。🚨')
            
            # 削除される前のメッセージに添付されていた画像がある場合、それを一緒に送信
            if len(before.attachments) > 0:
                for attachment in before.attachments:
                    # 保存した画像を直接メッセージに添付
                    with open(f'/home/discord/python/saved_images/{attachment.filename}', 'rb') as image_file:
                        image = discord.File(image_file)
                        await after.channel.send('😏',file=image)

                        logging.info("Quote sent successfully")
            pass

@tree.command(name="test",description="テストコマンドです。")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("しらすじゅーす！",ephemeral=False)

    logging.info("Test command executed")

@tree.command(name="help", description="コマンドのヘルプを表示します")
async def help_command(interaction: discord.Interaction):
    # コマンド一覧を作成
    command_list = [
        ("/test", "Botの動作が怪しいときに使ってください　適当に返答します"),
        ("/ping", "Botにpingを打ちます。応答するかどうか　testとほぼ一緒です"),
        # ("/echo", "好きなことを言わすことができます"),
        ("/omikuji", "凶しか入ってないおみくじです"),
        # ("/google", "google検索します　そのまま"),
        ("/yahoo", "yahooニュースを表示します"),
        ("/embed", "Botがユーザーの代わりにembedを送信します"),
        # ("/screenshot", "Webサイトのスクリーンショットを送信します(httpsをちゃんとつけてください)")
        ("/tw_archive", "Twitter(X)の画像を保存し、表示します サーバーに保存をするのでツイートが削除されても、凍結されても残ります。魚拓用にどうぞ"),
        ("/set_auto_tw_archive", "設定したテキストチャンネルに貼られたTwitter(X)の画像に対し自動的に/tw_img_archiveを実行します　イラスト共有チャンネルなどに如何でしょう？")
    ]

    # Embedを作成
    embed = discord.Embed(title="Help! 📕", description="利用可能なコマンドの一覧です", color=0x00ff00)

    # コマンド一覧をEmbedに追加
    for name, description in command_list:
        embed.add_field(name=name, value=description, inline=False)

    # メッセージを送信
    await interaction.response.send_message(embed=embed, ephemeral=True)

    logging.info("Help command executed")

@tree.command(name="ping", description="BOTにpingを打ちます")
async def ping_command(interaction: discord.Interaction):
    # Ping値を秒単位で取得
    raw_ping = client.latency

    # ミリ秒に変換して丸める
    ping = round(raw_ping * 1000)

    # 送信する
    embed = discord.Embed(
        title="Pong!🏓", 
        color=0x00ff00,
        description=f"BotのPing値は{ping}msです。")
    await interaction.response.send_message(embed=embed)

@tree.command(name="omikuji", description="おみくじ　凶限定")
async def ping_command(interaction: discord.Interaction):
    omikuji = ["大凶","中凶","小凶","末凶","吉凶","凶"]
    await interaction.response.send_message(f"今日のお前の運勢 {random.choice(omikuji)}")

    logging.info("Omikuji command executed")

#@tree.command(name="echo", description="あんなことやそんなことまで言います")
#async def echo_command(interaction: discord.Interaction, *, text: str):
#    await interaction.response.send_message(text, ephemeral=False)

#@tree.command(name="google", description="Googleで検索結果を表示します")
#async def google_command(interaction: discord.Interaction, *, search_word: str):
#    pages_num = 10 + 1  # 上位から何件までのサイトを抽出するか指定
#    result_embed = discord.Embed(title=f"Google検索結果: {search_word}", color=0xfabb05)
#
#    url = f'https://www.google.co.jp/search?hl=ja&num={pages_num}&q={search_word}'
#    request = requests.get(url)
#    soup = BeautifulSoup(request.text, "html.parser")
#    search_site_list = soup.select('div.tF2Cxc > a')
#
#    for site in search_site_list:
#        try:
#            site_title = site.select('h3')[0].text
#        except IndexError:
#            try:
#                site_title = site.select('img')[0]['alt']
#            except IndexError:
#                site_title = "No title available"
#
#        site_url = site['href'].replace('/url?q=', '').split('&')[0]
#
#        link_text = f"[{site_title}]({site_url})"
#        result_embed.add_field(name='\u200b', value=link_text, inline=False)
#
#    await interaction.response.send_message(embed=result_embed, ephemeral=False)


@tree.command(name="yahoo", description="yahooニュースの記事を出力します")
async def yahoo_news_command(interaction: discord.Interaction):
    URL = "https://www.yahoo.co.jp/"
    rest = requests.get(URL)
    soup = BeautifulSoup(rest.text, "html.parser")

    data_list = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))

    result_embed = discord.Embed(title="Yahooニューストップ見出し", color=0xff0839)
    for data in data_list:
        title = data.span.string
        url = data.attrs["href"]

        # マークダウン形式でリンクを埋め込む
        link_text = f"[{title}]({url})"
        result_embed.add_field(name='\u200b', value=link_text, inline=False)

    await interaction.response.send_message(embed=result_embed, ephemeral=False)
    
    logging.info("Yahoo news command executed")

@tree.command(name="server_info", description="サーバーの情報を表示します")
async def server_info_command(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"{guild.name} の情報", color=0x00ff00)
    embed.add_field(name="サーバー名", value=guild.name, inline=False)
    embed.add_field(name="サーバーID", value=guild.id, inline=False)
    embed.add_field(name="サーバー人数", value=guild.member_count, inline=False)
    embed.add_field(name="サーバー作成日", value=guild.created_at.strftime("%Y/%m/%d %H:%M:%S"), inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=False)

    logging.info("Server info command executed")

@tree.command(name="embed", description="Embedを代わりに送信してくれます")
async def embed_command(interaction: discord.Interaction, text: str, title: str = None, color: str = None,
                        author_name: str = None, author_url: str = None, author_icon_url: str = None,
                        thumbnail_url: str = None, image_url: str = None, footer_text: str = None):
    user_avatar = interaction.user.display_avatar
    user_name = interaction.user.display_name

    if color:
        # カラーコードが指定されている場合、16進数に変換
        try:
            color = int(color, 16)
        except ValueError:
            await interaction.followup.send("無効なカラーコードです。")
            return
    else:
        # カラーコードが指定されていない場合はデフォルトの色を使用
        color = 0x00ff00

    embed = discord.Embed(description=text, color=color)
    await interaction.response.defer()
    if title:
        embed.title = title 

    if author_name:
        embed.set_author(name=author_name, url=author_url, icon_url=author_icon_url)

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    if image_url:
        embed.set_image(url=image_url)

    if footer_text:
        embed.set_footer(text=footer_text)

    webhook = await interaction.channel.create_webhook(name="Embed Webhook")

    await webhook.send(embed=embed, username=user_name, avatar_url=user_avatar)
    followup_message = await interaction.followup.send("embedを作成しました。")

    # 3秒後にメッセージを削除
    await asyncio.sleep(3)
    await followup_message.delete()

    await webhook.delete()

@tree.command(name="server_usage", description="botの使用率を表示します")
async def server_usage_command(interaction: discord.Interaction):
    # プログレスバーを作成する関数
    def create_progress_bar(percentage, width=30):
        filled = math.floor(width * (percentage / 100))
        empty = width - filled
        return '[' + '|' * filled + ' ' * empty + ']'

    # CPU使用率
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # RAM使用率
    memory = psutil.virtual_memory()
    ram_used = memory.used / (1024 ** 3)  # GiBに変換
    ram_total = memory.total / (1024 ** 3)  # GiBに変換
    ram_percent = memory.percent
    
    # ディスク使用率
    disk = psutil.disk_usage('/')
    disk_used = disk.used / (1024 ** 3)  # GiBに変換
    disk_total = disk.total / (1024 ** 3)  # GiBに変換
    disk_percent = disk.percent
    
    # メッセージの構築
    embed = discord.Embed(title="サーバーステータス", color=0x00ff00)
    
    # CPU
    cpu_bar = create_progress_bar(cpu_percent)
    embed.add_field(
        name="CPU使用率",
        value=f"```{cpu_bar} [{cpu_percent:.1f}%]```",
        inline=False
    )
    
    # RAM
    ram_bar = create_progress_bar(ram_percent)
    embed.add_field(
        name="RAM使用率",
        value=f"[{ram_used:.2f}GiB / {ram_total:.2f}GiB]\n```{ram_bar} [{ram_percent:.1f}%]```",
        inline=False
    )
    
    # Disk
    disk_bar = create_progress_bar(disk_percent)
    embed.add_field(
        name="ディスク使用率",
        value=f"[{disk_used:.2f}GiB / {disk_total:.2f}GiB]\n```{disk_bar} [{disk_percent:.1f}%]```",
        inline=False
    )

    await interaction.response.send_message(embed=embed, ephemeral=False)

    logging.info("Server usage command executed")

@tree.command(name="filecount",description="現在の画像保存状況を表示します")
async def test_command(interaction: discord.Interaction):

    total_file_count = 0
    total_file_size = 0

    def get_directory_stats(path):
        total_size = 0
        file_count = 0
        
        try:
            for root, dirs, files in os.walk(path):
                file_count += len(files)
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        total_size += os.path.getsize(file_path)
                    except (OSError, PermissionError):
                        continue
            return file_count, total_size
        except (OSError, PermissionError):
            return 0, 0

    directories = {
        '/home/discord/python/saved_images': 'Make it a Quote',
        '/var/www/html/images': 'Twitterの画像',
        '/var/www/html/combined': 'Twitterの画像（合成）',
        '/var/www/html/videos': 'Twitterの動画',
        '/var/www/html/archive': 'Twitterのツイート情報',
    }
    
    embed = discord.Embed(title="画像保存状況", color=0x00ff00)
    
    for path, display_name in directories.items():
        file_count, total_size = get_directory_stats(path)
        total_file_count += file_count
        total_file_size += total_size

        if total_size >= 1024 ** 3:
            size_str = f"{total_size / (1024 ** 3):.2f} GiB"
        elif total_size >= 1024 ** 2:
            size_str = f"{total_size / (1024 ** 2):.2f} MiB"
        elif total_size >= 1024:
            size_str = f"{total_size / 1024:.2f} KiB"
        else:
            size_str = f"{total_size} B"
        
        embed.add_field (
            name=display_name,
            value=f"ファイル数: {file_count:,}\n合計サイズ: {size_str}",
            inline=False,
        )

    if total_file_size >= 1024 ** 3:
        total_size_str = f"{total_file_size / (1024 ** 3):.2f} GiB"
    elif total_file_size >= 1024 ** 2:
        total_size_str = f"{total_file_size / (1024 ** 2):.2f} MiB"
    elif total_file_size >= 1024:
        total_size_str = f"{total_file_size / 1024:.2f} KiB"
    else:
        total_size_str = f"{total_file_size} B"
    
    embed.add_field (
        name="合計",
        value=f"総ファイル数: {total_file_count:,}\n総サイズ: {total_size_str}",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=False)

    logging.info("file count command executed")

#@tree.command(name="screenshot", description="指定されたURLのスクリーンショットを撮ります")
#async def screenshot_command(interaction: discord.Interaction, url: str):
#    try:
        # Playwrightを非同期で操作
#        async with async_playwright() as p:
#            browser = await p.chromium.launch(headless=True)
#            page = await browser.new_page()
#            await page.goto(url)
            
            # スクリーンショットを撮って保存
#            screenshot_path = os.path.join("screen_image", "screenshot.png")
#            await page.screenshot(path=screenshot_path)
#            await browser.close()

        # Discordにスクリーンショットを送信
#        await interaction.response.send_message(file=discord.File(screenshot_path))

#    except Exception as e:
#        await interaction.response.send_message(f"エラーが発生しました: {e}")

# 保存先ディレクトリとベースURLの設定
SAVE_DIR = "/var/www/html/images"  # 画像保存用ディレクトリ
COMBINED_DIR = "/var/www/html/combined"  # 合成画像用ディレクトリ
ARCHIVE_DIR = "/var/www/html/archive" # ツイート情報格納ディレクトリ
VIDEO_DIR = "/var/www/html/videos" # 動画保存用ディレクトリ
PREVIEW_DIR = "/var/www/html/previews" # プレビュー画像保存用ディレクトリ
BASE_URL = "https://discord.256server.com"  # 公開URLのベース
CONFIG_FILE = "config.json"  # 設定ファイル
## 雑とか言わないで

# ログ(デバッグ用だったけどかっこいいから残す)
logging.basicConfig(level=logging.INFO)

###           Twitter画像保存関係           ###
# 選択肢用のEnum
class ActionChoice(Enum):
    add = "add"
    remove = "remove"

# 同時実行を制限するためのセマフォ
semaphore = asyncio.Semaphore(10)

# 設定ファイルの読み書き
def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        logging.error(f"設定ファイルの読み込みに失敗: {e}")
        return {}

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        logging.error(f"設定ファイルの保存に失敗: {e}")

# fxtwitter APIからツイートデータを取得
async def get_tweet_data(tweet_id):
    api_url = f"https://api.fxtwitter.com/twitter/status/{tweet_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status != 200:
                return None
            data = await response.json()
            if data.get("code") != 200:
                return None
            return data["tweet"]

# ツイートが既にアーカイブされているか確認する関数
def tweet_already_archived(tweet_id: str) -> bool:
    return os.path.exists(os.path.join(ARCHIVE_DIR, tweet_id, "tweet.json"))

# 画像をダウンロードする関数
async def download_image(session, url, save_path):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                with open(save_path, 'wb') as f:
                    f.write(await response.read())
                return save_path
    except Exception as e:
        logging.error(f"画像ダウンロードに失敗しました {url}: {e}")
    return None

# 動画のプレビュー画像をダウンロードする関数
async def download_file(session, url, save_path):
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(save_path, "wb") as f:
                    f.write(await resp.read())
                return save_path
    except Exception as e:
        logging.error(f"ダウンロード失敗 {url}: {e}")
    return None

# エラー時の送信関数
async def send_error(target, message, url, is_interaction, webhook=None):
    text = f"{message}\n[実行ツイート]({url})"
    if is_interaction:
        await target.followup.send(text)
    else:
        await webhook.send(
            text,
            username=target.author.display_name,
            avatar_url=target.author.avatar.url if target.author.avatar else None
        )

# 日付の解析関数
def parse_created_at(raw: str) -> datetime:
    return datetime.strptime(
        raw,
        "%a %b %d %H:%M:%S %z %Y"
    ).astimezone(pytz.timezone("Asia/Tokyo"))

# tweet.jsonを保存する関数
def save_tweet_json(
    tweet_id: str,
    tweet_data: dict,
    created_at: str,
    image_files=None,
    video_files=None,
    preview_files=None,
):
    archive_dir = os.path.join(ARCHIVE_DIR, tweet_id)
    os.makedirs(archive_dir, exist_ok=True)

    path = os.path.join(archive_dir, "tweet.json")

    data = {
        "tweet_id": tweet_id,
        "url": f"https://x.com/i/status/{tweet_id}",
        "author": {
            "name": tweet_data["author"]["name"],
            "screen_name": tweet_data["author"]["screen_name"],
            "avatar_url": tweet_data["author"]["avatar_url"],
        },
        "created_at": created_at,  # ISO8601 string
        "text": tweet_data.get("text", ""),
        "media": {
            "images": image_files or [],
            "videos": video_files or [],
            "previews": preview_files or [],
        }
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 動画ファイルの名前決定関数
def extract_filename(url: str) -> str:
    return url.split("/")[-1].split("?")[0]

# metrics スナップショット保存関数
def save_metrics_snapshot(tweet_id, tweet_data):
    metrics_dir = os.path.join(ARCHIVE_DIR, tweet_id, "metrics")
    os.makedirs(metrics_dir, exist_ok=True)

    now = datetime.now(pytz.timezone("Asia/Tokyo"))
    filename = now.isoformat(timespec="seconds").replace(":", "-") + ".json"
    path = os.path.join(metrics_dir, filename)

    data = {
        "captured_at": now.isoformat(),
        "like": tweet_data.get("likes"),
        "retweet": tweet_data.get("retweets"),
        "reply": tweet_data.get("replies"),
        "view": tweet_data.get("views"),
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# indexを更新する関数
INDEX_PATH = os.path.join(ARCHIVE_DIR, "index_media.json")

def update_media_index(
    tweet_id: str,
    filenames: list[str]
):
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            index = json.load(f)
    else:
        index = {}

    for name in filenames:
        index[name] = tweet_id

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

# 画像からtweetへ逆引きする関数
def find_tweet_by_image(filename):
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index = json.load(f)

    tweet_id = index.get(filename)
    if not tweet_id:
        return None

    return os.path.join(ARCHIVE_DIR, tweet_id, "tweet.json")

# 複数画像を合成する関数
def combine_images(image_paths):
    images = [Image.open(path) for path in image_paths]
    widths, heights = zip(*(img.size for img in images))

    if len(images) == 1:
        return image_paths[0]

    # 2x2グリッドで配置（最大4枚）
    max_width = max(widths)
    max_height = max(heights)
    grid_size = 2 if len(images) > 2 else 1
    total_width = max_width * grid_size
    total_height = max_height * grid_size

    new_image = Image.new('RGB', (total_width, total_height), color=(255, 255, 255))

    positions = [
        (0, 0),
        (max_width, 0),
        (0, max_height),
        (max_width, max_height)
    ]

    for img, pos in zip(images, positions):
        x_offset = pos[0] + (max_width - img.width) // 2
        y_offset = pos[1] + (max_height - img.height) // 2
        new_image.paste(img, (x_offset, y_offset))

    combined_filename = os.path.basename(image_paths[0])  # 元画像のファイル名をそのまま使用
    combined_path = os.path.join(COMBINED_DIR, combined_filename)
    new_image.save(combined_path, quality=95)
    return combined_path

# ツイート画像を処理する共通関数
async def process_tweet(interaction_or_message, url, webhook=None, silent=False,):
    is_interaction = isinstance(interaction_or_message, discord.Interaction)
    target = interaction_or_message

    # ========= URL 正規化 =========
    if not url.startswith("http"):
        url = "https://" + url

    if "x.com" not in url and "twitter.com" not in url:
        await send_error(target, "Twitter(X)のURLのみ対応しています。", url, is_interaction, webhook)
        return

    # ========= tweet_id 抽出 =========
    m = re.search(r"status/(\d+)", url)
    if not m:
        await send_error(target, "ツイートIDが見つかりませんでした。", url, is_interaction, webhook)
        return

    tweet_id = m.group(1)
    tweet_url = f"https://x.com/i/status/{tweet_id}"

    # ========= tweet_data 取得（最重要） =========
    tweet_data = await get_tweet_data(tweet_id)
    if not tweet_data:
        await send_error(target, "ツイートデータの取得に失敗しました。", url, is_interaction, webhook)
        return

    # ========= 既存チェック =========
    if tweet_already_archived(tweet_id):
        logging.info(f"{tweet_id} already archived, skip")
        return
    
    # ========= created_at =========
    created_at_dt = parse_created_at(tweet_data["created_at"])
    created_at_str = created_at_dt.isoformat()

    # ========= NSFW =========
    if tweet_data.get("possibly_sensitive") and not target.channel.is_nsfw():
        await send_error(target, "センシティブなツイートです。NSFWチャンネルで実行してください。", url, is_interaction, webhook)
        return

    # ========= media 抽出 =========
    media = tweet_data.get("media", {})
    photos = media.get("photos", [])
    videos = media.get("videos", [])

    image_urls = [p["url"] for p in photos]
    video_urls = []
    preview_urls = []

    for v in videos:
        mp4s = [f["url"] for f in v.get("formats", []) if f.get("container") == "mp4"]
        if mp4s:
            video_urls.append(mp4s[-1])

        if v.get("thumbnail_url"):
            preview_urls.append(v["thumbnail_url"])

    # ========= ダウンロード =========
    saved_images = []
    saved_videos = []
    saved_previews = []

    async with aiohttp.ClientSession() as session:
        tasks = []

        for u in image_urls:
            name = extract_filename(u)
            tasks.append(download_image(session, u, os.path.join(SAVE_DIR, name)))

        for u in video_urls:
            name = extract_filename(u)
            tasks.append(download_file(session, u, os.path.join(VIDEO_DIR, name)))

        for u in preview_urls:
            name = extract_filename(u)
            tasks.append(download_file(session, u, os.path.join(PREVIEW_DIR, name)))

        results = await asyncio.gather(*tasks)

    for p in results:
        if not p:
            continue
        name = os.path.basename(p)
        if name.endswith(".mp4"):
            saved_videos.append(name)
        elif p.startswith(PREVIEW_DIR):
            saved_previews.append(name)
        else:
            saved_images.append(name)

    # ========= index =========
    update_media_index(tweet_id, saved_images)
    update_media_index(tweet_id, saved_videos)
    update_media_index(tweet_id, saved_previews)

    # ========= JSON =========
    save_tweet_json(
        tweet_id,
        tweet_data,
        created_at_str,
        saved_images,
        saved_videos,
        saved_previews,
    )

    save_metrics_snapshot(tweet_id, tweet_data)

    # ========= embed =========
    archive_links = []

    # ===== 画像リンク =====
    if len(saved_images) == 1:
        f = saved_images[0]
        archive_links.append(f"[画像]({BASE_URL}/images/{f})")
    elif len(saved_images) > 1:
        for i, f in enumerate(saved_images, start=1):
            archive_links.append(f"[{i}枚目]({BASE_URL}/images/{f})")

    # ===== 動画リンク =====
    if len(saved_videos) == 1:
        f = saved_videos[0]
        archive_links.append(f"[動画]({BASE_URL}/videos/{f})")
    elif len(saved_videos) > 1:
        for i, f in enumerate(saved_videos, start=1):
            archive_links.append(f"[{i}本目]({BASE_URL}/videos/{f})")

    archive_text = " ".join(archive_links)

    embed = discord.Embed(
        description=(
            f"{tweet_data.get('text','')[:3000]}"
            f"\n\n[元ツイート]({tweet_url})"
            + (f"\n{archive_text}" if archive_links else "")
        ),
        timestamp=created_at_dt,
        color=discord.Color(0x1DA1F2)
    )

    embed.set_author(
        name=f"{tweet_data['author']['name']} (@{tweet_data['author']['screen_name']})",
        icon_url=tweet_data["author"]["avatar_url"]
    )

    # 表示画像（preview 優先）
    if saved_previews:
        embed.set_image(url=f"{BASE_URL}/previews/{saved_previews[0]}")
    elif saved_images:
        embed.set_image(url=f"{BASE_URL}/images/{saved_images[0]}")

    # ========= 送信 =========
    if not silent:
        if is_interaction:
            await target.followup.send(embed=embed)
        else:
            await webhook.send(
                embed=embed,
                username=target.author.display_name,
                avatar_url=target.author.avatar.url if target.author.avatar else None
            )

# 手動コマンド
@tree.command(name="tw_archive", description="ツイートの画像を保存し、表示します")
@app_commands.describe(url="ツイートのURLを入力")
async def save_tweet_image(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    logging.info(f"コマンドが実行されました: tw_img_archive with URL: {url}")
    await process_tweet(interaction, url)

# 自動監視チャンネル設定コマンド
@tree.command(name="set_auto_tw_archive", description="Twitter(X)の画像自動保存の監視チャンネルを設定します")
@app_commands.describe(
    textchannel="監視するテキストチャンネル",
    action="監視リストに追加(add)するか削除(remove)するか選択"
)
async def set_auto_tw_archive(interaction: discord.Interaction, textchannel: discord.TextChannel, action: ActionChoice):
    config = load_config()
    
    guild_id = str(interaction.guild.id)
    if guild_id not in config:
        config[guild_id] = []

    monitored_channels = config[guild_id]

    # 管理者権限を持っているかチェック
    if interaction.user.guild_permissions.administrator:
        if action == ActionChoice.add:
            if textchannel.id in monitored_channels:
                await interaction.response.send_message(f"{textchannel.mention} はすでに監視リストに含まれています。", ephemeral=False)
                return
            monitored_channels.append(textchannel.id)
            config[guild_id] = monitored_channels
            save_config(config)
            await interaction.response.send_message(f"{textchannel.mention} を監視チャンネルに追加しました！", ephemeral=False)
            logging.info(f"Added channel {textchannel.id} to monitored channels for guild {guild_id}")

        elif action == ActionChoice.remove:
            if textchannel.id not in monitored_channels:
                await interaction.response.send_message(f"{textchannel.mention} は監視リストに含まれていません。", ephemeral=False)
                return
            monitored_channels.remove(textchannel.id)
            config[guild_id] = monitored_channels
            save_config(config)
            await interaction.response.send_message(f"{textchannel.mention} を監視チャンネルから削除しました。", ephemeral=False)
            logging.info(f"Removed channel {textchannel.id} from monitored channels for guild {guild_id}")
    else:
        await interaction.response.send_message("このコマンドを実行するには管理者権限が必要です。", ephemeral=False)

# メッセージ監視
@client.event
async def on_message(message):
    # Bot自身のメッセージは無視
    if message.author.bot or message.webhook_id is not None:
        return
    
    # DM（ダイレクトメッセージ）の場合は処理をスキップ
    if message.guild is None:
        return

    config = load_config()
    guild_id = str(message.guild.id)
    monitored_channels = config.get(guild_id, [])
    
    if message.channel.id in monitored_channels:
        urls = [u for u in message.content.split() if re.search(r'(https?://)?(x|twitter)\.com', u)]
        if not urls:
            return

        logging.info(f"Tweet Archiver invoked in channel {message.channel.id} by {message.author.id}")
        
        # 計測開始
        start = time.perf_counter()

        # メッセージ削除
        try:
            await message.delete()
            logging.info(f"Message deleted: {message.content}")
        except Exception as e:
            logging.error(f"メッセージの削除に失敗: {e}")

        # Webhookの取得または作成
        webhook = None
        try:
            # 権限チェック
            if not message.channel.permissions_for(message.guild.me).manage_webhooks:
                await message.channel.send("Webhookの作成に必要な権限がありません。")
                logging.error("ボットにWebhook管理権限がありません。")
                return

            # 既存のWebhookを検索
            webhooks = await message.channel.webhooks()
            webhook = next((w for w in webhooks if w.name == "TweetArchiver"), None)

            # Webhookが存在する場合、最新の状態を取得
            if webhook:
                try:
                    webhook = await webhook.fetch()  # 最新のWebhook情報を取得
                    if not webhook.token:
                        # トークンがない場合、既存のWebhookを削除して再作成
                        await webhook.delete()
                        logging.info("トークンのないWebhookを削除しました")
                        webhook = None
                except Exception as e:
                    logging.error(f"Webhookの取得に失敗、削除して再作成します: {e}")
                    await webhook.delete()
                    webhook = None

            # Webhookが存在しない、または削除された場合、新規作成
            if not webhook:
                webhook = await message.channel.create_webhook(name="TweetArchiver")
                logging.info("新しいWebhookを作成しました")

        except Exception as e:
            logging.error(f"Webhookの取得/作成に失敗: {e}")
            await message.channel.send("Webhookの設定に失敗しました。管理者に連絡してください。")
            return

        # アクセス時間計測開始
        ac_start = time.perf_counter()

        for url in urls:
            async with semaphore:
                await process_tweet(message, url, webhook)

        # 計測終了
        ac_end = time.perf_counter()
        end = time.perf_counter()
        elapsed = end - start
        elapsed_dl = ac_end - ac_start
        logging.info(f"processing time: {elapsed:.2f}sec, access time: {elapsed_dl:.2f}sec")

# トークン
client.run(os.getenv("TOKEN"))