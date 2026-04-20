"""Google OAuth2 auth provider (dormant until configured)."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationError
from app.core.models.user import User


class GoogleOAuthProvider:
    """Google OAuth2 provider.

    Set AUTH_PROVIDER=google and configure GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET
    to activate. Direct login is not supported; use the OAuth redirect flow.
    """

    async def authenticate(
        self, email: str, password: str, session: AsyncSession
    ) -> User:
        """Not supported for Google OAuth — use the redirect flow instead."""
        raise AuthenticationError(
            "Google OAuth requires redirect flow, not direct login"
        )

    async def handle_callback(self, code: str, session: AsyncSession) -> User:
        """Handle the OAuth callback by exchanging the code for user info.

        TODO: Implement when activating Google OAuth.
        """
        raise NotImplementedError(
            "Set AUTH_PROVIDER=google and configure Google credentials"
        )
