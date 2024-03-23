fetch('/ping')
  .then(response => response.json())
  .then(data => {
    // JSONデータを処理する
    displayServerStatus(data.servers);
  })
  .catch(error => console.error('Error:', error));

function displayServerStatus(servers) {
  const statusContainer = document.getElementById('server-status');
  servers.forEach(server => {
    const serverStatus = document.createElement('div');
    serverStatus.textContent = `${server.server} is ${server.isAlive ? 'running' : 'not running'}`;
    statusContainer.appendChild(serverStatus);
  });
}