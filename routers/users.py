from fastapi import (APIRouter, 
                     HTTPException, 
                     Depends, 
                     Path, 
                     Query)

from models.db.utils import get_db

from schemas.user import User, UserPost, UserPatch

from models.user.retrieve import read_users, read_user_by_id

from models.crud.users import (create_user, 
                               update_user,
                               remove_user)

from sqlalchemy.orm import Session
from typing import Annotated
from uuid import UUID, uuid4


API_ROUTER_CONFIG: dict = {
    'prefix': '/users',
    'tags': ['users']
}

GET_USERS_METADATA: dict = {
    'summary': 'GET /users', 
    'description': 'This endpoint lets you get a list of configured users (if any).', 
    'response_model': list[User]
}

GET_USERS_BY_ID_METADATA: dict = {
    'summary': 'GET /users/{user_id}', 
    'description': 'This endpoint lets you get a user selecting it by its id (if any).', 
    'response_model': User
}

POST_USERS_METADATA: dict = {
    'summary': 'POST /users', 
    'description': 'This endpoint lets you create a new user.', 
    'response_model': User
}

PATCH_USERS_METADATA: dict = {
    'summary': 'PATCH /users/{user_id}', 
    'description': 'This endpoint lets you update the information of an existing user, specifying its id.', 
    'response_model': User
}

DELETE_USERS_METADATA: dict = {
    'summary': 'DELETE /users/{user_id}', 
    'description': 'This endpoint lets you delete a user, specifying its id.', 
    'response_model': None
}



router = APIRouter(**API_ROUTER_CONFIG)


# @router.get('/', **GET_USERS_METADATA)
# async def get_users(name_like: Annotated[str, Query(description='Filter for the user name')] = '%', 
#                     surname_like: Annotated[str, Query(description='Filter for the user surname')] = '%', 
#                     email_like: Annotated[str, Query(description='Filter for the user email')] = '%',
#                     include_deleted: bool = False, 
#                     db_session: Session = Depends(get_db)):
    
#     users: list[User] = []
    
#     db_users = read_users(db_session, name_like, surname_like, email_like, include_deleted)
#     if not db_users:
#         raise HTTPException(status_code=200, detail='No users found')
#     else:                
#         users = [User(**db_user) for db_user in db_users]

#     return users

@router.get('/', **GET_USERS_METADATA)
async def get_users(name_like: Annotated[str, Query(description='Filter for the user name')] = '%', 
                    surname_like: Annotated[str, Query(description='Filter for the user surname')] = '%', 
                    email_like: Annotated[str, Query(description='Filter for the user email')] = '%',
                    include_deleted: bool = False, 
                    db_session: Session = Depends(get_db)):
    
    users: list[User] = []
    
    users = read_users(db_session, name_like, surname_like, email_like, include_deleted)
    if users:
        return users
    
    raise HTTPException(status_code=404, detail='No users found')


# @router.get('/{user_id}', **GET_USERS_BY_ID_METADATA)
# async def get_user_by_id(user_id: Annotated[UUID, Path(description='User ID of the user to select')], 
#                          include_deleted: bool = False, 
#                          db_session: Session = Depends(get_db)):
      
#     db_user = read_user_by_id(db_session, user_id, include_deleted)
#     if db_user:
#         return User(**db_user)
#     else:
#         raise HTTPException(status_code=200, detail='No user found')
    
@router.get('/{user_id}', **GET_USERS_BY_ID_METADATA)
async def get_user_by_id(user_id: Annotated[UUID, Path(description='User ID of the user to select')], 
                         include_deleted: bool = False, 
                         db_session: Session = Depends(get_db)):
      
    user = read_user_by_id(db_session, user_id, include_deleted)
    if user is not None:
        return user
    
    raise HTTPException(status_code=404, detail='No user found')


@router.post('/', **POST_USERS_METADATA)
async def post_user(user_post: UserPost, db_session: Session = Depends(get_db)):
    
    # Get user input in a dict
    new_user: dict = user_post.model_dump()
    
    # Assign id to the new record
    new_user['id'] = uuid4()
    
    # Create the record
    user = create_user(db_session, new_user)
    
    # Convert the record to a valid schema object
    user = User(**user)

    return user


@router.patch('/{user_id}', **PATCH_USERS_METADATA)
def patch_user(user_id: Annotated[UUID, Path(description='User ID of the user to update')], 
               user: UserPatch, 
               db_session: Session = Depends(get_db)):
    
    # Obtain user data that has been updated, excluding what hasn't been set
    updated_user_info: dict = user.model_dump(exclude_unset=True)

    # If the user actually filled the dict with some valid info
    if updated_user_info:
        updated_user: User = User(**update_user(db_session, user_id, updated_user_info))

        return updated_user
    
    else:
        raise HTTPException(status_code=422, detail='Invalid input')
    

@router.delete('/{user_id}', **DELETE_USERS_METADATA)
def delete_user(user_id: Annotated[UUID, Path(description='Used ID of the user to delete')],
                db_session: Session = Depends(get_db)):
    
    deleted_user_id: dict = remove_user(db_session, user_id)
    
    if deleted_user_id:
        return deleted_user_id
    else:        
        raise HTTPException(status_code=200, detail='No user found')