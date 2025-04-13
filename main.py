import psutil
import json
import requests
from time import sleep

# 各サーバーのIPアドレス
#servers = {
#    "hp1": "http://192.168.1.9:2000/system_info",
#    "hp2": "http://192.168.1.5:2000/system_info",
#    "nec1": "http://192.168.1.6:2000/system_info"
#}

# 自身のWebサーバー情報を取得
def get_web_server_info():
    # CPU使用率
    cpu_usage = psutil.cpu_percent(interval=1)
    # RAM使用率
    ram_usage = psutil.virtual_memory().percent
    # CPUの物理コア数と論理コア数
    cpu_physical_cores = psutil.cpu_count(logical=False)
    cpu_logical_cores = psutil.cpu_count(logical=True)
    # ディスク使用率
    disk_usage = psutil.disk_usage('/')
    disk_total = disk_usage.total
    disk_used = disk_usage.used
    disk_percent = disk_usage.percent
    # RAMの実装容量
    ram_total = psutil.virtual_memory().total
    
    return {
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage
    }

# 他のサーバーの情報を取得
#def get_server_info(server_url):
#    try:
#        response = requests.get(server_url)
#        response.raise_for_status()  # エラーチェック
#        return response.json()
#    except requests.exceptions.RequestException as e:
#        print(f"Error fetching data from {server_url}: {e}")
#        return None

# 全ての情報をまとめてJSONとして保存
def monitor_system():
    while True:
        # Webサーバーの情報を取得
        system_info = {"web_server": get_web_server_info()}
        
        # 各サーバーの情報を取得してまとめる
#        for server_name, server_url in servers.items():
#            server_data = get_server_info(server_url)
#            if server_data:
#                system_info[server_name] = server_data

        # JSONファイルに書き込み
        with open("system_info.json", "w") as f:
            json.dump(system_info, f, indent=4)

        sleep(5)  # 5秒ごとに更新

if __name__ == "__main__":
    monitor_system()
