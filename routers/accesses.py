from fastapi import APIRouter, HTTPException, Depends, Query
from db.utils import get_db
from models.access.create import do_access
from models.access.retrieve import read_accesses
from schemas.access import Access, AccessPost
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
async def get_users(in_timestamp_min: Annotated[str, Query(description='Filter for in_timestamp_min')] = '', 
                    in_timestamp_max: Annotated[str, Query(description='Filter for in_timestamp_min')] = '', 
                    db_session: Session = Depends(get_db)):
    
    
    accesses: list[Access] = read_accesses(db_session, in_timestamp_min, in_timestamp_max)
    if not accesses:
        raise HTTPException(status_code=404, detail='No access found')
    
    return accesses
  

@router.post('/', **POST_ACCESSES_METADATA)
async def post_user(access_post: AccessPost, db_session: Session = Depends(get_db)):

    # Get user input in a dict
    new_access: dict = access_post.model_dump()
    badge_id: UUID = new_access['badge_id']
    badge_reader_id: UUID = new_access['badge_reader_id']

    # Do the access depending of entering/exiting a specified area
    access = do_access(db_session, badge_id, badge_reader_id)

    if access:
        return access
    else:
        raise HTTPException(status_code=401, detail='User not authorized')
