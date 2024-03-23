const http = require('http');
const fs = require('fs');

// サーバーのIPアドレスとポート番号のリスト
const servers = [
    { ip: '192.168.100.4', port: 3000 },
    { ip: '192.168.100.5', port: 3000 },
    { ip: '192.168.100.6', port: 3000 }
];

// CPU使用率とRAM使用率を取得する関数
async function fetchData() {
    try {
        // テキストファイルを新規に作成
        fs.writeFileSync('server_stats.txt', '');

        for (const server of servers) {
            // CPU使用率を取得
            const cpuResponse = await getJson(`http://${server.ip}:${server.port}/cpu`);
            const cpuData = JSON.parse(cpuResponse);
            const cpuUsage = Math.floor(cpuData.cpuUsage * 10) / 10; // 小数点第1位で切り捨て

            // RAM使用率を取得
            const ramResponse = await getJson(`http://${server.ip}:${server.port}/ram`);
            const ramData = JSON.parse(ramResponse);
            const ramUsage = Math.floor((100 - ramData.ramUsage) * 10) / 10; // 空き容量のパーセンテージから100を引く
            const totalMemoryGB = (ramData.totalMemory / 1000).toFixed(1); // MBからGBに変換
            const freeMemoryGB = (ramData.freeMemory / 1000).toFixed(1); // MBからGBに変換

            // テキストファイルに出力
            const outputText = `Server: ${server.ip}\nCPU Usage: ${cpuUsage}, numCores: ${cpuData.numCores}\nRAM Usage: ${ramUsage}%, Total Memory: ${totalMemoryGB} GB, Free Memory: ${freeMemoryGB} GB\n`;

            fs.appendFileSync('server_stats.txt', outputText);
        }

        console.log('Data written successfully');
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

// データを取得してテキストファイルに出力
fetchData();
