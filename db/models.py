from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List
from uuid import UUID  # https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapped-column-derives-the-datatype-and-nullability-from-the-mapped-annotation

from datetime import datetime
from pytz import timezone


def now_with_timezone(tz: str = 'Europe/Rome'):
    return datetime.now(timezone(tz)).strftime('%Y-%m-%d %H:%M:%S%z')


class Base(DeclarativeBase):
    pass

class User(Base):

    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[str] = mapped_column(nullable=False, default=now_with_timezone)
    updated_at: Mapped[str] = mapped_column(nullable=True)
    deleted_at: Mapped[str] = mapped_column(nullable=True)

class BadgeReader_Badge(Base):

    __tablename__ = 'badge_readers_badges'

    badge_reader_id: Mapped[UUID] = mapped_column(ForeignKey('badge_readers.id'), primary_key=True, nullable=False)
    badge_id: Mapped[UUID] = mapped_column(ForeignKey('badges.id'), primary_key=True, nullable=False)
    badge_reader: Mapped[BadgeReader] = relationship(back_populates='badges')
    badge: Mapped[Badge] = relationship(back_populates='badge_readers')

class BadgeReader(Base):

    __tablename__ = 'badge_readers'

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)
    ip_address: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[str] = mapped_column(nullable=False, default=now_with_timezone)
    updated_at: Mapped[str] = mapped_column(nullable=True)
    deleted_at: Mapped[str] = mapped_column(nullable=True)
    badges: Mapped[List[BadgeReader_Badge]] = relationship(back_populates='badge_reader')

class Badge(Base):

    __tablename__ = 'badges'

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)
    code: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[str] = mapped_column(nullable=False, default=now_with_timezone)
    updated_at: Mapped[str] = mapped_column(nullable=True)
    deleted_at: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    badge_readers: Mapped[List[BadgeReader_Badge]] = relationship(back_populates='badge')
    
class Access(Base):

    __tablename__ = 'accesses'

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)
    in_timestamp: Mapped[str] = mapped_column(nullable=False, default=now_with_timezone)
    out_timestamp: Mapped[str] = mapped_column(nullable=True)
    badge_id: Mapped[UUID] = mapped_column(ForeignKey('badges.id'))
    badge_reader_id: Mapped[UUID] = mapped_column(ForeignKey('badge_readers.id'))