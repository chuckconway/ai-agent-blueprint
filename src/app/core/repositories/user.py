"""Repository for User aggregate root."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.user import User
from app.core.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for managing User entities."""

    model_class = User

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository with a database session."""
        super().__init__(session)

    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by email address, or None if not found."""
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
