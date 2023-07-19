const ping = require('ping');

// 監視するサーバーのリスト
const servers = [
    '192.168.1.1',
    '192.168.1.2',
    '192.168.1.3'
];

// ピンポンの応答をチェックする関数
function checkPing(server) {
    return new Promise((resolve, reject) => {
        ping.sys.probe(server, (isAlive) => {
        if (isAlive) {
            resolve(server + ' はオンラインです');
        } else {
            reject(server + ' にPing応答がありません');
        }
        });
    });
}

// サーバーのリストを順にチェック
async function monitorServers() {
    try {
        const results = await Promise.all(servers.map(checkPing));
        console.log(results);
    } catch (error) {
        console.error(error);
        // 通知の処理を追加
    }
}

// サーバーの監視を開始
monitorServers();