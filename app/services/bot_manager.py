import asyncio
from typing import Dict
from app.database import get_db
from app.models.bot import Bot
from app.services.bot_worker import BotWorker

class BotManager:
    def __init__(self):
        self.active_bots: Dict[int, BotWorker] = {}
        self._running_tasks = set()

    async def start_all_bots(self):
        """Запускает всех ботов из базы при старте"""
        db = next(get_db())
        bots = db.query(Bot).all()
        
        for bot in bots:
            await self.start_bot(bot)

    async def start_bot(self, bot):
        """Запускает одного бота"""
        if bot.id in self.active_bots:
            return
            
        worker = BotWorker(bot.bot_token)
        task = asyncio.create_task(self._run_worker(worker))
        self._running_tasks.add(task)
        task.add_done_callback(self._running_tasks.discard)
        
        self.active_bots[bot.id] = worker

    async def _run_worker(self, worker):
        """Обертка для запуска воркера с обработкой ошибок"""
        try:
            await worker.run_polling()
        except Exception as e:
            print(f"Bot failed: {e}")

    async def stop_bot(self, bot_id: int):
        """Останавливает бота"""
        if bot_id in self.active_bots:
            await self.active_bots[bot_id].stop()
            del self.active_bots[bot_id]