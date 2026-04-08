from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=255, pattern="^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(..., min_length=6)

    @field_validator("email")
    def normalize_email(cls, v):
        return v.lower().strip()

    class Config:
        extra = "forbid"


class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        None, min_length=3, max_length=255, pattern="^[a-zA-Z0-9_]+$"
    )
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)

    class Config:
        extra = "forbid"


class UserAdminCreate(UserCreate):
    is_active: bool = True
    is_verified: bool = False


class UserAdminUpdate(UserUpdate):
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
