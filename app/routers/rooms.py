from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.enums import Role
from app.schemas.room import RoomCreate, RoomUpdate, RoomResponse
from app.services.room_service import RoomService
from app.security.dependencies import require_role

router = APIRouter(prefix="/admin/hotels/{hotel_id}/rooms", tags=["Room Admin Management"])


@router.post("", response_model=RoomResponse, status_code=201)
async def create_room(
    hotel_id: int,
    room_data: RoomCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([Role.HOTEL_MANAGER]))
):
    """Create a new room in a hotel."""
    service = RoomService(db)
    return await service.create_room(hotel_id, room_data, current_user)


@router.get("", response_model=List[RoomResponse])
async def get_all_rooms(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([Role.HOTEL_MANAGER]))
):
    """Get all rooms for a hotel."""
    service = RoomService(db)
    return await service.get_all_rooms(hotel_id, current_user)


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room_by_id(
    hotel_id: int,
    room_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([Role.HOTEL_MANAGER]))
):
    """Get room details."""
    service = RoomService(db)
    return await service.get_room_by_id(hotel_id, room_id, current_user)


@router.put("/{room_id}", response_model=RoomResponse)
async def update_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([Role.HOTEL_MANAGER]))
):
    """Update room details."""
    service = RoomService(db)
    return await service.update_room(hotel_id, room_id, room_data, current_user)


@router.delete("/{room_id}", status_code=204)
async def delete_room(
    hotel_id: int,
    room_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([Role.HOTEL_MANAGER]))
):
    """Delete a room."""
    service = RoomService(db)
    await service.delete_room(hotel_id, room_id, current_user)
