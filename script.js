const client_h = document.getElementById('footer').clientHeight;
document.querySelector('main').style.minHeight = `calc(100vh - 39px - 33.5px - ${client_h}px)`;

console.log(client_h + 'px');