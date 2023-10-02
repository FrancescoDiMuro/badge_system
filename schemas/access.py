from pydantic import BaseModel
from uuid import UUID


class AccessPost(BaseModel):
    id: UUID | None = None    
    badge_id: UUID
    badge_reader_id: UUID


class Access(AccessPost):
    in_timestamp: str
    out_timestamp: str | None = None