const http = require('http');
const { exec } = require('child_process');
const fs = require('fs');

const hostname = '127.0.0.1';
const port = 3000;
const sites = [
  { name: '256server.com', status: 'unknown' },
  { name: 'doremire-server.com', status: 'unknown' },
  { name: 'rumiserver.com', status: 'unknown' },
  { name: 'discord.com', status: 'unknown' },
  { name: '5ch.net', status: 'unknown' },
  { name: 'twitter.com', status: 'unknown' },
  { name: 'facebook.com', status: 'unknown' },
];

function checkStatus(site) {
  exec(`ping -c 1 ${site.name}`, (error, stdout, stderr) => {
    if (error) {
      site.status = 'down';
    } else {
      const packetLoss = stdout.match(/(\d+)% packet loss/);
      if (packetLoss && parseInt(packetLoss[1]) === 100) {
        site.status = 'down';
      } else {
        site.status = 'up';
      }
    }
  });
}

setInterval(() => {
  sites.forEach(site => {
    checkStatus(site);
  });
}, 15000);

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/html');
  let html = '<body>';
  html += '<h1>Site Status</h1><table><tr><th>サイト</th><th>稼働状況</th>';
  sites.forEach(site => {
    html += `<tr><td>${site.name}</td><td>${site.status}</td></tr>`;
  });
  html += '</body></html>';
  fs.writeFile('a.html', html, (err) => {
    if (err) throw err;
    console.log('File saved successfully');
  });
  res.end(html);
});

server.listen(port, hostname, () => {
  console.log(`Server runn g at http://${hostname}:${port}/`);
});