import discord
from discord import app_commands
import aiohttp
import re
import os
import logging
import asyncio
from PIL import Image
import aiofiles
from dotenv import load_dotenv
from datetime import datetime
import pytz
import json
from enum import Enum
import time
from collections import defaultdict
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# 環境変数の読み込み
load_dotenv()

# ログ設定（必要最低限に抑える）
logging.basicConfig(level=logging.WARNING)

# Discordクライアントとコマンドツリーの初期化
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容の読み取りを有効化
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# 保存先ディレクトリとベースURLの設定
TW_SAVE_DIR = "/var/www/html/test/images"  # Twitter画像保存用ディレクトリ
TW_COMBINED_DIR = "/var/www/html/test/combined"  # Twitter合成画像用ディレクトリ
OGP_SAVE_DIR = "/var/www/html/test/ogp/images"  # OGP画像保存用ディレクトリ
OGP_COMBINED_DIR = "/var/www/html/test/ogp/combined"  # OGP合成画像用ディレクトリ
BASE_URL = "https://discord.256server.com/test"  # 公開URLのベース
TW_CONFIG_FILE = "tw_config.json"  # Twitter設定ファイル
OGP_CONFIG_FILE = "ogp_config.json"  # OGP設定ファイル
MAX_IMAGE_SIZE = 1024  # 画像の最大サイズ（ピクセル）
CACHE_TTL = 3600  # キャッシュの有効期限（秒）

# 選択肢用のEnum
class ActionChoice(Enum):
    add = "add"
    remove = "remove"

# グローバルなセッションとキャッシュ
session = None  # aiohttp.ClientSession（ネットワークリクエスト用）
tweet_cache = {}  # ツイートキャッシュ {tweet_id: (data, timestamp)}
webhook_cache = {}  # Webhookキャッシュ {channel_id: webhook}
tw_config_cache = None  # Twitter設定キャッシュ
ogp_config_cache = None  # OGP設定キャッシュ
semaphore = asyncio.Semaphore(20)  # 同時実行を制限

# 設定ファイルの読み書き（キャッシュ付き）
def load_tw_config():
    global tw_config_cache
    if tw_config_cache is None:
        try:
            with open(TW_CONFIG_FILE, 'r') as f:
                tw_config_cache = json.load(f)
        except FileNotFoundError:
            tw_config_cache = {}
        except Exception as e:
            logging.error(f"Twitter設定ファイルの読み込みに失敗: {e}")
            tw_config_cache = {}
    return tw_config_cache

async def save_tw_config(config):
    global tw_config_cache
    tw_config_cache = config
    try:
        async with aiofiles.open(TW_CONFIG_FILE, 'w') as f:
            await f.write(json.dumps(config, indent=4))
    except Exception as e:
        logging.error(f"Twitter設定ファイルの保存に失敗: {e}")

def load_ogp_config():
    global ogp_config_cache
    if ogp_config_cache is None:
        try:
            with open(OGP_CONFIG_FILE, 'r') as f:
                ogp_config_cache = json.load(f)
        except FileNotFoundError:
            ogp_config_cache = {}
        except Exception as e:
            logging.error(f"OGP設定ファイルの読み込みに失敗: {e}")
            ogp_config_cache = {}
    return ogp_config_cache

async def save_ogp_config(config):
    global ogp_config_cache
    ogp_config_cache = config
    try:
        async with aiofiles.open(OGP_CONFIG_FILE, 'w') as f:
            await f.write(json.dumps(config, indent=4))
    except Exception as e:
        logging.error(f"OGP設定ファイルの保存に失敗: {e}")

# 画像をダウンロードする関数（非同期I/O）
async def download_image(url, save_path):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(save_path, 'wb') as f:
                    await f.write(await response.read())
                return save_path
    except Exception as e:
        logging.error(f"画像ダウンロードに失敗しました {url}: {e}")
    return None

# 画像を合成する関数（リサイズ対応）
async def combine_images(image_paths):
    images = []
    for path in image_paths:
        img = Image.open(path)
        if img.width > MAX_IMAGE_SIZE or img.height > MAX_IMAGE_SIZE:
            img.thumbnail((MAX_IMAGE_SIZE, MAX_IMAGE_SIZE), Image.Resampling.LANCZOS)
        images.append(img)

    if len(images) == 1:
        return image_paths[0]

    max_width = max(img.width for img in images)
    max_height = max(img.height for img in images)
    grid_size = 2 if len(images) > 2 else 1
    total_width = max_width * grid_size
    total_height = max_height * grid_size if len(images) > 2 else max_height

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

    combined_filename = os.path.basename(image_paths[0])
    combined_path = os.path.join(OGP_COMBINED_DIR if "ogp" in image_paths[0] else TW_COMBINED_DIR, combined_filename)
    async with aiofiles.open(combined_path, 'wb') as f:
        await f.write(new_image.tobytes())
    return combined_path

