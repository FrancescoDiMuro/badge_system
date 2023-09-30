import schemas.access
from models.access.access import Access
from models.badge.badge import Badge
from models.badge_reader.badge_reader import BadgeReader
from models.utils import get_fields_from_model, now_with_timezone
from sqlalchemy import Insert, Select, Update, insert, select, update, and_
from sqlalchemy.orm import Session
from uuid import UUID, uuid4


def do_access(session: Session, badge_id: UUID, badge_reader_id: UUID) -> schemas.access.Access | None:
    
    new_access: dict = {}

    # Checking if the badge exists and the user has the rights to access the area
    sql_statement: Select = select(Badge) \
                            .where(Badge.id == badge_id)
    
    user_badge: Badge = session.scalars(sql_statement).one_or_none()
    if user_badge:
        if badge_reader_id in user_badge.badge_reader_ids:

            sql_statement: Select = select(Access.id) \
                                    .where(
                                        and_(
                                            Access.badge_id == badge_id),
                                            Access.badge_reader_id == badge_reader_id,
                                            Access.out_timestamp.is_(None)
                                        )
            
            access_id = session.execute(sql_statement).scalar_one_or_none()
            if not access_id:
                new_access['id'] = uuid4()
                new_access['in_timestamp'] = now_with_timezone()
                new_access['badge_id'] = badge_id
                new_access['badge_reader_id'] = badge_reader_id
                
                sql_statement: Insert = insert(Access) \
                                        .values(**new_access) \
                                        .returning(Access)
                
            else:

                sql_statement: Update = update(Access) \
                                        .where(Access.id == access_id) \
                                        .values(out_timestamp=now_with_timezone()) \
                                        .returning(Access)

            query_result = session.scalars(sql_statement).one_or_none()
            model_fields: dict = get_fields_from_model(query_result)
            access: schemas.access.Access = schemas.access.Access(**model_fields)

            if access:
                session.commit()
            
            return access
        
    return None