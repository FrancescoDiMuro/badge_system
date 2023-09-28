from datetime import datetime
from pytz import timezone
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Association table for managing many-to-many relationship between BadgeReaders and Badges
badge_readers_badges = Table('badge_readers_badges',
                             Base.metadata,
                             Column('badge_reader_id', ForeignKey('badge_readers.id')),
                             Column('badge_id', ForeignKey('badges.id'))
                            )


def now_with_timezone(tz: str = 'Europe/Rome'):
    return datetime.now(timezone(tz)).strftime('%Y-%m-%d %H:%M:%S%z')


def get_fields_from_model(model) -> dict:
    '''Get fields from the SQLAlchemy model

    Arguments:
    - model: SQLAlchemy model to extract the fields from

    Returns:
    - model_fields (dict): fields extracted from the SQLAlchemy model
    '''
    return {k: v for k, v in model.__dict__.items() if not k.startswith('_')}