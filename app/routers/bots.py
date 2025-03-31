from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.bot import BotCreate, Bot as BotSchema
from app.models import Command
from app.models.bot import Bot
from app.crud.bot import create_bot
from app.models.user import User
from app.database import get_db
from app.utils.security import get_current_user
from app.services import bot_manager

router = APIRouter()

@router.post("/bots", response_model=BotSchema)
async def create_bot_handler(
    bot_data: BotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_bot = create_bot(db, bot_data, current_user.id)
    await bot_manager.start_bot(db_bot)
    return db_bot

@router.delete("/bots/{bot_id}")
async def delete_bot(
    bot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bot = db.query(Bot).filter(
        Bot.id == bot_id,
        Bot.user_id == current_user.id
    ).first()
    
    if not bot:
        raise HTTPException(status_code=404, detail="Бот не найден")
    
    await bot_manager.stop_bot(bot.id)
    db.delete(bot)
    db.commit()
    return {"status": "ok"}


@router.get("/debug/commands")
def debug_commands(db: Session = Depends(get_db)):
    commands = db.query(Command).all()
    return {
        "count": len(commands),
        "commands": [{"name": c.command_name, "response": c.response_text} for c in commands]
    }


