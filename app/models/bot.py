from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.database import Base

class Bot(Base):
    __tablename__ = "bots"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    bot_token = Column(String(100), unique=True)
    bot_name = Column(String(50))
    is_active = Column(Boolean, default=False)