import schemas.badge

from models.utils import get_fields_from_model
from models.badge.badge import Badge
from models.badge_reader.badge_reader import BadgeReader
from models.utils import now_with_timezone
from sqlalchemy import Select, select
from sqlalchemy.orm import Session
from uuid import UUID


def update_badge(session: Session, badge_id: UUID, badge_update: dict) -> schemas.badge_reader.BadgeReader:      

    # Getting the Badge Reader IDs attribute (if present)
    badge_reader_ids = badge_update.get('badge_reader_ids', [])

    # If any badge_reader_ids has been provided
    if badge_reader_ids:
        sql_statement = select(BadgeReader) \
                       .where(BadgeReader.id.in_(badge_reader_ids))

        # Getting BadgeReader models
        badge_readers: list[BadgeReader] = session.scalars(sql_statement).all()

    # Select all the info from the BadgeReader the user is updating
    sql_statement: Select = select(Badge) \
                            .where(Badge.id == badge_id)

    current_badge: Badge = session.scalars(sql_statement).one()
    
    if current_badge:
        current_badge.updated_at = now_with_timezone()

        # Remove the badge_reader_ids key from dict (if present)
        badge_update.pop('badge_reader_ids', None)
        
        # Updating all attributes of the current badge
        for key, value in badge_update.items():            
            setattr(current_badge, key, value)

        # If the badge_reader_ids list for the current badge has been provided,
        # then update it
        if badge_reader_ids:
            current_badge.badge_readers = badge_readers

        model_fields: dict = get_fields_from_model(current_badge)
        badge: schemas.badge.Badge = schemas.badge.Badge(**model_fields)

        badge['badge_reader_ids'] = badge_reader_ids

        session.commit()

    return badge
    