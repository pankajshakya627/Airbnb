import enum


class Role(str, enum.Enum):
    """User roles for authorization."""
    GUEST = "GUEST"
    HOTEL_MANAGER = "HOTEL_MANAGER"


class Gender(str, enum.Enum):
    """Gender options."""
    MALE = "MALE"
    FEMALE = "FEMALE"


class BookingStatus(str, enum.Enum):
    """Booking status states."""
    RESERVED = "RESERVED"
    GUESTS_ADDED = "GUESTS_ADDED"
    PAYMENTS_PENDING = "PAYMENTS_PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class PaymentStatus(str, enum.Enum):
    """Payment status states."""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
