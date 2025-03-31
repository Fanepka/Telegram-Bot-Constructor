from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Text, Boolean
from app.database import Base

class Command(Base):
    __tablename__ = "commands"
    
    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey("bots.id"))
    command_name = Column(String(50))
    response_text = Column(Text)  # Увеличили размер
    parse_mode = Column(String(10), default="MarkdownV2")  # HTML/Markdown
    buttons = Column(JSON)  # [{text: "", url: ""}]
    is_active = Column(Boolean, default=True)