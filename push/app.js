// プッシュ通知を購読
document.getElementById('subscribeButton').addEventListener('click', () => {
    Push.create('あなた!', {
        body: 'お前、それは閲覧だ',
        icon: 'icon.png',
        timeout: 4000, // 通知は4秒後に自動的に閉じます
        onClick: function () {
            // 通知クリックイベントを処理
            window.focus();
            this.close();
        }
    });
});

// プッシュ通知の購読解除
document.getElementById('unsubscribeButton').addEventListener('click', () => {
    Push.clear();
});
