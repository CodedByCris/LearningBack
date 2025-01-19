from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

# Documentación de FastAPI https://fastapi.tiangolo.com/

# Instalamos FastAPI con el comando: pip install "fastapi[all]"

# Para JWT necesitas la encriptación con pip install "python-jose[cryptography]" 
# y el paquete de JWT con pip install "passlib[bcrypt]"

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

# URL local -> http://127.0.0.1:8000
@app.get("/")
async def root():
    return {"¡Hola FastAPI!"}

# URL local -> http://127.0.0.1:8000/url
@app.get("/url")
async def url():
    return {"url": "https://github.com/CodedByCris"}

# Inicia el server: uvicorn main:app --reload
# Detener el server: Ctrl + C

# Documentación de Swagger -> http://127.0.0.1:8000/docs
# Documentación de ReDoc -> http://127.0.0.1:8000/redoc