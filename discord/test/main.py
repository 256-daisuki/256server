import discord
from discord import app_commands
import aiohttp
import re
import os
import logging
import asyncio
from PIL import Image
from dotenv import load_dotenv
from datetime import datetime
import pytz
import json
from enum import Enum
import time

# 環境変数の読み込み
load_dotenv()

# ログ設定
logging.basicConfig(level=logging.INFO)

# Discordクライアントとコマンドツリーの初期化
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容の読み取りを有効化
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# 保存先ディレクトリとベースURLの設定
SAVE_DIR = "/var/www/html/test/images"  # 画像保存用ディレクトリ
COMBINED_DIR = "/var/www/html/test/combined"  # 合成画像用ディレクトリ
ARCHIVE_DIR = "/var/www/html/test/archive" # ツイート情報格納ディレクトリ
VIDEO_DIR = "/var/www/html/test/videos" # 動画保存用ディレクトリ
PREVIEW_DIR = "/var/www/html/test/previews" # プレビュー画像保存用ディレクトリ
BASE_URL = "https://discord.256server.com/test"  # 公開URLのベース
CONFIG_FILE = "config.json"  # 設定ファイル

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
async def process_tweet(interaction_or_message, url, webhook=None):
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

    # ========= embed =========
    archive_links = []

    for f in saved_images:
        archive_links.append(f"[画像]({BASE_URL}/images/{f})")

    for f in saved_videos:
        archive_links.append(f"[動画]({BASE_URL}/videos/{f})")

    # for f in saved_previews:
        archive_links.append(f"[Preview]({BASE_URL}/previews/{f})")

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

    if saved_previews:
        embed.set_image(url=f"{BASE_URL}/previews/{saved_previews[0]}")
    elif saved_images:
        embed.set_image(url=f"{BASE_URL}/images/{saved_images[0]}")

    # ========= 送信 =========
    if is_interaction:
        await target.followup.send(embed=embed)
    else:
        await webhook.send(
            embed=embed,
            username=target.author.display_name,
            avatar_url=target.author.avatar.url if target.author.avatar else None
        )

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

# Discordボットの起動
@client.event
async def on_ready():
    await tree.sync()  # コマンドを同期
    logging.info("ボットが起動し、コマンドが同期されました")

client.run(os.getenv("TOKEN"))