from models.utils import Base, badge_readers_badges, now_with_timezone
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from uuid import UUID


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
