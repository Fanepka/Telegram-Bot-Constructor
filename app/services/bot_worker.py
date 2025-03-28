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
        """Регистрация обработчиков команд из БД"""
        db = next(get_db())
        commands = db.query(Command).all()
        
        for cmd in commands:
            self.application.add_handler(
                CommandHandler(cmd.command_name, self._make_handler(cmd.response_text))
            )


    async def _start_survey(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начало опроса"""
        await update.message.reply_text("Введите ваше имя:")
        return self.STATES['AWAIT_NAME']
    
    async def _process_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка имени"""
        context.user_data['name'] = update.message.text
        await update.message.reply_text("Теперь введите ваш возраст:")
        return self.STATES['AWAIT_AGE']
    
    def _register_conversation(self):
        """Регистрация диалога"""
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('survey', self._start_survey)],
            states={
                self.STATES['AWAIT_NAME']: [MessageHandler(filters.TEXT, self._process_name)],
                self.STATES['AWAIT_AGE']: [MessageHandler(filters.TEXT, self._process_age)]
            },
            fallbacks=[CommandHandler('cancel', self._cancel_survey)]
        )
        self.application.add_handler(conv_handler)

    async def _start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик /start с клавиатурой"""
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Пример кнопки", callback_data="sample_button")]
        ])
        await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)
        
    def _load_commands_from_db(self):
        db = next(get_db())
        commands = db.query(Command).all()
        self.application.add_handler(CommandHandler("test", self._start_handler))
        
        for cmd in commands:
            handler = CommandHandler(
                cmd.command_name,
                self._make_db_handler(cmd.response_text)
            )
            self.application.add_handler(handler)

    def _make_db_handler(self, response_text: str):
        async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text(response_text)
        return handler
    
    async def _button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на inline-кнопки"""
        await update.callback_query.answer()
        await update.callback_query.edit_message_text("Вы нажали кнопку!")
    
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
        """Запускает бота в текущем event loop"""
        if self._running:
            return

        self.application = Application.builder().token(self.token).build()
        self._register_handlers()
        self._running = True
        
        # Отключаем обработку сигналов для polling
        await self.application.initialize()
        await self.application.updater.start_polling(drop_pending_updates=True)
        await self.application.start()

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
            'date': datetime.now().strftime("%d.%m.%Y"),
            'time': datetime.now().strftime("%H:%M")
        }
        
        # Добавляем кастомные переменные из БД
        db = next(get_db())
        for var in db.query(Variable).filter(Variable.bot_id == self.bot.id).all():
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