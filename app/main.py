import asyncio

from telegram import WebAppData

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, bots, commands, variables
from app.database import init_db
from app.services import bot_manager

app = FastAPI()

app.include_router(auth.router)
app.include_router(bots.router)
app.include_router(commands.router)
app.include_router(variables.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

@app.on_event("startup")
async def startup_event():
    """Запускаем всех ботов при старте сервера"""
    await bot_manager.start_all_bots()

@app.get("/")
def health_check():
    return {"status": "API работает!"}

@app.post("/validate-webapp")
async def validate_webapp(request: Request):
    init_data = await request.json()
    try:
        data = WebAppData(**init_data)
        return {"status": "ok"}
    except:
        raise HTTPException(status_code=400, detail="Invalid init data")