from models.user.user import User
from models.utils import now_with_timezone
from sqlalchemy import Update, update
from sqlalchemy.orm import Session
from uuid import UUID


def remove_user(session: Session, user_id: UUID) -> dict | None: 
       
    sql_statement: Update = update(User) \
                            .where(User.id == user_id) \
                            .values(deleted_at=now_with_timezone()) \
                            .returning(User.id)

    deleted_user_id: UUID = session.scalar(sql_statement)

    if deleted_user_id:
        session.commit()
        
        return {'user_id': deleted_user_id}
    
    return None