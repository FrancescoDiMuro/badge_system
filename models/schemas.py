from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserPost(BaseModel):      
    id: UUID | None = None
    name: str
    surname: str
    email: EmailStr
    phone: str
        
class User(UserPost):
    created_at: str
    updated_at: str | None = None
    deleted_at: str | None = None

class UserPatch(BaseModel):
    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None
    phone: str | None = None

class BadgeReaderPost(BaseModel):
    id: UUID | None = None
    ip_address: str
    location: str

class BadgeReader(BadgeReaderPost):
    created_at: str
    updated_at: str | None = None
    deleted_at: str | None = None
    badges: list

class BadgeReaderPatch(BaseModel):
    ip_address: str | None = None
    location: str | None = None