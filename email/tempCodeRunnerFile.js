axios.post(url, payload)
    .then(response => {
        console.log(response.data);
    })
    .catch(error => {
        console.error(error);
});
