from sqlalchemy.orm import Session

from app.utils.telegram_validation import validate_telegram_token
from app.models.bot import Bot
from app.schemas.bot import BotCreate

def create_bot(db: Session, bot: BotCreate, user_id: int):
    telegram_id = validate_telegram_token(bot.bot_token)  # Валидация токена
    db_bot = Bot(**bot.dict(), telegram_id=telegram_id, user_id=user_id)
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    return db_bot

def get_user_bots(db: Session, user_id: int):
    return db.query(Bot).filter(Bot.user_id == user_id).all()

def get_bot_by_tg_id(db: Session, tg_bot_id: int) -> Bot:
    return db.query(Bot).filter(Bot.telegram_id == tg_bot_id).first()