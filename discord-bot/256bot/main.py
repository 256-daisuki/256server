import discord
import random
import requests
import subprocess
import re
import os
import math
import aiohttp
import asyncio
import aiofiles
from aiohttp import ClientSession, ClientResponseError
import uuid
import json
import time
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

    # ブラウザ周り
    global global_browser, global_context
    logging.info("Bot is ready. Launching browser with persistent context...")
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    # STATE_FILE からストレージ状態を読み込み
    state = None
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    global_context = await browser.new_context(storage_state=state)
    global_browser = playwright
    logging.info("Browser with persistent context launched.")

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
        allowed_users = [891521181990129675, 997588139235360958]  # 許可するユーザーのIDリスト
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
        ("/tw_img_archive", "Twitter(X)の画像を保存し、表示します サーバーに保存をするのでツイートが削除されても、凍結されても残ります。魚拓用にどうぞ"),
        ("/set_auto_tw_img_archive", "設定したテキストチャンネルに貼られたTwitter(X)の画像に対し自動的に/tw_img_archiveを実行します　イラスト共有チャンネルなどに如何でしょう？")
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

@tree.command(name="filecount",description="あ")
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
        '/var/www/html/combined': 'Twitterの画像（合成）'
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
            value=f"ファイル数: {file_count}\n合計サイズ: {size_str}",
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
        value=f"総ファイル数: {total_file_count}\n総サイズ: {total_size_str}",
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

SAVE_DIR = "/var/www/html/images"
COMBINED_DIR = "/var/www/html/combined"
BASE_URL = "https://discord.256server.com"
CONFIG_FILE = "config.json"
STATE_FILE = "twitter_state.json"
SENSITIVE_EYE_PATH = "M3.693 21.707l-1.414-1.414 2.429-2.429c-2.479-2.421-3.606-5.376-3.658-5.513l-.131-.352.131-.352c.133-.353 3.331-8.648 10.937-8.648 2.062 0 3.989.621 5.737 1.85l2.556-2.557 1.414 1.414L3.693 21.707zm-.622-9.706c.356.797 1.354 2.794 3.051 4.449l2.417-2.418c-.361-.609-.553-1.306-.553-2.032 0-2.206 1.794-4 4-4 .727 0 1.424.192 2.033.554l2.263-2.264C14.953 5.434 13.512 5 11.986 5c-5.416 0-8.258 5.535-8.915 7.001zM11.986 10c-1.103 0-2 .897-2 2 0 .178.023.352.067.519l2.451-2.451c-.167-.044-.341-.067-.519-.067zm10.951 1.647l.131.352-.131.352c-.133.353-3.331 8.648-10.937 8.648-.709 0-1.367-.092-2-.223v-2.047c.624.169 1.288.27 2 .27 5.415 0 8.257-5.533 8.915-7-.252-.562-.829-1.724-1.746-2.941l1.438-1.438c1.53 1.971 2.268 3.862 2.33 4.027z"
## 雑とか言わないで

# ログ(デバッグ用だったけどかっこいいから残す)
logging.basicConfig(level=logging.INFO)

###           Twitter画像保存関係           ###
# 設定の読み書き
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

# 画像URLのパラメータを修正する関数
def clean_image_url(url):
    if "pbs.twimg.com/media/" in url:
        base_url = url.split("?")[0]
        match = re.search(r"(\?format=[^&]+)", url)
        format_part = match.group(1) if match else "?format=jpg"
        return f"{base_url}{format_part}&name=orig"
    return url

async def download_image(session, image_url, save_path):
    async with session.get(image_url) as resp:
        if resp.status == 200:
            async with aiofiles.open(save_path, "wb") as f:
                await f.write(await resp.read())
            logging.info(f"Saved image: {save_path}")
            return save_path
        return None

async def download_image(session, image_url, save_path):
    async with session.get(image_url) as resp:
        if resp.status == 200:
            async with aiofiles.open(save_path, "wb") as f:
                await f.write(await resp.read())
            logging.info(f"Saved image: {save_path}")
            return save_path
        return None

