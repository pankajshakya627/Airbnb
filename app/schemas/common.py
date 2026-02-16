from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""

    data: T | None = None
    success: bool = True
    message: str | None = None
    timestamp: str | None = None


class APIError(BaseModel):
    """API error response."""

    error: str
    status_code: int
    details: str | None = None
