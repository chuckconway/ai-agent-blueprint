"""Development auth provider for local testing without external dependencies."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationError
from app.core.models.user import User
from app.core.repositories.user import UserRepository


class DevAuthProvider:
    """Development auth provider that accepts hardcoded credentials.

    Accepts dev@example.com / dev for frictionless local development.
    """

    async def authenticate(
        self, email: str, password: str, session: AsyncSession
    ) -> User:
        """Authenticate against hardcoded dev credentials.

        Creates the dev user on first login. Raises AuthenticationError
        if credentials don't match.
        """
        if email != "dev@example.com" or password != "dev":
            raise AuthenticationError("Invalid credentials")

        repo = UserRepository(session)
        user = await repo.get_by_email(email)
        if not user:
            user = User(
                email=email, display_name="Dev User", auth_provider="dev"
            )
            user = await repo.create(user)
            await session.commit()
        return user
