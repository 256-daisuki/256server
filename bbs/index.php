<?php
    if(!empty($_POST["submitButton"])) {
        echo $_POST["username"];
        echo $_POST["comment"];
    }

    //データベース接続
    $pdo =  new PDO('mysql:host=192.168.3.13;dbname=bbs',"root","");
?>

<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>256ch</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1 class="title">256ch</h1>
    <hr>
    <div class="boardWrapper">
        <section>
            <article>
                <div class="wrapper">
                    <div class="nameArea">
                        <span>名前:</span>
                        <p class="username">256daisuke</p>
                        <time>:2022/10/17</time>
                    </div>
                    <p class="comment">hello world</p>
                </div>
            </article>
        </section>
        <form class="formWrapper" method="POST">
            <div>
                <input type="submit" value="書き込む" name="submitButton">
                <label for="">名前:</label>
                <input type="text" name="username">
            </div>
            <div>
                <textarea class="commentTextArea" name="comment"></textarea>
            </div>
            </div>
        </form>
    </div>
</body>
</html>