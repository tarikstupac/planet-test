from fastapi import FastAPI, Depends
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware
from routers import users, tiles, oauth2
from sqlalchemy.orm import Session
from database import SessionLocal, engine, get_db
from models import base
from helpers import db_init

#create db tables
base.Base.metadata.create_all(bind = engine)
db_init.seed_test_data()

app = FastAPI(
    title="PlanetIX API",
    description="The API for the PlanetIX project, built with Fast API.",
    version="1.0"
)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/')
def index():
    return {"Access /docs or /redoc to view API documentation!"}
#place static routes (/user/inactive)  above dynamic routes (/user/{id}) 

app.include_router(users.router)
app.include_router(tiles.router)
app.include_router(oauth2.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("PORT", 5000))