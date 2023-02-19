const http = require("http");
const PORT = 8000;

svr.listen(8081);

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

var CPU = (`CPU使用率: ${cpuUsage}%`);
var MEM = (`メモリ使用率: ${memUsage}%`);

console.log(CPU);
console.log(MEM);