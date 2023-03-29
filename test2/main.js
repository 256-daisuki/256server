const http = require('http');
const fs = require('fs');
const osUtils = require('os-utils');
const os = require('os');

const server = http.createServer((req, res) => {
  if (req.url === '/') {
    fs.readFile('a.html', (err, data) => {
      if (err) {
        res.writeHead(404);
        res.write('Not Found!');
      } else {
        res.writeHead(200, {'Content-Type': 'text/html'});
        res.write(data);
      }
      res.end();
    });
  } else {
    res.writeHead(404);
    res.write('Not Found!');
    res.end();
  }
});

// ディスクの情報を取得する
const totalDiskSpace = os.totalmem();
const freeDiskSpace = os.freemem();

// ディスクの使用率を計算する
const diskUsage = ((totalDiskSpace - freeDiskSpace) / totalDiskSpace) * 100;

server.listen(3010, () => {
  console.log('Server is running at http://localhost:3000');

  setInterval(() => {
    osUtils.cpuUsage((cpuUsage) => {
      const totalMem = osUtils.totalmem();
      const freeMem = osUtils.freemem();
      const memUsage = ((totalMem - freeMem) / totalMem) * 100;

      const html = `<o style="color: #808080;">CPU: ${Math.floor(cpuUsage.toFixed(2) * 100) }% MEM: ${memUsage.toFixed(2)}% Disk:${diskUsage.toFixed(2)}%</o>`;
      fs.writeFile('a.html', html, (err) => {
        if (err) {
          console.error(err);
        }
      });
    });
  }, 5000);
});