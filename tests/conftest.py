"""Shared test fixtures for the blueprint project."""

from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture()
def mock_db_session() -> AsyncMock:
    """Provide a mock async database session for unit tests.

    Supports: execute, commit, rollback, flush, add, delete, get, close.
    """
    session = AsyncMock(spec=AsyncSession)
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.flush = AsyncMock()
    session.add = AsyncMock()
    session.delete = AsyncMock()
    session.get = AsyncMock(return_value=None)
    session.close = AsyncMock()
    return session
