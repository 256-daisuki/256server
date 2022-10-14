<?php
$num = $_GET["256"];
echo (1 + ( 1 / $num))**$num;
?>
<!DOCTYPE html>
<html lang="ja" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>e(ネイピア数)の計算</title>
  </head>
  <body>
    <form action="/php/e/index.php" method="get">
      <input type="text" name="256"><br>
      <input type="submit" value="送信">
    </form>
  </body>
</html>