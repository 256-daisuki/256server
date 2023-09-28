const axios = require('axios');
const qs = require('querystring');
require('dotenv').config();

const apiUrl = 'https://api.xrea.com/v1/mail/edit';

const payload = {
    account: process.env.ACCOUNT,
    server_name: process.env.SERVER_NAME,
    api_secret_key: process.env.API_SECRET_KEY,
    param: [
        {
        address_name: 'test',
        address_domain: '256.email',
        address: 'test@256.email',
        force: 0,
        pop_how: 1,
        address_trans: 'exampletrans@example.com',
        pop_pass: 'xxxxxxxx', // パスワード
        quota: 100000, // バイト
        autorespond: 1, // 自動返信
        autorespond_body: 'xxx', // 自動返信内容
        clamd: 1, // ウイルスフィルター
        spamd: 1, // スパムフィルター
        customd: 1, // カスタムフィルター
        customd_body: [
            {
            allow_stringcase: 0,
            save_mail: 0,
            conditions: [
                {
                target: 'all',
                body: 'example_string',
                condition: 'match',
                },
                {
                target: 'subject',
                body: 'sibject_ignore',
                condition: 'notmatch',
                },
            ],
            action_body: 'example@example.com',
            action_type: 'forward',
            },
        ],
        pop_pass_rand: 1, // パスワードランダム設定
        },
    ],
};

// メールアカウントを作成するリクエストを送信
axios.post(apiUrl, qs.stringify(payload))
    .then(response => {
        console.log(response.data);
    })
    .catch(error => {
        console.error(error);
    });
