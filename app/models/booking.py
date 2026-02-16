from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Table
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import BookingStatus

if TYPE_CHECKING:
    from app.models.guest import Guest
    from app.models.hotel import Hotel
    from app.models.room import Room
    from app.models.user import User


# Association table for many-to-many relationship between Booking and Guest
booking_guest = Table(
    "booking_guest",
    Base.metadata,
    Column("booking_id", Integer, ForeignKey("booking.id"), primary_key=True),
    Column("guest_id", Integer, ForeignKey("guest.id"), primary_key=True),
)


class Booking(Base):
    """Booking entity representing a reservation."""

    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    rooms_count: Mapped[int] = mapped_column(Integer, nullable=False)
    check_in_date: Mapped[date] = mapped_column(Date, nullable=False)
    check_out_date: Mapped[date] = mapped_column(Date, nullable=False)
    booking_status: Mapped[BookingStatus] = mapped_column(
        SQLAEnum(BookingStatus), default=BookingStatus.RESERVED, nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    payment_session_id: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Foreign keys
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"), nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("app_user.id"), nullable=False)

    # Relationships
    hotel: Mapped["Hotel"] = relationship("Hotel")
    room: Mapped["Room"] = relationship("Room")
    user: Mapped["User"] = relationship("User", back_populates="bookings")
    guests: Mapped[set["Guest"]] = relationship("Guest", secondary=booking_guest, back_populates="bookings")
