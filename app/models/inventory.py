from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.hotel import Hotel
    from app.models.room import Room


class Inventory(Base):
    """Inventory entity tracking room availability and pricing by date."""

    __tablename__ = "inventory"
    __table_args__ = (UniqueConstraint("hotel_id", "room_id", "date", name="unique_hotel_room_date"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    book_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reserved_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_count: Mapped[int] = mapped_column(Integer, nullable=False)
    surge_factor: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=1.0, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    closed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Foreign keys
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"), nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"), nullable=False)

    # Relationships
    hotel: Mapped["Hotel"] = relationship("Hotel")
    room: Mapped["Room"] = relationship("Room", back_populates="inventories")

    @property
    def available_count(self) -> int:
        """Calculate available rooms for this date."""
        return self.total_count - self.book_count - self.reserved_count
