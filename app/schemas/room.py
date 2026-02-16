from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class RoomCreate(BaseModel):
    """Schema for creating a room."""

    type: str
    base_price: Decimal
    photos: list[str] | None = None
    amenities: list[str] | None = None
    total_count: int
    capacity: int


class RoomUpdate(BaseModel):
    """Schema for updating a room."""

    type: str | None = None
    base_price: Decimal | None = None
    photos: list[str] | None = None
    amenities: list[str] | None = None
    total_count: int | None = None
    capacity: int | None = None


class RoomResponse(BaseModel):
    """Response schema for room data."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    hotel_id: int
    type: str
    base_price: Decimal
    photos: list[str] | None = None
    amenities: list[str] | None = None
    total_count: int
    capacity: int
    created_at: datetime
    updated_at: datetime
