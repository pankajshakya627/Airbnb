from pydantic import BaseModel, ConfigDict

from app.models.enums import Gender


class GuestCreate(BaseModel):
    """Schema for creating a guest."""

    name: str
    gender: Gender
    age: int | None = None


class GuestUpdate(BaseModel):
    """Schema for updating a guest."""

    name: str | None = None
    gender: Gender | None = None
    age: int | None = None


class GuestResponse(BaseModel):
    """Response schema for guest data."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    gender: Gender
    age: int | None = None
