from models.utils import Base, now_with_timezone
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID


class Access(Base):

    __tablename__ = 'accesses'

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)
    in_timestamp: Mapped[str] = mapped_column(nullable=False, default=now_with_timezone)
    out_timestamp: Mapped[str] = mapped_column(nullable=True)
    badge_id: Mapped[UUID] = mapped_column(ForeignKey('badges.id'))
    badge_reader_id: Mapped[UUID] = mapped_column(ForeignKey('badge_readers.id'))