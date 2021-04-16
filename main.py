from fastapi import FastAPI
from routers import users, tiles
from database import SessionLocal, engine
from models import base


base.Base.metadata.create_all(bind = engine)
app = FastAPI()

@app.get('/')
def index():
    return {"Access /docs or /redoc to view API documentation!"}
#place static routes (/user/inactive)  above dynamic routes (/user/{id}) 

app.include_router(users.router)
app.include_router(tiles.router)