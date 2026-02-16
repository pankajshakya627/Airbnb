from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.room import Room
    from app.models.user import User


@dataclass
class HotelContactInfo:
    """Embedded contact information for hotels."""

    phone: str | None = None
    email: str | None = None
    address: str | None = None


class Hotel(Base):
    """Hotel entity representing a property."""

    __tablename__ = "hotel"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    photos: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    amenities: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)

    # Contact info as separate columns
    contact_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_address: Mapped[str | None] = mapped_column(String(500), nullable=True)

    active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Foreign keys
    owner_id: Mapped[int] = mapped_column(ForeignKey("app_user.id"), nullable=False)

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="hotels")
    rooms: Mapped[list["Room"]] = relationship("Room", back_populates="hotel", cascade="all, delete-orphan")

    @property
    def contact_info(self) -> HotelContactInfo:
        """Get contact info as embedded object."""
        return HotelContactInfo(phone=self.contact_phone, email=self.contact_email, address=self.contact_address)
