from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hotel import Hotel
from app.models.user import User
from app.schemas.hotel import HotelCreate, HotelResponse, HotelUpdate


class HotelService:
    """Service for hotel management operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_hotel(self, hotel_data: HotelCreate, owner: User) -> HotelResponse:
        """Create a new hotel."""
        hotel = Hotel(
            name=hotel_data.name,
            city=hotel_data.city,
            photos=hotel_data.photos,
            amenities=hotel_data.amenities,
            active=False,
            owner_id=owner.id,
        )

        if hotel_data.contact_info:
            hotel.contact_phone = hotel_data.contact_info.phone
            hotel.contact_email = hotel_data.contact_info.email
            hotel.contact_address = hotel_data.contact_info.address

        self.db.add(hotel)
        await self.db.flush()
        await self.db.refresh(hotel)

        return HotelResponse.model_validate(hotel)

    async def get_hotel_by_id(self, hotel_id: int, owner: User) -> HotelResponse:
        """Get hotel by ID (must be owned by user)."""
        hotel = await self._get_owned_hotel(hotel_id, owner)
        return HotelResponse.model_validate(hotel)

    async def get_all_hotels(self, owner: User) -> list[HotelResponse]:
        """Get all hotels owned by user."""
        result = await self.db.execute(select(Hotel).where(Hotel.owner_id == owner.id))
        hotels = result.scalars().all()
        return [HotelResponse.model_validate(h) for h in hotels]

    async def update_hotel(self, hotel_id: int, hotel_data: HotelUpdate, owner: User) -> HotelResponse:
        """Update hotel details."""
        hotel = await self._get_owned_hotel(hotel_id, owner)

        if hotel_data.name is not None:
            hotel.name = hotel_data.name
        if hotel_data.city is not None:
            hotel.city = hotel_data.city
        if hotel_data.photos is not None:
            hotel.photos = hotel_data.photos
        if hotel_data.amenities is not None:
            hotel.amenities = hotel_data.amenities
        if hotel_data.contact_info:
            if hotel_data.contact_info.phone is not None:
                hotel.contact_phone = hotel_data.contact_info.phone
            if hotel_data.contact_info.email is not None:
                hotel.contact_email = hotel_data.contact_info.email
            if hotel_data.contact_info.address is not None:
                hotel.contact_address = hotel_data.contact_info.address

        await self.db.flush()
        await self.db.refresh(hotel)

        return HotelResponse.model_validate(hotel)

    async def delete_hotel(self, hotel_id: int, owner: User) -> None:
        """Delete a hotel."""
        hotel = await self._get_owned_hotel(hotel_id, owner)
        await self.db.delete(hotel)

    async def activate_hotel(self, hotel_id: int, owner: User) -> None:
        """Activate a hotel."""
        hotel = await self._get_owned_hotel(hotel_id, owner)
        hotel.active = True
        await self.db.flush()

    async def _get_owned_hotel(self, hotel_id: int, owner: User) -> Hotel:
        """Get hotel ensuring ownership."""
        result = await self.db.execute(select(Hotel).where(Hotel.id == hotel_id))
        hotel = result.scalar_one_or_none()

        if not hotel:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel not found with id: {hotel_id}")

        if hotel.owner_id != owner.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't own this hotel")

        return hotel
