const express = require('express');
const os = require('os-utils');

const app = express();

// CPU使用率を取得するエンドポイント
app.get('/cpu', (req, res) => {
    os.cpuUsage((value) => {
        res.json({ cpuUsage: value });
    });
});

// RAM使用率とメモリ情報を取得するエンドポイント
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
