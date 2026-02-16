from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class HotelContactInfoSchema(BaseModel):
    """Schema for hotel contact information."""

    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None


class HotelCreate(BaseModel):
    """Schema for creating a hotel."""

    name: str
    city: str | None = None
    photos: list[str] | None = None
    amenities: list[str] | None = None
    contact_info: HotelContactInfoSchema | None = None


class HotelUpdate(BaseModel):
    """Schema for updating a hotel."""

    name: str | None = None
    city: str | None = None
    photos: list[str] | None = None
    amenities: list[str] | None = None
    contact_info: HotelContactInfoSchema | None = None


class HotelResponse(BaseModel):
    """Response schema for hotel data."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    city: str | None = None
    photos: list[str] | None = None
    amenities: list[str] | None = None
    contact_phone: str | None = None
    contact_email: str | None = None
    contact_address: str | None = None
    active: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime


class HotelInfoResponse(BaseModel):
    """Public hotel info response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    city: str | None = None
    photos: list[str] | None = None
    amenities: list[str] | None = None
    contact_phone: str | None = None
    contact_email: str | None = None
    contact_address: str | None = None
