import schemas.badge_reader

from models.utils import get_fields_from_model
from models.badge_reader.badge_reader import BadgeReader
from sqlalchemy import Insert, insert
from sqlalchemy.orm import Session


def create_badge_reader(session: Session, badge_reader_post: dict) -> schemas.badge_reader.BadgeReader:
    
    sql_statement: Insert = insert(BadgeReader) \
                            .values(**badge_reader_post) \
                            .returning(BadgeReader)
    
    query_result = session.scalars(sql_statement).one_or_none()
    if query_result:
        model_fields: dict = get_fields_from_model(query_result)
        badge_reader: schemas.badge_reader.BadgeReader = schemas.badge_reader.BadgeReader(**model_fields)
        session.commit()

        return badge_reader
