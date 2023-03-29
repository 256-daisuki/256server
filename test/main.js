const os = require('os');
const osUtils = require('os-utils');

const networkInterfaces = os.networkInterfaces();
const interface = Object.keys(networkInterfaces)[0];

setInterval(() => {
  osUtils.networkUsage(interface, (err, result) => {
    if (err) {
      console.error(err);
      return;
    }
    console.log(`Network usage: ${Math.floor(result.rx_sec / 1024)} KB/s received, ${Math.floor(result.tx_sec / 1024)} KB/s transmitted`);
  });
}, 5000);
