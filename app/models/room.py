from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.hotel import Hotel
    from app.models.inventory import Inventory


class Room(Base):
    """Room entity representing room types within a hotel."""

    __tablename__ = "room"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    base_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    photos: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    amenities: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    total_count: Mapped[int] = mapped_column(Integer, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Foreign keys
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"), nullable=False)

    # Relationships
    hotel: Mapped["Hotel"] = relationship("Hotel", back_populates="rooms")
    inventories: Mapped[list["Inventory"]] = relationship(
        "Inventory", back_populates="room", cascade="all, delete-orphan"
    )
