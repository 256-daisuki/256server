const http = require('http');
const fs = require('fs');

const server = http.createServer((req, res) => {
  if (req.url === '/percent') {
    let data = '';
    req.on('data', chunk => {
      data += chunk;
    });
    req.on('end', () => {
      const percent = data.split('=')[1];
      const html = `<p>${percent}%</p>`;
      fs.writeFile('a.html', html, err => {
        if (err) {
          console.error(err);
        } else {
          console.log('Saved response body to a.html');
        }
      });
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.write(html);
      res.end();
    });
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.write('Not Found');
    res.end();
  }
});

const port = 3001;
server.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});
