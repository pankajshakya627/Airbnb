from typing import List, Optional
from datetime import date
from decimal import Decimal
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from pydantic import BaseModel, ConfigDict

from app.database import get_db
from app.models.hotel import Hotel
from app.models.room import Room
from app.models.inventory import Inventory
from app.schemas.hotel import HotelInfoResponse

router = APIRouter(prefix="/hotels", tags=["Hotel Browse"])


class HotelSearchResult(BaseModel):
    """Hotel search result with pricing."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    city: Optional[str] = None
    photos: Optional[List[str]] = None
    amenities: Optional[List[str]] = None
    min_price: Optional[Decimal] = None


@router.get("/search", response_model=List[HotelSearchResult])
async def search_hotels(
    city: str = Query(..., description="City to search hotels in"),
    check_in_date: date = Query(..., description="Check-in date"),
    check_out_date: date = Query(..., description="Check-out date"),
    rooms_count: int = Query(1, description="Number of rooms needed"),
    db: AsyncSession = Depends(get_db)
):
    """Search for available hotels in a city."""
    # Find hotels with available rooms for the given dates
    subquery = (
        select(
            Inventory.hotel_id,
            func.min(Inventory.price).label("min_price")
        )
        .where(
            and_(
                Inventory.city.ilike(f"%{city}%"),
                Inventory.date >= check_in_date,
                Inventory.date <= check_out_date,
                Inventory.closed == False,
                (Inventory.total_count - Inventory.book_count - Inventory.reserved_count) >= rooms_count
            )
        )
        .group_by(Inventory.hotel_id)
        .having(func.count(Inventory.id) >= (check_out_date - check_in_date).days + 1)
        .subquery()
    )
    
    result = await db.execute(
        select(Hotel, subquery.c.min_price)
        .join(subquery, Hotel.id == subquery.c.hotel_id)
        .where(Hotel.active == True)
    )
    
    hotels = []
    for hotel, min_price in result.all():
        hotels.append(HotelSearchResult(
            id=hotel.id,
            name=hotel.name,
            city=hotel.city,
            photos=hotel.photos,
            amenities=hotel.amenities,
            min_price=min_price
        ))
    
    return hotels


@router.get("/{hotel_id}/info", response_model=HotelInfoResponse)
async def get_hotel_info(
    hotel_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get public information about a hotel."""
    result = await db.execute(
        select(Hotel).where(and_(Hotel.id == hotel_id, Hotel.active == True))
    )
    hotel = result.scalar_one_or_none()
    
    if not hotel:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=404, detail="Hotel not found")
    
    return HotelInfoResponse.model_validate(hotel)
