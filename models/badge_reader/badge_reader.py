from models.utils import Base, badge_readers_badges, now_with_timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from uuid import UUID


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
