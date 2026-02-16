from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.hotel import Hotel


class HotelMinPrice(Base):
    """Tracks minimum room price for a hotel by date for search optimization."""

    __tablename__ = "hotel_min_price"
    __table_args__ = (UniqueConstraint("hotel_id", "date", name="unique_hotel_date"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Foreign keys
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"), nullable=False)

    # Relationships
    hotel: Mapped["Hotel"] = relationship("Hotel")
