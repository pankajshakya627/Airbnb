from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.enums import Gender


class UserCreate(BaseModel):
    """Schema for user registration."""

    email: EmailStr
    password: str
    name: str | None = None


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class ProfileUpdate(BaseModel):
    """Schema for profile updates."""

    name: str | None = None
    date_of_birth: date | None = None
    gender: Gender | None = None


class UserResponse(BaseModel):
    """Response schema for user data."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str | None = None
    date_of_birth: date | None = None
    gender: Gender | None = None
    roles: list[str] = []


class LoginResponse(BaseModel):
    """Response schema for login."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""

    user_id: int | None = None
    roles: list[str] = []
