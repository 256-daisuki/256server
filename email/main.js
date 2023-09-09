const axios = require('axios');

const url = "https://api.xrea.com/v1/user/info";
const payload = { account: "n256" , server_name: "m4.xrea.com" , api_secret_key: "PBGuaXAozsGdgTULQeLmDzdoEDAWrUAG" }; // ここに実際のAPIキーを追加

axios.post(url, payload)
    .then(response => {
    console.log(response.data);
    })
    .catch(error => {
    console.error(error);
    });