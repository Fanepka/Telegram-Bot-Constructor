import asyncio

from fastapi import FastAPI
from app.routers import auth, bots, commands, variables
from app.database import init_db
from app.services import bot_manager

app = FastAPI()

app.include_router(auth.router)
app.include_router(bots.router)
app.include_router(commands.router)
app.include_router(variables.router)

init_db()

@app.on_event("startup")
async def startup_event():
    """Запускаем всех ботов при старте сервера"""
    await bot_manager.start_all_bots()

@app.get("/")
def health_check():
    return {"status": "API работает!"}