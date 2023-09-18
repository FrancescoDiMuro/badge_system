from fastapi import (APIRouter, 
                     HTTPException, 
                     Depends, 
                     Path, 
                     Query)

from models.db.utils import get_db

from models.schemas import (Badge, 
                            BadgePost, 
                            BadgePatch)

from models.crud.badges import (read_badges, 
                               read_badge_by_id, 
                               create_badge, 
                               update_badge,
                               remove_badge)

from sqlalchemy.orm import Session
from typing import Annotated
from uuid import UUID, uuid4


API_ROUTER_CONFIG: dict = {
    'prefix': '/badges',
    'tags': ['badges']
}

GET_BADGES_METADATA: dict = {
    'summary': 'GET /badges', 
    'description': 'This endpoint lets you get a list of configured badges (if any).', 
    'response_model': list[Badge]
}

GET_BADGES_BY_ID_METADATA: dict = {
    'summary': 'GET /badge/{badge_id}', 
    'description': 'This endpoint lets you get a badge selecting it by its id (if any).', 
    'response_model': Badge
}

POST_BADGES_METADATA: dict = {
    'summary': 'POST /badges', 
    'description': 'This endpoint lets you create a new badge.', 
    'response_model': Badge
}

PATCH_BADGES_METADATA: dict = {
    'summary': 'PATCH /badges/{badges_id}', 
    'description': 'This endpoint lets you update the information of an existing badge, specifying its id.', 
    'response_model': Badge
}

DELETE_BADGES_METADATA: dict = {
    'summary': 'DELETE /badges/{badge_id}', 
    'description': 'This endpoint lets you delete a badge, specifying its id.', 
    'response_model': None
}


router = APIRouter(**API_ROUTER_CONFIG)


@router.get('/', **GET_BADGES_METADATA)
async def get_badges(code_like: Annotated[str, Query(description='Filter for the badge code')] = '%',
                     db_session: Session = Depends(get_db)):
    
    badges: list[Badge] = []
    
    db_badges = read_badges(db_session, code_like)
    if not db_badges:
        raise HTTPException(status_code=200, detail='No badges found')
    else:
        badges = [db_badge for db_badge in db_badges]

    return badges


@router.get('/{badge_id}', **GET_BADGES_BY_ID_METADATA)
async def get_badge_by_id(badge_id: Annotated[UUID, Path(description='Badge ID of the Badge to select')], 
                          db_session: Session = Depends(get_db)):
      
    db_badge = read_badge_by_id(db_session, badge_id)
    if db_badge:
        return Badge(**db_badge)
    else:
        raise HTTPException(status_code=200, detail='No badge found')
    

@router.post('/', **POST_BADGES_METADATA)
async def post_badge(badge_post: BadgePost, db_session: Session = Depends(get_db)):

    # Get user input in a dict
    new_badge: dict = badge_post.model_dump()
    
    # Assign id to the new record
    new_badge['id'] = uuid4()

    # Create the record
    badge = create_badge(db_session, new_badge)
    
    # Convert the record to a valid schema object
    badge = Badge(**badge)

    return badge


@router.patch('/{badge_id}', **PATCH_BADGES_METADATA)
def patch_badge_reader(badge_id: Annotated[UUID, Path(description='Badge ID of the badge to update')], 
                       badge: BadgePatch, 
                       db_session: Session = Depends(get_db)):
    
    # Obtain badge data that has been updated, excluding what hasn't been set
    updated_badge_info: dict = badge.model_dump(exclude_unset=True)

    # If the user actually filled the dict with some valid info
    if updated_badge_info:
        updated_badge: Badge = Badge(**update_badge(db_session, badge_id, updated_badge_info))

        return updated_badge
    
    else:
        raise HTTPException(status_code=422, detail='Invalid input')
    

@router.delete('/{badge_id}', **DELETE_BADGES_METADATA)
def delete_badge(badge_id: Annotated[UUID, Path(description='Badge ID of the badge to delete')],
                 db_session: Session = Depends(get_db)):
    
    deleted_badge_id: dict = remove_badge(db_session, badge_id)
    
    if deleted_badge_id:
        return deleted_badge_id
    else:        
        raise HTTPException(status_code=200, detail='No badge found')
    