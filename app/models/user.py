from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, String
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.enums import Gender, Role

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.guest import Guest
    from app.models.hotel import Hotel


class User(Base):
    """User entity for authentication and profile management."""

    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    gender: Mapped[Gender | None] = mapped_column(SQLAEnum(Gender), nullable=True)
    roles: Mapped[list[str]] = mapped_column(ARRAY(String), default=["GUEST"])

    # Relationships
    hotels: Mapped[list["Hotel"]] = relationship("Hotel", back_populates="owner")
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="user")
    guests: Mapped[list["Guest"]] = relationship("Guest", back_populates="user")

    def has_role(self, role: Role) -> bool:
        """Check if user has a specific role."""
        return role.value in self.roles
