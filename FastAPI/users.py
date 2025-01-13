from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Inicia el server: uvicorn users:app --reload

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

@app.get("/usersjson")
async def usersjson():
    return [{"name": "Cris", "surname": "arellano", "url": "https://github.com/CodedByCris", "age": 23},
            {"name": "Cris2", "surname": "arellano2", "url": "https://github.com/CodedByCris2", "age": 25},
            {"name": "Cris3", "surname": "arellano3", "url": "https://github.com/CodedByCris3", "age": 30}]
    
@app.get("/users")
async def users():
    return users_list

# Entre llaves se pone el nombre de la variable que se quiere obtener
# PATH para parámetros fijos
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)
 
# QUERY para parámetros que pueden no ser necesarios para la petición
@app.get("/user/")
async def user(id: int):
    return search_user(id)
    
@app.post("/user/")
async def user(user: User):
    if type(search_user(User.id)) == User:
        return {"error": "User already exists"}
    else:
        users_list.append(user)

#Put para todo el user y Patch para una parte
@app.put("/user/")
async def user(user: User):
    
    found = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == User.id:
            users_list[index] = user
            found = True
            
    if not found :
        return {"error": "User not found"}

    
def search_user(id: int):
    # Se obtiene el usuario con el id que se pasa por parametro
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "User not found"}
    
