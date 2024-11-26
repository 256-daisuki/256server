<?php

function download_youtube_video($video_url, $output_path) {
    // yt-dlp のフルパスを指定
    $yt_dlp_path = '/home/youtube/.local/bin/yt-dlp';

    $escaped_output_path = escapeshellarg($output_path);

    // yt-dlp コマンドを構築
    $command = sprintf(
        '%s -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o %s %s',
        $yt_dlp_path,
        $escaped_output_path,
        $video_url
    );

    // コマンドを実行
    $output = shell_exec($command . " 2>&1"); // エラーもキャプチャ
    return $output;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['video_url'])) {
    $video_url = trim($_POST['video_url']);
    $output_dir = '/home/youtube/movie/';
    $output_file = uniqid('video_', true) . '.mp4';
    $output_path = $output_dir . $output_file;

    // ダウンロード処理
    $result = download_youtube_video($video_url, $output_path);

    // 保存先確認
    echo "<h1>ダウンロード結果</h1>";
    echo "<p>保存先: $output_path</p>";
    echo "<pre>" . htmlspecialchars($result) . "</pre>";

    // 保存が成功しているか確認
    if (file_exists($output_path)) {
        echo "<p>ダウンロードが成功しました！</p>";
    } else {
        echo "<p>ダウンロードに失敗しました。出力ファイルが存在しません。</p>";
    }
} else {
    echo "<p>エラー: URLが送信されていません。</p>";
}
?>
