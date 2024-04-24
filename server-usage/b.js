const http = require('http');
const fs = require('fs');

// サーバーのIPアドレスとポート番号のリスト
const servers = [
    { ip: '192.168.100.4', hostname: 'hp1' },
    { ip: '192.168.100.5', hostname: 'hp2' },
    { ip: '192.168.100.6', hostname: 'fuji1' }
];

// CPU使用率とRAM使用率を取得する関数
async function fetchData() {
    try {
        let outputText = ''; // 出力用のテキスト

        for (const server of servers) {
            // CPU使用率を取得
            const cpuResponse = await getJson(`http://${server.ip}:3000/cpu`);
            const cpuData = JSON.parse(cpuResponse);
            const cpuUsage = Math.floor(cpuData.cpuUsage * 1000) / 10; // 小数点第1位で切り捨て

            // RAM使用率を取得
            const ramResponse = await getJson(`http://${server.ip}:3000/ram`);
            const ramData = JSON.parse(ramResponse);
            const ramUsage = Math.floor(ramData.ramUsage * 10) / 10; // 小数点第1位で切り捨て
            const totalMemoryGB = (ramData.totalMemory / 1000).toFixed(1); // MBからGBに変換
            const freeMemoryGB = (ramData.freeMemory / 1000).toFixed(1); // MBからGBに変換

            // テキストに出力を追加
            outputText += `
  <h2>サーバー: ${server.hostname}</h2>
  <h3>CPU</h3>
  <ul>
    <li>CPU使用率: ${cpuUsage}%</li>
    <li>コア数: ${cpuData.numCores}コア</li>
  </ul>
  <h3>RAM</h3>
  <ul>
    <li>RAM使用率: ${ramUsage}%</li>
    <li>総メモリ容量: ${totalMemoryGB}GB</li>
    <li>空きメモリ容量: ${freeMemoryGB}GB</li>
  </ul>
            `;
        }

        // テキストファイルに出力
        fs.writeFileSync('server_stats.html', outputText);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// HTTP GETリクエストを行う関数
function getJson(url) {
    return new Promise((resolve, reject) => {
        http.get(url, (res) => {
            let data = '';

            res.on('data', (chunk) => {
                data += chunk;
            });

            res.on('end', () => {
                resolve(data);
            });
        }).on('error', (error) => {
            reject(error);
        });
    });
}

// 15秒ごとに実行
setInterval(fetchData, 5000);

// 初回実行
fetchData();
