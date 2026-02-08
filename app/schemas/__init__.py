# Schemas package
from app.schemas.user import (
    UserCreate, UserLogin, UserResponse, ProfileUpdate, LoginResponse, TokenData
)
from app.schemas.hotel import (
    HotelCreate, HotelUpdate, HotelResponse, HotelInfoResponse, HotelContactInfoSchema
)
from app.schemas.room import RoomCreate, RoomUpdate, RoomResponse
from app.schemas.booking import (
    BookingCreate, BookingResponse, BookingStatusResponse, BookingPaymentResponse, HotelReportResponse
)
from app.schemas.inventory import InventoryResponse, InventoryUpdate
from app.schemas.guest import GuestCreate, GuestUpdate, GuestResponse
from app.schemas.common import APIResponse

__all__ = [
    "UserCreate", "UserLogin", "UserResponse", "ProfileUpdate", "LoginResponse", "TokenData",
    "HotelCreate", "HotelUpdate", "HotelResponse", "HotelInfoResponse", "HotelContactInfoSchema",
    "RoomCreate", "RoomUpdate", "RoomResponse",
    "BookingCreate", "BookingResponse", "BookingStatusResponse", "BookingPaymentResponse", "HotelReportResponse",
    "InventoryResponse", "InventoryUpdate",
    "GuestCreate", "GuestUpdate", "GuestResponse",
    "APIResponse",
]
