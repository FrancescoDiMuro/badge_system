from fastapi import (APIRouter, 
                     HTTPException, 
                     Depends, 
                     Path, 
                     Query)

from models.db.utils import get_db

from models.user.create import create_user
from models.user.retrieve import retrieve_users, retrieve_user_by_id
from models.user.update import update_user
from models.user.delete import remove_user
from models.user.utils import user_is_deleted

from schemas.user import User, UserPost, UserPatch

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


@router.get('/', **GET_USERS_METADATA)
async def get_users(name_like: Annotated[str, Query(description='Filter for the user name')] = '%', 
                    surname_like: Annotated[str, Query(description='Filter for the user surname')] = '%', 
                    email_like: Annotated[str, Query(description='Filter for the user email')] = '%',
                    include_deleted: bool = False, 
                    db_session: Session = Depends(get_db)):
    
    users: list[User] = retrieve_users(db_session, name_like, surname_like, email_like, include_deleted)
    if users:
        return users
    
    raise HTTPException(status_code=404, detail='No users found')

    
@router.get('/{user_id}', **GET_USERS_BY_ID_METADATA)
async def get_user_by_id(user_id: Annotated[UUID, Path(description='User ID of the user to select')], 
                         include_deleted: bool = False, 
                         db_session: Session = Depends(get_db)):
      
    user: User = retrieve_user_by_id(db_session, user_id, include_deleted)
    if user:
        return user
    
    raise HTTPException(status_code=404, detail='User not found')


@router.post('/', **POST_USERS_METADATA)
async def post_user(user_post: UserPost, db_session: Session = Depends(get_db)):
    
    # Get user input in a dict
    user_post: dict = user_post.model_dump()
    
    # Assign id to the new record
    user_post['id'] = uuid4()
    
    # Create the record
    user = create_user(db_session, user_post)

    return user


@router.patch('/{user_id}', **PATCH_USERS_METADATA)
def patch_user(user_id: Annotated[UUID, Path(description='User ID of the user to update')], 
               user_patch: UserPatch, 
               db_session: Session = Depends(get_db)):
    
    if user_is_deleted(db_session, user_id):
        raise HTTPException(status_code=404, detail='User not found')
    
    # Obtain user data that has been updated, excluding what hasn't been set
    # Setting invalid properties not contained in the Pydantic model will remove
    # them from the dictionary
    user_update: dict = user_patch.model_dump(exclude_unset=True)

    # If the user actually filled the dict with some valid info
    if user_update:
        user_patch: User = update_user(db_session, user_id, user_update)

        return user_patch
    
    else:
        raise HTTPException(status_code=422, detail='Invalid input')
    

@router.delete('/{user_id}', **DELETE_USERS_METADATA)
def delete_user(user_id: Annotated[UUID, Path(description='Used ID of the user to delete')],
                db_session: Session = Depends(get_db)):
    
    deleted_user_id: dict = remove_user(db_session, user_id)
    
    if deleted_user_id:
        return deleted_user_id
    else:        
        raise HTTPException(status_code=404, detail='User not found')
    