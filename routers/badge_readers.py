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


# Create the router with given config
router = APIRouter(**API_ROUTER_CONFIG)


@router.get('/', response_model=list[BadgeReader])
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


@router.get('/{badge_reader_id}', response_model=BadgeReader)
async def get_badge_reader_by_id(badge_reader_id: Annotated[UUID, Path(description='BadgeReader ID of the BadgeReader to select')], 
                                 db_session: Session = Depends(get_db)):
      
    db_badge_reader = read_badge_reader_by_id(db_session, badge_reader_id)
    if db_badge_reader:
        return BadgeReader(**db_badge_reader)
    else:
        raise HTTPException(status_code=200, detail='No badge reader found')
    

@router.post('/', response_model=BadgeReader)
async def post_badge_reader(badge_reader_post: BadgeReaderPost, db_session: Session = Depends(get_db)):

    # Obtaining badge reader input
    new_badge_reader: dict = badge_reader_post.model_dump()
    
    # Adding the UUID to the badge reader input dict
    new_badge_reader['id'] = uuid4()

    # Create the badge reader
    badge_reader = create_badge_reader(db_session, new_badge_reader)
    
    # Make the badge_reader a schemas.BadgeReader
    badge_reader = BadgeReader(**badge_reader)

    return badge_reader

@router.patch('/{badge_reader_id}', response_model=BadgeReader)
def patch_badge_reader(badge_reader_id: Annotated[UUID, Path(description='BadgeReader ID of the BadgeReader to update')], 
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
    

@router.delete('/{badge_reader_id}')
def delete_badge_reader(badge_reader_id: Annotated[UUID, Path(description='BadgeReader ID of the BadgeReader to delete')],
                db_session: Session = Depends(get_db)):
    
    deleted_badge_id: dict = remove_badge_reader(db_session, badge_reader_id)
    
    if deleted_badge_id:
        return deleted_badge_id
    else:        
        raise HTTPException(status_code=200, detail='No badge reader found')