from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, LoginResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["User Authentication"])


@router.post("/signup", response_model=UserResponse, status_code=201)
async def signup(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user account."""
    service = AuthService(db)
    return await service.signup(user_data)


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return JWT access token."""
    service = AuthService(db)
    access_token, refresh_token = await service.login(login_data)
    
    # Set refresh token in HTTP-only cookie
    response.set_cookie(
        key="refreshToken",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax"
    )
    
    return LoginResponse(access_token=access_token)


@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(
    request_cookies: str = Depends(lambda request: request.cookies.get("refreshToken", "")),
    db: AsyncSession = Depends(get_db)
):
    """Generate new access token using refresh token from cookie."""
    from fastapi import HTTPException, status, Request
    
    service = AuthService(db)
    access_token = await service.refresh_token(request_cookies)
    return LoginResponse(access_token=access_token)
