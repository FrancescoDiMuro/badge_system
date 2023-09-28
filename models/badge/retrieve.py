import schemas.badge_reader

from models.utils import get_fields_from_model
from models.badge_reader.badge_reader import BadgeReader
from sqlalchemy import Select, select, and_
from sqlalchemy.orm import Session
from uuid import UUID


def retrieve_badge_readers(session: Session, ip_address_like: str, location_like: str, include_deleted: bool) -> list[schemas.user.User]:
  
    badge_readers: list[schemas.user.User] = []
    
    sql_statement: Select = select(BadgeReader) \
                            .where(
                                and_( \
                                    True if include_deleted else BadgeReader.deleted_at.is_(None),
                                    BadgeReader.ip_address.like(ip_address_like),
                                    BadgeReader.location.like(location_like)
                                    )
                                ) \
                            .order_by(BadgeReader.created_at)
    
    query_result = session.scalars(sql_statement).all()

    badge_readers = [schemas.badge_reader.BadgeReader(**get_fields_from_model(model)) for model in query_result]
    
    return badge_readers


def retrieve_badge_reader_by_id(session: Session, badge_reader_id: UUID, include_deleted: bool) -> schemas.badge_reader.BadgeReader | None:
    
    sql_statement: Select = select(BadgeReader) \
                            .where(
                                and_( \
                                    True if include_deleted else BadgeReader.deleted_at.is_(None),
                                    BadgeReader.id == badge_reader_id)
                                ) \
                            .order_by(BadgeReader.created_at)
    
    query_result = session.scalars(sql_statement).one_or_none()
    if query_result:        
        badge_reader: schemas.badge_reader.BadgeReader = schemas.badge_reader.BadgeReader(**get_fields_from_model(query_result))

        return badge_reader

    return None