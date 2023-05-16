<form id="myForm" method="post" action="write.php">
    名前：<input type="text" id="name" name="name"><br>
    本文：<br>
    <textarea id="body" name="body" cols="40" rows="5"></textarea><br>
    <input type="button" value="書き込む" onclick="submitForm()">
</form>

<script>
function submitForm() {
    var name = document.getElementById("name").value;
    var body = document.getElementById("body").value;
    
    // 改行コードを空白に置き換える
    body = body.replace(/\n/g, "");
    
    // 名前が未入力の場合はデフォルト値を設定する
    if (name === "") {
        name = "名無し";
    }
    
    // フォームを送信する
    document.getElementById("name").value = name;
    document.getElementById("body").value = body;
    document.getElementById("myForm").submit();
}
</script>