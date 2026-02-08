from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, EmailStr


class HotelContactInfoSchema(BaseModel):
    """Schema for hotel contact information."""
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None


class HotelCreate(BaseModel):
    """Schema for creating a hotel."""
    name: str
    city: Optional[str] = None
    photos: Optional[List[str]] = None
    amenities: Optional[List[str]] = None
    contact_info: Optional[HotelContactInfoSchema] = None


class HotelUpdate(BaseModel):
    """Schema for updating a hotel."""
    name: Optional[str] = None
    city: Optional[str] = None
    photos: Optional[List[str]] = None
    amenities: Optional[List[str]] = None
    contact_info: Optional[HotelContactInfoSchema] = None


class HotelResponse(BaseModel):
    """Response schema for hotel data."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    city: Optional[str] = None
    photos: Optional[List[str]] = None
    amenities: Optional[List[str]] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    contact_address: Optional[str] = None
    active: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime


class HotelInfoResponse(BaseModel):
    """Public hotel info response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    city: Optional[str] = None
    photos: Optional[List[str]] = None
    amenities: Optional[List[str]] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    contact_address: Optional[str] = None
