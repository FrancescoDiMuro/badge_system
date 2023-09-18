from sqlalchemy.orm import Session
from sqlalchemy import (Select, 
                        Insert, 
                        Update, 
                        select, 
                        insert, 
                        update, 
                        and_)

from sqlalchemy.exc import NoResultFound

from models.models import BadgeReader, Badge
from uuid import UUID
from models.utils import now_with_timezone

def read_badge_readers(session: Session, ip_address_like: str, location_like: str) -> list[dict]:
  
    badge_readers: list = []
    
    sql_statement: Select = select(BadgeReader) \
                            .where(
                                and_( \
                                    BadgeReader.deleted_at.is_(None),
                                    BadgeReader.ip_address.like(ip_address_like),
                                    BadgeReader.location.like(location_like))
                                ) \
                            .order_by(BadgeReader.created_at)
        
    query_result = session.execute(sql_statement).all()

    for record in query_result:        
        badge_reader = {k: v for k, v in record[0].__dict__.items()
                        if not k.startswith('_') and k != 'badges'}
        
        badge_reader['badge_ids'] = record[0].badge_ids
        badge_readers.append(badge_reader)
    
    return badge_readers


def read_badge_reader_by_id(session: Session, badge_reader_id: UUID) -> dict:

    badge_reader: dict = {}
    
    sql_statement: Select = select(BadgeReader) \
                            .where(and_( \
                                BadgeReader.deleted_at.is_(None),
                                BadgeReader.id == badge_reader_id)) \
                            .order_by(BadgeReader.created_at)        
    
    try:
        query_result = session.execute(sql_statement).one()[0]        
    except NoResultFound:        
        return {}
    
    badge_reader = {k: v for k, v in query_result.__dict__.items()
                        if not k.startswith('_') and k != 'badges'}
    
    badge_reader['badge_ids'] = query_result.badge_ids

    return badge_reader


def create_badge_reader(session: Session, new_badge_reader: dict) -> dict:
    
    # badges: list[Badge] = []

    # badge_ids = new_badge_reader['badge_ids']

    # sql_statement: Select = select(Badge) \
                            # .where(Badge.id.in_(badge_ids))
    
    # query_result = session.scalars(sql_statement).all()
    # for badge in query_result:
    #     badges.append(Badge(**{k: v for k, v in badge.__dict__.items() if not k.startswith('_')}))

    # new_badge_reader['badges'] = badges   
    
    sql_statement: Insert = insert(BadgeReader) \
                            .values(**new_badge_reader) \
                            .returning(BadgeReader)
    
    badge_reader: dict = session.scalars(sql_statement).all()[0]
    badge_reader = {k: v for k, v in badge_reader.__dict__.items() if not k.startswith('_')}

    if badge_reader:
        session.commit()

    return badge_reader


def update_badge_reader(session: Session, badge_reader_id: UUID, updated_badge_reader_info: dict):
    
    badge_ids = updated_badge_reader_info.get('badge_ids', [])

    sql_statement = select(Badge) \
                   .where(Badge.id.in_(badge_ids))

    badges = session.execute(sql_statement).scalars().all()

    sql_statement = select(BadgeReader) \
                    .where(BadgeReader.id == badge_reader_id)

    current_badge_reader = session.execute(sql_statement).scalars().first()

    if current_badge_reader:
        current_badge_reader.updated_at = now_with_timezone()

        for key, value in updated_badge_reader_info.items():
            if key != 'badge_ids':
                setattr(current_badge_reader, key, value)

        # Update the badges list (relationship)
        current_badge_reader.badges = badges

        badge_reader: dict = {k: v for k, v in current_badge_reader.__dict__.items() if not k.startswith('_')}

        badge_reader['badge_ids'] = badge_ids
        
        session.commit()

    return badge_reader


def remove_badge_reader(session: Session, badge_reader_id: UUID) -> dict: 
       
    sql_statement: Update = update(BadgeReader) \
                            .where(and_(
                                BadgeReader.id == badge_reader_id,
                                BadgeReader.deleted_at.is_(None)) \
                            ) \
                            .values(deleted_at=now_with_timezone()) \
                            .returning(BadgeReader.id)

    deleted_badge_reader_id: UUID = session.scalar(sql_statement)

    if deleted_badge_reader_id is not None:
        session.commit()
    else:
        return {}

    return {'badge_reader_id': deleted_badge_reader_id}
