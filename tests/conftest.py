import asyncio
from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import get_settings
from app.database import Base, get_db
from app.main import app
from app.models.enums import Role
from app.security.jwt import create_access_token
from app.security.password import hash_password

# Test database URL - uses same database with test_ prefix
settings = get_settings()
TEST_DATABASE_URL = settings.DATABASE_URL.replace("/airbnb", "/airbnb_test")

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
)
TestAsyncSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestAsyncSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession):
    """Create a test user."""
    from app.models.user import User

    user = User(
        email="test@example.com", password=hash_password("testpassword123"), name="Test User", roles=[Role.GUEST.value]
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_hotel_manager(db_session: AsyncSession):
    """Create a test hotel manager."""
    from app.models.user import User

    user = User(
        email="manager@example.com",
        password=hash_password("managerpass123"),
        name="Hotel Manager",
        roles=[Role.GUEST.value, Role.HOTEL_MANAGER.value],
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def auth_headers(test_user):
    """Get auth headers for test user."""
    token = create_access_token(test_user.id, test_user.roles)
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def manager_auth_headers(test_hotel_manager):
    """Get auth headers for hotel manager."""
    token = create_access_token(test_hotel_manager.id, test_hotel_manager.roles)
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def test_hotel(db_session: AsyncSession, test_hotel_manager):
    """Create a test hotel."""
    from app.models.hotel import Hotel

    hotel = Hotel(
        name="Test Hotel",
        city="Test City",
        photos=["https://example.com/photo.jpg"],
        amenities=["wifi", "pool"],
        active=True,
        owner_id=test_hotel_manager.id,
        contact_phone="+1-555-0100",
        contact_email="hotel@test.com",
        contact_address="123 Test St",
    )
    db_session.add(hotel)
    await db_session.commit()
    await db_session.refresh(hotel)
    return hotel


@pytest_asyncio.fixture
async def test_room(db_session: AsyncSession, test_hotel):
    """Create a test room."""
    from app.models.room import Room

    room = Room(
        hotel_id=test_hotel.id,
        type="Deluxe",
        base_price=199.99,
        photos=["https://example.com/room.jpg"],
        amenities=["king_bed", "balcony"],
        total_count=5,
        capacity=2,
    )
    db_session.add(room)
    await db_session.commit()
    await db_session.refresh(room)
    return room


@pytest_asyncio.fixture
async def test_guest(db_session: AsyncSession, test_user):
    """Create a test guest."""
    from app.models.enums import Gender
    from app.models.guest import Guest

    guest = Guest(name="Test Guest", gender=Gender.MALE, age=30, user_id=test_user.id)
    db_session.add(guest)
    await db_session.commit()
    await db_session.refresh(guest)
    return guest
