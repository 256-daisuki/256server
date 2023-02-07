import "./styles.css";

const onClickAdd = () => {
  // 入力値を取得する
  const inputText = document.getElementById("add-text").value;
  // フォームを空にする
  document.getElementById("add-text").value = "";

  // divを生成
  const div = document.createElement("div");
  console.log(div);
  // <div></div>

  // クラス名を追加
  div.className = "list-row";
  console.log(div);
  // <div class="list-row"></div>

  // liタグ生成
  const li = document.createElement("li");
  console.log(li);
  // <li></li>
  // liの中にinputTextの内容を取得
  li.innerText = inputText;
  // <li>テスト</li>

  // divの子要素に各要素を設定する
  div.appendChild(li);
  /*
    <div class="list-row">
      <li>テスト</li>
    </div>
  */

  // 未完了リストにタスクを追加
  document.getElementById("incomplete-list").appendChild(div);
  // 未完了リストの一番下にフォームに入力した内容が表示される
};

// 追加ボタンをクリックした際にonClickAddを実行
document.getElementById("add-button").addEventListener("click", () => onClickAdd());