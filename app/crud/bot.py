from sqlalchemy.orm import Session

from app.utils.telegram_validation import validate_telegram_token
from app.models.bot import Bot
from app.schemas.bot import BotCreate

def create_bot(db: Session, bot: BotCreate, user_id: int):
    db_bot = Bot(**bot.dict(), user_id=user_id)
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    return db_bot

def get_user_bots(db: Session, user_id: int):
    return db.query(Bot).filter(Bot.user_id == user_id).all()

def create_bot(db: Session, bot: BotCreate, user_id: int):
    validate_telegram_token(bot.bot_token)  # Валидация токена
    db_bot = Bot(**bot.dict(), user_id=user_id)
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    return db_bot