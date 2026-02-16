from datetime import date, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hotel import Hotel
from app.models.inventory import Inventory
from app.models.room import Room
from app.models.user import User
from app.schemas.room import RoomCreate, RoomResponse, RoomUpdate


class RoomService:
    """Service for room management operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_room(self, hotel_id: int, room_data: RoomCreate, owner: User) -> RoomResponse:
        """Create a new room and generate inventory for 1 year."""
        hotel = await self._get_owned_hotel(hotel_id, owner)

        room = Room(
            hotel_id=hotel.id,
            type=room_data.type,
            base_price=room_data.base_price,
            photos=room_data.photos,
            amenities=room_data.amenities,
            total_count=room_data.total_count,
            capacity=room_data.capacity,
        )

        self.db.add(room)
        await self.db.flush()
        await self.db.refresh(room)

        # Generate inventory for the next 365 days
        await self._create_inventory_for_room(room, hotel)

        return RoomResponse.model_validate(room)

    async def get_room_by_id(self, hotel_id: int, room_id: int, owner: User) -> RoomResponse:
        """Get room by ID."""
        await self._get_owned_hotel(hotel_id, owner)
        room = await self._get_room(room_id, hotel_id)
        return RoomResponse.model_validate(room)

    async def get_all_rooms(self, hotel_id: int, owner: User) -> list[RoomResponse]:
        """Get all rooms for a hotel."""
        await self._get_owned_hotel(hotel_id, owner)

        result = await self.db.execute(select(Room).where(Room.hotel_id == hotel_id))
        rooms = result.scalars().all()
        return [RoomResponse.model_validate(r) for r in rooms]

    async def update_room(self, hotel_id: int, room_id: int, room_data: RoomUpdate, owner: User) -> RoomResponse:
        """Update room details."""
        await self._get_owned_hotel(hotel_id, owner)
        room = await self._get_room(room_id, hotel_id)

        if room_data.type is not None:
            room.type = room_data.type
        if room_data.base_price is not None:
            room.base_price = room_data.base_price
        if room_data.photos is not None:
            room.photos = room_data.photos
        if room_data.amenities is not None:
            room.amenities = room_data.amenities
        if room_data.total_count is not None:
            room.total_count = room_data.total_count
        if room_data.capacity is not None:
            room.capacity = room_data.capacity

        await self.db.flush()
        await self.db.refresh(room)

        return RoomResponse.model_validate(room)

    async def delete_room(self, hotel_id: int, room_id: int, owner: User) -> None:
        """Delete a room."""
        await self._get_owned_hotel(hotel_id, owner)
        room = await self._get_room(room_id, hotel_id)
        await self.db.delete(room)

    async def _get_owned_hotel(self, hotel_id: int, owner: User) -> Hotel:
        """Get hotel ensuring ownership."""
        result = await self.db.execute(select(Hotel).where(Hotel.id == hotel_id))
        hotel = result.scalar_one_or_none()

        if not hotel:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel not found with id: {hotel_id}")

        if hotel.owner_id != owner.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't own this hotel")

        return hotel

    async def _get_room(self, room_id: int, hotel_id: int) -> Room:
        """Get room by ID."""
        result = await self.db.execute(select(Room).where(Room.id == room_id, Room.hotel_id == hotel_id))
        room = result.scalar_one_or_none()

        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room not found with id: {room_id}")

        return room

    async def _create_inventory_for_room(self, room: Room, hotel: Hotel) -> None:
        """Create inventory entries for the next 365 days."""
        today = date.today()
        city = hotel.city or ""

        inventories = []
        for i in range(365):
            inv_date = today + timedelta(days=i)
            inventory = Inventory(
                hotel_id=hotel.id,
                room_id=room.id,
                date=inv_date,
                book_count=0,
                reserved_count=0,
                total_count=room.total_count,
                surge_factor=1.0,
                price=room.base_price,
                city=city,
                closed=False,
            )
            inventories.append(inventory)

        self.db.add_all(inventories)
        await self.db.flush()
