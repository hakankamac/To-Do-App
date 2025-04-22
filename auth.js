document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const tabItems = document.querySelectorAll('.tab-item');
    const forms = document.querySelectorAll('.form');

    // 🧩 Arka plan animasyonları
    setupFloatingItems();

    // 🔁 Sekme geçişleri (login/register)
    tabItems.forEach(item => {
        item.addEventListener('click', () => {
            tabItems.forEach(tab => tab.classList.remove('active'));
            item.classList.add('active');

            const tabName = item.dataset.tab;
            forms.forEach(form => form.classList.remove('active'));
            document.getElementById(`${tabName}-form`).classList.add('active');
        });
    });

    // 👁️ Parola görünürlüğü
    setupPasswordVisibility();

    // ✅ Giriş işlemi
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const email = document.getElementById('login-email').value.trim();
        const password = document.getElementById('login-password').value;

        if (!email || !password) {
            showMessage(loginForm, 'error', 'Lütfen tüm alanları doldurun.');
            return;
        }

        fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: email, password })
        })
        .then(res => res.json())
        .then(data => {
            if (data.message === 'Giriş başarılı') {
                showMessage(loginForm, 'success', 'Giriş başarılı! Yönlendiriliyorsunuz...');
                
                localStorage.setItem('user', JSON.stringify({
                    username: data.username,
                    id: data.user_id
                }));

                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1500);
            } else {
                showMessage(loginForm, 'error', data.error || 'Giriş başarısız.');
            }
        })
        .catch(() => {
            showMessage(loginForm, 'error', 'Sunucuya bağlanılamadı.');
        });
    });

    registerForm.addEventListener('submit', (e) => {
        e.preventDefault();
    
        const name = document.getElementById('register-name').value.trim();
        const email = document.getElementById('register-email').value.trim();
        const password = document.getElementById('register-password').value;
        const confirmPassword = document.getElementById('register-password-confirm').value;
    
        if (!name || !email || !password || !confirmPassword) {
            showMessage(registerForm, 'error', 'Lütfen tüm alanları doldurun.');
            return;
        }
    
        if (password !== confirmPassword) {
            showMessage(registerForm, 'error', 'Şifreler eşleşmiyor.');
            return;
        }
    
        fetch('http://localhost:5000/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: email, password: password })
        })
        .then(res => res.json())
        .then(data => {
            if (data.message === 'Kayıt başarılı') {
                showMessage(registerForm, 'success', 'Kayıt başarılı! Giriş yapabilirsiniz.');
    
                // Burada ad-soyadı da localStorage'a kaydediyoruz:
                localStorage.setItem('user', JSON.stringify({
                    username: email,
                    id:data.user_id,
                    name: name
                }));
    
                registerForm.reset();
                document.querySelector('[data-tab="login"]').click();
            } else {
                showMessage(registerForm, 'error', data.error || 'Kayıt başarısız.');
            }
        })
        .catch(() => {
            showMessage(registerForm, 'error', 'Sunucuya bağlanılamadı.');
        });
    });

    // 🎯 Yardımcı: Hata/başarı mesajı göster
    function showMessage(formElement, type, message) {
        const existingMessages = formElement.querySelectorAll('.error-message, .success-message');
        existingMessages.forEach(msg => msg.remove());

        const messageElement = document.createElement('div');
        messageElement.classList.add(`${type}-message`);
        messageElement.textContent = message;
        formElement.prepend(messageElement);

        setTimeout(() => {
            messageElement.remove();
        }, 5000);
    }

    // 🎨 Arka plan animasyonları
    function setupFloatingItems() {
        const backgroundAnimations = document.querySelector('.background-animations');
        const items = ['check-circle', 'tasks', 'clipboard-list', 'calendar-check', 'list-alt', 'clipboard-check'];

        setInterval(() => {
            const newItem = document.createElement('div');
            newItem.className = 'floating-item';
            const randomIcon = items[Math.floor(Math.random() * items.length)];
            newItem.innerHTML = `<i class="fas fa-${randomIcon}"></i>`;
            newItem.style.left = `${Math.floor(Math.random() * 100)}%`;
            newItem.style.top = '-50px';
            const size = Math.floor(Math.random() * 20) + 30;
            newItem.style.fontSize = `${size}px`;
            const duration = Math.floor(Math.random() * 3) + 5;
            newItem.style.animationDuration = `${duration}s`;
            backgroundAnimations.appendChild(newItem);
            setTimeout(() => newItem.remove(), duration * 1000 + 500);
        }, 3000);
    }

    // 🔒 Parola görünürlük toggle
    function setupPasswordVisibility() {
        const passwordFields = document.querySelectorAll('input[type="password"]');

        passwordFields.forEach(field => {
            const container = field.parentElement;
            const toggleBtn = document.createElement('i');
            toggleBtn.className = 'fas fa-eye password-toggle';
            container.appendChild(toggleBtn);

            toggleBtn.addEventListener('click', () => {
                if (field.type === 'password') {
                    field.type = 'text';
                    toggleBtn.className = 'fas fa-eye-slash password-toggle';
                } else {
                    field.type = 'password';
                    toggleBtn.className = 'fas fa-eye password-toggle';
                }
            });
        });
    }
});
