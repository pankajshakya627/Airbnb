from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""
    data: Optional[T] = None
    success: bool = True
    message: Optional[str] = None
    timestamp: Optional[str] = None


class APIError(BaseModel):
    """API error response."""
    error: str
    status_code: int
    details: Optional[str] = None
