from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class InventoryResponse(BaseModel):
    """Response schema for inventory data."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    hotel_id: int
    room_id: int
    date: date
    book_count: int
    reserved_count: int
    total_count: int
    surge_factor: Decimal
    price: Decimal
    city: str
    closed: bool


class InventoryUpdate(BaseModel):
    """Schema for updating inventory."""
    surge_factor: Optional[Decimal] = None
    price: Optional[Decimal] = None
    closed: Optional[bool] = None
    total_count: Optional[int] = None


class InventoryBulkUpdate(BaseModel):
    """Schema for bulk inventory updates."""
    start_date: date
    end_date: date
    surge_factor: Optional[Decimal] = None
    price: Optional[Decimal] = None
    closed: Optional[bool] = None
