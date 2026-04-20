"""Unit of Work pattern for scoping database transactions."""

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.engine import get_session_factory


class AsyncUnitOfWork:
    """Scopes a database transaction. Commits on clean exit, rolls back on exception."""

    def __init__(self) -> None:
        self.session: AsyncSession  # set in __aenter__

    async def __aenter__(self) -> "AsyncUnitOfWork":
        """Open a new session and begin a transaction."""
        factory = get_session_factory()
        self.session = factory()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        """Commit on success, rollback on exception, then close the session."""
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
        return False

    async def flush(self) -> None:
        """Flush pending changes to get generated IDs without committing."""
        await self.session.flush()
