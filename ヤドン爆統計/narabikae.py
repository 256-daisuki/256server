def sort_by_count(data):
    # 辞書を回数(count)でソートし、降順に並べる
    sorted_data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
    return sorted_data

def main():
    # ファイルから回数データを読み込む
    with open('toukei.txt', 'r') as f:
        data = {}
        for line in f:
            hoge, count = line.strip().split(': ')
            data[hoge] = int(count)

    # 回数が多い順にソート
    sorted_data = sort_by_count(data)

    # 結果を表示
    for hoge, count in sorted_data.items():
        print(f'{hoge}: {count}')

if __name__ == "__main__":
    main()
