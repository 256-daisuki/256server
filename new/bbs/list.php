<hr>
<h2>投稿一覧</h2>
<?php
$datafile = "bbs.txt";
if (file_exists($datafile)) {
    $data = file($datafile, FILE_IGNORE_NEW_LINES);
    $count = count($data);
    if ($count > 0) {
        echo "<ol>";
        foreach ($data as $row) {
            $cols = explode("\t", $row);
            $name = htmlspecialchars($cols[0], ENT_QUOTES, "UTF-8");
            $time = htmlspecialchars($cols[1], ENT_QUOTES, "UTF-8");
            $body = htmlspecialchars($cols[2], ENT_QUOTES, "UTF-8");
            echo "<li>{$name} ({$time})<br>{$body}</li>";
        }
        echo "</ol>";
    } else {
        echo "まだ投稿がありません。";
    }
} else {
    echo "まだ投稿がありません。";
}
?>
