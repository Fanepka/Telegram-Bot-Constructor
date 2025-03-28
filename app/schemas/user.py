from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    telegram_id: str
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    is_premium: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    telegram_id: Optional[str] = None