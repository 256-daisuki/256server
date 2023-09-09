require('dotenv').config(); // .envファイルの読み込み

const axios = require('axios');

const url = "https://api.xrea.com/v1/user/info";
const payload = new URLSearchParams();
payload.append('api_secret_key', process.env.API_SECRET_KEY);
payload.append('account', process.env.ACCOUNT);
payload.append('server_name', process.env.SERVER_NAME);

axios.post(url, payload)
    .then(response => {
        console.log(response.data);
    })
    .catch(error => {
        console.error(error);
});
