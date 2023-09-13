const express = require('express');
const dns = require('dns');

const app = express();
const port = 3000;

app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

app.post('/lookup', (req, res) => {
    const domain = req.body.domain;

    dns.lookup(domain, { all: true }, (err, addresses) => {
        if (err) {
            console.error('エラー:', err);
            res.send('エラーが発生しました。');
        } else {
            const dnsInfo = JSON.stringify(addresses);
            res.send(`DNS情報: ${dnsInfo}`);
        }
    });

    dns.resolveNs(domain, (err, nameservers) => {
        if (err) {
            console.error('エラー:', err);
        } else {
            const nsInfo = JSON.stringify(nameservers);
            console.log('ネームサーバー情報:', nameservers);
        }
    });
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
