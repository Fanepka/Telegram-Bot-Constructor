from app.plugins.base import BasePlugin
from telegram.ext import CommandHandler, Application, ContextTypes
from telegram import Update

class WeatherPlugin(BasePlugin):
    def register_handlers(self, app: Application):
        app.add_handler(CommandHandler("weather", self._weather_handler))
    
    async def _weather_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Погодный плагин в разработке!")