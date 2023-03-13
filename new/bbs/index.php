<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>256server|開発中 256ch</title>
</head>
<body>
    <h1>256ch</h1>
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
</body>
</html>
