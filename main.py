from sqlalchemy.orm import Session

from db.utils import db_connect
from db.utils import now_with_timezone

from fastapi import FastAPI
from db.users.utils import read_users, read_user_by_id

from db.dtos import User

from uuid import UUID


# Connect to the database
engine = db_connect(create_metadata=False, echo=True)
if engine is not None:
            
    # Create the session
    with Session(bind=engine) as session:
        app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Root directory'}

@app.get('/users')
async def get_users(name_like: str = '%', surname_like: str = '%', email_like: str = '%'):
    
    users: list[User] = []
    
    db_users = read_users(session, name_like, surname_like, email_like)

    for db_user in db_users:
        users.append(User(**db_user))

    return users

@app.get('/users/{user_id}')
async def get_user_by_id(user_id: UUID):
      
    db_user = read_user_by_id(session=session, user_id=user_id)
    if isinstance(db_user, dict):
        return User(**db_user)
                