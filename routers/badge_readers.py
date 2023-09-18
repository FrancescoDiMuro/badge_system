from fastapi import (APIRouter, 
                     HTTPException, 
                     Depends, 
                     Path, 
                     Query)

from models.db.utils import get_db

from models.schemas import (BadgeReader, 
                            BadgeReaderPost, 
                            BadgeReaderPatch)

from models.crud.badge_readers import (read_badge_readers, 
                               read_badge_reader_by_id, 
                               create_badge_reader, 
                               update_badge_reader,
                               remove_badge_reader)

from sqlalchemy.orm import Session
from typing import Annotated
from uuid import UUID, uuid4


API_ROUTER_CONFIG: dict = {
    'prefix': '/badge_readers',
    'tags': ['badge_readers']
}

GET_BADGE_READERS_METADATA: dict = {
    'summary': 'GET /badge_readers', 
    'description': 'This endpoint lets you get a list of configured badge readers (if any).', 
    'response_model': list[BadgeReader]
}

GET_BADGE_READERS_BY_ID_METADATA: dict = {
    'summary': 'GET /badge_readers/{badge_reader_id}', 
    'description': 'This endpoint lets you get a badge reader selecting it by its id (if any).', 
    'response_model': BadgeReader
}

POST_BADGE_READERS_METADATA: dict = {
    'summary': 'POST /badge_readers', 
    'description': 'This endpoint lets you create a new badge reader.', 
    'response_model': BadgeReader
}

PATCH_BADGE_READER_METADATA: dict = {
    'summary': 'PATCH /badge_readers/{badge_reader_id}', 
    'description': 'This endpoint lets you update the information of an existing badge reader, specifying its id.', 
    'response_model': BadgeReader
}

DELETE_BADGE_READERS_METADATA: dict = {
    'summary': 'DELETE /badge_readers/{badge_reader_id}', 
    'description': 'This endpoint lets you delete a badge reader, specifying its id.', 
    'response_model': None
}


router = APIRouter(**API_ROUTER_CONFIG)


@router.get('/', **GET_BADGE_READERS_METADATA)
async def get_badge_readers(ip_address_like: Annotated[str, Query(description='Filter for the badge reader IP address')] = '%', 
                            location_like: Annotated[str, Query(description='Filter for the badge reader location')] = '%',                              
                            db_session: Session = Depends(get_db)):
    
    badge_readers: list[BadgeReader] = []
    
    db_badge_readers = read_badge_readers(db_session, ip_address_like, location_like)
    if not db_badge_readers:
        raise HTTPException(status_code=200, detail='No badge readers found')
    else:
        badge_readers = [db_badge_reader for db_badge_reader in db_badge_readers]

    return badge_readers


@router.get('/{badge_reader_id}', **GET_BADGE_READERS_BY_ID_METADATA)
async def get_badge_reader_by_id(badge_reader_id: Annotated[UUID, Path(description='BadgeReader ID of the BadgeReader to select')], 
                                 db_session: Session = Depends(get_db)):
      
    db_badge_reader = read_badge_reader_by_id(db_session, badge_reader_id)
    if db_badge_reader:
        return BadgeReader(**db_badge_reader)
    else:
        raise HTTPException(status_code=200, detail='No badge reader found')
    

@router.post('/', **POST_BADGE_READERS_METADATA)
async def post_badge_reader(badge_reader_post: BadgeReaderPost, db_session: Session = Depends(get_db)):

    # Get user input in a dict
    new_badge_reader: dict = badge_reader_post.model_dump()
    
    # Assign id to the new record
    new_badge_reader['id'] = uuid4()

    # Create the record
    badge_reader = create_badge_reader(db_session, new_badge_reader)
    
    # Convert the record to a valid schema object
    badge_reader = BadgeReader(**badge_reader)

    return badge_reader


@router.patch('/{badge_reader_id}', **PATCH_BADGE_READER_METADATA)
def patch_badge_reader(badge_reader_id: Annotated[UUID, Path(description='Badge reader ID of the badge reader to update')], 
                       badge_reader: BadgeReaderPatch, 
                       db_session: Session = Depends(get_db)):
    
    # Obtain badge reader data that has been updated, excluding what hasn't been set
    updated_badge_reader_info: dict = badge_reader.model_dump(exclude_unset=True)

    # If the user actually filled the dict with some valid info
    if updated_badge_reader_info:
        updated_badge_reader: BadgeReader = BadgeReader(**update_badge_reader(db_session, badge_reader_id, updated_badge_reader_info))

        return updated_badge_reader
    
    else:
        raise HTTPException(status_code=422, detail='Invalid input')
    

@router.delete('/{badge_reader_id}', **DELETE_BADGE_READERS_METADATA)
def delete_badge_reader(badge_reader_id: Annotated[UUID, Path(description='Badge reader ID of the badge reader to delete')],
                        db_session: Session = Depends(get_db)):
    
    deleted_badge_id: dict = remove_badge_reader(db_session, badge_reader_id)
    
    if deleted_badge_id:
        return deleted_badge_id
    else:        
        raise HTTPException(status_code=200, detail='No badge reader found')