# fxtwitter APIからツイートデータを取得（キャッシュ付き）
async def get_tweet_data(tweet_id):
    current_time = time.time()
    if tweet_id in tweet_cache:
        data, timestamp = tweet_cache[tweet_id]
        if current_time - timestamp < CACHE_TTL:
            return data
        else:
            del tweet_cache[tweet_id]

    api_url = f"https://api.fxtwitter.com/twitter/status/{tweet_id}"
    async with session.get(api_url) as response:
        if response.status != 200:
            return None
        data = await response.json()
        if data.get("code") != 200:
            return None
        tweet_data = data["tweet"]
        tweet_cache[tweet_id] = (tweet_data, current_time)
        return tweet_data

# Twitter画像処理
async def process_tweet(interaction_or_message, url, webhook=None):
    is_interaction = isinstance(interaction_or_message, discord.Interaction)
    target = interaction_or_message

    if not url.startswith("http"):
        url = "https://" + url
    if "x.com" not in url and "twitter.com" not in url:
        if is_interaction:
            await target.followup.send("エラー: Twitter (X) のURLのみ対応しています。")
        else:
            await webhook.send(
                "エラー: Twitter (X) のURLのみ対応しています。",
                username=target.author.display_name,
                avatar_url=target.author.avatar.url if target.author.avatar else None
            )
        return None

    tweet_id_match = re.search(r'status/(\d+)', url)
    if not tweet_id_match:
        if is_interaction:
            await target.followup.send("エラー: ツイートIDが見つかりませんでした。")
        else:
            await webhook.send(
                "エラー: ツイートIDが見つかりませんでした。",
                username=target.author.display_name,
                avatar_url=target.author.avatar.url if target.author.avatar else None
            )
        return None
    tweet_id = tweet_id_match.group(1)

    tweet_data = await get_tweet_data(tweet_id)
    if not tweet_data:
        if is_interaction:
            await target.followup.send("ツイートデータの取得に失敗しました。")
        else:
            await webhook.send(
                "ツイートデータの取得に失敗しました。",
                username=target.author.display_name,
                avatar_url=target.author.avatar.url if target.author.avatar else None
            )
        return None

    is_sensitive = tweet_data.get("possibly_sensitive", False)
    channel = target.channel
    if is_sensitive and not channel.is_nsfw():
        if is_interaction:
            await target.followup.send("このツイートはセンシティブな内容を含みます。NSFWチャンネルで実行してください。")
        else:
            await webhook.send(
                "このツイートはセンシティブな内容を含みます。NSFWチャンネルで実行してください。",
                username=target.author.display_name,
                avatar_url=target.author.avatar.url if target.author.avatar else None
            )
        return None

    tweet_text = tweet_data.get("text", "")
    author_name = tweet_data["author"]["name"]
    author_id = tweet_data["author"]["screen_name"]
    author_icon = tweet_data["author"]["avatar_url"]
    media = tweet_data.get("media", {})
    photos = media.get("photos", [])
    image_urls = [photo["url"] for photo in photos if photo["type"] == "photo"]

    tweet_time_raw = tweet_data.get("created_at", None)
    if tweet_time_raw:
        try:
            tweet_time_dt = datetime.strptime(tweet_time_raw, "%a %b %d %H:%M:%S %z %Y")
            jst_tz = pytz.timezone("Asia/Tokyo")
            tweet_time_dt = tweet_time_dt.astimezone(jst_tz)
            tweet_time = tweet_time_dt.strftime("%Y/%m/%d %H:%M")
        except ValueError as e:
            logging.error(f"ツイート時間のパースに失敗しました: {e}")
            tweet_time = "不明"
    else:
        tweet_time = "不明"

    if not image_urls:
        if is_interaction:
            await target.followup.send("画像が見つかりませんでした。")
        else:
            await webhook.send(
                "画像が見つかりませんでした。",
                username=target.author.display_name,
                avatar_url=target.author.avatar.url if target.author.avatar else None
            )
        return None

    os.makedirs(TW_SAVE_DIR, exist_ok=True)
    os.makedirs(TW_COMBINED_DIR, exist_ok=True)
    saved_images = []

    async with semaphore:
        tasks = []
        for image_url in image_urls:
            filename = image_url.split("/")[-1].split("?")[0]
            save_path = os.path.join(TW_SAVE_DIR, filename)
            tasks.append(download_image(image_url, save_path))
        saved_images = [result for result in await asyncio.gather(*tasks) if result is not None]

    if not saved_images:
        if is_interaction:
            await target.followup.send("画像の保存に失敗しました")
        else:
            await webhook.send(
                "画像の保存に失敗しました。",
                username=target.author.display_name,
                avatar_url=target.author.avatar.url if target.author.avatar else None
            )
        return None

    if len(saved_images) > 1:
        combined_image_path = await combine_images(saved_images[:4])
        image_url = f"{BASE_URL}/combined/{os.path.basename(combined_image_path)}"
        archive_urls = [f"{BASE_URL}/images/{os.path.basename(path)}" for path in saved_images]
        archive_links = ' '.join([f'[{i+1}枚目]({url})' for i, url in enumerate(archive_urls)])
    else:
        image_url = f"{BASE_URL}/images/{os.path.basename(saved_images[0])}"
        archive_urls = [image_url]
        archive_links = f'[リンク]({image_url})'

    embed = discord.Embed(
        description=f"{tweet_text[:4000]}\n\n[元ツイート]({url})\nアーカイブ画像: {archive_links}",
        color=0x1DA1F2
    )
    embed.set_author(name=f"{author_name} ({author_id})", icon_url=author_icon)
    embed.set_image(url=image_url)
    embed.set_footer(text=f"ツイート時間: {tweet_time}")
    return embed

