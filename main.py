from fastapi import FastAPI
from routers import users

app = FastAPI()

@app.get('/')
def index():
    return {"data":{"name":"Index"}}
#place static routes (/user/inactive)  above dynamic routes (/user/{id}) 

app.include_router(users.router)