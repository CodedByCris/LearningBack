from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
 
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1

# openssl rand -hex 32 -> Genera una clave secreta
SECRET = "ONJISADAD973H3BD3827D2G3H8D327GD3287G"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

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
    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Incorrect username")
    
    user = search_users_db(form.username)
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Incorrect password")
        
    # Crear el tiempo de expiración    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    
    access_token = {"sub": user.username, "exp": expire}
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

# Criterio de dependencia
async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Invalid authentication credentials", 
                                headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except JWTError:
        raise exception
    
    return search_users(username)
            
        
async def current_user(user: User = Depends(auth_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid authentication credentials", 
                            headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Inactive user")

@router.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user