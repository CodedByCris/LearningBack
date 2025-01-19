from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/user",
                   tags=["user"],
                   responses={404: {"message": "Not found"}})
 
# Entidad user
class User(BaseModel):
    id : int
    name : str
    surname : str
    url : str
    age : int

users_list = [
        User(id=1, name="Cris", surname="arellano", url="https://github.com/CodedByCris", age=23),
        User(id=2, name="Cris2", surname="arellano2", url="https://github.com/CodedByCris2", age=25),
        User(id=3, name="Cris3", surname="arellano3", url="https://github.com/CodedByCris3", age=30)
        ]

@router.get("/json")
async def usersjson():
    return [{"name": "Cris", "surname": "arellano", "url": "https://github.com/CodedByCris", "age": 23},
            {"name": "Cris2", "surname": "arellano2", "url": "https://github.com/CodedByCris2", "age": 25},
            {"name": "Cris3", "surname": "arellano3", "url": "https://github.com/CodedByCris3", "age": 30}]
    
@router.get("/list")
async def users():
    return users_list

# Entre llaves se pone el nombre de la variable que se quiere obtener
# PATH para parámetros fijos
@router.get("/{id}")
async def user(id: int):
    return search_user(id)
 
# QUERY para parámetros que pueden no ser necesarios para la petición
@router.get("/")
async def user(id: int):
    return search_user(id)
    
@router.post("/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(User.id)) == User:
        # para los errores se utiliza Raise
        raise HTTPException(status_code=404, detail="User already exists")
    
    users_list.append(user)
    return user

#Put para todo el user y Patch para una parte
@router.put("/")
async def user(user: User):
    
    found = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == User.id:
            users_list[index] = user
            found = True
            
    if not found :
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.delete("/{id}")
async def delete_user(id: int):
    found = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            
    if not found:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}

# ...existing code...
    
def search_user(id: int):
    # Se obtiene el usuario con el id que se pasa por parametro
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        raise HTTPException(status_code=404, detail="User not found")
    