# tw保存
@tree.command(name="tw_img_archive", description="ツイートの画像を保存し、表示します")
@app_commands.describe(url="ツイートのURLを入力")
async def save_tweet_image(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    logging.info(f"Command invoked: tw_img_archive with URL: {url}")

    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url

    if "x.com" not in url and "twitter.com" not in url:
        await interaction.followup.send("エラー: Twitter (X) のURLのみ対応しています。")
        logging.warning("Invalid URL: not a Twitter/X URL")
        return

    # ツイートIDの抽出
    tweet_id_match = re.search(r'status/(\d+)', url)
    if not tweet_id_match:
        await interaction.followup.send("エラー: ツイートIDが見つかりませんでした。")
        logging.warning("Tweet ID not found in URL")
        return
    tweet_id = tweet_id_match.group(1)
    base_url = f"https://x.com{url.split('x.com')[1].split('?')[0]}"

    # persistent な global_context を利用して新たなページを作成
    try:
        page = await global_context.new_page()
    except Exception as e:
        logging.error(f"Persistent browser context not available: {e}")
        await interaction.followup.send("内部エラーが発生しました。")
        return

    await page.goto(url)

    try:
        # 最初のarticle（対象ツイート）を待つ
        await page.wait_for_selector("article", timeout=10000)
        main_article = page.locator("article").first
        tweet_text_elem = main_article.locator('div[data-testid="tweetText"]').first
        tweet_text = await tweet_text_elem.text_content(timeout=10000) or ""
        
        sensitive_eye = await main_article.locator(f"svg path[d='{SENSITIVE_EYE_PATH}']").count()
        is_sensitive = sensitive_eye > 0
        # logging.info(f"Sensitive check: {is_sensitive}, Eye count: {sensitive_eye}")
    except Exception as e:
        logging.warning(f"ツイート本文の取得に失敗: {e}")
        tweet_text = ""
        is_sensitive = False

    try:
        author_name = await main_article.locator("a[role='link'] span").nth(0).text_content(timeout=10000)
        author_id = await main_article.locator("span").filter(has_text=re.compile(r"^@")).first.text_content(timeout=10000)
        author_icon = await main_article.locator("img").first.get_attribute("src", timeout=10000)
    except Exception as e:
        logging.error(f"ツイート情報の取得に失敗: {e}")
        await page.close()
        return

    # メイン画像の取得
    image_urls = []
    try:
        images = await main_article.locator('div[data-testid="tweetPhoto"] img[alt="Image"]').all()
        for img in images:
            src = await img.get_attribute("src")
            if src and "pbs.twimg.com/media/" in src:
                image_urls.append(src)
                logging.info(f"Found main image in tweet: {src}")
            else:
                logging.info(f"Ignored non-media image: {src}")
        if not image_urls:
            logging.warning("No media images found in main tweet")
    except Exception as e:
        logging.warning(f"画像の取得に失敗: {e}")

    await page.close()

    if not image_urls:
        await interaction.followup.send("画像が見つかりませんでした。")
        logging.warning("No image URLs found")
        return

    is_nsfw_channel = interaction.channel.is_nsfw()
    # logging.info(f"Channel NSFW status: {is_nsfw_channel}")
    if is_sensitive and not is_nsfw_channel:
        await interaction.followup.send(
            "このツイートにはセンシティブなコンテンツが含まれています。NSFWチャンネルで実行してください。"
        )
        logging.info("Blocked due to sensitive content in non-NSFW channel")
        return

    os.makedirs(SAVE_DIR, exist_ok=True)
    os.makedirs(COMBINED_DIR, exist_ok=True)
    saved_images = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        for image_url in image_urls:
            image_url = clean_image_url(image_url)
            match = re.search(r"format=(\w+)", image_url)
            ext = f".{match.group(1)}" if match else ".jpg"
            filename = image_url.split("/")[-1].split("?")[0] + ext
            save_path = os.path.join(SAVE_DIR, filename)
            tasks.append(download_image(session, image_url, save_path))
        saved_images = [result for result in await asyncio.gather(*tasks) if result is not None]
        logging.info(f"Saved {len(saved_images)} images")

    if not saved_images:
        await interaction.followup.send("画像の保存に失敗しました")
        logging.warning("No images saved")
        return

    original_image_urls = [BASE_URL + '/images/' + os.path.basename(img) for img in saved_images]

    combined_image_path = None
    if len(saved_images) > 1:
        images_to_merge = []
        for img_path in saved_images[:4]:
            try:
                img = Image.open(img_path)
                images_to_merge.append(img)
            except Exception as e:
                logging.warning(f"Failed to open image {img_path}: {e}")
                continue

        if not images_to_merge:
            await interaction.followup.send("合成する画像がありません")
            logging.warning("No valid images to merge")
            return

        try:
            if len(images_to_merge) == 2:
                img1, img2 = images_to_merge
                total_width = img1.width + img2.width
                total_height = max(img1.height, img2.height)
                new_image = Image.new('RGB', (total_width, total_height), color=(255, 255, 255))
                y1_offset = (total_height - img1.height) // 2
                y2_offset = (total_height - img2.height) // 2
                new_image.paste(img1, (0, y1_offset))
                new_image.paste(img2, (img1.width, y2_offset))
            else:
                max_width = max(img.width for img in images_to_merge)
                max_height = max(img.height for img in images_to_merge)
                total_width = max_width * 2
                total_height = max_height * 2 if len(images_to_merge) > 2 else max_height
                new_image = Image.new('RGB', (total_width, total_height), color=(255, 255, 255))

                if len(images_to_merge) == 3:
                    x1_offset = (max_width - images_to_merge[0].width) // 2
                    y1_offset = (max_height - images_to_merge[0].height) // 2
                    new_image.paste(images_to_merge[0], (x1_offset, y1_offset))
                    x2_offset = max_width + (max_width - images_to_merge[1].width) // 2
                    y2_offset = (max_height - images_to_merge[1].height) // 2
                    new_image.paste(images_to_merge[1], (x2_offset, y2_offset))
                    x3_offset = (total_width - images_to_merge[2].width) // 2
                    y3_offset = max_height + (max_height - images_to_merge[2].height) // 2
                    new_image.paste(images_to_merge[2], (x3_offset, y3_offset))
                else:
                    x1_offset = (max_width - images_to_merge[0].width) // 2
                    y1_offset = (max_height - images_to_merge[0].height) // 2
                    new_image.paste(images_to_merge[0], (x1_offset, y1_offset))
                    x2_offset = max_width + (max_width - images_to_merge[1].width) // 2
                    y2_offset = (max_height - images_to_merge[1].height) // 2
                    new_image.paste(images_to_merge[1], (x2_offset, y2_offset))
                    x3_offset = (max_width - images_to_merge[2].width) // 2
                    y3_offset = max_height + (max_height - images_to_merge[2].height) // 2
                    new_image.paste(images_to_merge[2], (x3_offset, y3_offset))
                    x4_offset = max_width + (max_width - images_to_merge[3].width) // 2
                    y4_offset = max_height + (max_height - images_to_merge[3].height) // 2
                    new_image.paste(images_to_merge[3], (x4_offset, y4_offset))

            combined_image_filename = f"{uuid.uuid4().hex}.jpg"
            combined_image_path = os.path.join(COMBINED_DIR, combined_image_filename)
            new_image.save(combined_image_path, quality=95)
            logging.info(f"Saved combined image: {combined_image_path}")
        except Exception as e:
            logging.error(f"Image merging failed: {e}")

    if len(original_image_urls) == 1:
        image_urls_text = f"[リンク]({original_image_urls[0]})"
    else:
        image_urls_text = "".join([f"[{i+1}枚目]({url}) " for i, url in enumerate(original_image_urls)])

    tweet_text_display = tweet_text if tweet_text is not None else ""
    embed = discord.Embed(
        description=f"{tweet_text_display[:4000]}\n\n[元ツイート]({url})\n{image_urls_text}",
        color=0x1DA1F2
    )
    embed.set_author(name=f"{author_name} ({author_id})", icon_url=author_icon)

    if combined_image_path:
        embed.set_image(url=BASE_URL + '/combined/' + os.path.basename(combined_image_path))
    else:
        embed.set_image(url=original_image_urls[0])

    await interaction.followup.send(embed=embed)
    logging.info("Embed sent successfully")

# 自動のチャンネル設定のソレ
# 選択肢用のEnum
class ActionChoice(Enum):
    add = "add"
    remove = "remove"

# 同時実行を制限するためのセマフォ
semaphore = asyncio.Semaphore(10)

@tree.command(name="set_auto_tw_img_archive", description="Twitter(X)の画像自動保存の監視チャンネルを設定します")
@app_commands.describe(
    textchannel="監視するテキストチャンネル",
    action="監視リストに追加(add)するか削除(remove)するか選択"
)
async def set_auto_tw_img_archive(interaction: discord.Interaction, textchannel: discord.TextChannel, action: ActionChoice):
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

@client.event
async def on_message(message):
    await handle_commands(message)

    # Bot自身のメッセージは無視
    if message.author == bot.user:
        return
    
    # DM（ダイレクトメッセージ）の場合は処理をスキップ
    if message.guild is None:
        return  # ダイレクトメッセージの場合は処理しない

    config = load_config()
    guild_id = str(message.guild.id)
    monitored_channels = config.get(guild_id, [])
    
    if message.channel.id in monitored_channels:
        urls = [u for u in message.content.split() if re.search(r'(https?://)?(x|twitter)\.com', u)]
        if not urls:
            return

        logging.info(f"Tweet Archiver invoked in channel {message.channel.id} by {message.author.id}")
        
        ######### 計測開始 #########
        start = 0
        end = 0
        ac_start = 0
        ac_end = 0

        start = time.perf_counter()
        ###########################

        await message.delete()
        logging.info(f"Message deleted: {message.content}")

        webhooks = await message.channel.webhooks()
        webhook = next((w for w in webhooks if w.name == "TweetArchiver"), None)
        if not webhook:
            webhook = await message.channel.create_webhook(name="TweetArchiver")

        ###########################    
        ac_start = time.perf_counter()
        ###########################        

        for url in urls:
            if not url.startswith("http"):
                url = "https://" + url

            async with semaphore:
                # persistentなブラウザから新しいページを作成する
                page = await global_context.new_page()
                try:
                    await page.goto(url, wait_until="domcontentloaded")
                    
                    # DOMが読み込まれるのを待つ
                    await page.wait_for_selector("article", timeout=10000)
                    main_article = page.locator("article").first
                    tweet_text_elem = main_article.locator('div[data-testid="tweetText"]').first
                    try:
                        tweet_text = await tweet_text_elem.text_content(timeout=5000) or ""
                    except Exception as e:
                        logging.debug(f"ツイート本文の取得に失敗: {e}")
                        tweet_text = ""
                    
                    sensitive_eye = await main_article.locator(f"svg path[d='{SENSITIVE_EYE_PATH}']").count()
                    is_sensitive = sensitive_eye > 0
                    # logging.info(f"Sensitive check: {is_sensitive}, Eye count: {sensitive_eye}")
   
                    ac_end = time.perf_counter()

                except Exception as e:
                    logging.warning(f"ツイート本文の取得に失敗: {e}")
                    tweet_text = ""
                    is_sensitive = False
                
                try:
                    author_name = await main_article.locator("a[role='link'] span").nth(0).text_content(timeout=5000)
                    author_id = await main_article.locator("span").filter(has_text=re.compile(r"^@")).first.text_content(timeout=5000)
                    author_icon = await main_article.locator("img").first.get_attribute("src", timeout=5000)
                    
                    image_urls = []
                    images = await main_article.locator('div[data-testid="tweetPhoto"] img[alt="Image"]').all()
                    for img in images:
                        src = await img.get_attribute("src")
                        if src and "pbs.twimg.com/media/" in src:
                            image_urls.append(src)
                            logging.info(f"Found main image in tweet: {src}")
                        else:
                            logging.info(f"Ignored non-media image: {src}")
                    if not image_urls:
                        logging.warning("No media images found in main tweet")
                except Exception as e:
                    logging.error(f"ツイート情報の取得に失敗: {e}")
                    await page.close()
                    continue

                # ページは使い終わったので閉じる
                await page.close()

                if not image_urls:
                    await webhook.send(
                        "画像が見つかりませんでした。",
                        username=message.author.display_name,
                        avatar_url=message.author.avatar.url if message.author.avatar else None
                    )
                    logging.warning("No image URLs found")
                    continue

                is_nsfw_channel = message.channel.is_nsfw()
                # logging.info(f"Channel NSFW status: {is_nsfw_channel}")
                if is_sensitive and not is_nsfw_channel:
                    await webhook.send(
                        "このツイートにはセンシティブなコンテンツが含まれています。NSFWチャンネルで実行してください。",
                        username=message.author.display_name,
                        avatar_url=message.author.avatar.url if message.author.avatar else None
                    )
                    continue

                os.makedirs(SAVE_DIR, exist_ok=True)
                os.makedirs(COMBINED_DIR, exist_ok=True)
                saved_images = []

                async with aiohttp.ClientSession() as session:
                    tasks = []
                    for image_url in image_urls:
                        image_url = clean_image_url(image_url)
                        match = re.search(r"format=(\w+)", image_url)
                        ext = f".{match.group(1)}" if match else ".jpg"
                        filename = image_url.split("/")[-1].split("?")[0] + ext
                        save_path = os.path.join(SAVE_DIR, filename)
                        tasks.append(download_image(session, image_url, save_path))
                    saved_images = [result for result in await asyncio.gather(*tasks) if result]
                    logging.info(f"Saved {len(saved_images)} images")
    
                if not saved_images:
                    await webhook.send(
                        "画像の保存に失敗しました。",
                        username=message.author.display_name,
                        avatar_url=message.author.avatar.url if message.author.avatar else None
                    )
                    logging.warning("No images saved")
                    continue

                original_image_urls = [BASE_URL + '/images/' + os.path.basename(img) for img in saved_images]

                combined_image_path = None
                if len(saved_images) > 1:
                    images_to_merge = []
                    for img_path in saved_images[:4]:
                        try:
                            img = Image.open(img_path)
                            images_to_merge.append(img)
                        except Exception as e:
                            logging.warning(f"Failed to open image {img_path}: {e}")
                            continue

                    if images_to_merge:
                                try:
                                    if len(images_to_merge) == 2:
                                        img1, img2 = images_to_merge
                                        total_width = img1.width + img2.width
                                        total_height = max(img1.height, img2.height)
                                        new_image = Image.new('RGB', (total_width, total_height), color=(255, 255, 255))
                                        y1_offset = (total_height - img1.height) // 2
                                        y2_offset = (total_height - img2.height) // 2
                                        new_image.paste(img1, (0, y1_offset))
                                        new_image.paste(img2, (img1.width, y2_offset))
                                    else:
                                        max_width = max(img.width for img in images_to_merge)
                                        max_height = max(img.height for img in images_to_merge)
                                        total_width = max_width * 2
                                        total_height = max_height * 2 if len(images_to_merge) > 2 else max_height
                                        new_image = Image.new('RGB', (total_width, total_height), color=(255, 255, 255))

                                        if len(images_to_merge) == 3:
                                            x1_offset = (max_width - images_to_merge[0].width) // 2
                                            y1_offset = (max_height - images_to_merge[0].height) // 2
                                            new_image.paste(images_to_merge[0], (x1_offset, y1_offset))
                                            x2_offset = max_width + (max_width - images_to_merge[1].width) // 2
                                            y2_offset = (max_height - images_to_merge[1].height) // 2
                                            new_image.paste(images_to_merge[1], (x2_offset, y2_offset))
                                            x3_offset = (total_width - images_to_merge[2].width) // 2
                                            y3_offset = max_height + (max_height - images_to_merge[2].height) // 2
                                            new_image.paste(images_to_merge[2], (x3_offset, y3_offset))
                                        else:
                                            x1_offset = (max_width - images_to_merge[0].width) // 2
                                            y1_offset = (max_height - images_to_merge[0].height) // 2
                                            new_image.paste(images_to_merge[0], (x1_offset, y1_offset))
                                            x2_offset = max_width + (max_width - images_to_merge[1].width) // 2
                                            y2_offset = (max_height - images_to_merge[1].height) // 2
                                            new_image.paste(images_to_merge[1], (x2_offset, y2_offset))
                                            x3_offset = (max_width - images_to_merge[2].width) // 2
                                            y3_offset = max_height + (max_height - images_to_merge[2].height) // 2
                                            new_image.paste(images_to_merge[2], (x3_offset, y3_offset))
                                            x4_offset = max_width + (max_width - images_to_merge[3].width) // 2
                                            y4_offset = max_height + (max_height - images_to_merge[3].height) // 2
                                            new_image.paste(images_to_merge[3], (x4_offset, y4_offset))

                                    combined_image_filename = f"{uuid.uuid4().hex}.jpg"
                                    combined_image_path = os.path.join(COMBINED_DIR, combined_image_filename)
                                    new_image.save(combined_image_path, quality=95)
                                    logging.info(f"Saved combined image: {combined_image_path}")
                                except Exception as e:
                                    logging.error(f"Image merging failed: {e}")

                image_urls_text = "".join([f"[{i+1}枚目]({url}) " for i, url in enumerate(original_image_urls)]) if len(original_image_urls) > 1 else f"[リンク]({original_image_urls[0]})"
                
                embed = discord.Embed(
                    description=f"{tweet_text[:4000]}\n\n[元ツイート]({url})\n{image_urls_text}",
                    color=0x1DA1F2
                )
                embed.set_author(name=f"{author_name} ({author_id})", icon_url=author_icon)
                embed.set_image(url=BASE_URL + '/combined/' + os.path.basename(combined_image_path) if combined_image_path else original_image_urls[0])

                await webhook.send(
                    embed=embed,
                    username=message.author.display_name,
                    avatar_url=message.author.avatar.url if message.author.avatar else None
                )
                logging.info("Embed sent successfully")

        ######### 計測終了 #########
        end = time.perf_counter()
        elapsed = end - start
        elapsed_dl = ac_end - ac_start
        
        logging.info(f"processing time: {elapsed:.2f}sec, access time: {elapsed_dl:.2f}sec")
        ###########################

# トークン
client.run(os.getenv("TOKEN"))