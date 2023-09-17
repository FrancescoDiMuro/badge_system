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
