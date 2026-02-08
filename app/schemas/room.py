from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class RoomCreate(BaseModel):
    """Schema for creating a room."""
    type: str
    base_price: Decimal
    photos: Optional[List[str]] = None
    amenities: Optional[List[str]] = None
    total_count: int
    capacity: int


class RoomUpdate(BaseModel):
    """Schema for updating a room."""
    type: Optional[str] = None
    base_price: Optional[Decimal] = None
    photos: Optional[List[str]] = None
    amenities: Optional[List[str]] = None
    total_count: Optional[int] = None
    capacity: Optional[int] = None


class RoomResponse(BaseModel):
    """Response schema for room data."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    hotel_id: int
    type: str
    base_price: Decimal
    photos: Optional[List[str]] = None
    amenities: Optional[List[str]] = None
    total_count: int
    capacity: int
    created_at: datetime
    updated_at: datetime
