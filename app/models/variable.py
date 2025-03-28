from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.database import Base

class Variable(Base):
    __tablename__ = "variables"
    
    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey("bots.id"))
    name = Column(String(50), nullable=False)  # Например: "user_name"
    value = Column(String(500))                # Статическое значение
    is_dynamic = Column(Boolean, default=False)  # Динамическая переменная
