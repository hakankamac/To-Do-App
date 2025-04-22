// Global değişkenler ve element tanımlamaları
const todoForm = document.getElementById('todo-form');
const todoInput = document.getElementById('todo-input');
const todoList = document.getElementById('todo-list');
const userNameElement = document.getElementById('user-name');
const logoutBtn = document.getElementById('logout-btn');

const API_URL = 'http://localhost:5000'; // merkezi API URL

let todos = [];
let isLoading = false;
let user = null;

document.addEventListener('DOMContentLoaded', () => {
    // Kullanıcı oturumunu kontrol et
    const userData = localStorage.getItem('user');
    if (!userData) {
        window.location.href = 'login.html';
        return;
    }

    try {
        user = JSON.parse(userData);
        //const displayName = user.name ? user.name : user.username.split('@')[0];
        const displayName = user.name
            ? user.name
            : formatFromEmail(user.username);
        userNameElement.textContent = `Hoş geldin, ${displayName}`;
    } catch (error) {
        console.error('Oturum bilgisi alınırken hata:', error);
        localStorage.removeItem('user');
        window.location.href = 'login.html';
        return;
    }

    // Görevleri getir
    displayTodos();
});

// Çıkış butonuna tıklandığında
logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('user');
    window.location.href = 'login.html';
});

// Yeni görev ekleme
todoForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const todoText = todoInput.value.trim();
    if (todoText !== '') {
        await addTodo(todoText);
        todoInput.value = '';
        todoInput.focus();
    }
});

// SUNUCUDAN GÖREVLERİ GETİR
async function displayTodos() {
    todoList.innerHTML = '';

    try {
        const response = await fetch(`${API_URL}/todos?user_id=${user.id}`);
        const data = await response.json();
        todos = data;

        if (todos.length === 0) {
            todoList.innerHTML = '<li class="todo-item">Henüz görev eklenmedi</li>';
            return;
        }

        todos.forEach(todo => {
            const todoItem = document.createElement('li');
            todoItem.classList.add('todo-item');
            if (todo.completed) todoItem.classList.add('completed');

            todoItem.innerHTML = `
                <span class="todo-text">${todo.text}</span>
                <div>
                    <button class="edit-btn" data-id="${todo.id}">Düzenle</button>
                    <button class="delete-btn" data-id="${todo.id}">Sil</button>
                </div>
            `;

            todoItem.querySelector('.todo-text').addEventListener('click', () => {
                toggleComplete(todo.id);
            });

            todoItem.querySelector('.edit-btn').addEventListener('click', () => {
                editTodo(todo.id);
            });

            todoItem.querySelector('.delete-btn').addEventListener('click', () => {
                deleteTodo(todo.id);
            });

            todoList.appendChild(todoItem);
        });

    } catch (error) {
        console.error('Görevler alınırken hata:', error);
        todoList.innerHTML = '<li class="todo-item">Sunucudan veri alınamadı.</li>';
    }
}

// GÖREV EKLE
async function addTodo(text) {
    const newTodo = {
        id: Date.now(),
        text: text,
        completed: false,
        user_id: user.id
    };

    try {
        const response = await fetch(`${API_URL}/todos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newTodo)
        });

        if (response.ok) {
            await displayTodos();
        } else {
            alert('Görev eklenemedi.');
        }
    } catch (error) {
        console.error('Ekleme hatası:', error);
    }
}

// GÖREV SİL
async function deleteTodo(id) {
    try {
        const response = await fetch(`${API_URL}/todos/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            await displayTodos();
        } else {
            alert('Görev silinemedi.');
        }
    } catch (error) {
        console.error('Silme hatası:', error);
    }
}

// GÖREVİ TAMAMLANDI YAP / GERİ AL
async function toggleComplete(id) {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;

    const updated = { ...todo, completed: !todo.completed };

    try {
        const response = await fetch(`${API_URL}/todos/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updated)
        });

        if (response.ok) {
            await displayTodos();
        }
    } catch (error) {
        console.error('Tamamlama hatası:', error);
    }
}

// GÖREVİ DÜZENLE
async function editTodo(id) {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;

    const newText = prompt('Yeni görev metni:', todo.text);
    if (!newText || newText.trim() === '' || newText === todo.text) return;

    const updated = { ...todo, text: newText.trim() };

    try {
        const response = await fetch(`${API_URL}/todos/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updated)
        });

        if (response.ok) {
            await displayTodos();
        }
    } catch (error) {
        console.error('Düzenleme hatası:', error);
    }
}

// Yükleniyor göstergesi fonksiyonu (isteğe bağlı kullanım)
function setLoading(loading) {
    isLoading = loading;
    // Buraya istersen yükleniyor animasyonu kodu eklersin
}

function formatFromEmail(email){
    let base = email.split('@')[0];
    base = base.replace(/[0-9]/g, '');         // hakankamac
    base = base.replace(/[_\-.]/g, ' ');

    return base
    .split(' ')
    .filter(kelime => kelime) // boş string varsa at
    .map(kelime =>  kelime.charAt(0).toUpperCase() + kelime.slice(1))
    .join(' ');
}