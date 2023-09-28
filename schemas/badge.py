from pydantic import BaseModel
from uuid import UUID


class BadgePost(BaseModel):
    id: UUID | None = None
    code: int


class Badge(BadgePost):
    created_at: str
    updated_at: str | None = None
    deleted_at: str | None = None
    user_id: UUID | None = None
    badge_reader_ids: list[UUID] | None = None

    class Config:
        from_attributes = True


class BadgePatch(BaseModel):
    code: int | None = None
    user_id: UUID | None = None
    badge_reader_ids: list[UUID] | None = None