const http = require('http');
const { exec } = require('child_process');

const hostname = '127.0.0.1';
const port = 3000;
const sites = [
  { name: '256server.com', status: 'unknown' },
  { name: 'doremire-server.com', status: 'unknown' },
  { name: 'koeniaydkoluaesr-pdyaeul.com', status: 'unknown' }
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
  let html = '<html><head><title>Site Status</title></head><body>';
  html += '<h1>Site Status</h1><ul>';
  sites.forEach(site => {
    html += `<li>${site.name}: ${site.status}</li>`;
  });
  html += '</ul></body></html>';
  res.end(html);
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});