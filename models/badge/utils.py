from models.badge.badge import Badge
from sqlalchemy import Select, select
from sqlalchemy.orm import Session
from uuid import UUID


def badge_is_deleted(session: Session, badge_id: UUID) -> bool:

    sql_statement: Select = select(Badge.deleted_at) \
                            .where(Badge.id == badge_id)
    
    return session.scalar(sql_statement) is not None