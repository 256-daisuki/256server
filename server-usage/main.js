const express = require('express');
const os = require('os-utils');
const cors = require('cors');

const app = express();
app.use(cors());

// CPU使用率とコア数を取得
app.get('/cpu', (req, res) => {
  os.cpuUsage((value) => {
    const numCores = os.cpuCount();

    res.json({ 
      cpuUsage: value,
      numCores: numCores
    });
  });
});

// RAM使用率とメモリ情報を取得
app.get('/ram', (req, res) => {
  const ramUsage = os.freememPercentage() * 100;
  const totalMemory = os.totalmem();
  const freeMemory = os.freemem();

  res.json({ 
      ramUsage: ramUsage,
      totalMemory: totalMemory,
      freeMemory: freeMemory
  });
});

// サーバーを起動する
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
