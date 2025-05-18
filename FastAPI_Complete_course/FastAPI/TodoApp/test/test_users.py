from .utils import *
from fastapi import status
from TodoApp.routers.users import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == test_user.username
    assert response.json()["email"] == test_user.email
    assert response.json()["first_name"] == test_user.first_name
    assert response.json()["last_name"] == test_user.last_name
    assert response.json()["role"] == test_user.role
    assert response.json()["phone_number"] == test_user.phone_number
    
def test_change_password_success(test_user):
    response = client.put("/user/password", json={"password": "testpassword", "new_password": "newpassword"})

    assert response.status_code == status.HTTP_204_NO_CONTENT
    
def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/password", json={"password": "wrongpassword", "new_password": "newpassword"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}
    
def test_change_phone_number_success(test_user):
    response = client.put("/user/phone_number/123456789")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
