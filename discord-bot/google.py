import requests
from bs4 import BeautifulSoup

# Google検索するキーワードを設定
search_word = 'python'

# 上位から何件までのサイトを抽出するか指定する
pages_num = 10 + 1

print(f'【検索ワード】{search_word}')

# Googleから検索結果ページを取得する
url = f'https://www.google.co.jp/search?hl=ja&num={pages_num}&q={search_word}'
request = requests.get(url)

# Googleのページ解析を行う
soup = BeautifulSoup(request.text, "html.parser")
search_site_list = soup.select('div.kCrYT > a')

# ページ解析と結果の出力
for rank, site in zip(range(1, pages_num), search_site_list):
    try:
        site_title = site.select('h3.zBAuLc')[0].text
    except IndexError:
        site_title = site.select('img')[0]['alt']
    site_url = site['href'].replace('/url?q=', '')
    # 結果を出力する
    print(str(rank) + "位: " + site_title + ": " + site_url)