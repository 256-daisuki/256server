<?php
// おみくじを作る
// 大吉　中吉　小吉　末吉　凶
$omikuji = rand(1,8);
if($omikuji == 1) {
    echo "大吉";
    } elseif ($omikuji == 2) {
        echo "中吉";
    } elseif ($omikuji <= 4) { // 3,4を小吉に
        echo "小吉";
    } elseif ($omikuji <= 7) { // 5,6,7を末吉に
        echo "末吉";
    } else {
        echo "凶";
    }
?>