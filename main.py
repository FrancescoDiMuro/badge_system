from fastapi import FastAPI
from routers import users, badge_readers

APP_CONFIG: dict = {}

app = FastAPI()

app.include_router(users.router)
app.include_router(badge_readers.router)

@app.get('/')
async def get_root():
    return {'message': 'Application root'}



