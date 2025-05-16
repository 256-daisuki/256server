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
SAVE_DIR = "/var/www/html/test/images"  # 画像保存用ディレクトリ
COMBINED_DIR = "/var/www/html/test/combined"  # 合成画像用ディレクトリ
BASE_URL = "https://discord.256server.com/test"  # 公開URLのベース
CONFIG_FILE = "config.json"  # 設定ファイル

# 選択肢用のEnum
class ActionChoice(Enum):
    add = "add"
    remove = "remove"

# グローバルなセッションとキャッシュ
session = None  # aiohttp.ClientSession（ネットワークリクエスト用）
tweet_cache = {}  # ツイートキャッシュ {tweet_id: (data, timestamp)}
webhook_cache = {}  # Webhookキャッシュ {channel_id: webhook}
config_cache = None  # 設定キャッシュ
MAX_IMAGE_SIZE = 1024  # 画像の最大サイズ（ピクセル）
CACHE_TTL = 3600  # キャッシュの有効期限（秒）

# 同時実行を制限するためのセマフォ（調整）
semaphore = asyncio.Semaphore(20)

# 設定ファイルの読み書き（キャッシュ付き）
def load_config():
    global config_cache
    if config_cache is None:
        try:
            with open(CONFIG_FILE, 'r') as f:
                config_cache = json.load(f)
        except FileNotFoundError:
            config_cache = {}
        except Exception as e:
            logging.error(f"設定ファイルの読み込みに失敗: {e}")
            config_cache = {}
    return config_cache

async def save_config(config):
    global config_cache
    config_cache = config
    try:
        async with aiofiles.open(CONFIG_FILE, 'w') as f:
            await f.write(json.dumps(config, indent=4))
    except Exception as e:
        logging.error(f"設定ファイルの保存に失敗: {e}")

# fxtwitter APIからツイートデータを取得（キャッシュ付き）
async def get_tweet_data(tweet_id):
    current_time = time.time()
    # キャッシュを確認
    if tweet_id in tweet_cache:
        data, timestamp = tweet_cache[tweet_id]
        if current_time - timestamp < CACHE_TTL:
            return data
        else:
            del tweet_cache[tweet_id]  # 期限切れ

    api_url = f"https://api.fxtwitter.com/twitter/status/{tweet_id}"
    async with session.get(api_url) as response:
        if response.status != 200:
            return None
        data = await response.json()
        if data.get("code") != 200:
            return None
        tweet_data = data["tweet"]
        # キャッシュに保存
        tweet_cache[tweet_id] = (tweet_data, current_time)
        return tweet_data

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
        # 画像をリサイズ（最大サイズを制限）
        if img.width > MAX_IMAGE_SIZE or img.height > MAX_IMAGE_SIZE:
            img.thumbnail((MAX_IMAGE_SIZE, MAX_IMAGE_SIZE), Image.Resampling.LANCZOS)
        images.append(img)

    if len(images) == 1:
        return image_paths[0]

    # 2x2グリッドで配置（最大4枚）
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
    combined_path = os.path.join(COMBINED_DIR, combined_filename)
    # 非同期で保存
    async with aiofiles.open(combined_path, 'wb') as f:
        await f.write(new_image.tobytes())  # 直接バイト形式で保存
    return combined_path

# ツイート画像を処理する共通関数
async def process_tweet(interaction_or_message, url, webhook=None):
    # interaction_or_message が interaction の場合は応答用、message の場合は webhook 用
    is_interaction = isinstance(interaction_or_message, discord.Interaction)
    target = interaction_or_message

    # URLの正規化
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
        return None  # エラー時はNoneを返す

    # ツイートIDの抽出
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

    # fxtwitter APIでツイートデータを取得
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

    # センシティブチェック
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

    # ツイート情報と画像URLの取得
    tweet_text = tweet_data.get("text", "")
    author_name = tweet_data["author"]["name"]
    author_id = tweet_data["author"]["screen_name"]
    author_icon = tweet_data["author"]["avatar_url"]
    media = tweet_data.get("media", {})
    photos = media.get("photos", [])
    image_urls = [photo["url"] for photo in photos if photo["type"] == "photo"]

    # ツイート時間のフォーマット
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

    # 画像がない場合
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

    # 画像のダウンロード
    os.makedirs(SAVE_DIR, exist_ok=True)
    os.makedirs(COMBINED_DIR, exist_ok=True)
    saved_images = []

    tasks = []
    for image_url in image_urls:
        filename = image_url.split("/")[-1].split("?")[0]
        save_path = os.path.join(SAVE_DIR, filename)
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

    # 画像URLの生成
    if len(saved_images) > 1:
        combined_image_path = await combine_images(saved_images[:4])
        image_url = f"{BASE_URL}/combined/{os.path.basename(combined_image_path)}"
        archive_urls = [f"{BASE_URL}/images/{os.path.basename(path)}" for path in saved_images]
        archive_links = ' '.join([f'[{i+1}枚目]({url})' for i, url in enumerate(archive_urls)])
    else:
        image_url = f"{BASE_URL}/images/{os.path.basename(saved_images[0])}"
        archive_urls = [image_url]
        archive_links = f'[リンク]({image_url})'

    # 埋め込みの作成
    embed = discord.Embed(
        description=f"{tweet_text[:4000]}\n\n[元ツイート]({url})\nアーカイブ画像: {archive_links}",
        color=0x1DA1F2
    )
    embed.set_author(name=f"{author_name} ({author_id})", icon_url=author_icon)
    embed.set_image(url=image_url)
    embed.set_footer(text=f"ツイート時間: {tweet_time}")

    # 結果を返す（Webhook送信は呼び出し元で処理）
    return embed

