from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine( #engine establishes the connection between FastAPI/SQLAlchemy and the Database.
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False) 
"""A Sessionmaker is a factory for creating new Session objects, which are used to interact with the database. 
The bind parameter specifies the engine to use for the session, and autoflush and autocommit control how changes are flushed to the database and whether transactions are automatically committed."""

class Base(DeclarativeBase):
    pass

def get_db(): #db is a generator function that yields a database session. 
    db = SessionLocal() #SessionLocal() is a callable object -> __call__(): - special memthod that allows an instance of a class to be called as a function.
    try:
        yield db
    finally:
        db.close()
    
    #engine(connection) -> sessionmaker(session factory) -> session(session object) -> db queries/transactions