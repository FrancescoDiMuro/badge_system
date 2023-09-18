from sqlalchemy.orm import Session
from sqlalchemy import (Select, Insert, Update, 
                        select, insert, update, and_)
from models.models import Access
from uuid import UUID, uuid4
from models.utils import now_with_timezone


def read_accesses(session: Session, in_timestamp: str, out_timestamp: str) -> list[dict]:
  
    accesses: list = []
    
    sql_statement: Select = select(Access) \
                            .order_by(Access.in_timestamp)
        
    query_result = session.scalars(sql_statement).all()

    accesses = [{k: v for k, v in record.__dict__.items() if not k.startswith('_')} 
                for record in query_result]
    
    return accesses


def do_access(session: Session, badge_id: UUID, badge_reader_id: UUID) -> dict:
    
    access: dict = {}
    
    sql_statement: Select = select(Access.id) \
                            .where(and_(
                                Access.badge_id == badge_id),
                                Access.badge_reader_id == badge_reader_id,
                                Access.out_timestamp.is_(None)
                            )
    
    access_id = session.execute(sql_statement).scalar_one_or_none()
    if not access_id:
        access['id'] = uuid4()
        access['in_timestamp'] = now_with_timezone()
        access['badge_id'] = badge_id
        access['badge_reader_id'] = badge_reader_id
        
        sql_statement: Insert = insert(Access) \
                                .values(**access) \
                                .returning(Access)
        
    else:

        sql_statement: Update = update(Access) \
                                .where(Access.id == access_id) \
                                .values(out_timestamp=now_with_timezone()) \
                                .returning(Access)

    access_dict = {k: v for k, v in session.execute(sql_statement).scalars().first().__dict__.items() 
                   if not k.startswith('_')}

    if access_dict:
        session.commit()
    
    return access_dict
