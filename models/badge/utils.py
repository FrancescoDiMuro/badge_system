from models.badge_reader.badge_reader import BadgeReader
from sqlalchemy import Select, select
from sqlalchemy.orm import Session
from uuid import UUID


def badge_reader_is_deleted(session: Session, badge_reader: UUID) -> bool:

    sql_statement: Select = select(BadgeReader.deleted_at) \
                            .where(BadgeReader.id == badge_reader)
    
    return session.scalar(sql_statement) is not None