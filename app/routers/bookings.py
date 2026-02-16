from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingPaymentResponse, BookingResponse, BookingStatusResponse
from app.security.dependencies import get_current_user
from app.services.booking_service import BookingService
from app.services.checkout_service import CheckoutService

router = APIRouter(prefix="/bookings", tags=["Booking Flow"])


@router.post("/init", response_model=BookingResponse)
async def initialize_booking(
    booking_data: BookingCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Initialize a new booking reservation."""
    service = BookingService(db)
    return await service.initialise_booking(booking_data, current_user)


@router.post("/{booking_id}/addGuests", response_model=BookingResponse, tags=["Booking Guests"])
async def add_guests_to_booking(
    booking_id: int,
    guest_ids: list[int],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add guests to a booking."""
    service = BookingService(db)
    return await service.add_guests(booking_id, guest_ids, current_user)


@router.post("/{booking_id}/payments", response_model=BookingPaymentResponse)
async def initiate_payment(
    booking_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Initiate payment for a booking using Stripe."""
    service = CheckoutService(db)
    session_url = await service.create_checkout_session(booking_id, current_user)
    return BookingPaymentResponse(session_url=session_url)


@router.post("/{booking_id}/cancel", status_code=204)
async def cancel_booking(
    booking_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Cancel a booking."""
    service = BookingService(db)
    await service.cancel_booking(booking_id, current_user)


@router.get("/{booking_id}/status", response_model=BookingStatusResponse)
async def get_booking_status(
    booking_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Check the status of a booking."""
    service = BookingService(db)
    status = await service.get_booking_status(booking_id, current_user)
    return BookingStatusResponse(booking_status=status)
