from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session 
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Todos
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(    
    prefix="/admin",
    tags=["admin"])

# Inicializa la base de datos antes de la llamada y la cierra después de la llamada
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#La función depende de que se abra la base de datos y se cierre después de la llamada
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency, status_code=status.HTTP_200_OK):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    return db.query(Todos).all()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo_model)
    db.commit()