import os
from pixivapi import Client, Size
import pathlib
from pixivapi.errors import LoginError

# 認証情報を直接設定
username = "user_nkxd2358"  # あなたのユーザー名
password = "256daisuki!"  # ここにパスワードを入力

# 環境変数のチェックはスキップ
if not username or not password:
    print("ユーザー名とパスワードを設定してください。")
    exit(1)

# クライアントオブジェクトを作成
client = Client()

# ログイン
try:
    client.login(username, password)
except LoginError as e:
    print(f"ログインエラー: {e}")
    print("ユーザー名とパスワードを確認してください。")
    exit(1)

# イラストIDでイラストを取得（例: 75523989）
illustration = client.fetch_illustration(75523989)

# 画像を保存するディレクトリを作成
directory = pathlib.Path.home() / "pixiv_images"
directory.mkdir(parents=True, exist_ok=True)

# イラストをダウンロード
illustration.download(directory=directory, size=Size.ORIGINAL)