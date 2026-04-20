"""Generic base repository with common CRUD operations."""

from collections.abc import Sequence
from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """Base repository providing common CRUD operations for an aggregate root.

    Subclasses must set `model_class` to the SQLAlchemy model they manage.
    """

    model_class: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository with a database session."""
        self.session = session

    async def get_by_id(self, id: UUID) -> ModelT | None:
        """Retrieve an entity by its primary key, or None if not found."""
        return await self.session.get(self.model_class, id)

    async def get_all(self) -> Sequence[ModelT]:
        """Retrieve all entities of this type."""
        result = await self.session.execute(select(self.model_class))
        return result.scalars().all()

    async def create(self, entity: ModelT) -> ModelT:
        """Add a new entity to the session and flush to obtain generated values."""
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def delete(self, entity: ModelT) -> None:
        """Mark an entity for deletion and flush."""
        await self.session.delete(entity)
        await self.session.flush()