# OGPメタデータ処理
async def process_ogp(interaction, link):
    await interaction.response.defer()

    try:
        async with session.get(link, headers={'User-Agent': 'Mozilla/5.0'}) as response:
            if response.status != 200:
                await interaction.followup.send(f"URLの取得に失敗しました: ステータスコード {response.status}", ephemeral=True)
                return
            html = await response.text()

        soup = BeautifulSoup(html, 'html.parser')
        og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
        theme_color_orig = soup.find('meta', attrs={'name': 'theme-color-orig'})
        theme_color = soup.find('meta', attrs={'name': 'theme-color'})
        icon = soup.find('link', rel=lambda x: x in ['icon', 'shortcut icon'])

        color = 0x00ff00
        if theme_color_orig and theme_color_orig.get('content'):
            try:
                color = int(theme_color_orig['content'].lstrip('#'), 16)
            except ValueError:
                pass
        elif theme_color and theme_color.get('content'):
            try:
                color = int(theme_color['content'].lstrip('#'), 16)
            except ValueError:
                pass

        embed = discord.Embed(title="OGPメタデータ", color=color)
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            embed.title = og_title['content'][:256]

        og_description = soup.find('meta', property='og:description')
        if og_description and og_description.get('content'):
            embed.description = og_description['content'][:2048]
        else:
            embed.description = ""

        og_url = soup.find('meta', property='og:url')
        url_to_display = og_url['content'] if og_url and og_url.get('content') else link
        embed.description += f"\n[リンク]({url_to_display})"

        exclude_tags = ['og:title', 'og:description', 'og:url', 'og:site_name', 'og:type', 'og:image']
        for tag in og_tags:
            property_name = tag.get('property', '不明')
            content = tag.get('content', '見つかりませんでした')
            if property_name not in exclude_tags:
                embed.add_field(name=property_name, value=content[:1024], inline=True)

        og_site_name = soup.find('meta', property='og:site_name')
        footer_text = og_site_name['content'] if og_site_name and og_site_name.get('content') else "サイト名不明"
        embed.set_footer(text=footer_text)
        
        if icon and icon.get('href'):
            icon_url = urljoin(link, icon['href'])
            embed.set_footer(text=footer_text, icon_url=icon_url)

        # og:imageの処理（最初の1枚のみ）
        og_image = soup.find('meta', property='og:image')
        image_url = None
        if og_image and og_image.get('content'):
            image_url = urljoin(link, og_image['content'])
            filename = image_url.split("/")[-1].split("?")[0]
            save_path = os.path.join(OGP_SAVE_DIR, filename)
            os.makedirs(OGP_SAVE_DIR, exist_ok=True)
            async with semaphore:
                saved_path = await download_image(image_url, save_path)
            if saved_path:
                image_url = f"{BASE_URL}/ogp/images/{os.path.basename(saved_path)}"
                embed.set_image(url=image_url)

        await interaction.followup.send(embed=embed, ephemeral=False)
        logging.info(f"AAA command executed for URL: {link}")

    except Exception as e:
        await interaction.followup.send(f"エラーが発生しました: {str(e)}", ephemeral=True)
        logging.error(f"Error in aaa_command: {str(e)}")

