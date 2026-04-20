"""Agno SDK adapter factory."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .adapter import AgnoAdapter


def create_adapter(settings: object) -> "AgnoAdapter":
    """Create an AgnoAdapter configured from application settings."""
    from .adapter import AgnoAdapter

    return AgnoAdapter(settings)
