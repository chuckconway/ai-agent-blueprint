"""Factory for selecting the appropriate auth provider based on configuration."""

from app.api.auth.dev_provider import DevAuthProvider
from app.api.auth.google_provider import GoogleOAuthProvider
from app.api.auth.protocol import AuthProvider
from app.core.config import Settings


def get_auth_provider(settings: Settings) -> AuthProvider:
    """Return the auth provider instance matching the configured auth_provider setting.

    Raises ValueError if the configured provider is unknown.
    """
    if settings.auth_provider == "dev":
        return DevAuthProvider()
    elif settings.auth_provider == "google":
        return GoogleOAuthProvider()
    else:
        raise ValueError(f"Unknown auth provider: {settings.auth_provider}")
