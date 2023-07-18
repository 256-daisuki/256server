import shutil
import os
import datetime
import time

def backup_bbs_data(source_file, destination_path):
    # BBSのデータをNASに保存する関数
    try:
        # 現在の日時を取得してフォーマット
        current_time = datetime.datetime.now()
        time_string = current_time.strftime("%Y%m%d%H%M%S")
        
        # ファイルをNASにコピーし、送信時間をファイル名に含める
        destination_file = os.path.join(destination_path, f"{time_string}_counter")
        shutil.copy2(source_file, destination_file)
        
        print("BBSデータをNASに保存しました。")
        
    except Exception as e:
        print("保存中にエラーが発生しました:", str(e))

# BBSデータのソースファイルとNASの保存先ディレクトリを指定
source_file = "/home/counter/MoeCounter/"
destination_directory = "/mnt/NAS/server-backup/counter-backup"

# データのバックアップを0.5時間ごとに実行
while True:
    backup_bbs_data(source_file, destination_directory)
    # 0.5時間待機
    time.sleep(1800)