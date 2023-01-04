//. cpumem.js
const os = require( 'os' );
const settings = require( './settings' );

function getInfo(){
  var cpus = os.cpus();
  var loads = [];
  for( var i = 0, len = cpus.length; i < len; i ++ ){
    var cpu = cpus[i], total = 0;
    for( var type in cpu.times ){
      total += cpu.times[type];
    }
    
    var load = {};
    for( var type in cpu.times ){
      load[type] = cpu.times[type] / total * 100;
    }
    loads[i] = load;
  }
  
  var info = {
    cpus: loads,
    totalmem: os.totalmem(),
    freemem: os.freemem(),
    uptime: os.uptime(),
    loadavg: os.loadavg(),   //. 1, 5, and 15 min's load avg
    timestamp: ( new Date() ).getTime()
  };
  
  return info;
}

function showInfo(){
  var info = getInfo();
  console.log( JSON.stringify( info, null, 2 ) );
}

setInterval( showInfo, settings.intervalms );