# 手動コマンド
@tree.command(name="tw_img_archive", description="ツイートの画像を保存し、表示します")
@app_commands.describe(url="ツイートのURLを入力")
async def save_tweet_image(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    logging.info(f"コマンドが実行されました: tw_img_archive with URL: {url}")
    await process_tweet(interaction, url)

# 自動監視チャンネル設定コマンド
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

# ツイート画像を処理する関数（埋め込みを返す形に変更）
async def process_tweet(message, url, webhook=None):
    # URLの正規化
    if not url.startswith("http"):
        url = "https://" + url
    if "x.com" not in url and "twitter.com" not in url:
        return discord.Embed(description="エラー: Twitter (X) のURLのみ対応しています。", color=0xFF0000)

    # ツイートIDの抽出
    tweet_id_match = re.search(r'status/(\d+)', url)
    if not tweet_id_match:
        return discord.Embed(description="エラー: ツイートIDが見つかりませんでした。", color=0xFF0000)
    tweet_id = tweet_id_match.group(1)

    # fxtwitter APIでツイートデータを取得
    tweet_data = await get_tweet_data(tweet_id)
    if not tweet_data:
        return discord.Embed(description="ツイートデータの取得に失敗しました。", color=0xFF0000)

    # センシティブチェック
    is_sensitive = tweet_data.get("possibly_sensitive", False)
    if is_sensitive and not message.channel.is_nsfw():
        return discord.Embed(description="このツイートはセンシティブな内容を含みます。NSFWチャンネルで実行してください。", color=0xFF0000)

    # ツイート情報と画像URLの取得
    tweet_text = tweet_data.get("text", "")
    author_name = tweet_data["author"]["name"]
    author_id = tweet_data["author"]["screen_name"]
    author_icon = tweet_data["author"]["avatar_url"]
    media = tweet_data.get("media", {})
    photos = media.get("photos", [])
    image_urls = [photo["url"] for photo in photos if photo["type"] == "photo"]

    # ツイート時間のフォーマット
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
        return discord.Embed(description="画像が見つかりませんでした。", color=0xFF0000)

    # 画像のダウンロード
    os.makedirs(SAVE_DIR, exist_ok=True)
    os.makedirs(COMBINED_DIR, exist_ok=True)
    saved_images = []

    async with semaphore:
        tasks = []
        for image_url in image_urls:
            filename = image_url.split("/")[-1].split("?")[0]
            save_path = os.path.join(SAVE_DIR, filename)
            tasks.append(download_image(image_url, save_path))
        saved_images = [result for result in await asyncio.gather(*tasks) if result is not None]

    if not saved_images:
        return discord.Embed(description="画像の保存に失敗しました。", color=0xFF0000)

    # 画像URLの生成
    if len(saved_images) > 1:
        combined_image_path = await combine_images(saved_images[:4])
        image_url = f"{BASE_URL}/combined/{os.path.basename(combined_image_path)}"
        archive_urls = [f"{BASE_URL}/images/{os.path.basename(path)}" for path in saved_images]
        archive_links = ' '.join([f'[{i+1}枚目]({url})' for i, url in enumerate(archive_urls)])
    else:
        image_url = f"{BASE_URL}/images/{os.path.basename(saved_images[0])}"
        archive_urls = [image_url]
        archive_links = f'[リンク]({image_url})'

    # 埋め込みの作成
    embed = discord.Embed(
        description=f"{tweet_text[:4000]}\n\n[元ツイート]({url})\nアーカイブ画像: {archive_links}",
        color=0x1DA1F2
    )
    embed.set_author(name=f"{author_name} ({author_id})", icon_url=author_icon)
    embed.set_image(url=image_url)
    embed.set_footer(text=f"ツイート時間: {tweet_time}")
    return embed

# メッセージ監視
@client.event
async def on_message(message):
    # Bot自身のメッセージは無視
    if message.author == client.user:
        return
    
    # DM（ダイレクトメッセージ）の場合は処理をスキップ
    if message.guild is None:
        return

    config = load_config()
    guild_id = str(message.guild.id)
    monitored_channels = config.get(guild_id, [])
    
    if message.channel.id in monitored_channels:
        # URLをリストとして取得（順番を保持）
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

        except Exception as e:
            logging.error(f"Webhookの取得/作成に失敗: {e}")
            await message.channel.send("Webhookの設定に失敗しました。管理者に連絡してください。")
            return

        # アクセス時間計測開始
        ac_start = time.perf_counter()

        # 並列でツイートデータを取得し、埋め込みを作成
        embed_tasks = [process_tweet(message, url, webhook) for url in urls]
        embeds = await asyncio.gather(*embed_tasks)

        # 埋め込みをまとめて送信（最大10個まで）
        try:
            await webhook.send(
                embeds=embeds[:10],  # 最大10個の埋め込みを送信
                username=message.author.display_name,
                avatar_url=message.author.avatar.url if message.author.avatar else None
            )
        except ValueError as e:
            logging.error(f"Webhook送信に失敗: {e}")
            await message.channel.send("Webhookの送信に失敗しました。管理者に連絡してください。")

        # 計測終了
        ac_end = time.perf_counter()
        end = time.perf_counter()
        elapsed = end - start
        elapsed_dl = ac_end - ac_start
        logging.info(f"processing time: {elapsed:.2f}sec, access time: {elapsed_dl:.2f}sec")
# Discordボットの起動
@client.event
async def on_ready():
    await tree.sync()  # コマンドを同期
    logging.info("ボットが起動し、コマンドが同期されました")

client.run(os.getenv("TOKEN"))