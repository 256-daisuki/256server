def count_hoge_in_urls(urls):
    hoge_count = {}
    for url in urls:
        parts = url.split('/')
        if len(parts) >= 4:
            hoge = parts[3]
            if hoge in hoge_count:
                hoge_count[hoge] += 1
            else:
                hoge_count[hoge] = 1
    return hoge_count

def main():
    # ファイルからURLリストを読み込む
    with open('url.txt', 'r') as f:
        urls = f.readlines()

    # 改行文字を取り除く
    urls = [url.strip() for url in urls]

    # URLからhogeの部分を数える
    hoge_count = count_hoge_in_urls(urls)

    # 結果をtoukei.txtに出力
    with open('toukei.txt', 'w') as f:
        for hoge, count in hoge_count.items():
            f.write(f'{hoge}: {count}\n')

if __name__ == "__main__":
    main()
