import requests

def get_website_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # エラーチェック

        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

if __name__ == "__main__":
    target_url = "https://256server.com"  # 取得したいサイトのURLを指定
    website_text = get_website_text(target_url)
    
    print(website_text)