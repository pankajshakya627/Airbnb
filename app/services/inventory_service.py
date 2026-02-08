from typing import List
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update
from fastapi import HTTPException, status

from app.models.inventory import Inventory
from app.models.hotel import Hotel
from app.models.room import Room
from app.models.user import User
from app.schemas.inventory import InventoryResponse, InventoryUpdate


class InventoryService:
    """Service for inventory management operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_inventory_by_room(
        self, room_id: int, owner: User, start_date: date = None, end_date: date = None
    ) -> List[InventoryResponse]:
        """Get inventory for a room."""
        room = await self._get_room_with_ownership(room_id, owner)
        
        query = select(Inventory).where(Inventory.room_id == room_id)
        
        if start_date:
            query = query.where(Inventory.date >= start_date)
        if end_date:
            query = query.where(Inventory.date <= end_date)
        
        query = query.order_by(Inventory.date)
        
        result = await self.db.execute(query)
        inventories = result.scalars().all()
        
        return [InventoryResponse.model_validate(inv) for inv in inventories]
    
    async def update_inventory(
        self, room_id: int, update_data: InventoryUpdate, owner: User,
        start_date: date = None, end_date: date = None
    ) -> List[InventoryResponse]:
        """Update inventory for a room within date range."""
        room = await self._get_room_with_ownership(room_id, owner)
        
        if not start_date:
            start_date = date.today()
        if not end_date:
            end_date = start_date
        
        update_dict = {}
        if update_data.surge_factor is not None:
            update_dict["surge_factor"] = update_data.surge_factor
        if update_data.price is not None:
            update_dict["price"] = update_data.price
        if update_data.closed is not None:
            update_dict["closed"] = update_data.closed
        if update_data.total_count is not None:
            update_dict["total_count"] = update_data.total_count
        
        if update_dict:
            await self.db.execute(
                update(Inventory)
                .where(
                    and_(
                        Inventory.room_id == room_id,
                        Inventory.date >= start_date,
                        Inventory.date <= end_date
                    )
                )
                .values(**update_dict)
            )
        
        return await self.get_inventory_by_room(room_id, owner, start_date, end_date)
    
    async def _get_room_with_ownership(self, room_id: int, owner: User) -> Room:
        """Get room and verify ownership through hotel."""
        result = await self.db.execute(
            select(Room).where(Room.id == room_id)
        )
        room = result.scalar_one_or_none()
        
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Room not found: {room_id}"
            )
        
        # Verify hotel ownership
        result = await self.db.execute(
            select(Hotel).where(Hotel.id == room.hotel_id)
        )
        hotel = result.scalar_one_or_none()
        
        if not hotel or hotel.owner_id != owner.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        return room
