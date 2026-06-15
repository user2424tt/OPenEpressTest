// simple_realtime.js - AJAX версия

window.globalData = {
    login: {},
    register: {},
    opros: {}
};

// Отправка данных на сервер
function sendToServer(dataType, data) {
    // Сохраняем локально
    if (dataType === 'login') window.globalData.login = data;
    else if (dataType === 'register') window.globalData.register = data;
    else if (dataType === 'opros') window.globalData.opros = data;
    
    // Отправляем AJAX
    fetch('/api/update_realtime', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: dataType, data: data })
    })
    .then(response => response.json())
    .then(result => {
        console.log('Sent to Python:', result);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Обработка всех кнопок
document.addEventListener('click', (event) => {
    if (event.target.tagName === 'BUTTON') {
        const button = event.target;
        const form = button.closest('form');
        
        if (form) {
            const formData = new FormData(form);
            const data = {};
            
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            
            // Определяем тип данных
            if (form.action.includes('/enter')) {
                sendToServer('login', data);
            } else if (form.action.includes('/register')) {
                sendToServer('register', data);
            } else if (form.action.includes('/opros1_data')) {
                // Для чекбоксов
                const checkboxes = form.querySelectorAll('input[name="boxx"]:checked');
                data.boxx = Array.from(checkboxes).map(cb => cb.value);
                sendToServer('opros', data);
            }
        }
    }
});

console.log('Real-time handler loaded');