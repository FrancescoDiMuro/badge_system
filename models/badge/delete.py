from models.badge_reader.badge_reader import BadgeReader
from models.utils import now_with_timezone
from sqlalchemy import Update, update
from sqlalchemy.orm import Session
from uuid import UUID


def remove_badge_reader(session: Session, badge_reader_id: UUID) -> dict | None: 
       
    sql_statement: Update = update(BadgeReader) \
                            .where(BadgeReader.id == badge_reader_id) \
                            .values(deleted_at=now_with_timezone()) \
                            .returning(BadgeReader.id)

    deleted_badge_reader_id: UUID = session.scalar(sql_statement)

    if deleted_badge_reader_id:
        
        session.commit()
        
        return {'badge_reader_id': deleted_badge_reader_id}
    
    return None