import schemas.badge_reader

from models.utils import get_fields_from_model
from models.badge_reader.badge_reader import BadgeReader
from models.badge.badge import Badge
from models.utils import now_with_timezone
from sqlalchemy import Select, select
from sqlalchemy.orm import Session
from uuid import UUID


def update_badge_reader(session: Session, badge_reader_id: UUID, badge_reader_update: dict) -> schemas.badge_reader.BadgeReader:      

    # Getting the Badge IDs attribute (if present)
    badge_ids = badge_reader_update.get('badge_ids', [])

    # If any badge_id has been provided
    if badge_ids:
        sql_statement = select(Badge) \
                       .where(Badge.id.in_(badge_ids))

        # Getting Badge models
        badges: list[Badge] = session.scalars(sql_statement).all()

    # Select all the info from the BadgeReader the user is updating
    sql_statement: Select = select(BadgeReader) \
                            .where(BadgeReader.id == badge_reader_id)

    current_badge_reader: BadgeReader = session.scalars(sql_statement).one()
    
    if current_badge_reader:
        current_badge_reader.updated_at = now_with_timezone()

        # Remove the badge_ids key from dict (if present)
        badge_reader_update.pop('badge_ids', None)
        
        # Updating all attributes of the current badge reader
        for key, value in badge_reader_update.items():            
            setattr(current_badge_reader, key, value)

        # If the badge_ids list for the current badge reader has been provided,
        # then update it
        if badge_ids:
            current_badge_reader.badges = badges

        model_fields: dict = get_fields_from_model(current_badge_reader)
        model_fields['badge_ids'] = badge_ids
        badge_reader: schemas.badge_reader.BadgeReader = schemas.badge_reader.BadgeReader(**model_fields)        

        session.commit()

    return badge_reader
    