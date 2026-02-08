from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.enums import Role
from app.schemas.hotel import HotelCreate, HotelUpdate, HotelResponse
from app.schemas.booking import BookingResponse, HotelReportResponse
from app.services.hotel_service import HotelService
from app.services.booking_service import BookingService
from app.security.dependencies import get_current_user, require_role

router = APIRouter(prefix="/admin/hotels", tags=["Hotel Management"])


@router.post("", response_model=HotelResponse, status_code=201)
async def create_hotel(
    hotel_data: HotelCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([Role.HOTEL_MANAGER]))
):
    """Create a new hotel."""
    service = HotelService(db)
    return await service.create_hotel(hotel_data, current_user)


@router.get("", response_model=List[HotelResponse])
async def get_all_hotels(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([Role.HOTEL_MANAGER]))
):
    """Get all hotels owned by the current user."""
    service = HotelService(db)
    return await service.get_all_hotels(current_user)


@router.get("/{hotel_id}", response_model=HotelResponse)
async def get_hotel_by_id(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([Role.HOTEL_MANAGER]))
):
    """Get hotel details by ID."""
    service = HotelService(db)
    return await service.get_hotel_by_id(hotel_id, current_user)


@router.put("/{hotel_id}", response_model=HotelResponse)
async def update_hotel(
    hotel_id: int,
    hotel_data: HotelUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([Role.HOTEL_MANAGER]))
):
    """Update hotel details."""
    service = HotelService(db)
    return await service.update_hotel(hotel_id, hotel_data, current_user)


@router.delete("/{hotel_id}", status_code=204)
async def delete_hotel(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([Role.HOTEL_MANAGER]))
):
    """Delete a hotel."""
    service = HotelService(db)
    await service.delete_hotel(hotel_id, current_user)


@router.patch("/{hotel_id}/activate", status_code=204)
async def activate_hotel(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([Role.HOTEL_MANAGER]))
):
    """Activate a hotel to make it visible to guests."""
    service = HotelService(db)
    await service.activate_hotel(hotel_id, current_user)


@router.get("/{hotel_id}/bookings", response_model=List[BookingResponse], tags=["Booking Flow"])
async def get_hotel_bookings(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([Role.HOTEL_MANAGER]))
):
    """Get all bookings for a hotel."""
    service = BookingService(db)
    return await service.get_all_bookings_by_hotel_id(hotel_id, current_user)


@router.get("/{hotel_id}/reports", response_model=HotelReportResponse, tags=["Booking Flow"])
async def get_hotel_report(
    hotel_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([Role.HOTEL_MANAGER]))
):
    """Generate booking report for a hotel."""
    if start_date is None:
        start_date = date.today().replace(day=1)
    if end_date is None:
        end_date = date.today()
    
    service = BookingService(db)
    return await service.get_hotel_report(hotel_id, start_date, end_date, current_user)
