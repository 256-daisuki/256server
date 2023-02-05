<?php
$name = "";
$message = "";
 
if (isset($_POST['send']) === true) {
    $name = $_POST["name"];
    $message = $_POST["message"];
    $fp = fopen("bord.txt", "a");
    fwrite($fp, $name . "t" . $message . "n");
    fclose($fp);
 
}
 
$fp = fopen("bord.txt", "r");
 
$bord_array = [];
while ($line = fgets($fp)) {
    $temp = explode("t", $line);
    $temp_array = [
        "name" => $temp[0],
        "message" => $temp[1]
    ];
    $bord_array[] = $temp_array;
}
?>
 
 
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>testbord</title>
</head>
<body>
<form action="" method="post">
    <div>
        <label for="name">名前</label>
        <input type="text" id="name" name="name">
    </div>
    <div>
        <label for="message">内容</label>
        <input type="text" id="message" name="message">
    </div>
    <input type="submit" name="send" value="送信する">
</form>
<h2>表示欄</h2>
<ul>
    <?php foreach ($bord_array as $data): ?>
        <?= "<li>" ?>
        <?= $data["name"] . ":" . $data["message"]; ?>
        <?= "</li>" ?>
    <?php endforeach; ?>
</ul>
</body>
</html>