"""JWT token creation utilities."""

from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import Settings
from app.core.models.user import User


def create_jwt_token(user: User, settings: Settings) -> str:
    """Create a signed JWT token for the given user.

    The token includes the user's ID (sub), email, display name, and expiration.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_expire_minutes
    )
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "name": user.display_name,
        "exp": expire,
    }
    return jwt.encode(
        payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
