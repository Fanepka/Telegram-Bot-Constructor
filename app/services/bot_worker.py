import re
import asyncio

from threading import Thread

from telegram import Bot, Update
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters
)
from app.crud.bot import get_bot_by_tg_id
from app.crud.variable import get_bot_variables
from app.database import get_db
from app.models.command import Command
from app.models.variable import Variable
from datetime import datetime


class BotWorker:

    STATES = {
        'AWAIT_NAME': 1,
        'AWAIT_AGE': 2
    }

    def __init__(self, token: str):
        self.token = token
        self.application = None
        self._running = False

    def _register_handlers(self):
        """Регистрация обработчиков команд из БД с логгированием"""
        db = next(get_db())
        commands = db.query(Command).all()
        
        print(f"Found {len(commands)} commands in DB")  # Логируем количество команд
        
        for cmd in commands:
            print(f"Registering command: /{cmd.command_name}")  # Логируем регистрацию
            handler = CommandHandler(cmd.command_name, self._make_handler(cmd))
            self.application.add_handler(handler) 
        
        # Добавляем fallback handler для логгирования неизвестных команд
        async def unknown_command(update, context):
            print(f"Received unknown command: {update.message.text}")
            await update.message.reply_text("Unknown command")
        
        self.application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    

    def _make_handler(self, cmd: Command):
        async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            # Поддержка Markdown
            await update.message.reply_text(
                text=str(self._process_variables(cmd.response_text, update)),
                #reply_markup=self._create_keyboard(cmd.buttons)
            )
        return handler

    
    def _create_markup(self, buttons: list):
        """Создает клавиатуру из кнопок"""
        from telegram import InlineKeyboardMarkup, InlineKeyboardButton
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(btn['text'], url=btn.get('url'), callback_data=btn.get('callback_data'))]
            for btn in buttons
        ])
    
    async def _photo_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик получения фото"""
        photo = update.message.photo[-1]  # Берем самое качественное фото
        file = await context.bot.get_file(photo.file_id)
        await update.message.reply_text(f"Получено фото размером {photo.file_size} байт")
    
    async def run_polling(self):
        if self._running:
            return

        print(f"Starting bot with token: {self.token[:5]}...")  # Логируем запуск
        
        try:
            self.application = Application.builder().token(self.token).build()
            self._register_handlers()
            
            # Явная инициализация
            await self.application.initialize()
            await self.application.updater.start_polling(
                drop_pending_updates=True,
                timeout=10,
                read_timeout=5
            )
            await self.application.start()
            
            print("Bot started successfully")
            self._running = True
            
        except Exception as e:
            print(f"Failed to start bot: {str(e)}")
            raise

    async def stop(self):
        """Останавливает бота"""
        if self._running and self.application:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            self._running = False

    def _process_variables(self, text: str, update: Update) -> str:
        """Заменяет переменные в тексте на значения"""
        
        variables = {
            'user_name': update.effective_user.full_name,
            'user_id': update.effective_user.id,
            'date': datetime.now().strftime("%d\.%m\.%Y"),
            'time': datetime.now().strftime("%H:%M")
        }
        
        # Добавляем кастомные переменные из БД
        db = next(get_db())
        
        for var in get_bot_variables(db, get_bot_by_tg_id(db, self.application.bot.id).id):
            variables[var.name] = var.value if not var.is_dynamic else self._get_dynamic_value(var.name, update)
        
        return re.sub(
            r'{(.*?)}',
            lambda m: str(variables.get(m.group(1), m.group(0))),
            text
        )
    
    
    def _get_dynamic_value(self, var_name: str, update: Update) -> str:
        """Обработка динамических переменных"""
        # Можно добавить логику для API-запросов и т.д.
        return f"<{var_name}>"  # Заглушка