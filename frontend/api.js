// frontend/api.js
const API_URL = 'http://localhost:8000'; // Замените на ваш URL

export async function fetchBots() {
    const response = await fetch(`${API_URL}/bots`, {
        headers: {
            'Authorization': `Bearer ${window.Telegram.WebApp.initData}`
        }
    });
    return await response.json();
}

let authToken = window.Telegram?.WebApp?.initData || '';

export function setAuthToken(token) {
    authToken = token;
}

export async function createBot(botData) {
    const response = await fetch(`${API_URL}/bots`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${window.Telegram.WebApp.initData}`
        },
        body: JSON.stringify(botData)
    });
    return await response.json();
}

export async function fetchBotCommands(botId) {
    const response = await fetch(`${API_URL}/bots/${botId}/commands`, {
        headers: {
            'Authorization': `Bearer ${window.Telegram.WebApp.initData}`
        }
    });
    return await response.json();
}

export async function createCommand(botId, commandData) {
    const response = await fetch(`${API_URL}/bots/${botId}/commands`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${window.Telegram.WebApp.initData}`
        },
        body: JSON.stringify(commandData)
    });
    return await response.json();
}

export async function deleteCommand(botId, commandId) {
    const response = await fetch(`${API_URL}/bots/${botId}/commands/${commandId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${window.Telegram.WebApp.initData}`
        }
    });
    return await response.json();
}