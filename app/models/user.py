from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String(50), unique=True, index=True)
    email = Column(String(100), nullable=True)
    is_premium = Column(Boolean, default=False)
    hashed_password = Column(String(255))