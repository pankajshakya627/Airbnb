from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLAEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import Gender

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.user import User


class Guest(Base):
    """Guest entity representing a person staying in a booking."""

    __tablename__ = "guest"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    gender: Mapped[Gender] = mapped_column(SQLAEnum(Gender), nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey("app_user.id"), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="guests")
    bookings: Mapped[set["Booking"]] = relationship("Booking", secondary="booking_guest", back_populates="guests")
