"""Example test demonstrating project test patterns."""

import pytest


@pytest.mark.unit
def test_blueprint_runs() -> None:
    """Verify the test infrastructure works."""
    assert True


@pytest.mark.unit
def test_config_loads() -> None:
    """Verify settings can be instantiated."""
    from app.core.config import Settings

    settings = Settings()
    assert settings.app_name == "AI Agent Blueprint"
    assert settings.auth_provider == "dev"


@pytest.mark.unit
def test_domain_exceptions() -> None:
    """Verify domain exception hierarchy."""
    from app.core.exceptions import (
        AuthenticationError,
        DomainError,
        ResourceNotFoundError,
    )

    assert issubclass(ResourceNotFoundError, DomainError)
    assert issubclass(AuthenticationError, DomainError)

    exc = ResourceNotFoundError("User not found", detail="id=123")
    assert exc.message == "User not found"
    assert exc.detail == "id=123"
