fetch('https://256server.com/system_info.json')
.then(response => response.json())
.then(data => {
    // Web
    const webServer = data.web_server;
    document.getElementById('web-server-cpu').textContent = webServer.cpu_usage;
    document.getElementById('web-server-ram').textContent = webServer.ram_usage;
    
    // hp1
    const hp1 = data.hp1;
    document.getElementById('hp1-cpu').textContent = hp1.cpu_usage;
    document.getElementById('hp1-cpu-logical-cores').textContent = hp1.cpu_logical_cores;
    document.getElementById('hp1-cpu-physical-cores').textContent = hp1.cpu_physical_cores;
    document.getElementById('hp1-ram').textContent = hp1.ram_usage;
    document.getElementById('hp1-ram-total').textContent = Math.floor(hp1.ram_total / (1024 * 1024 * 1024));
    document.getElementById('hp1-disk').textContent = hp1.disk_percent;
    
    // hp2
    const hp2 = data.hp2;
    document.getElementById('hp2-cpu').textContent = hp2.cpu_usage;
    document.getElementById('hp2-cpu-logical-cores').textContent = hp2.cpu_logical_cores;
    document.getElementById('hp2-cpu-physical-cores').textContent = hp2.cpu_physical_cores;
    document.getElementById('hp2-ram').textContent = hp2.ram_usage;
    document.getElementById('hp2-ram-total').textContent = Math.floor(hp2.ram_total / (1024 * 1024 * 1024));
    document.getElementById('hp2-disk').textContent = hp2.disk_percent;

    // nec1
    const nec1 = data.nec1;
    document.getElementById('nec1-cpu').textContent = nec1.cpu_usage;
    document.getElementById('nec1-cpu-logical-cores').textContent = nec1.cpu_logical_cores;
    document.getElementById('nec1-cpu-physical-cores').textContent = nec1.cpu_physical_cores;
    document.getElementById('nec1-ram').textContent = nec1.ram_usage;
    document.getElementById('nec1-ram-total').textContent = Math.floor(nec1.ram_total / (1024 * 1024 * 1024));
    document.getElementById('nec1-disk').textContent = nec1.disk_percent;
})
.catch(error => {
    console.error('データの取得に失敗しました:', error);
});