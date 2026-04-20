"""Application configuration via environment variables and .env file."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for the AI Agent Blueprint application.

    Values are loaded from environment variables and .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # App
    app_name: str = "AI Agent Blueprint"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://app:app@localhost:5432/app"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Auth
    auth_provider: str = "dev"  # "dev" or "google"
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24  # 24 hours

    # Google OAuth (dormant by default)
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/api/auth/google/callback"

    # LLM
    llm_provider: str = "anthropic"  # anthropic, openai, google
    llm_model: str = "claude-sonnet-4-20250514"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    google_api_key: str = ""


def get_settings() -> Settings:
    """Return the application settings singleton."""
    return Settings()
