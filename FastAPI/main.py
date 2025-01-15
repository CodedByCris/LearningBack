from fastapi import FastAPI
from routers import products, users
from fastapi.staticfiles import StaticFiles

# Documentación de FastAPI https://fastapi.tiangolo.com/

# Instalamos FastAPI con el comando: pip install "fastapi[all]"

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
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