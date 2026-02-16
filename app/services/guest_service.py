from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.guest import Guest
from app.models.user import User
from app.schemas.guest import GuestCreate, GuestResponse, GuestUpdate


class GuestService:
    """Service for guest management operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_guest(self, guest_data: GuestCreate, user: User) -> GuestResponse:
        """Create a new guest."""
        guest = Guest(name=guest_data.name, gender=guest_data.gender, age=guest_data.age, user_id=user.id)

        self.db.add(guest)
        await self.db.flush()
        await self.db.refresh(guest)

        return GuestResponse.model_validate(guest)

    async def get_all_guests(self, user: User) -> list[GuestResponse]:
        """Get all guests for a user."""
        result = await self.db.execute(select(Guest).where(Guest.user_id == user.id))
        guests = result.scalars().all()
        return [GuestResponse.model_validate(g) for g in guests]

    async def update_guest(self, guest_id: int, guest_data: GuestUpdate, user: User) -> GuestResponse:
        """Update a guest."""
        guest = await self._get_user_guest(guest_id, user)

        if guest_data.name is not None:
            guest.name = guest_data.name
        if guest_data.gender is not None:
            guest.gender = guest_data.gender
        if guest_data.age is not None:
            guest.age = guest_data.age

        await self.db.flush()
        await self.db.refresh(guest)

        return GuestResponse.model_validate(guest)

    async def delete_guest(self, guest_id: int, user: User) -> None:
        """Delete a guest."""
        guest = await self._get_user_guest(guest_id, user)
        await self.db.delete(guest)

    async def _get_user_guest(self, guest_id: int, user: User) -> Guest:
        """Get guest ensuring ownership."""
        result = await self.db.execute(select(Guest).where(Guest.id == guest_id, Guest.user_id == user.id))
        guest = result.scalar_one_or_none()

        if not guest:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Guest not found: {guest_id}")

        return guest
