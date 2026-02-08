from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.enums import Role
from app.schemas.inventory import InventoryResponse, InventoryUpdate
from app.services.inventory_service import InventoryService
from app.security.dependencies import require_role

router = APIRouter(prefix="/admin/inventory", tags=["Admin Inventory"])


@router.get("/rooms/{room_id}", response_model=List[InventoryResponse])
async def get_room_inventory(
    room_id: int,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([Role.HOTEL_MANAGER]))
):
    """Get inventory for a room."""
    service = InventoryService(db)
    return await service.get_inventory_by_room(room_id, current_user, start_date, end_date)


@router.patch("/rooms/{room_id}", response_model=List[InventoryResponse])
async def update_room_inventory(
    room_id: int,
    update_data: InventoryUpdate,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([Role.HOTEL_MANAGER]))
):
    """Update inventory for a room within a date range."""
    service = InventoryService(db)
    return await service.update_inventory(room_id, update_data, current_user, start_date, end_date)
