from sqlalchemy.orm import Session
from app.schemas.variable import VariableCreate
from app.models.variable import Variable

def create_variable(db: Session, variable: VariableCreate, bot_id: int):
    db_variable = Variable(**variable.dict(), bot_id=bot_id)
    db.add(db_variable)
    db.commit()
    db.refresh(db_variable)
    return db_variable

def get_bot_variables(db: Session, bot_id: int):
    return db.query(Variable).filter(Variable.bot_id == bot_id).all()