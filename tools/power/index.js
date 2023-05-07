function generate_table() {
  // body の参照を取得
  var body = document.getElementsByTagName("body")[0];

  // <table> 要素と <tbody> 要素を作成
  var tbl = document.createElement("table");
  var tblBody = document.createElement("tbody");

  // すべてのセルを作成
  for (var i = 0; i < 21; i++) {
    // 表の行を作成
    var row = document.createElement("tr");

    for (var j = 0; j < 2; j++) {
      // <td> 要素とテキストノードを作成し、テキストノードを
      // <td> の内容として、その <td> を表の行の末尾に追加
      var cell = document.createElement("td");
      var cellText = document.createTextNode(i+"");
      cell.appendChild(cellText);
      row.appendChild(cell);
    }

    // 表の本体の末尾に行を追加
    tblBody.appendChild(row);
  }

  // <tbody> を <table> の中に追加
  tbl.appendChild(tblBody);
  // <table> を <body> の中に追加
  body.appendChild(tbl);
  // tbl の border 属性を 2 に設定
  tbl.setAttribute("border", "2");
}
