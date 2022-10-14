<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>e(ネイピア数)の計算</title>
</head>
<body>
    <h1>ネイピア数を計算するよ</h1>
    <h2>下のところに数字を入れてね（できれば100以上）</h2>
    <form method="post">
        <input type="text" name="num" value="">
        <input type="submit">
    </form>
    <?php
    $num = $_POST["num"];
    echo (1 + ( 1 / $num))**$num;
    ?>
</body>
</html>