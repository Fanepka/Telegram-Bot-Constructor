from sqlalchemy.orm import Session
from app.models.command import Command
from app.schemas.command import CommandCreate

def create_command(db: Session, command: CommandCreate, bot_id: int):
    db_command = Command(**command.dict(), bot_id=bot_id)
    db.add(db_command)
    db.commit()
    db.refresh(db_command)
    return db_command

def get_bot_commands(db: Session, bot_id: int):
    return db.query(Command).filter(Command.bot_id == bot_id).all()