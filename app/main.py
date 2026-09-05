from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth

Base.metadata.create_all(bind=engine)
"""This line creates the database tables based on the defined models in the Base class. 
It uses the engine to connect to the database and create the necessary tables if they do not already exist.
""" 

app = FastAPI(title="Auth API")
app.include_router(auth.router) #It includes the authentication router from the auth module, allowing the defined authentication endpoints to be accessible through the FastAPI application.

@app.get('/')
def root():
    return {'message': 'Auth API Active'}