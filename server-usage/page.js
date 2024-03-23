const ping = require('ping');
const express = require('express');

const app = express();

//ping
app.get('/ping', (req, res) => {
  const hostsToPing = ['192.168.100.4', '192.168.100.5', '192.168.100.6'];

  res.json({ 
      ramUsage: ramUsage,
      totalMemory: totalMemory,
      freeMemory: freeMemory
  });
});

// 使用例:
const hostsToPing = ['192.168.100.4', '192.168.100.5', '192.168.100.6'];
pingHosts(hostsToPing);
