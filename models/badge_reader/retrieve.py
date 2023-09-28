import schemas.badge_reader

from models.utils import get_fields_from_model
from models.badge_reader.badge_reader import BadgeReader
from sqlalchemy import Select, select, and_
from sqlalchemy.orm import Session
from uuid import UUID


def retrieve_badge_readers(session: Session, ip_address_like: str, 
                           location_like: str, include_deleted: bool) -> list[schemas.badge_reader.BadgeReader]:

    # http://127.0.0.1:8080/badge_readers/?ip_address_like=%%2510
  
    badge_readers: list[schemas.badge_reader.BadgeReader] = []
    
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

    for model in query_result:
        model_fields = get_fields_from_model(model)
        model_fields['badge_ids'] = model.badge_ids
        badge_readers.append(schemas.badge_reader.BadgeReader(**model_fields))
    
    return badge_readers


def retrieve_badge_reader_by_id(session: Session, badge_reader_id: UUID, include_deleted: bool) -> schemas.badge_reader.BadgeReader | None:
    
    sql_statement: Select = select(BadgeReader) \
                            .where(
                                and_( \
                                    True if include_deleted else BadgeReader.deleted_at.is_(None),
                                    BadgeReader.id == badge_reader_id)
                                )
    
    query_result = session.scalars(sql_statement).one_or_none()
    if query_result:
        model_fields = get_fields_from_model(query_result)
        model_fields['badge_ids'] = query_result.badge_ids
        badge_reader: schemas.badge_reader.BadgeReader = schemas.badge_reader.BadgeReader(**model_fields)

        return badge_reader

    return None