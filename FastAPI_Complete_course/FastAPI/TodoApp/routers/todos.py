from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session 
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from ..models import Todos
from ..database import SessionLocal
from .auth import get_current_user



router = APIRouter(    
    prefix="/todos",
    tags=["todos"])

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

class TodoRequest(BaseModel):
    title: str = Field(min_length = 3)
    description: str = Field(min_length = 3, max_length = 100)
    priority: int = Field(gt=0, lt=6)
    completed: bool
        
@router.get("/")
async def read_all(user: user_dependency, db: db_dependency, status_code=status.HTTP_200_OK):
    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency,todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return todo_model


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo: TodoRequest):
    
    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    todo_model = Todos(**todo.model_dump(), owner_id=user.get("id"))
    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    # \ Se usa para dividir la línea en varias líneas
    todo_model = db.query(Todos).filter(Todos.id == todo_id).\
        filter(Todos.owner_id == user.get("id")).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    for key, value in todo_request.model_dump().items():
        setattr(todo_model, key, value)
    
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo_model)
    db.commit()