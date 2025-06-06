from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
#! PostgreSQL
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Criss027_@localhost/TodoApplicationDatabase'

#! MYSQL
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:Criss027_@localhost/TodoApplicationDatabase'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

#! PostgreSQL and MYSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()