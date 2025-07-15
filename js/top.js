// ==========リンク疎通確認用==========
async function updateStatuses() {
try {
    const response = await fetch('/status.json');
    const statuses = await response.json();            
            
    document.querySelectorAll('#link-list li').forEach(li => {
    const name = li.getAttribute('data-name');
    const status = statuses[name] || 'down'; // デフォルトは'down'
    const statusDot = li.querySelector('.status');
    statusDot.className = `status ${status}`;
    });
} catch (error) {
    console.error('ステータスを取得できませんでした:', error);
    }
}
// 初回更新と一定間隔での更新
updateStatuses();
setInterval(updateStatuses, 300000); // 5分ごとに更新