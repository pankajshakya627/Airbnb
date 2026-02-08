from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, composite
from sqlalchemy.dialects.postgresql import ARRAY
from dataclasses import dataclass

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.room import Room


@dataclass
class HotelContactInfo:
    """Embedded contact information for hotels."""
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class Hotel(Base):
    """Hotel entity representing a property."""
    
    __tablename__ = "hotel"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    photos: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
    amenities: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
    
    # Contact info as separate columns
    contact_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    
    # Foreign keys
    owner_id: Mapped[int] = mapped_column(ForeignKey("app_user.id"), nullable=False)
    
    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="hotels")
    rooms: Mapped[List["Room"]] = relationship(
        "Room", back_populates="hotel", cascade="all, delete-orphan"
    )
    
    @property
    def contact_info(self) -> HotelContactInfo:
        """Get contact info as embedded object."""
        return HotelContactInfo(
            phone=self.contact_phone,
            email=self.contact_email,
            address=self.contact_address
        )
