from datetime import date
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Date, Enum as SQLAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from app.database import Base
from app.models.enums import Gender, Role

if TYPE_CHECKING:
    from app.models.hotel import Hotel
    from app.models.booking import Booking
    from app.models.guest import Guest


class User(Base):
    """User entity for authentication and profile management."""
    
    __tablename__ = "app_user"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    gender: Mapped[Optional[Gender]] = mapped_column(SQLAEnum(Gender), nullable=True)
    roles: Mapped[List[str]] = mapped_column(ARRAY(String), default=["GUEST"])
    
    # Relationships
    hotels: Mapped[List["Hotel"]] = relationship("Hotel", back_populates="owner")
    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="user")
    guests: Mapped[List["Guest"]] = relationship("Guest", back_populates="user")
    
    def has_role(self, role: Role) -> bool:
        """Check if user has a specific role."""
        return role.value in self.roles
