from fastapi import FastAPI
from routers import users

APP_CONFIG: dict = {}

app = FastAPI()

app.include_router(users.router)

@app.get('/')
async def get_root():
    return {'message': 'Application root'}



