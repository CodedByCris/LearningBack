from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

@router.get("/", response_model= list[User])
async def users():
    return users_schema(db_client.users.find())

# Entre llaves se pone el nombre de la variable que se quiere obtener
# PATH para parámetros fijos
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))
 
# QUERY para parámetros que pueden no ser necesarios para la petición
@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))
    
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User already exists")
    
    # Convertimos el objeto User a un diccionario
    user_dict = dict(user)
    
    # Eliminamos el atributo id del diccionario para que MongoDB lo genere automáticamente
    del user_dict["id"]
    
    # Insertamos el diccionario en la colección users de la base de datos local y obtenemos el id generado
    id = db_client.users.insert_one(user_dict).inserted_id
    
    # Obtenemos el usuario insertado en la base de datos con el nuevo id
    new_user = user_schema(db_client.users.find_one({"_id":id}))
    
    # Añadimos el usuario a la lista de usuarios
    return User(**new_user)

@router.put("/", response_model=User)
async def user(user: User):
    user_dict = dict(user)
    del user_dict["id"]
    
    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")        
    
    return search_user("_id", ObjectId(user.id))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    found = db_client.users.find_one_and_delete({"_id":ObjectId(id)})
    
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return {"message": "User deleted successfully"}

    
def search_user(field: str, key):
    try:
        user = user_schema(db_client.users.find_one({field: key}))
        return User(**user_schema(user))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
