const http = require('http');
const fs = require('fs');

const PORT = 3001;

const server = http.createServer((request, response) => {
  fs.readFile('./index.html', 'UTF-8', (error, data) => {
    if (error) {
      response.writeHead(500, { 'Content-Type': 'text/plain' });
      response.write('Internal Server Error');
      response.end();
    } else {
      response.writeHead(200, { 'Content-Type': 'text/html' });
      response.write(data);
      response.end();
    }
  });
});

server.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});

//main
const os = require('os');

// CPU使用率を取得する
const cpuUsage = os.cpus().map(cpu => {
  const total = Object.values(cpu.times).reduce((acc, time) => acc + time, 0);
  const idle = cpu.times.idle;
  return (1 - idle / total) * 100;
});

// メモリ使用率を取得する
const totalMem = os.totalmem();
const freeMem = os.freemem();
const memUsage = ((totalMem - freeMem) / totalMem) * 100;

var cpu = (`CPU使用率: ${cpuUsage}%`);
var MEM = (`メモリ使用率: ${memUsage}%`);

var str = cpu;
var CPU = str.split(',');
console.log(CPU);

console.log(MEM);