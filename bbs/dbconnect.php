<?php
try {
    $db = new PDO ('mysql:dbname=bbs;host=192.168.3.13; charset=utf8', 'root', '');
} catch (PDOException $e) {
    echo 'DB接続エラー' . $e->getMessage;
}
?>