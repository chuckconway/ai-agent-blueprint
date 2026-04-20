"""JWT authentication middleware and dependencies for FastAPI."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.core.config import get_settings

security = HTTPBearer()


class UserContext:
    """Carries authenticated user info through the request lifecycle."""

    def __init__(self, user_id: str, email: str, display_name: str) -> None:
        """Initialize with user identity fields extracted from the JWT."""
        self.user_id = user_id
        self.email = email
        self.display_name = display_name


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UserContext:
    """FastAPI dependency that validates a JWT bearer token and returns UserContext.

    Raises HTTPException 401 if the token is invalid or expired.
    """
    settings = get_settings()
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return UserContext(
            user_id=payload["sub"],
            email=payload["email"],
            display_name=payload["name"],
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
