from fastapi import (APIRouter, 
                     HTTPException, 
                     Depends, 
                     Path, 
                     Query)

from models.db.utils import get_db

from models.schemas import (User, 
                            UserPost, 
                            UserPatch)

from models.crud.users import (read_users, 
                               read_user_by_id, 
                               create_user, 
                               update_user,
                               remove_user)

from sqlalchemy.orm import Session
from typing import Annotated
from uuid import UUID, uuid4


API_ROUTER_CONFIG: dict = {
    'prefix': '/users',
    'tags': ['users']
}


# Create the router with given config
router = APIRouter(**API_ROUTER_CONFIG)


@router.get('/', response_model=list[User])
async def get_users(name_like: Annotated[str, Query(description='Filter for the user name')] = '%', 
                    surname_like: Annotated[str, Query(description='Filter for the user surname')] = '%', 
                    email_like: Annotated[str, Query(description='Filter for the user email')] = '%', 
                    db_session: Session = Depends(get_db)):
    
    users: list[User] = []
    
    db_users = read_users(db_session, name_like, surname_like, email_like)
    if not db_users:
        raise HTTPException(status_code=200, detail='No users found')
    else:                
        users = [User(**db_user) for db_user in db_users]

    return users


@router.get('/{user_id}', response_model=User)
async def get_user_by_id(user_id: Annotated[UUID, Path(description='User ID of the User to select')], db_session: Session = Depends(get_db)):
      
    db_user = read_user_by_id(db_session, user_id)
    if db_user:
        return User(**db_user)
    else:
        raise HTTPException(status_code=200, detail='No user found')
    

@router.post('/', response_model=User)
async def post_user(user_post: UserPost, db_session: Session = Depends(get_db)):

    # Obtaining user input
    new_user: dict = user_post.model_dump()
    
    # Adding the UUID to the user input dict
    new_user['id'] = uuid4()

    # Create the user
    user = create_user(db_session, new_user)
    
    # Make the user a schemas.User
    user = User(**user)

    return user

@router.patch('/{user_id}', response_model=User)
def patch_user(user_id: Annotated[UUID, Path(description='User ID of the User to update')], 
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
    

@router.delete('/{user_id}')
def delete_user(user_id: Annotated[UUID, Path(description='Used ID of the User to delete')],
                db_session: Session = Depends(get_db)):
    
    deleted_user_id: dict = remove_user(db_session, user_id)
    
    if deleted_user_id:
        return deleted_user_id
    else:        
        raise HTTPException(status_code=200, detail='No user found')