<!DOCTYPE html>
<html lang="ja">
<head>
   <meta charset="UTF-8">
   <meta http-equiv="X-UA-Compatible" content="IE=edge">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>BBS</title>
</head>
<body>
   <ol reversed>
   <?php
      // bbs.txtファイルの内容を読み込む
      $data = file_get_contents('bbs.txt');

      // 改行で区切って、配列に格納する
      $lines = explode("\n", $data);

      // 最新の書き込みから順に表示する
      for ($i = count($lines) - 1; $i >= 0; $i--) {
         $line = $lines[$i];
         // タブで区切って、名前と内容と書き込み時間を取得する
         list($name, $content, $time) = explode("\t", $line);
         // HTMLに変換して表示する
         echo '<li><strong>' . htmlspecialchars($name) . '</strong> (' . nl2br(htmlspecialchars($content)) . ')<br><p>' .  nl2br(htmlspecialchars($time)) . '</p></li>';
      }
   ?>
   </ol>
</body>
</html>
