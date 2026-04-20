# Vulture whitelist — add false-positive "unused" symbols here.
# Vulture scans for dead code but can't detect dynamic usage (e.g., ORM models
# referenced by SQLAlchemy, Pydantic validators, FastAPI dependency injection).
# List such symbols below so vulture stops reporting them.
#
# Example:
#   from app.core.database.models import User  # noqa
#   User.email  # attribute accessed dynamically by SQLAlchemy
