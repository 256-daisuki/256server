const express = require('express');
const ping = require('ping');
const cors = require('cors');

const app = express();

app.use(cors());

const serverList = [
    { name: 'hp1', ip: '192.168.100.4' },
    { name: 'hp2', ip: '192.168.100.5' },
    { name: 'fuji1', ip: '192.168.100.6'}
];

app.get('/ping', (req, res) => {
    const responses = [];

    serverList.forEach((server) => {
        ping.sys.probe(server.ip, (isAlive) => {
            responses.push({ server: server.name, isAlive: isAlive });
            if (responses.length === serverList.length) {
                res.json({ servers: responses });
            }
        });
    });
});

const PORT = 3001;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
