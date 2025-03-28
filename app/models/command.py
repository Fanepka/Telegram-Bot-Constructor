from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from app.database import Base

class Command(Base):
    __tablename__ = "commands"
    
    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey("bots.id"))
    command_name = Column(String(50), nullable=False)
    response_text = Column(String(2000), nullable=False)
    buttons = Column(JSON, nullable=True)  # Хранение кнопок в формате JSON