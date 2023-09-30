from models.badge.badge import Badge
from models.utils import now_with_timezone
from sqlalchemy import Update, update
from sqlalchemy.orm import Session
from uuid import UUID


def remove_badge(session: Session, badge_id: UUID) -> dict | None: 
       
    sql_statement: Update = update(Badge) \
                            .where(Badge.id == badge_id) \
                            .values(deleted_at=now_with_timezone()) \
                            .returning(Badge.id)

    deleted_badge_id: UUID = session.scalar(sql_statement)

    if deleted_badge_id:        
        session.commit()
        
        return {'badge_id': deleted_badge_id}
    
    return None