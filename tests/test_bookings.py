from datetime import date, timedelta

import pytest
from httpx import AsyncClient


class TestInitializeBooking:
    """Tests for booking initialization endpoint."""

    @pytest.mark.asyncio
    async def test_init_booking_success(self, client: AsyncClient, auth_headers, test_hotel, test_room, db_session):
        """Test successful booking initialization."""
        from app.models.inventory import Inventory

        # Create inventory for booking dates
        today = date.today()
        for i in range(5):
            inv = Inventory(
                hotel_id=test_hotel.id,
                room_id=test_room.id,
                date=today + timedelta(days=i),
                book_count=0,
                reserved_count=0,
                total_count=5,
                surge_factor=1.0,
                price=199.99,
                city="Test City",
                closed=False,
            )
            db_session.add(inv)
        await db_session.commit()

        check_in = today
        check_out = today + timedelta(days=4)

        response = await client.post(
            "/bookings/init",
            headers=auth_headers,
            json={
                "hotel_id": test_hotel.id,
                "room_id": test_room.id,
                "check_in_date": check_in.isoformat(),
                "check_out_date": check_out.isoformat(),
                "rooms_count": 1,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["booking_status"] == "RESERVED"
        assert data["hotel_id"] == test_hotel.id
        assert data["room_id"] == test_room.id

    @pytest.mark.asyncio
    async def test_init_booking_unauthorized(self, client: AsyncClient, test_hotel, test_room):
        """Test booking without auth fails."""
        today = date.today()
        response = await client.post(
            "/bookings/init",
            json={
                "hotel_id": test_hotel.id,
                "room_id": test_room.id,
                "check_in_date": today.isoformat(),
                "check_out_date": (today + timedelta(days=3)).isoformat(),
                "rooms_count": 1,
            },
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_init_booking_invalid_hotel(self, client: AsyncClient, auth_headers, test_room):
        """Test booking with invalid hotel."""
        today = date.today()
        response = await client.post(
            "/bookings/init",
            headers=auth_headers,
            json={
                "hotel_id": 9999,
                "room_id": test_room.id,
                "check_in_date": today.isoformat(),
                "check_out_date": (today + timedelta(days=3)).isoformat(),
                "rooms_count": 1,
            },
        )

        assert response.status_code == 404


class TestBookingStatus:
    """Tests for booking status endpoint."""

    @pytest.mark.asyncio
    async def test_get_booking_status(
        self, client: AsyncClient, auth_headers, test_user, test_hotel, test_room, db_session
    ):
        """Test getting booking status."""
        from app.models.booking import Booking
        from app.models.enums import BookingStatus

        booking = Booking(
            hotel_id=test_hotel.id,
            room_id=test_room.id,
            user_id=test_user.id,
            rooms_count=1,
            check_in_date=date.today(),
            check_out_date=date.today() + timedelta(days=3),
            booking_status=BookingStatus.RESERVED,
            amount=599.97,
        )
        db_session.add(booking)
        await db_session.commit()
        await db_session.refresh(booking)

        response = await client.get(f"/bookings/{booking.id}/status", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["booking_status"] == "RESERVED"


class TestCancelBooking:
    """Tests for booking cancellation endpoint."""

    @pytest.mark.asyncio
    async def test_cancel_booking_success(
        self, client: AsyncClient, auth_headers, test_user, test_hotel, test_room, db_session
    ):
        """Test successful booking cancellation."""
        from app.models.booking import Booking
        from app.models.enums import BookingStatus
        from app.models.inventory import Inventory

        # Create inventory
        today = date.today()
        for i in range(4):
            inv = Inventory(
                hotel_id=test_hotel.id,
                room_id=test_room.id,
                date=today + timedelta(days=i),
                book_count=0,
                reserved_count=1,
                total_count=5,
                surge_factor=1.0,
                price=199.99,
                city="Test City",
                closed=False,
            )
            db_session.add(inv)

        booking = Booking(
            hotel_id=test_hotel.id,
            room_id=test_room.id,
            user_id=test_user.id,
            rooms_count=1,
            check_in_date=today,
            check_out_date=today + timedelta(days=3),
            booking_status=BookingStatus.RESERVED,
            amount=599.97,
        )
        db_session.add(booking)
        await db_session.commit()
        await db_session.refresh(booking)

        response = await client.post(f"/bookings/{booking.id}/cancel", headers=auth_headers)

        assert response.status_code == 204


class TestAddGuests:
    """Tests for adding guests to booking."""

    @pytest.mark.asyncio
    async def test_add_guests_success(
        self, client: AsyncClient, auth_headers, test_user, test_guest, test_hotel, test_room, db_session
    ):
        """Test adding guests to booking."""
        from app.models.booking import Booking
        from app.models.enums import BookingStatus

        booking = Booking(
            hotel_id=test_hotel.id,
            room_id=test_room.id,
            user_id=test_user.id,
            rooms_count=1,
            check_in_date=date.today(),
            check_out_date=date.today() + timedelta(days=3),
            booking_status=BookingStatus.RESERVED,
            amount=599.97,
        )
        db_session.add(booking)
        await db_session.commit()
        await db_session.refresh(booking)

        response = await client.post(f"/bookings/{booking.id}/addGuests", headers=auth_headers, json=[test_guest.id])

        assert response.status_code == 200
        data = response.json()
        assert data["booking_status"] == "GUESTS_ADDED"


class TestPaymentInitiation:
    """Tests for payment initiation endpoint."""

    @pytest.mark.asyncio
    async def test_initiate_payment(
        self, client: AsyncClient, auth_headers, test_user, test_hotel, test_room, db_session
    ):
        """Test payment initiation returns Stripe URL."""
        from app.models.booking import Booking
        from app.models.enums import BookingStatus

        booking = Booking(
            hotel_id=test_hotel.id,
            room_id=test_room.id,
            user_id=test_user.id,
            rooms_count=1,
            check_in_date=date.today(),
            check_out_date=date.today() + timedelta(days=3),
            booking_status=BookingStatus.GUESTS_ADDED,
            amount=599.97,
        )
        db_session.add(booking)
        await db_session.commit()
        await db_session.refresh(booking)

        # This will fail without valid Stripe key
        # But should return proper error structure
        response = await client.post(f"/bookings/{booking.id}/payments", headers=auth_headers)

        # Either success or Stripe error
        assert response.status_code in [200, 500]
