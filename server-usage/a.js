const http = require('http');
const fs = require('fs');

// サーバーのIP
const servers = [
    { ip: '192.168.100.4', hostname: 'hp1'},
    { ip: '192.168.100.5', hostname: 'hp2'},
    { ip: '192.168.100.6', hostname: 'fuji1'}
];

// CPU使用率とRAM使用率を取得する関数
async function fetchData() {
  // テキストファイル作成
  fs.writeFileSync('server_stats.txt', '');

  for (const server of servers) {
    // CPU使用率
    const cpuResponse = await getJson(`http://${server.ip}:3000/cpu`);
    const cpuData = JSON.parse(cpuResponse);
    const cpuUsage = Math.floor(cpuData.cpuUsage * 10) / 10; // 小数点第1位で切り捨て

    // RAM使用率
    const ramResponse = await getJson(`http://${server.ip}:3000/ram`);
    const ramData = JSON.parse(ramResponse);
    const ramUsage = Math.floor((100 - ramData.ramUsage) * 10) / 10;
    const totalMemoryGB = (ramData.totalMemory / 1000).toFixed(1); // MBからGBに変換
    const freeMemoryGB = (ramData.freeMemory / 1000).toFixed(1); // MBからGBに変換

    // テキストファイルに出す
    const outputText = `
    <h1>サーバー: ${server.hostname}</h1>
    <h2>CPU</h2>
    <li>
      <ul>CPU使用率: ${cpuUsage}%</ul>
      <ul>コア数: ${cpuData.numCores}コア</ul>
    </li>
    <h2>RAM</h2>
    <li>
      <ul>RAM使用率: ${ramUsage}%</ul>
      <ul>総メモリ容量: ${totalMemoryGB}GB</ul>
      <ul>空きメモリ容量: ${freeMemoryGB}GB</ul>
    </li>
    `;
    fs.appendFileSync('server_stats.html', outputText);
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

// 初回実行
fetchData();

// 15秒ごとに実行
setInterval(fetchData, 15000);
