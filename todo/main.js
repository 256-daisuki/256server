// クラス
class TodoList {
    // コンストラクタ
    constructor() {
            this.DOM = {};
            this.DOM.incomplete = document.querySelector(".item-area-incomplete ul");
            this.DOM.complete = document.querySelector(".item-area-complete ul");

        }
        // リストを生成
    _createItem(text) {
            const liElm = document.createElement('li');
            const pElm = document.createElement('p');
            const deleteButton = document.createElement('button');
            const completeButton = document.createElement('button');

            completeButton.classList.add('complete-button');
            completeButton.innerText = '完了';
            deleteButton.classList.add('incomplete-button');
            deleteButton.innerText = '削除';
            pElm.innerText = text;

            // 完了ボタンクリック
            completeButton.addEventListener('click', (e) => {
                this.deleteItem(e.srcElement.parentNode, this.DOM.incomplete);
                this.addCompleteItem(text);
            });
            // 削除ボタンクリック
            deleteButton.addEventListener('click', (e) => {
                const confirmation = confirm("本当に消しますか？");

                if (confirmation) {
                    this.deleteItem(e.srcElement.parentNode, this.DOM.incomplete);
                }
            });

            // 生成した要素
            liElm.appendChild(pElm);
            liElm.appendChild(completeButton);
            liElm.appendChild(deleteButton);

            return liElm;
        }
        // 完了に追加
    _completeItem(text) {
            const liElm = document.createElement('li');
            const pElm = document.createElement('p');
            const backButton = document.createElement('button');

            backButton.classList.add('complete-button');
            backButton.innerText = '戻る';
            pElm.innerText = text;
            // 戻るボタンクリック
            backButton.addEventListener('click', (e) => {
                this.deleteItem(e.srcElement.parentNode, this.DOM.complete);
                this.addItem(text);
            });

            liElm.appendChild(pElm);
            liElm.appendChild(backButton);

            return liElm;
        }
        // リストを追加
    addItem(text) {
            this.DOM.incomplete.appendChild(this._createItem(text));
        }
        // 完了に追加
    addCompleteItem(text) {
            this.DOM.complete.appendChild(this._completeItem(text));
        }
        // リストを削除
    deleteItem(target, domparent) {
        domparent.removeChild(target);
    }
}

function addtodoEvent() {
    const addItemTxt = document.querySelector(".add-item").value;
    // 値を入力していない時は処理を終了
    if (addItemTxt == "") {
        alert("値を入力してください");
        return
    }
    // フォームの値をリセット
    document.querySelector(".add-item").value = "";
    // インスタンス化
    const totoList = new TodoList();
    totoList.addItem(addItemTxt);
}

// クリックイベント
document.querySelector(".add-button").addEventListener('click', () => {
    addtodoEvent();
});

// キーボードイベント
document.addEventListener('keypress', keypress);
const regexEnter = new RegExp('(=|Enter)');

function keypress(e) {
    // エンターが押されたら
    if (regexEnter.test(e.key)) {
        addtodoEvent();
    } else {
        return false;
    }
}