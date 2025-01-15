from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

ALGORITHM = "HS256"

app = FastAPI()

# Para JWT necesitas la encriptación con pip install "python-jose[cryptography]" 
# y el paquete de JWT con pip install "passlib[bcrypt]"

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    usename : str
    fullname : str
    email : str
    disabled : bool
    
class UserDB(User):
    password : str
    
users_db = {
    "Cris": {
        "username": "Cris",
        "full_name": "Cristian Arellano Agudo",
        "email": "cris@gmail.com",
        "disabled": False,
        "password": "123456"
        },
    "Cris2": {
        "username": "Cris2",
        "full_name": "Cristian Arellano Agudo",
        "email": "cris2@gmail.com",
        "disabled": True,
        "password": "654321"
        }
}    

def search_users_db(username: str):
    if username in users_db:
        # ** indica que se pueden pasar todos los argumentos
        return UserDB(**users_db[username])
    
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Incorrect username")
    
    user = search_users_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Incorrect password")
        
    return {"access_token": user.username, "token_type": "bearer"}