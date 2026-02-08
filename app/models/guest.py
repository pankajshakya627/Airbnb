from typing import Optional, Set, TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Enum as SQLAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import Gender

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.booking import Booking


class Guest(Base):
    """Guest entity representing a person staying in a booking."""
    
    __tablename__ = "guest"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    gender: Mapped[Gender] = mapped_column(SQLAEnum(Gender), nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey("app_user.id"), nullable=False)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="guests")
    bookings: Mapped[Set["Booking"]] = relationship(
        "Booking", secondary="booking_guest", back_populates="guests"
    )
