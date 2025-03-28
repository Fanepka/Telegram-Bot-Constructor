from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.command import CommandCreate, Command
from app.crud.command import create_command, get_bot_commands
from app.database import get_db
from app.utils.security import get_current_user
from app.models.bot import Bot

router = APIRouter()

@router.post("/bots/{bot_id}/commands", response_model=Command)
def add_command(
    bot_id: int,
    command: CommandCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    # Проверка что бот принадлежит пользователю
    bot = db.query(Bot).filter(Bot.id == bot_id, Bot.user_id == current_user.id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    return create_command(db, command, bot_id)

@router.get("/bots/{bot_id}/commands", response_model=list[Command])
def read_commands(
    bot_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    bot = db.query(Bot).filter(Bot.id == bot_id, Bot.user_id == current_user.id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    return get_bot_commands(db, bot_id)