const markdownInput = document.getElementById('markdown_input');
const markdownPreview = document.getElementById('markdown_preview');

document.getElementById('markdown_input').addEventListener('input', (e) => {
  const lines = document.getElementById('markdown_input').value.split('\n'); // 入力されたテキストを行ごとに分ける
  const textareaLists = document.getElementById('textarea_lists');

  textareaLists.textContent = '';  // 初期化
  lines.forEach((line, index) => {
    const lineElement = document.createElement('div');

    let spaceCount = 3;  // デフォルトでは3つ
    if (index + 1 >= 1000) {
      spaceCount = 0;
    } else if (index + 1 >= 100) {
      spaceCount = 1;
    } else if (index + 1 >= 10) {
      spaceCount = 2;
    }

    const spaces = ' '.repeat(spaceCount);
    lineElement.textContent = `${spaces} ${index + 1}`;
    textareaLists.appendChild(lineElement); 
  });
});


markdownInput.addEventListener('input', () => {
  const markdownText = markdownInput.value;
  const html = marked.parse(markdownText);  // .parse()を使う
  markdownPreview.innerHTML = html;
});
