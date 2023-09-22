from __future__ import annotations
from models.utils import now_with_timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.ext.hybrid import hybrid_property
from uuid import UUID


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


# Association table for managing many-to-many relationship between BadgeReaders and Badges
badge_readers_badges = Table('badge_readers_badges',
                             Base.metadata,
                             Column('badge_reader_id', ForeignKey('badge_readers.id')),
                             Column('badge_id', ForeignKey('badges.id'))
                            )


class BadgeReader(Base):

    __tablename__ = 'badge_readers'

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)
    ip_address: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[str] = mapped_column(nullable=False, default=now_with_timezone)
    updated_at: Mapped[str] = mapped_column(nullable=True)
    deleted_at: Mapped[str] = mapped_column(nullable=True)

    badges = relationship('Badge', secondary=badge_readers_badges, back_populates='badge_readers')

    @hybrid_property
    def badge_ids(self):
        return [badge.id for badge in self.badges if badge.deleted_at is None]


class Badge(Base):

    __tablename__ = 'badges'

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)
    code: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[str] = mapped_column(nullable=False, default=now_with_timezone)
    updated_at: Mapped[str] = mapped_column(nullable=True)
    deleted_at: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=True)

    badge_readers = relationship('BadgeReader', secondary=badge_readers_badges, back_populates='badges')

    @hybrid_property
    def badge_reader_ids(self):
        return [badge_reader.id for badge_reader in self.badge_readers if badge_reader.deleted_at is None]


class Access(Base):

    __tablename__ = 'accesses'

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)
    in_timestamp: Mapped[str] = mapped_column(nullable=False, default=now_with_timezone)
    out_timestamp: Mapped[str] = mapped_column(nullable=True)
    badge_id: Mapped[UUID] = mapped_column(ForeignKey('badges.id'))
    badge_reader_id: Mapped[UUID] = mapped_column(ForeignKey('badge_readers.id'))