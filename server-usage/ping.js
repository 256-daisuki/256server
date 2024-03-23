const express = require('express');
const ping = require('ping');

const app = express();

// /ping ルートにアクセスがあったらPingを実行するエンドポイント
app.get('/ping', async (req, res) => {
  try {
    const hosts = ['192.168.100.4', '192.168.100.5', '192.168.100.6'];
    const results = await pingHosts(hosts);
    res.json(results);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// 指定されたホストにPingを送信する関数
function pingHosts(hosts) {
  return Promise.all(hosts.map(async host => {
    try {
      const result = await ping.promise.probe(host);
      return {
        host: host,
        status: result.alive ? 'running' : 'down',
        roundtripTime: result.alive ? result.avg : null
      };
    } catch (error) {
      return {
        host: host,
        status: 'error',
        error: error.message
      };
    }
  }));
}

// Expressアプリケーションをポート3000で起動
const port = 3001;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
