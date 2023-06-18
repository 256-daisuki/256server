<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>サインイン</title>
</head>
<body>
    <h1>ユーザー登録フォーム</h1>
    <form action="register.php" method="POST">
        <p>
            <label for="username">ユーザー名：</label>
            <input type="text" name="username">
        </p>
        <p>
            <label for="email">メールアドレス：</label>
            <input type="email" name="email">
        </p>
        <p>
            <label for="password">パスワード：</label>
            <input type="password" name="password">
        </p>
        <p>
            <label for="password_conf">パスワード確認：</label>
            <input type="password" name="password_conf">
        </p>
        <p>
            <input type="submit" value="新規登録">
        </p>
    </form>
</body>
</html>