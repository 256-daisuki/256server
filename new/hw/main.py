import psutil
from flask import Flask, jsonify

app = Flask(__name__)

def get_system_info():
    # CPU使用率
    cpu_usage = psutil.cpu_percent(interval=1)
    # CPUの物理コア数と論理コア数
    cpu_physical_cores = psutil.cpu_count(logical=False)
    cpu_logical_cores = psutil.cpu_count(logical=True)
    # RAM使用率と実装容量
    ram_usage = psutil.virtual_memory().percent
    ram_total = psutil.virtual_memory().total
    # ディスクの全体容量と使用容量
    disk_usage = psutil.disk_usage('/')
    disk_total = disk_usage.total
    disk_used = disk_usage.used
    disk_percent = disk_usage.percent

    system_info = {
        "cpu_usage": cpu_usage,
        "cpu_physical_cores": cpu_physical_cores,
        "cpu_logical_cores": cpu_logical_cores,
        "ram_usage": ram_usage,
        "ram_total": ram_total,
        "disk_total": disk_total,
        "disk_used": disk_used,
        "disk_percent": disk_percent,
    }
    
    return system_info

# JSONを送るヤツ
@app.route('/system_info', methods=['GET'])
def system_info():
    system_info = get_system_info()
    return jsonify(system_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000)
