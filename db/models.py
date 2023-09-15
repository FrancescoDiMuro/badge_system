from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Uuid, Table, Column
from typing import List
from .utils import now_with_timezone


class Base(DeclarativeBase):
    pass

class Users(Base):

    __tablename__ = 'users'

    id: Mapped[Uuid] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[str] = mapped_column(nullable=False, default=now_with_timezone)
    updated_at: Mapped[str] = mapped_column(nullable=True)
    deleted_at: Mapped[str] = mapped_column(nullable=True)

badge_readers_badges =  Table('badge_readers_badges', 
                              Base.metadata,
                              Column('badge_reader_id', ForeignKey('badge_readers.id'), primary_key=True, nullable=False),
                              Column('badge_id', ForeignKey('badges.id'), primary_key=True, nullable=False))

class BadgerReaders(Base):

    __tablename__ = 'badge_readers'

    id: Mapped[Uuid] = mapped_column(primary_key=True, nullable=False)
    ip_address: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[str] = mapped_column(nullable=False, default=now_with_timezone)
    updated_at: Mapped[str] = mapped_column(nullable=True)
    deleted_at: Mapped[str] = mapped_column(nullable=True)
    badges: Mapped[List[Badges]] = relationship(secondary=badge_readers_badges, back_populates='badge_readers')

class Badges(Base):

    __tablename__ = 'badges'

    id: Mapped[Uuid] = mapped_column(primary_key=True, nullable=False)
    code: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[str] = mapped_column(nullable=False, default=now_with_timezone)
    updated_at: Mapped[str] = mapped_column(nullable=True)
    deleted_at: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[Uuid] = mapped_column(ForeignKey('users.id'))
    badge_readers: Mapped[List[BadgerReaders]] = relationship(secondary=badge_readers_badges, back_populates='badges')

class Accesses(Base):

    __tablename__ = 'accesses'

    id: Mapped[Uuid] = mapped_column(primary_key=True, nullable=False)
    in_timestamp: Mapped[str] = mapped_column(nullable=True)
    out_timestamp: Mapped[str] = mapped_column(nullable=True)
    badge_id: Mapped[Uuid] = mapped_column(ForeignKey('badges.id'))
    badge_reader_id: Mapped[Uuid] = mapped_column(ForeignKey('badge_readers.id'))    
