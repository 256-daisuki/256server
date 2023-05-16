<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST["name"];
    $body = $_POST["body"];
    $time = date("Y/m/d H:i");
    $datafile = "bbs.txt";
    if (!file_exists($datafile)) {
        touch($datafile);
    }
    $data = file($datafile, FILE_IGNORE_NEW_LINES);
    if (count($data) >= 9999) {
        echo "このスレッドは9999書き込みを超えたので、封鎖されました。";
    } else {
        $data[] = "{$name}\t{$time}\t{$body}";
        file_put_contents($datafile, implode("\n", $data));
        header("Location: index.php");
    }
}
?>
