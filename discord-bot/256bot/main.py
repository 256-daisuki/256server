import discord
import random
import requests
import subprocess
import re
import os
import aiohttp
import asyncio
import aiofiles
from aiohttp import ClientSession, ClientResponseError
import uuid
import json
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

@client.event
async def on_ready():

    # 認識しているサーバーをlist型で取得し、その要素の数を 変数:guild_count に格納しています。
    guild_count = len(client.guilds)
    # 関数:lenは、引数に指定したオブジェクトの長さや要素の数を取得します。
    
    game = discord.Game(f'{guild_count} サーバー数の人たちを監視中')
    # game = discord.Game(f'お前らを監視中')
    # f文字列(フォーマット済み文字列リテラル)は、Python3.6からの機能です。
    
    # BOTのステータスを変更する
    await client.change_presence(status=discord.Status.online, activity=game)
    # パラメーターの status でステータス状況(オンライン, 退席中など)を変更できます。

    print("起動完了")
    await tree.sync()#スラッシュコマンドを同期

# メッセージを受信した時に呼ばれる
@client.event
async def on_message(message):
    # 自分のメッセージを無効
    if message.author == client.user:
        return

    # shellコマンド
    if message.content.startswith('$'):
        allowed_users = [891521181990129675, 997588139235360958]  # 許可するユーザーのIDリスト
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
            pass

@tree.command(name="test",description="テストコマンドです。")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("しらすじゅーす！",ephemeral=False)

@tree.command(name="help", description="コマンドのヘルプを表示します")
async def help_command(interaction: discord.Interaction):
    # コマンド一覧を作成
    command_list = [
        ("/test", "Botの動作が怪しいときに使ってください　適当に返答します"),
        ("/ping", "Botにpingを打ちます。応答するかどうか　testとほぼ一緒です"),
        # ("/echo", "好きなことを言わすことができます"),
        ("/omikuji", "凶しか入ってないおみくじです"),
        ("/google", "google検索します　そのまま"),
        ("/yahoo", "yahooニュースを表示します"),
        ("/embed", "Botがユーザーの代わりにembedを送信します"),
        # ("/screenshot", "Webサイトのスクリーンショットを送信します(httpsをちゃんとつけてください)")
        ("/tw_img_archive", "Twitter(X)の画像を保存し、表示します 保存をするのでツイートが削除されても、凍結されても残ります"),
        ("/set_auto_tw_img_archive", "設定したテキストチャンネルに貼られたTwitter(X)の画像に対し自動的に/tw_img_archiveを実行します　イラスト共有チャンネルなどに")
    ]

    # Embedを作成
    embed = discord.Embed(title="Help! 📕", description="利用可能なコマンドの一覧です", color=0x00ff00)

    # コマンド一覧をEmbedに追加
    for name, description in command_list:
        embed.add_field(name=name, value=description, inline=False)

    # メッセージを送信
    await interaction.response.send_message(embed=embed, ephemeral=True)

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

#@tree.command(name="echo", description="あんなことやそんなことまで言います")
#async def echo_command(interaction: discord.Interaction, *, text: str):
#    await interaction.response.send_message(text, ephemeral=False)

@tree.command(name="google", description="Googleで検索結果を表示します")
async def google_command(interaction: discord.Interaction, *, search_word: str):
    pages_num = 10 + 1  # 上位から何件までのサイトを抽出するか指定
    result_embed = discord.Embed(title=f"Google検索結果: {search_word}", color=0xfabb05)

    url = f'https://www.google.co.jp/search?hl=ja&num={pages_num}&q={search_word}'
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    search_site_list = soup.select('div.tF2Cxc > a')

    for site in search_site_list:
        try:
            site_title = site.select('h3')[0].text
        except IndexError:
            try:
                site_title = site.select('img')[0]['alt']
            except IndexError:
                site_title = "No title available"

        site_url = site['href'].replace('/url?q=', '').split('&')[0]

        link_text = f"[{site_title}]({site_url})"
        result_embed.add_field(name='\u200b', value=link_text, inline=False)

    await interaction.response.send_message(embed=result_embed, ephemeral=False)

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

