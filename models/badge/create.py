import schemas.badge

from models.utils import get_fields_from_model
from models.badge.badge import Badge
from sqlalchemy import Insert, insert
from sqlalchemy.orm import Session


def create_badge(session: Session, badge_post: dict) -> schemas.badge.Badge:
    
    sql_statement: Insert = insert(Badge) \
                            .values(**badge_post) \
                            .returning(Badge)
    
    query_result = session.scalars(sql_statement).one_or_none()
    if query_result:
        model_fields: dict = get_fields_from_model(query_result)
        badge: schemas.badge.Badge = schemas.badge.Badge(**model_fields)
        session.commit()

        return badge
