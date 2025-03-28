from pydantic import BaseModel
from typing import Optional

class VariableBase(BaseModel):
    name: str
    value: Optional[str] = None
    is_dynamic: bool = False

class VariableCreate(VariableBase):
    pass

class Variable(VariableBase):
    id: int
    bot_id: int

    class Config:
        from_attributes = True