# tw保存
@tree.command(name="tw_img_archive", description="ツイートの画像を保存し、表示します")
@app_commands.describe(url="ツイートのURLを入力")
async def save_tweet_image(interaction: discord.Interaction, url: str):
    await interaction.response.defer()

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    if "x.com" not in url and "twitter.com" not in url:
        await interaction.followup.send("エラー: Twitter (X) のURLのみ対応しています。")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(url)
        await page.wait_for_selector("article", timeout=10000) 

        try:
            tweet_text = await page.locator("article div[lang]").text_content()
        except:
            tweet_text = None

        author_name = await page.locator("article a[role='link'] span").nth(0).text_content()
        author_id = await page.locator("article span").filter(has_text=re.compile(r"^@")).first.text_content()
        author_icon = await page.locator("article img").first.get_attribute("src")

        images = await page.locator("article img").all()
        image_urls = [await img.get_attribute("src") for img in images]

        await browser.close()

    if not image_urls:
        await interaction.followup.send("画像が見つかりませんでした。")
        return

    os.makedirs(SAVE_DIR, exist_ok=True)
    os.makedirs(COMBINED_DIR, exist_ok=True)
    saved_images = []

    # 画像を並列ダウンロード　これはgrokがつけてきたやつ　私知りません　勝手に並列にして来やがりました
    async with aiohttp.ClientSession() as session:
        tasks = []
        for image_url in image_urls:
            if "profile_images" in image_url or "twemoji" in image_url or ".svg" in image_url:
                continue

            image_url = clean_image_url(image_url)
            match = re.search(r"format=(\w+)", image_url)
            ext = f".{match.group(1)}" if match else ".jpg"
            filename = image_url.split("/")[-1].split("?")[0] + ext
            save_path = os.path.join(SAVE_DIR, filename)
            tasks.append(download_image(session, image_url, save_path))

        saved_images = [result for result in await asyncio.gather(*tasks) if result is not None]

    if not saved_images:
        await interaction.followup.send("画像の保存に失敗しました")
        return

    original_image_urls = [BASE_URL + '/images/' + os.path.basename(img) for img in saved_images]

    combined_image_path = None
    if len(saved_images) > 1:
        images_to_merge = []
        for img_path in saved_images[:4]:
            try:
                img = Image.open(img_path)
                images_to_merge.append(img)
            except IOError:
                print(f"Skipping non-image file: {img_path}")
                continue

        if not images_to_merge:
            await interaction.followup.send("合成する画像がありません")
            return

        # ここ全部grokが書いてきたやつ　私知りません2
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

