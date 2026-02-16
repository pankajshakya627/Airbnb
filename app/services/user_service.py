from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import ProfileUpdate, UserResponse


class UserService:
    """Service for user profile operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_profile(self, user: User) -> UserResponse:
        """Get user profile."""
        return UserResponse.model_validate(user)

    async def update_profile(self, update_data: ProfileUpdate, user: User) -> UserResponse:
        """Update user profile."""
        if update_data.name is not None:
            user.name = update_data.name
        if update_data.date_of_birth is not None:
            user.date_of_birth = update_data.date_of_birth
        if update_data.gender is not None:
            user.gender = update_data.gender

        await self.db.flush()
        await self.db.refresh(user)

        return UserResponse.model_validate(user)
