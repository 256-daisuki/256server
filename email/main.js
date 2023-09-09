require('dotenv').config(); // .envファイルの読み込み

const axios = require('axios');

const url = "https://api.xrea.com/v1/user/info";

const data = {
    account: process.env.ACCOUNT,
    server_name: process.env.SERVER_NAME,
    api_secret_key: process.env.API_SECRET_KEY
};

axios.post(url, data, {
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

