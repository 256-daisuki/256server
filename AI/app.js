//server
const http = require("http");
const server = http.createServer();

server.on("request", function( request, response ) {
    response.writeHead(200, {"Content-Type" : "text/plain"});
    response.write( "Node.js Web Server" );
    response.end();
});

//main
server.listen(3001);

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