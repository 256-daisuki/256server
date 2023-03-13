<form method="post" action="write.php">
    名前：<input type="text" name="name" id="name"><br>
    本文：<br>
    <textarea name="body" id="body" cols="40" rows="5"></textarea><br>
    <input type="submit" value="書き込む" onclick="checkForm()">
</form>

<script>
function checkForm() {
  var nameField = document.getElementById("name");
  var bodyField = document.getElementById("body");

  if (nameField.value == "") {
    nameField.value = "名無し";
  }

  if (bodyField.value.trim() == "") {
    alert("本文を入力してください。");
    event.preventDefault();
  }
}
</script>