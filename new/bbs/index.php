<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>BBS</title>
</head>
<body>
    <h1>BBS</h1>
    <?php
    $datafile = "bbs.txt";
    if (!file_exists($datafile)) {
        touch($datafile);
    }
    $data = file($datafile, FILE_IGNORE_NEW_LINES);
    if (count($data) >= 1024) {
        echo "このスレッドは1024書き込みを超えたので、封鎖されました。";
    } else {
        include "form.php";
    }
    include "list.php";
    ?>
</body>
</html>
