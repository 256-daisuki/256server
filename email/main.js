require('dotenv').config(); // .envファイルの読み込み

const axios = require('axios');

const url_edit = "https://api.xrea.com/v1/mail/edit";
const url_info = "https://api.xrea.com/v1/user/info";

const data = {
    account: process.env.ACCOUNT,
    server_name: process.env.SERVER_NAME,
    api_secret_key: process.env.API_SECRET_KEY,
    reset_flg: "1",
    box_reset_flg: "1",
    param: [
        {
            address_name: "test",
            address_domain: "256.email",
            address: "test@256.email",
            pop_how: "3", //転送+PPO/WEB受信のできるように3番を選択
            quota: "128", //利用可能記憶域容量
            autorespond: "0", //自動返信設定 無し
            clamd: "1", //ウイルスフィルター　有り
            spamd: "1", //スパムフィルター　有り
            customd: "0", //カスタムフィルター　無し
            pop_pass_rand: "1", //パスワードランダム設定
            customd_body: {
                allow_stringcase: "0", //大文字小文字区別
                save_mail: "1", //メールを残すか
                conditions: [
                        {
                            target: "all",
                            body: "example_string",
                            condition: "match",
                        },
                    ],
                action_body: "forward",
                action_type: "admin@256server.com", // forward：メール転送 , maildir：振り分け , change_subject：題名変更 , change_from：from変更 , add_header：header追加 , delete：破棄
                }
            }
        ]
    };

axios.post(url_edit, data, {
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded', // フォームデータを指定
    }
})
.then(response => {
    console.log(response.data);
})
.catch(error => {
    console.error(error);
});
