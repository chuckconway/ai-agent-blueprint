"""Base response schemas for the API layer."""

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standard success response wrapper."""

    status: str = "ok"
    data: T


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str
    detail: str | None = None
