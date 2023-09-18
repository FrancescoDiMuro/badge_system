from models.models import BadgeReader, Badge
from models.utils import now_with_timezone
from sqlalchemy.orm import Session
from sqlalchemy import (Select, Insert, Update, 
                        select, insert, update, and_)
from uuid import UUID


def read_badges(session: Session, code_like: str) -> list[dict]:
  
    badges: list = []
    
    sql_statement: Select = select(Badge) \
                            .where(
                                and_( \
                                    Badge.deleted_at.is_(None),
                                    Badge.code.like(code_like))
                                ) \
                            .order_by(Badge.created_at)
        
    query_result = session.scalars(sql_statement).all()

    for record in query_result:
        badge = {k: v for k, v in record.__dict__.items()
                 if not k.startswith('_') and k != 'badges'}
        
        badge['badge_reader_ids'] = record.badge_reader_ids
        badges.append(badge)
    
    return badges


def read_badge_by_id(session: Session, badge_id: UUID) -> dict:

    badge: dict = {}
    
    sql_statement: Select = select(Badge) \
                            .where(and_( \
                                Badge.deleted_at.is_(None),
                                Badge.id == badge_id)) \
                            .order_by(Badge.created_at)        
    
    query_result = session.scalars(sql_statement).one_or_none()
    
    if query_result:

        badge = {k: v for k, v in query_result.__dict__.items()
                            if not k.startswith('_') and k != 'badges'}
        
        badge['badge_reader_ids'] = query_result.badge_reader_ids

        return badge

    return {}


def create_badge(session: Session, new_badge: dict) -> dict:
    
    sql_statement: Insert = insert(Badge) \
                            .values(**new_badge) \
                            .returning(Badge)
    
    badge: dict = session.scalars(sql_statement).all()[0]
    badge = {k: v for k, v in badge.__dict__.items() if not k.startswith('_')}

    if badge:
        session.commit()

    return badge


def update_badge(session: Session, badge_id: UUID, updated_badge_info: dict):
    
    badge_reader_ids = updated_badge_info.get('badge_reader_ids', [])

    sql_statement = select(BadgeReader) \
                   .where(BadgeReader.id.in_(badge_reader_ids))

    badge_readers = session.execute(sql_statement).scalars().all()

    sql_statement = select(Badge) \
                    .where(Badge.id == badge_id)

    current_badge = session.execute(sql_statement).scalars().first()

    if current_badge:
        current_badge.updated_at = now_with_timezone()

        for key, value in updated_badge_info.items():
            if key != 'badge_reader_ids':
                setattr(current_badge, key, value)

        # Update the badge_readers list (relationship)
        current_badge.badge_readers = badge_readers

        badge: dict = {k: v for k, v in current_badge.__dict__.items() if not k.startswith('_')}

        badge['badge_reader_ids'] = badge_reader_ids
        
        session.commit()

    return badge


def remove_badge(session: Session, badge_id: UUID) -> dict: 
       
    sql_statement: Update = update(Badge) \
                            .where(and_(
                                Badge.id == badge_id,
                                Badge.deleted_at.is_(None)) \
                            ) \
                            .values(deleted_at=now_with_timezone()) \
                            .returning(Badge.id)

    deleted_badge_id: UUID = session.scalar(sql_statement)

    if deleted_badge_id is not None:
        session.commit()
    else:
        return {}

    return {'badge_id': deleted_badge_id}
