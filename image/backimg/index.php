<?php
// 画像ファイルのリスト
$images = ['images/1.png', 'images/2.png', 'images/3.png', 'images/4.png', 'images/5.png', 'images/6.png', 'images/7.png', 'images/8.png', 'images/9.png'];

// ランダムに画像を選択
$randomImage = $images[array_rand($images)];

// 画像のMIMEタイプを設定
header('Content-Type: image/png');

// 画像を読み込んで出力
readfile($randomImage);
exit;
?>