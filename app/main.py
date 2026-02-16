from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.exceptions.handlers import register_exception_handlers
from app.routers import (
    auth_router,
    bookings_router,
    browse_router,
    hotels_router,
    inventory_router,
    rooms_router,
    users_router,
    webhooks_router,
)

settings = get_settings()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="AirBnb Backend API",
        description="Backend API for hotel management, booking flow, and user authentication",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register exception handlers
    register_exception_handlers(app)

    # Register routers
    app.include_router(auth_router)
    app.include_router(hotels_router)
    app.include_router(rooms_router)
    app.include_router(inventory_router)
    app.include_router(bookings_router)
    app.include_router(users_router)
    app.include_router(browse_router)
    app.include_router(webhooks_router)

    @app.get("/", tags=["Health"])
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "message": "AirBnb API is running"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
