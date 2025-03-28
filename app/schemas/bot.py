from pydantic import BaseModel

class BotBase(BaseModel):
    bot_token: str
    bot_name: str

class BotCreate(BotBase):
    pass

class Bot(BotBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True