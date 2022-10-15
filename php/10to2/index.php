<!DOCTYPE html>
<html lang="ja" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>10進数を2進数にするよ</title>
  </head>
  <body>
    <h1>10進数を2進数と16進数にするよ</h1>
    <h2>下に変換する数字を入力してね</h2>
    <form action="/php/10to2/index.php" method="get">
      <input type="text" name="num" value="0"><br>
      <input type="submit" value="変換">
    </form>
    <?php
    $num = filter_input(INPUT_GET, "num");
    if($num >= 1) {
      echo $num . "は2進数で" . decbin($num);
      echo "<br/>";
      echo $num . "は16進数で" . dechex($num);
    }
    ?>
  </body>
</html>
