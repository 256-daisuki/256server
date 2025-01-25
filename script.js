// フッター用
const client_h = document.getElementById('footer').clientHeight;
document.querySelector('main').style.minHeight = `calc(100vh - 39px - 33.5px - ${client_h}px)`;

console.log(client_h + 'px');

fetch('https://256server.com/system_info.json')
.then(response => response.json())
.then(data => {
  // Webサーバーの情報を表示
  const webServer = data.web_server;
  document.getElementById('web-server-cpu').textContent = webServer.cpu_usage;
  document.getElementById('web-server-ram').textContent = webServer.ram_usage;
  console.log(document.getElementById('web-server-cpu').textContent);
})

.catch(error => {
  console.error('データの取得に失敗しました:', error);
});