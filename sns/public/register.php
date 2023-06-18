<?php

$err = [];

if($usrename = filter_input(INPUT_POST, 'username')) {
    $err[] = 'ユーザー名を記入しろ';
}

if($email = filter_input(INPUT_POST, 'email')) {
    $err[] = 'メールアドレスを記入しろ';
}

$password = filter_input(INPUT_POST, "password");
//正規表現
if (!preg_match("/\A[a-z\d]{8,256}+\z/i",$password)) {
    $err[] = 'パスワードは英数字8文字以上256文字以下にしろ';
}
$password_conf = filter_input(INPUT_POST, "password_conf");
if ($password !== $password_conf) {
    $err[] = "パスワードが一致しませーんm9(^Д^)ﾌﾟｷﾞｬｰ";
}

if (count($err) === 0) {
    //ユーザーを登録する処理だお

}

?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ユーザー登録完了</title>
</head>
<body>
    <?php if(count($err) > 0) : ?>
    <?php foreach($err as $e) : ?>
        <p><?php echo $e ?></p>
        <?php endforeach?>
    <?php else : ?>
    <p>ユーザー登録が完了しますた。</p>
    <?php endif ?>
    <a href="./signup_form.php">MODORU</a>
</body>
</html>