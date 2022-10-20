<?php
session_start();            //セッションを開始
require('dbconnect.php');   //dbconnect.phpのファイル読み込めよ！
if (!empty($_POST) ){
        $_SESSION['join'] = $_POST;
        header('Location: test3.php');
        exit();
    }
?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <title>会員登録をする</title>
</head>
<body>
    <!-- https://biz.addisteria.com/bbs_creation2/ こっからのコピペ　エラー吐いたら頑張ってね♥-->
<form action="" method="post" enctype="multipart/form-data" class="registrationform">
    <p>ニックネーム<input type="text" name="name" style="width:150px" value="<?php echo htmlspecialchars($_POST['name']??"", ENT_QUOTES); ?>"></p><!-- 入力したニックネームをPOST! nameだよ　htmlspecialcharsは<>をHTMLとして処理しなくなるみたい　私みたいなユーザーはがっかり -->
    <p>email<input type="text" name="email" style="width:150px" value="<?php echo htmlspecialchars($_POST['email']??"", ENT_QUOTES); ?>"></p>
    <p>パスワード<input type="password" name="password" style="width:150px" value="<?php echo htmlspecialchars($_POST['password']??"", ENT_QUOTES); ?>"></p>
    <p>パスワード再入力<span class="red">*</span><input type="password" name="password2″ style="width:150px"></p>
<input type="submit" value="確認する" class="button">
</form>
</body>
</html>