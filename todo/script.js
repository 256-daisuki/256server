const todoList = document.getElementById('todo-list');
const form = document.querySelector('form');
const input = form.querySelector('input');

function addTask(task) {
  const li = document.createElement('li');
  const span = document.createElement('span');
  const button = document.createElement('button');
  span.textContent = task;
  button.textContent = '削除';
  li.appendChild(span);
  li.appendChild(button);
  todoList.appendChild(li);
  button.addEventListener('click', () => {
    li.remove();
    saveTasks();
  });
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const task = input.value.trim();
  if (task !== '') {
    addTask(task);
    input.value = '';
    saveTasks();
  }
});

function saveTasks() {
  const tasks = Array.from(todoList.querySelectorAll('li span')).map((span) => span.textContent);
  localStorage.setItem('tasks', JSON.stringify(tasks));
}

function loadTasks() {
  const tasks = JSON.parse(localStorage.getItem('tasks') || '[]');
  tasks.forEach((task) => addTask(task));
}

window.addEventListener('load', () => {
  loadTasks();
});

window.addEventListener('beforeunload', () => {
  saveTasks();
});
