from models.utils import Base, now_with_timezone
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID


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
