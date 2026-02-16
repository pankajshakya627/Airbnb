from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.booking import Booking
from app.models.enums import BookingStatus
from app.models.guest import Guest
from app.models.hotel import Hotel
from app.models.inventory import Inventory
from app.models.room import Room
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingResponse, HotelReportResponse


class BookingService:
    """Service for booking operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def initialise_booking(self, booking_data: BookingCreate, user: User) -> BookingResponse:
        """Initialize a new booking reservation."""
        # Validate hotel and room
        hotel = await self._get_hotel(booking_data.hotel_id)
        room = await self._get_room(booking_data.room_id, booking_data.hotel_id)

        # Check availability and lock inventory
        inventories = await self._get_available_inventory(
            booking_data.room_id, booking_data.check_in_date, booking_data.check_out_date, booking_data.rooms_count
        )

        days_count = (booking_data.check_out_date - booking_data.check_in_date).days + 1
        if len(inventories) != days_count:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Room is not available for the selected dates"
            )

        # Reserve the rooms
        await self._reserve_inventory(
            booking_data.room_id, booking_data.check_in_date, booking_data.check_out_date, booking_data.rooms_count
        )

        # Calculate total price
        total_price = sum(inv.price for inv in inventories) * booking_data.rooms_count

        # Create booking
        booking = Booking(
            hotel_id=hotel.id,
            room_id=room.id,
            user_id=user.id,
            rooms_count=booking_data.rooms_count,
            check_in_date=booking_data.check_in_date,
            check_out_date=booking_data.check_out_date,
            booking_status=BookingStatus.RESERVED,
            amount=total_price,
        )

        self.db.add(booking)
        await self.db.flush()
        await self.db.refresh(booking)

        return BookingResponse.model_validate(booking)

    async def add_guests(self, booking_id: int, guest_ids: list[int], user: User) -> BookingResponse:
        """Add guests to a booking."""
        # Load booking with guests eagerly to avoid lazy-load in async context
        result = await self.db.execute(
            select(Booking)
            .options(selectinload(Booking.guests))
            .where(and_(Booking.id == booking_id, Booking.user_id == user.id))
        )
        booking = result.scalar_one_or_none()
        if not booking:
            raise HTTPException(status_code=404, detail=f"Booking not found: {booking_id}")

        # Get guests owned by user
        result = await self.db.execute(select(Guest).where(and_(Guest.id.in_(guest_ids), Guest.user_id == user.id)))
        guests = result.scalars().all()

        for guest in guests:
            booking.guests.add(guest)

        booking.booking_status = BookingStatus.GUESTS_ADDED

        await self.db.flush()
        await self.db.refresh(booking)

        return BookingResponse.model_validate(booking)

    async def get_booking_status(self, booking_id: int, user: User) -> BookingStatus:
        """Get booking status."""
        booking = await self._get_user_booking(booking_id, user)
        return booking.booking_status

    async def cancel_booking(self, booking_id: int, user: User) -> None:
        """Cancel a booking."""
        booking = await self._get_user_booking(booking_id, user)

        if booking.booking_status == BookingStatus.CONFIRMED:
            # Would need to handle refund via Stripe here
            pass

        # Release reserved inventory
        await self._release_inventory(
            booking.room_id, booking.check_in_date, booking.check_out_date, booking.rooms_count
        )

        booking.booking_status = BookingStatus.CANCELLED
        await self.db.flush()

    async def confirm_booking(self, booking_id: int) -> None:
        """Confirm booking after successful payment."""
        result = await self.db.execute(select(Booking).where(Booking.id == booking_id))
        booking = result.scalar_one_or_none()

        if booking:
            # Move from reserved to booked
            await self._confirm_inventory(
                booking.room_id, booking.check_in_date, booking.check_out_date, booking.rooms_count
            )
            booking.booking_status = BookingStatus.CONFIRMED
            await self.db.flush()

    async def get_all_bookings_by_hotel_id(self, hotel_id: int, owner: User) -> list[BookingResponse]:
        """Get all bookings for a hotel."""
        await self._verify_hotel_ownership(hotel_id, owner)

        result = await self.db.execute(select(Booking).where(Booking.hotel_id == hotel_id))
        bookings = result.scalars().all()
        return [BookingResponse.model_validate(b) for b in bookings]

    async def get_hotel_report(
        self, hotel_id: int, start_date: date, end_date: date, owner: User
    ) -> HotelReportResponse:
        """Generate hotel booking report."""
        await self._verify_hotel_ownership(hotel_id, owner)

        result = await self.db.execute(
            select(Booking).where(
                and_(
                    Booking.hotel_id == hotel_id,
                    Booking.booking_status == BookingStatus.CONFIRMED,
                    Booking.check_in_date >= start_date,
                    Booking.check_out_date <= end_date,
                )
            )
        )
        bookings = result.scalars().all()

        total_revenue = sum(b.amount for b in bookings)

        return HotelReportResponse(
            hotel_id=hotel_id,
            total_bookings=len(bookings),
            total_revenue=total_revenue,
            start_date=start_date,
            end_date=end_date,
        )

    async def get_user_bookings(self, user: User) -> list[BookingResponse]:
        """Get all bookings for a user."""
        result = await self.db.execute(select(Booking).where(Booking.user_id == user.id))
        bookings = result.scalars().all()
        return [BookingResponse.model_validate(b) for b in bookings]

    # Helper methods
    async def _get_hotel(self, hotel_id: int) -> Hotel:
        result = await self.db.execute(select(Hotel).where(Hotel.id == hotel_id))
        hotel = result.scalar_one_or_none()
        if not hotel:
            raise HTTPException(status_code=404, detail=f"Hotel not found: {hotel_id}")
        return hotel

    async def _get_room(self, room_id: int, hotel_id: int) -> Room:
        result = await self.db.execute(select(Room).where(and_(Room.id == room_id, Room.hotel_id == hotel_id)))
        room = result.scalar_one_or_none()
        if not room:
            raise HTTPException(status_code=404, detail=f"Room not found: {room_id}")
        return room

    async def _get_user_booking(self, booking_id: int, user: User) -> Booking:
        result = await self.db.execute(
            select(Booking).where(and_(Booking.id == booking_id, Booking.user_id == user.id))
        )
        booking = result.scalar_one_or_none()
        if not booking:
            raise HTTPException(status_code=404, detail=f"Booking not found: {booking_id}")
        return booking

    async def _verify_hotel_ownership(self, hotel_id: int, owner: User) -> None:
        result = await self.db.execute(select(Hotel).where(Hotel.id == hotel_id))
        hotel = result.scalar_one_or_none()
        if not hotel or hotel.owner_id != owner.id:
            raise HTTPException(status_code=403, detail="Access denied")

    async def _get_available_inventory(
        self, room_id: int, check_in: date, check_out: date, rooms_count: int
    ) -> list[Inventory]:
        result = await self.db.execute(
            select(Inventory).where(
                and_(
                    Inventory.room_id == room_id,
                    Inventory.date >= check_in,
                    Inventory.date <= check_out,
                    Inventory.closed == False,
                    (Inventory.total_count - Inventory.book_count - Inventory.reserved_count) >= rooms_count,
                )
            )
        )
        return list(result.scalars().all())

    async def _reserve_inventory(self, room_id: int, check_in: date, check_out: date, rooms_count: int) -> None:
        await self.db.execute(
            update(Inventory)
            .where(and_(Inventory.room_id == room_id, Inventory.date >= check_in, Inventory.date <= check_out))
            .values(reserved_count=Inventory.reserved_count + rooms_count)
        )

    async def _release_inventory(self, room_id: int, check_in: date, check_out: date, rooms_count: int) -> None:
        await self.db.execute(
            update(Inventory)
            .where(and_(Inventory.room_id == room_id, Inventory.date >= check_in, Inventory.date <= check_out))
            .values(reserved_count=Inventory.reserved_count - rooms_count)
        )

    async def _confirm_inventory(self, room_id: int, check_in: date, check_out: date, rooms_count: int) -> None:
        await self.db.execute(
            update(Inventory)
            .where(and_(Inventory.room_id == room_id, Inventory.date >= check_in, Inventory.date <= check_out))
            .values(
                reserved_count=Inventory.reserved_count - rooms_count, book_count=Inventory.book_count + rooms_count
            )
        )
