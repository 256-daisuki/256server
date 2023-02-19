//. cpumem.js
const os = require( 'os' );
const settings = require( './settings' );
  
  var info = {
    cpus: loads,
    totalmem: os.totalmem(),
    freemem: os.freemem(),
    uptime: os.uptime(),
    loadavg: os.loadavg(),   //. 1, 5, and 15 min's load avg
    timestamp: ( new Date() ).getTime()
  };
  
  return info;


function showInfo(){
  var info = getInfo();
  console.log( JSON.stringify( info, null, 2 ) );
}

setInterval( showInfo, settings.intervalms );

