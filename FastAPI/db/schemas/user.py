# Los schemas son clases que se utilizan para definir la estructura de los datos que se envían y reciben en una API.

def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user.username,
        "email": user.email,
    }
    
def users_schema(users) -> list:
    return [user_schema(user) for user in users]