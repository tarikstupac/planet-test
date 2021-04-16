from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {"data":{"name":"Index"}}
#place static routes (/user/inactive)  above dynamic routes (/user/{id}) 
