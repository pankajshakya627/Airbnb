from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from app.models.enums import BookingStatus
from app.schemas.guest import GuestResponse


class BookingCreate(BaseModel):
    """Schema for creating a booking."""
    hotel_id: int
    room_id: int
    check_in_date: date
    check_out_date: date
    rooms_count: int = 1


class BookingResponse(BaseModel):
    """Response schema for booking data."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    hotel_id: int
    room_id: int
    user_id: int
    rooms_count: int
    check_in_date: date
    check_out_date: date
    booking_status: BookingStatus
    amount: Decimal
    created_at: datetime
    updated_at: datetime


class BookingDetailResponse(BaseModel):
    """Detailed booking response with guests."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    hotel_id: int
    room_id: int
    user_id: int
    rooms_count: int
    check_in_date: date
    check_out_date: date
    booking_status: BookingStatus
    amount: Decimal
    guests: List[GuestResponse] = []
    created_at: datetime
    updated_at: datetime


class BookingStatusResponse(BaseModel):
    """Response for booking status check."""
    booking_status: BookingStatus


class BookingPaymentResponse(BaseModel):
    """Response for payment initiation."""
    session_url: str


class HotelReportResponse(BaseModel):
    """Response for hotel booking report."""
    hotel_id: int
    total_bookings: int
    total_revenue: Decimal
    start_date: date
    end_date: date
