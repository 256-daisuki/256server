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
  try {
      fs.writeFileSync('server_stats.html', '');
      let outputText = ''; // 出力するテキストを格納する変数

      for (const server of servers) {
          // CPU使用率を取得
          const cpuResponse = await getJson(`http://${server.ip}:3000/cpu`);
          const cpuData = JSON.parse(cpuResponse);
          const cpuUsage = Math.floor(cpuData.cpuUsage * 10) / 10; // 小数点第1位で切り捨て

          // RAM使用率を取得
          const ramResponse = await getJson(`http://${server.ip}:3000/ram`);
          const ramData = JSON.parse(ramResponse);
          const ramUsage = Math.floor((100 - ramData.ramUsage) * 10) / 10; // 空き容量のパーセンテージから100を引く
          const totalMemoryGB = (ramData.totalMemory / 1000).toFixed(1); // MBからGBに変換
          const freeMemoryGB = (ramData.freeMemory / 1000).toFixed(1); // MBからGBに変換

          // テキストファイルに出す
          const outputText = `
          <h1>サーバー: ${server.hostname}</h1>
          <h2>CPU</h2>
          <ul>
            <li>CPU使用率: ${cpuUsage}%</li>
            <li>コア数: ${cpuData.numCores}コア</li>
          </ul>
          <h2>RAM</h2>
          <ul>
            <li>RAM使用率: ${ramUsage}%</li>
            <li>総メモリ容量: ${totalMemoryGB}GB</li>
            <li>空きメモリ容量: ${freeMemoryGB}GB</li>
          </ul>
          `;
          fs.appendFileSync('server_stats.html', outputText);
        }
        // テキストファイルに出力
        fs.writeFileSync('server_stats.html', outputText);
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

// 初回実行
fetchData();

// 15秒ごとに実行
setInterval(fetchData, 5000);
