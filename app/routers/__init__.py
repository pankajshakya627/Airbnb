# Routers package
from app.routers.auth import router as auth_router
from app.routers.bookings import router as bookings_router
from app.routers.browse import router as browse_router
from app.routers.hotels import router as hotels_router
from app.routers.inventory import router as inventory_router
from app.routers.rooms import router as rooms_router
from app.routers.users import router as users_router
from app.routers.webhooks import router as webhooks_router

__all__ = [
    "auth_router",
    "hotels_router",
    "rooms_router",
    "inventory_router",
    "bookings_router",
    "users_router",
    "browse_router",
    "webhooks_router",
]
