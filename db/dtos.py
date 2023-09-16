from pydantic import BaseModel
from uuid import UUID


class User(BaseModel):
    id: UUID | None = None
    name: str
    surname: str
    email: str
    phone: str
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None