from models.user.user import User
from sqlalchemy import Select, select
from sqlalchemy.orm import Session
from uuid import UUID


def user_is_deleted(session: Session, user_id: UUID) -> bool:

    sql_statement: Select = select(User.deleted_at) \
                            .where(User.id == user_id)
    
    return session.scalar(sql_statement) is not None