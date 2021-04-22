from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware
from routers import users, tiles, oauth2, countries


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
    response = RedirectResponse("/docs")
    return response

app.include_router(users.router)
app.include_router(tiles.router)
app.include_router(oauth2.router)
app.include_router(countries.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("PORT", 5000))