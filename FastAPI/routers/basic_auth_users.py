from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# OAuth2PasswordBearer gestiona la autenticación de los usuarios
# OAuth2PasswordRequestForm es el formulario que se utiliza para la autenticación

router = APIRouter()

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
    
    
def search_users(username: str):
    if username in users_db:
        return User(**users_db[username])
    
# Criterio de dependencia
async def current_user(token: str = Depends(oauth2)):
    user = search_users(token)
    # El headers indica el tipo de autenticación
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid authentication credentials", 
                            headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Inactive user")
    
@router.post("/login")
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

# La operación de autenticación depende de la función oauth2
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user