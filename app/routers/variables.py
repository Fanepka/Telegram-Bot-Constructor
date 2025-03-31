import re

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.variable import VariableCreate, Variable
from app.models.bot import Bot
from app.models.variable import Variable as VDB
from app.crud.variable import create_variable, get_bot_variables
from app.database import get_db
from app.utils.security import get_current_user

router = APIRouter()

@router.post("/bots/{bot_id}/variables", response_model=Variable)
async def add_variable(
    bot_id: int,
    variable: VariableCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    # Проверяем владельца бота
    bot = db.query(Bot).filter(Bot.id == bot_id, Bot.user_id == current_user.id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    return create_variable(db, variable, bot_id)

@router.get("/bots/{bot_id}/variables", response_model=list[Variable])
async def read_variables(
    bot_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    bot = db.query(Bot).filter(Bot.id == bot_id, Bot.user_id == current_user.id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    return get_bot_variables(db, bot_id)

@router.post("/debug/test")
async def test_variables(text: str, bot_id: int, db: Session = Depends(get_db)):

    variables = {}


    db = next(get_db())
    for var in db.query(VDB).filter(VDB.bot_id == bot_id).all():
        variables[var.name] = var.value
    
    return {"result": re.sub(
        r'{(.*?)}',
        lambda m: str(variables.get(m.group(1), m.group(0))),
        text
    ),
    "variables": variables}