# 自動のチャンネル設定のソレ
@tree.command(name="set_auto_tw_img_archive", description="設定したテキストチャンネルに貼られたTwitter(X)の画像に対し自動的に/tw_img_archiveを実行します")
@app_commands.describe(textchannel="監視するテキストチャンネル")
async def hekta_command(interaction: discord.Interaction, textchannel: discord.TextChannel):
    config = load_config()
    config[str(interaction.guild.id)] = textchannel.id
    save_config(config)
    await interaction.response.send_message(f"{textchannel.mention} に貼られたツイートの画像をアーカイブ化します", ephemeral=False)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    config = load_config()
    monitored_channel = config.get(str(message.guild.id))
    
    if monitored_channel and message.channel.id == monitored_channel:
        if re.search(r'(https?://)?(x|twitter)\.com', message.content):
            await message.delete()
            
            webhooks = await message.channel.webhooks()
            webhook = next((w for w in webhooks if w.name == "TweetArchiver"), None)
            if not webhook:
                webhook = await message.channel.create_webhook(name="TweetArchiver")
            
            url = next((u for u in message.content.split() if re.search(r'(https?://)?(x|twitter)\.com', u)), None)
            if not url:
                return
            if not url.startswith("http"):
                url = "https://" + url

            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url)
                
                # タイムアウトを60秒に延長し、例外処理を追加 by grok
                try:
                    await page.wait_for_selector("article", timeout=5000)
                    tweet_text_elem = page.locator("article div[lang]").first
                    tweet_text = await tweet_text_elem.text_content(timeout=5000) or ""
                except Exception as e:
                    # logging.warning(f"ツイート本文の取得に失敗: {e}")
                    tweet_text = ""
                
                try:
                    author_name = await page.locator("article a[role='link'] span").nth(0).text_content(timeout=5000)
                    author_id = await page.locator("article span").filter(has_text=re.compile(r"^@")).first.text_content(timeout=5000)
                    author_icon = await page.locator("article img").first.get_attribute("src", timeout=5000)
                    images = await page.locator("article img").all()
                    image_urls = [await img.get_attribute("src", timeout=5000) for img in images if await img.get_attribute("src", timeout=5000)]
                except Exception as e:
                    logging.error(f"ツイート情報の取得に失敗: {e}")
                    await browser.close()
                    return

                await browser.close()

            if not image_urls:
                return

            os.makedirs(SAVE_DIR, exist_ok=True)
            os.makedirs(COMBINED_DIR, exist_ok=True)
            saved_images = []

            async with aiohttp.ClientSession() as session:
                tasks = []
                for image_url in image_urls:
                    if "profile_images" in image_url or "twemoji" in image_url or ".svg" in image_url:
                        continue
                    image_url = clean_image_url(image_url)
                    match = re.search(r"format=(\w+)", image_url)
                    ext = f".{match.group(1)}" if match else ".jpg"
                    filename = image_url.split("/")[-1].split("?")[0] + ext
                    save_path = os.path.join(SAVE_DIR, filename)
                    tasks.append(download_image(session, image_url, save_path))
                saved_images = [result for result in await asyncio.gather(*tasks) if result]

            if not saved_images:
                return

            original_image_urls = [BASE_URL + '/images/' + os.path.basename(img) for img in saved_images]

            combined_image_path = None
            if len(saved_images) > 1:
                images_to_merge = []
                for img_path in saved_images[:4]:
                    try:
                        img = Image.open(img_path)
                        images_to_merge.append(img)
                    except:
                        continue

                if images_to_merge:
                    if len(images_to_merge) == 2:
                        img1, img2 = images_to_merge
                        total_width = img1.width + img2.width
                        total_height = max(img1.height, img2.height)
                        new_image = Image.new('RGB', (total_width, total_height), (255, 255, 255))
                        y1_offset = (total_height - img1.height) // 2
                        y2_offset = (total_height - img2.height) // 2
                        new_image.paste(img1, (0, y1_offset))
                        new_image.paste(img2, (img1.width, y2_offset))
                    else:
                        max_width = max(img.width for img in images_to_merge)
                        max_height = max(img.height for img in images_to_merge)
                        cols = 2
                        rows = (len(images_to_merge) + 1) // 2
                        total_width = max_width * cols
                        total_height = max_height * rows
                        new_image = Image.new('RGB', (total_width, total_height), (255, 255, 255))
                        for i, img in enumerate(images_to_merge):
                            x_offset = (i % 2) * max_width + (max_width - img.width) // 2
                            y_offset = (i // 2) * max_height + (max_height - img.height) // 2
                            new_image.paste(img, (x_offset, y_offset))

                    combined_image_filename = f"{uuid.uuid4().hex}.jpg"
                    combined_image_path = os.path.join(COMBINED_DIR, combined_image_filename)
                    new_image.save(combined_image_path, quality=95)
                    logging.info(f"Saved combined image: {combined_image_path}")

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

# トークン
client.run(os.getenv("TOKEN"))