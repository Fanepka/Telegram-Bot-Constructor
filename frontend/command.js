// Инициализация Telegram WebApp
const tg = window.Telegram.WebApp;
tg.expand();

// Получаем ID бота из URL
const urlParams = new URLSearchParams(window.location.search);
const botId = urlParams.get('bot_id');

// DOM элементы
const botTitle = document.getElementById('botTitle');
const commandList = document.getElementById('commandList');
const addCommandBtn = document.getElementById('addCommandBtn');
const backBtn = document.getElementById('backBtn');

// Моковые данные (замените на API)
const mockCommands = [
    { id: 1, name: "start", response: "Добро пожаловать в бота!" },
    { id: 2, name: "help", response: "Список команд:\n/start - Начало работы\n/help - Помощь" }
];

// Загрузка данных бота
async function loadBotData() {
    try {
        const response = await fetch(`http://localhost:8000/bots/${botId}`);
        const bot = await response.json();
        botTitle.textContent = `Команды: ${bot.bot_name}`;
    } catch (error) {
        console.error('Ошибка загрузки данных бота:', error);
    }
}

// Отображение списка команд
function renderCommands(commands) {
    commandList.innerHTML = '';
    commands.forEach(cmd => {
        const cmdElement = document.createElement('div');
        cmdElement.className = 'command-card';
        cmdElement.innerHTML = `
            <h3>/${cmd.name}</h3>
            <p>${cmd.response}</p>
            <div class="command-actions">
                <button class="btn small" onclick="editCommand(${cmd.id})">
                    Редактировать
                </button>
                <button class="btn small danger" onclick="deleteCommand(${cmd.id})">
                    Удалить
                </button>
            </div>
        `;
        commandList.appendChild(cmdElement);
    });
}

// Управление модальным окном
function openModal() {
    document.getElementById('commandModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('commandModal').style.display = 'none';
    document.getElementById('commandForm').reset();
}

// Обработчики событий
backBtn.addEventListener('click', () => {
    window.location.href = 'index.html';
});

addCommandBtn.addEventListener('click', openModal);

document.getElementById('commandForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const commandData = {
        command_name: document.getElementById('commandName').value,
        response_text: document.getElementById('commandResponse').value
    };

    try {
        await createCommand(botId, commandData);
        closeModal();
        loadCommands();
    } catch (error) {
        console.error('Ошибка создания команды:', error);
        showError('Не удалось создать команду');
    }
});

// Загрузка команд
async function loadCommands() {
    try {
        const commands = await fetchBotCommands(botId);
        renderCommands(commands);
    } catch (error) {
        console.error('Ошибка загрузки команд:', error);
        showError('Не удалось загрузить команды');
    }
}

async function handleDeleteCommand(commandId) {
    try {
        await deleteCommand(botId, commandId);
        loadCommands();
    } catch (error) {
        console.error('Ошибка удаления команды:', error);
        showError('Не удалось удалить команду');
    }
}

// Инициализация
tg.ready();
loadBotData();
loadCommands();