require('dotenv').config(); // .envファイルの読み込み

const axios = require('axios');

const url_edit = "https://api.xrea.com/v1/mail/edit";
const url_info = "https://api.xrea.com/v1/user/info";

const data = {
    account: process.env.ACCOUNT,
    server_name: process.env.SERVER_NAME,
    api_secret_key: process.env.API_SECRET_KEY,
    box_reset_flg: "0",
    param: [
        {
            address_name: "test",
            address_domain: "256.email",
            address: "test@256.email",
            force: "0",
            pop_how: "3",
            // address_trans: "",
            // pop_pass: "",
            quota: "128", // メールボックスの容量(MB)
            autorespond: "0",
            clamd: "1",
            spam: "1",
            customd: "1",
            customd_body: [
                {
                    allow_stringcase: "0",
                    save_mail: "1",
                    conditions: [
                        {
                            target: "all",
                        }
                    ],
                action_body: "admin@256server.com",
                action_type: "forward",
                }
            ],
            pop_pass_rand: "1"
        },
    ]
}

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
