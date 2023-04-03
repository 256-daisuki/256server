const https = require('https');
const fs = require('fs');

https.get('http://192.168.100.4:8006', (res) => {
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });
  res.on('end', () => {
    fs.writeFileSync('a.html', data);
    console.log('Successfully saved the source code to a.html');
  });
}).on('error', (err) => {
  console.error(err);
});
