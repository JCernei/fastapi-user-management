from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, constr
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    username: constr(min_length=3, pattern="^[^\s]+$")
    password: constr(min_length=8)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[constr(min_length=3, pattern="^[^\s]+$")] = None
    password: Optional[constr(min_length=8)] = None


class UserResponse(BaseModel):
    email: EmailStr
    username: str
    id: UUID

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
