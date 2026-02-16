# Schemas package
from app.schemas.booking import (
    BookingCreate,
    BookingPaymentResponse,
    BookingResponse,
    BookingStatusResponse,
    HotelReportResponse,
)
from app.schemas.common import APIResponse
from app.schemas.guest import GuestCreate, GuestResponse, GuestUpdate
from app.schemas.hotel import HotelContactInfoSchema, HotelCreate, HotelInfoResponse, HotelResponse, HotelUpdate
from app.schemas.inventory import InventoryResponse, InventoryUpdate
from app.schemas.room import RoomCreate, RoomResponse, RoomUpdate
from app.schemas.user import LoginResponse, ProfileUpdate, TokenData, UserCreate, UserLogin, UserResponse

__all__ = [
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "ProfileUpdate",
    "LoginResponse",
    "TokenData",
    "HotelCreate",
    "HotelUpdate",
    "HotelResponse",
    "HotelInfoResponse",
    "HotelContactInfoSchema",
    "RoomCreate",
    "RoomUpdate",
    "RoomResponse",
    "BookingCreate",
    "BookingResponse",
    "BookingStatusResponse",
    "BookingPaymentResponse",
    "HotelReportResponse",
    "InventoryResponse",
    "InventoryUpdate",
    "GuestCreate",
    "GuestUpdate",
    "GuestResponse",
    "APIResponse",
]
