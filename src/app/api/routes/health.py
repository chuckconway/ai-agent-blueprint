"""Health check route for liveness probes."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict:
    """Return application health status."""
    return {"status": "ok"}
