from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = "1eda56e2b116bf90db4528c73977b88491463e4e81c54872b7df34ea87655db8"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str 
    password: str
    role: str
    phone_number: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
# Inicializa la base de datos antes de la llamada y la cierra después de la llamada
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#La función depende de que se abra la base de datos y se cierre después de la llamada
db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(db, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password): # Verifica la contraseña, convierte la contraseña en hash y la compara con la contraseña ya hasheada en la base de datos
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {"sub": username,"id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: int = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return {"username": username, "id": user_id, "role": user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    
    create_user_request = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password), # Hash the password 
        is_active=True,
        phone_number=create_user_request.phone_number
    )
    
    db.add(create_user_request)
    db.commit()
    
    
@router.post("/token", response_model=Token) # OAuth2PasswordRequestForm obliga al cliente a enviar el username y password en el body
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    token = create_access_token(
        user.username,
        user.id,
        user.role,
        expires_delta=timedelta(minutes=20) # El token expira en 20 minutos
    )
    return {"access_token": token, "token_type": "bearer"}