"""Auth provider protocol defining the authentication contract."""

from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.user import User


class AuthProvider(Protocol):
    """Protocol that all auth providers must implement."""

    async def authenticate(
        self, email: str, password: str, session: AsyncSession
    ) -> User:
        """Authenticate user credentials and return the User entity.

        Raises AuthenticationError on failure.
        """
        ...
