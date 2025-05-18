from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, text
from ..database import Base
from ..main import app
from ..models import Todos, Users
from ..routers.auth import bcrypt_context

SQLACHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLACHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=NullPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def override_get_current_user():
    return {"username":"test_user", "id": 1, "role": "admin",}

client = TestClient(app)

#Crea un usuario de prueba y al acabar lo elimina
@pytest.fixture()
def test_todo():
    todo = Todos(title="Test Todo", description="Test Description", priority=1, completed=False, owner_id=1)
    
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todos;"))
        conn.commit()
        
        
@pytest.fixture()
def test_user():
    user = Users(username="test_user", 
                 email="test@gmail.com", 
                 first_name="Test", 
                 last_name="User", 
                 hashed_password=bcrypt_context.hash("testpassword"), 
                 role="admin", 
                 phone_number="123456789")
    db = TestingSessionLocal()  
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM users;"))
        conn.commit()