<!DOCTYPE html>
<html lang="ja" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>e(ネイピア数)の計算</title>
  </head>
  <body>
    <h1>ネイピア数を計算するよ</h1>
    <h2>下に数字を入力してね（大きければ大きいほど正確になるよ）</h2>
    <form action="/php/e/index.php" method="get">
      <input type="text" name="256" value="0"><br>
      <input type="submit" value="送信">
    </form>
    <?php
    $num = $_GET["256"];
    echo (1 + ( 1 / $num))**$num;
  ?>
  </body>
</html>
