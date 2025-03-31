// Инициализация Telegram WebApp
const tg = window.Telegram.WebApp;
const API_URL = 'http://localhost:8000';
tg.expand();

// DOM элементы
const botList = document.getElementById('botList');
const createBotBtn = document.getElementById('createBotBtn');

// Моковые данные (замените на реальные API-запросы)
const mockBots = [
    { id: 1, name: "Маркетплейс бот", token: "123:ABC" },
    { id: 2, name: "Поддержка", token: "456:DEF" }
];

// Проверяем, открыто ли в Telegram
if (window.Telegram?.WebApp) {
    const tg = window.Telegram.WebApp;
    
    // Инициализация
    tg.expand();
    tg.enableClosingConfirmation();
    
    // Получаем данные пользователя
    const user = tg.initDataUnsafe.user;
    console.log('Telegram user:', user);
    
    // Используем для авторизации
    localStorage.setItem('tg_user', JSON.stringify(user));
    
    // Стили для WebApp
    document.documentElement.style.setProperty('--tg-viewport-height', tg.viewportHeight + 'px');
    
    // Обработка закрытия
    tg.onEvent('viewportChanged', () => {
        document.documentElement.style.setProperty('--tg-viewport-height', tg.viewportHeight + 'px');
    });
}

// Отображение списка ботов
function renderBots() {
    botList.innerHTML = '';
    mockBots.forEach(bot => {
        const botElement = document.createElement('div');
        botElement.className = 'bot-card';
        botElement.innerHTML = `
            <div>
                <h3>${bot.name}</h3>
                <small>ID: ${bot.id}</small>
            </div>
            <button class="btn small" onclick="editBot(${bot.id})">
                Редактировать
            </button>
        `;
        botList.appendChild(botElement);
    });
}

async function loadBots() {
    try {
        const bots = await fetchBots();
        renderBots(bots);
    } catch (error) {
        console.error('Ошибка загрузки ботов:', error);
        showError('Не удалось загрузить ботов');
    }
}

// Обработчики событий
createBotBtn.addEventListener('click', () => {
    alert('Функция создания бота будет здесь');
});

function editBot(botId) {
    alert(`Редактирование бота ${botId}`);
}

// Обновленный renderBots
function renderBots(bots) {
    botList.innerHTML = '';
    bots.forEach(bot => {
        // ... остальной код
    });
}

function setLoading(state) {
    if (state) {
        document.body.classList.add('loading');
    } else {
        document.body.classList.remove('loading');
    }
}

// Управление модальным окном
function openModal() {
    document.getElementById('botModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('botModal').style.display = 'none';
}

// Обработка формы
document.getElementById('botForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const botData = {
        bot_name: document.getElementById('botName').value,
        bot_token: document.getElementById('botToken').value
    };

    try {
        await createBot(botData);
        closeModal();
        loadBots();
    } catch (error) {
        console.error('Ошибка создания бота:', error);
        showError('Не удалось создать бота');
    }
});

function showError(message) {
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    document.body.appendChild(errorElement);
    setTimeout(() => errorElement.remove(), 3000);
}

// Обновляем обработчик кнопки
createBotBtn.addEventListener('click', openModal);

// Инициализация
tg.ready();
loadBots();