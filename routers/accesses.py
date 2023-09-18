from fastapi import (APIRouter, 
                     HTTPException, 
                     Depends, 
                     Query)

from models.db.utils import get_db

from models.schemas import (Access,
                            AccessPost)

from models.crud.accesses import (read_accesses, 
                                  do_access)

from sqlalchemy.orm import Session
from typing import Annotated
from uuid import UUID


API_ROUTER_CONFIG: dict = {
    'prefix': '/accesses',
    'tags': ['accesses']
}

GET_ACCESSES_METADATA: dict = {
    'summary': 'GET /accesses', 
    'description': 'This endpoint lets you get a list of accesses (if any).', 
    'response_model': list[Access]
}

POST_ACCESSES_METADATA: dict = {
    'summary': 'POST /accesses', 
    'description': 'This endpoint lets you get a make an access with the specified badge_id and badge_reader_id.', 
    'response_model': Access
}

router = APIRouter(**API_ROUTER_CONFIG)


@router.get('/', **GET_ACCESSES_METADATA)
async def get_users(in_timestamp: Annotated[str, Query(description='Filter for in_timestamp')] = '%', 
                    out_timestamp: Annotated[str, Query(description='Filter for out_timestamp')] = '%', 
                    db_session: Session = Depends(get_db)):
    
    accesses: list[Access] = []
    
    db_accesses = read_accesses(db_session, in_timestamp, out_timestamp)
    if not db_accesses:
        raise HTTPException(status_code=200, detail='No accesses found')
    else:                
        accesses = [Access(**db_access) for db_access in db_accesses]

    return accesses
  

@router.post('/', **POST_ACCESSES_METADATA)
async def post_user(access_post: AccessPost, db_session: Session = Depends(get_db)):

    # Get user input in a dict
    new_access: dict = access_post.model_dump()
    badge_id: UUID = new_access['badge_id']
    badge_reader_id: UUID = new_access['badge_reader_id']

    # Do the access depending of entering/exiting a specified area
    access = do_access(db_session, badge_id, badge_reader_id)
    
    # Convert the record to a valid schema object
    access = Access(**access)

    return access
