"""Authentication routes for login and current-user retrieval."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.factory import get_auth_provider
from app.api.auth.jwt import create_jwt_token
from app.api.middleware.auth import UserContext, get_current_user
from app.core.config import get_settings
from app.core.database.engine import get_session

router = APIRouter()


class LoginRequest(BaseModel):
    """Credentials payload for the login endpoint."""

    email: str
    password: str


class LoginResponse(BaseModel):
    """Response returned on successful authentication."""

    access_token: str
    token_type: str = "bearer"
    user: dict


@router.post("/login")
async def login(
    request: LoginRequest, session: AsyncSession = Depends(get_session)
) -> LoginResponse:
    """Authenticate user credentials and return a JWT token."""
    settings = get_settings()
    provider = get_auth_provider(settings)
    user = await provider.authenticate(request.email, request.password, session)
    token = create_jwt_token(user, settings)
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user={
            "user_id": str(user.id),
            "email": user.email,
            "display_name": user.display_name,
        },
    )


@router.get("/me")
async def get_me(user: UserContext = Depends(get_current_user)) -> dict:
    """Get the currently authenticated user's info from their JWT."""
    return {
        "user_id": user.user_id,
        "email": user.email,
        "display_name": user.display_name,
    }
