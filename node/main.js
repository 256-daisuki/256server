const http = require('http');
const fs = require('fs');
const osUtils = require('os-utils');

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

server.listen(3000, () => {
  console.log('Server is running at http://localhost:3000');

  setInterval(() => {
    osUtils.cpuUsage((cpuUsage) => {
      const totalMem = osUtils.totalmem();
      const freeMem = osUtils.freemem();
      const memUsage = ((totalMem - freeMem) / totalMem) * 100;

      const html = `
<p>CPU: ${Math.floor(cpuUsage.toFixed(2) * 100) }%</p>
<p>MEM: ${memUsage.toFixed(2)}%</p>
      `;
      fs.writeFile('a.html', html, (err) => {
        if (err) {
          console.error(err);
        }
      });
    });
  }, 3000);
});