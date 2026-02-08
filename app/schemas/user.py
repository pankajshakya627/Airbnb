from datetime import date
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict

from app.models.enums import Gender, Role


class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str
    name: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class ProfileUpdate(BaseModel):
    """Schema for profile updates."""
    name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None


class UserResponse(BaseModel):
    """Response schema for user data."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: str
    name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    roles: List[str] = []


class LoginResponse(BaseModel):
    """Response schema for login."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""
    user_id: Optional[int] = None
    roles: List[str] = []
