<?php
session_start();
require('dbconnect.php');
if (!isset($_SESSION['join'])) {
    header ('Location: index2.php');
    exit();
}
$hash = password_hash($_SESSION['join']['password'], PASSWORD_BCRYPT);
// 入力された文字をSQLに保存！！！
if(!empty($_POST)){
    $statement = $db->prepare('INSERT INTO members SET name=?, email=?, password=?, created=NOW()');
    $statement->execute(array(
        $_SESSION['join']['name'],
        $_SESSION['join']['email'],
        $hash));
        
    unset($_SESSION['join']);
    header('Location: index4.php');
    exit();
}
?>
<!DOCTYPE html>
<html lang="ja">
<head>
</head>
<body>
<form action="" method="post">
<input type="hidden" name="action" value="submit">
<div class="label">
    <p>ニックネーム
    <span class="check"><?php echo (htmlspecialchars($_SESSION['join']['name'], ENT_QUOTES)); ?></span>
    </p><br/>
    <p>email
    <span class="check"><?php echo (htmlspecialchars($_SESSION['join']['email'], ENT_QUOTES)); ?></span>
    </p><br/>
    <p>パスワード
    <span class="check">[セキュリティのため非表示] </span>
   </p><br/>
<input type="button" onclick="location.href='index2.php?action=rewrite'" value="修正する" name="rewrite" class="button02">
<input type="submit" onclick="location.href='index4.php'" value="登録する" name="registration" class="button">
</form>
</body>
</html>