"""Dynamic adapter discovery and loading."""

import importlib
from typing import Any


def load_adapter(framework: str, settings: Any) -> Any:
    """Dynamically load an adapter by framework name.

    Looks for a create_adapter() function in app.agent.adapters.<framework>/

    Args:
        framework: Adapter framework name (e.g., "agno").
        settings: Application settings to pass to the adapter factory.

    Returns:
        An instantiated adapter for the given framework.

    Raises:
        ModuleNotFoundError: If the adapter module doesn't exist.
        AttributeError: If the module lacks a create_adapter function.
    """
    module = importlib.import_module(f"app.agent.adapters.{framework}")
    return module.create_adapter(settings)
