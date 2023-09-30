import schemas.badge
from models.utils import get_fields_from_model
from models.badge.badge import Badge
from models.badge.utils import badge_code_to_qr_code
from qrcode.image.pil import PilImage
from sqlalchemy import Select, select, and_
from sqlalchemy.orm import Session
from uuid import UUID


def retrieve_badges(session: Session, code_like: str, include_deleted: bool) -> list[schemas.badge.Badge]:   
  
    badges: list[schemas.badge.Badge] = []
    
    sql_statement: Select = select(Badge) \
                            .where(
                                and_( \
                                    True if include_deleted else Badge.deleted_at.is_(None),
                                    Badge.code.like(code_like)
                                    )
                                ) \
                            .order_by(Badge.created_at)
    
    query_result = session.scalars(sql_statement).all()

    for model in query_result:
        model_fields = get_fields_from_model(model)
        model_fields['badge_reader_ids'] = model.badge_reader_ids
        badges.append(schemas.badge.Badge(**model_fields))
    
    return badges


def retrieve_badge_by_id(session: Session, badge_id: UUID, include_deleted: bool) -> schemas.badge.Badge | None:
    
    sql_statement: Select = select(Badge) \
                            .where(
                                and_( \
                                    True if include_deleted else Badge.deleted_at.is_(None),
                                    Badge.id == badge_id)
                                )
    
    query_result = session.scalars(sql_statement).one_or_none()
    if query_result:
        model_fields = get_fields_from_model(query_result)
        model_fields['badge_reader_ids'] = query_result.badge_reader_ids
        badge: schemas.badge.Badge = schemas.badge.Badge(**model_fields)

        return badge

    return None


def retrieve_badge_qr_code(session: Session, badge_id: UUID) -> PilImage | None:

    sql_statement: Select = select(Badge.code) \
                            .where(Badge.id == badge_id)
    
    badge_code = session.scalar(sql_statement)

    if badge_code:
        return badge_code_to_qr_code(badge_code)
    
    return None