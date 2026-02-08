from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User
from app.models.enums import Role
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.security.password import hash_password, verify_password
from app.security.jwt import create_access_token, create_refresh_token, verify_token


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def signup(self, user_data: UserCreate) -> UserResponse:
        """Register a new user."""
        # Check if email already exists
        result = await self.db.execute(
            select(User).where(User.email == user_data.email)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        user = User(
            email=user_data.email,
            password=hash_password(user_data.password),
            name=user_data.name,
            roles=[Role.GUEST.value]
        )
        
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        
        return UserResponse.model_validate(user)
    
    async def login(self, login_data: UserLogin) -> tuple[str, str]:
        """Authenticate user and return tokens."""
        result = await self.db.execute(
            select(User).where(User.email == login_data.email)
        )
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        access_token = create_access_token(user.id, user.roles)
        refresh_token = create_refresh_token(user.id)
        
        return access_token, refresh_token
    
    async def refresh_token(self, refresh_token: str) -> str:
        """Generate new access token from refresh token."""
        payload = verify_token(refresh_token, token_type="refresh")
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id = int(payload.get("sub"))
        
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return create_access_token(user.id, user.roles)
