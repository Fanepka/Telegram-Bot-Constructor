from pydantic import BaseModel
from typing import Optional, List, Dict

class Button(BaseModel):
    text: str
    url: Optional[str] = None
    callback_data: Optional[str] = None

class CommandBase(BaseModel):
    command_name: str
    response_text: str
    buttons: Optional[List[Button]] = None

class CommandCreate(CommandBase):
    pass

class Command(CommandBase):
    id: int
    bot_id: int

    class Config:
        from_attributes = True