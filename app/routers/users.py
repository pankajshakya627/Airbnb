from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.booking import BookingResponse
from app.schemas.guest import GuestCreate, GuestResponse, GuestUpdate
from app.schemas.user import ProfileUpdate, UserResponse
from app.security.dependencies import get_current_user
from app.services.booking_service import BookingService
from app.services.guest_service import GuestService
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["User Profile"])


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Get current user's profile."""
    service = UserService(db)
    return await service.get_profile(current_user)


@router.patch("/profile", response_model=UserResponse)
async def update_profile(
    update_data: ProfileUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """Update current user's profile."""
    service = UserService(db)
    return await service.update_profile(update_data, current_user)


@router.get("/myBookings", response_model=list[BookingResponse])
async def get_my_bookings(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Get all bookings for the current user."""
    service = BookingService(db)
    return await service.get_user_bookings(current_user)


# Guest management endpoints
@router.get("/guests", response_model=list[GuestResponse], tags=["Booking Guests"])
async def get_guests(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Get all saved guests for the current user."""
    service = GuestService(db)
    return await service.get_all_guests(current_user)


@router.post("/guests", response_model=GuestResponse, status_code=201, tags=["Booking Guests"])
async def create_guest(
    guest_data: GuestCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """Add a new guest."""
    service = GuestService(db)
    return await service.create_guest(guest_data, current_user)


@router.put("/guests/{guest_id}", response_model=GuestResponse, tags=["Booking Guests"])
async def update_guest(
    guest_id: int,
    guest_data: GuestUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a guest."""
    service = GuestService(db)
    return await service.update_guest(guest_id, guest_data, current_user)


@router.delete("/guests/{guest_id}", status_code=204, tags=["Booking Guests"])
async def delete_guest(
    guest_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """Delete a guest."""
    service = GuestService(db)
    await service.delete_guest(guest_id, current_user)
