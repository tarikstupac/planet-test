from fastapi import FastAPI, Depends
from routers import users, tiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine, get_db
from models import base
from helpers import db_init

#create db tables
base.Base.metadata.create_all(bind = engine)
#db_init.seed_test_data()

app = FastAPI()

@app.get('/')
def index():
    return {"Access /docs or /redoc to view API documentation!"}
#place static routes (/user/inactive)  above dynamic routes (/user/{id}) 

app.include_router(users.router)
app.include_router(tiles.router)