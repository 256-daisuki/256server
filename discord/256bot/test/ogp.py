import requests
from bs4 import BeautifulSoup
import urllib.request
import os
from urllib.parse import urljoin

def download_ogp_image(url, save_dir="/home/discord/python/test"):
    # ディレクトリが存在しない場合は作成
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    try:
        # URLからHTMLを取得
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # BeautifulSoupでHTMLを解析
        soup = BeautifulSoup(response.text, 'html.parser')

        # すべてのog:で始まるメタタグを取得
        og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
        
        # theme-color-origとtheme-colorを取得
        theme_color_orig = soup.find('meta', attrs={'name': 'theme-color-orig'})
        theme_color = soup.find('meta', attrs={'name': 'theme-color'})
        
        # iconを取得（rel="icon"またはrel="shortcut icon"）
        icon = soup.find('link', rel=lambda x: x in ['icon', 'shortcut icon'])

        # コンソールにメタデータをすべて出力
        print("=== メタデータ ===")
        
        # OGPメタタグの出力
        if og_tags:
            for tag in og_tags:
                property_name = tag.get('property', '不明')
                content = tag.get('content', '見つかりませんでした')
                print(f"{property_name}: {content}")
        else:
            print("OGPメタデータ: 見つかりませんでした")

        # theme-color-origの出力
        if theme_color_orig and theme_color_orig.get('content'):
            print(f"theme-color-orig: {theme_color_orig['content']}")
        else:
            print("theme-color-orig: 見つかりませんでした")

        # theme-colorの出力
        if theme_color and theme_color.get('content'):
            print(f"theme-color: {theme_color['content']}")
        else:
            print("theme-color: 見つかりませんでした")

        # iconの出力
        if icon and icon.get('href'):
            print(f"icon: {urljoin(url, icon['href'])}")
        else:
            print("icon: 見つかりませんでした")

        # 画像のダウンロード（og:image）
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            image_url = urljoin(url, og_image['content'])
            image_name = os.path.basename(image_url.split('?')[0])
            save_path = os.path.join(save_dir, image_name)
            urllib.request.urlretrieve(image_url, save_path)
            print(f"\nOGP画像を保存しました: {save_path}")
        else:
            print("\nOGPイメージが見つからなかったため、画像は保存されませんでした。")

        # アイコンのダウンロード
        if icon and icon.get('href'):
            icon_url = urljoin(url, icon['href'])
            icon_name = os.path.basename(icon_url.split('?')[0])
            icon_save_path = os.path.join(save_dir, icon_name)
            urllib.request.urlretrieve(icon_url, icon_save_path)
            print(f"アイコンを保存しました: {icon_save_path}")
        else:
            print("アイコンが見つからなかったため、アイコンは保存されませんでした。")

    except requests.RequestException as e:
        print(f"URLの取得に失敗しました: {e}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    # URLを入力
    target_url = input("画像とアイコンをダウンロードするURLを入力してください: ")
    download_ogp_image(target_url)