# コマンド
@tree.command(name="tw_img_archive", description="ツイートの画像を保存し、表示します")
@app_commands.describe(url="ツイートのURLを入力")
async def save_tweet_image(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    logging.info(f"コマンドが実行されました: tw_img_archive with URL: {url}")
    embed = await process_tweet(interaction, url)
    if embed:
        await interaction.followup.send(embed=embed)

@tree.command(name="set_auto_tw_img_archive", description="Twitter(X)の画像自動保存の監視チャンネルを設定します")
@app_commands.describe(
    textchannel="監視するテキストチャンネル",
    action="監視リストに追加(add)するか削除(remove)するか選択"
)
async def set_auto_tw_img_archive(interaction: discord.Interaction, textchannel: discord.TextChannel, action: ActionChoice):
    config = load_tw_config()
    
    guild_id = str(interaction.guild.id)
    if guild_id not in config:
        config[guild_id] = []

    monitored_channels = config[guild_id]

    if interaction.user.guild_permissions.administrator:
        if action == ActionChoice.add:
            if textchannel.id in monitored_channels:
                await interaction.response.send_message(f"{textchannel.mention} はすでに監視リストに含まれています。", ephemeral=False)
                return
            monitored_channels.append(textchannel.id)
            config[guild_id] = monitored_channels
            await save_tw_config(config)
            await interaction.response.send_message(f"{textchannel.mention} を監視チャンネルに追加しました！", ephemeral=False)
            logging.info(f"Added channel {textchannel.id} to monitored channels for guild {guild_id}")

        elif action == ActionChoice.remove:
            if textchannel.id not in monitored_channels:
                await interaction.response.send_message(f"{textchannel.mention} は監視リストに含まれていません。", ephemeral=False)
                return
            monitored_channels.remove(textchannel.id)
            config[guild_id] = monitored_channels
            await save_tw_config(config)
            await interaction.response.send_message(f"{textchannel.mention} を監視チャンネルから削除しました。", ephemeral=False)
            logging.info(f"Removed channel {textchannel.id} from monitored channels for guild {guild_id}")
    else:
        await interaction.response.send_message("このコマンドを実行するには管理者権限が必要です。", ephemeral=False)

@tree.command(name="aaa", description="指定したURLのOGPメタデータを取得して表示します。")
@app_commands.describe(link="OGPメタデータを取得するURL")
async def aaa_command(interaction: discord.Interaction, link: str):
    await process_ogp(interaction, link)

# メッセージ監視
@client.event
async def on_message(message):
    if message.author == client.user or message.guild is None:
        return

    config = load_tw_config()
    guild_id = str(message.guild.id)
    monitored_channels = config.get(guild_id, [])
    
    if message.channel.id in monitored_channels:
        urls = [u for u in message.content.split() if re.search(r'(https?://)?(x|twitter)\.com', u)]
        if not urls:
            return

        logging.info(f"Tweet Archiver invoked in channel {message.channel.id} by {message.author.id}")
        
        start = time.perf_counter()

        try:
            await message.delete()
            logging.info(f"Message deleted: {message.content}")
        except Exception as e:
            logging.error(f"メッセージの削除に失敗: {e}")

        if not message.channel.permissions_for(message.guild.me).manage_webhooks:
            await message.channel.send("Webhookの作成に必要な権限がありません。")
            logging.error("ボットにWebhook管理権限がありません。")
            return

        webhooks = await message.channel.webhooks()
        webhook = next((w for w in webhooks if w.name == "TweetArchiver"), None)

        if webhook:
            try:
                webhook = await webhook.fetch()
                if not webhook.token:
                    await webhook.delete()
                    logging.info("トークンのないWebhookを削除しました")
                    webhook = None
            except Exception as e:
                logging.error(f"Webhookの取得に失敗、削除して再作成します: {e}")
                await webhook.delete()
                webhook = None

        if not webhook:
            webhook = await message.channel.create_webhook(name="TweetArchiver")
            logging.info("新しいWebhookを作成しました")

        ac_start = time.perf_counter()
        embed_tasks = [process_tweet(message, url, webhook) for url in urls]
        embeds = await asyncio.gather(*embed_tasks)
        try:
            await webhook.send(
                embeds=[e for e in embeds if e][:10],
                username=message.author.display_name,
                avatar_url=message.author.avatar.url if message.author.avatar else None
            )
        except ValueError as e:
            logging.error(f"Webhook送信に失敗: {e}")
            await message.channel.send("Webhookの送信に失敗しました。管理者に連絡してください。")

        ac_end = time.perf_counter()
        end = time.perf_counter()
        elapsed = end - start
        elapsed_dl = ac_end - ac_start
        logging.info(f"processing time: {elapsed:.2f}sec, access time: {elapsed_dl:.2f}sec")

# ボットの起動
@client.event
async def on_ready():
    global session
    session = aiohttp.ClientSession()
    await tree.sync()
    logging.info("ボットが起動し、コマンドが同期されました")

# ボットの終了処理
@client.event
async def on_close():
    global session
    if session:
        await session.close()
        logging.info("HTTPセッションを閉じました")

client.run(os.getenv("TOKEN"))