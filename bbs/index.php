<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>256server｜bbs</title>
    <link rel="stylesheet" href="/style.css">
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BN5KGMB0GN"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() { dataLayer.push(arguments); }
        gtag('js', new Date());

        gtag('config', 'G-BN5KGMB0GN');
    </script>
        <style>
        header {
            background-color: #808080;
            width: 100%;
            padding: 0;
        }

        nav {
            height: 40px;
        }

        nav ul {
            list-style: none;
            display: flex;
            margin-top: -30px;
            margin-right: 3%;
            justify-content: flex-end;
        }
  
        header li {
            margin-left: 20px;
            text-align: right;
            margin-top: -24px;
        }

        header a {
            color: #fff;
            text-decoration: none;
        }
  
        header p {
            color: #fff;
            font-size: 1.5em;
            margin-left: 15px;
            margin-top: auto;
            padding-top: 3px;
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <p>256</p>
            <ul>
                <li><a href="/index.html">home</a></li>
                <li><a href="/tools/index.html">tools</a></li>
                <li><a href="/history/index.html">歴史（笑）</a></li>
                <li><a href="/bbs/index.php">BBS</a></li>
            </ul>
        </nav>
    </header>
      
    <main>
        <?php
        $datafile = "bbs.txt";
        if (!file_exists($datafile)) {
            touch($datafile);
        }
        $data = file($datafile, FILE_IGNORE_NEW_LINES);
        if (count($data) >= 9999) {
            echo "このスレッドは9999書き込みを超えたので、封鎖されました。";
        } else {
            include "form.php";
        }
        include "list.php";
        ?>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
            integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM"
            crossorigin="anonymous"></script>
    </main>
    <script>
        window.addEventListener('load', function() {
            // a.htmlを読み込む
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                // レスポンスの中身を取得
                document.getElementById('usage').innerHTML = this.responseText;
                }
            };
            xhttp.open("GET", "a.html", true);
            xhttp.send();
        });
    </script>
</body>
</html>