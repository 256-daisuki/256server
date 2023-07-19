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
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5856031137941875"
    crossorigin="anonymous"></script>
</head>
<body>
    <header>
        <ul class="header-ul">
            <li class="title-256"><a href="#">256</a></li>
            <li class="nav-link">
                <nav>
                    <ul>
                        <li><a href="/index.html">home</a></li>
                        <li><a href="/tools/index.html">tools</a></li>
                        <li><a href="/history/index.html">history</a></li>
                        <li><a href="#">BBS</a></li>
                    </ul>
                </nav>
            </li>
        </ul>
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