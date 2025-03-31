
# Telegram Bot Constructor (WebApp + FastAPI)

Проект для создания и управления Telegram ботами через Web-интерфейс.

## 📌 Текущая реализация (v0.1)

### ✅ Реализовано:
1. **Backend API (FastAPI)**
   - Аутентификация через Telegram (JWT)
   - CRUD для ботов:
     - Создание/удаление ботов
     - Привязка ботов к пользователям
   - Система команд:
     - Хранение команд в MySQL
     - Динамическая регистрация обработчиков
   - Переменные в ответах:
     - Поддержка `{user_name}`, `{date}` и др.

2. **База данных**
   - MySQL с SQLAlchemy ORM
   - Модели:
     - Пользователи (`users`)
     - Боты (`bots`)
     - Команды (`commands`)
     - Переменные (`variables`)

3. **Инфраструктура**
   - Docker-контейнеризация
   - Автоматический запуск ботов при старте
   - Логирование основных событий

4. **Базовый функционал бота**
   - Long Polling режим
   - Обработка текстовых команд
   - Система состояний (FSM)

## 🚧 Планы по развитию

### В разработке:
1. **WebApp интерфейс**
   - Панель управления ботами
   - Визуальный редактор команд
   - Просмотр статистики

2. **Расширенные функции ботов**
   - [ ] Вебхуки вместо Long Polling
   - [ ] Поддержка инлайн-режима
   - [ ] Платежная интеграция (Telegram Payments)

3. **Дополнительные модули**
   - [ ] Расписание сообщений
   - [ ] Интеграция с внешними API
   - [ ] Шаблоны сообщений
   - [ ] Мультиязычность

4. **Оптимизации**
   - [ ] Redis для кэширования
   - [ ] Celery для фоновых задач
   - [ ] Миграции через Alembic

## 🛠 Установка и запуск

1. Склонируйте репозиторий:
```bash
git clone https://github.com/Fanepka/telegram-bot-constructor.git
cd telegram-bot-constructor
```
