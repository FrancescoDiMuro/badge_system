from __future__ import annotations
from pydantic import BaseModel, EmailStr
from uuid import UUID


class BadgeReaderPost(BaseModel):
    id: UUID | None = None
    ip_address: str
    location: str


class BadgeReader(BadgeReaderPost):
    created_at: str
    updated_at: str | None = None
    deleted_at: str | None = None
    badge_ids: list[UUID] | None = None

    class Config:
        from_attributes = True


class BadgeReaderPatch(BaseModel):
    ip_address: str | None = None
    location: str | None = None
    badge_ids: list[UUID] | None = None


class AccessPost(BaseModel):
    id: UUID | None = None    
    badge_id: UUID
    badge_reader_id: UUID


class Access(AccessPost):
    in_timestamp: str | None = None
    out_timestamp: str | None = None
