<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="style.css"> <!-- 外部CSSファイルの読み込み -->
</head>
<body>
    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['url'])) {
        $url = $_GET['url'];

        // cURLを使用して指定されたURLの内容を取得
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $content = "" . qcurl_exec($ch);
        $content_type = curl_getinfo($ch, CURLINFO_CONTENT_TYPE); // コンテンツの種類を取得
        curl_close($ch);

        // 画像の場合
        if (strpos($content_type, 'image') === 0) {
            // 画像の場合はBase64エンコードして表示
            $base64_image = 'data:' . $content_type . ';base64,' . base64_encode($content);
            echo "<img src='$base64_image' alt='Image'>";
        } else {
            // 画像でない場合はそのまま表示
            echo $content;
        }
    }
    ?>
</body>
</html>
