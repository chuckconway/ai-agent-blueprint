"""Domain exception hierarchy for the application."""


class DomainError(Exception):
    """Base for all domain exceptions."""

    def __init__(self, message: str, detail: str | None = None) -> None:
        self.message = message
        self.detail = detail
        super().__init__(message)


class ResourceNotFoundError(DomainError):
    """Raised when a requested resource does not exist."""

    ...


class DuplicateResourceError(DomainError):
    """Raised when attempting to create a resource that already exists."""

    ...


class ValidationError(DomainError):
    """Raised when input fails domain validation rules."""

    ...


class AuthenticationError(DomainError):
    """Raised when authentication credentials are invalid or missing."""

    ...


class AuthorizationError(DomainError):
    """Raised when the user lacks permission for the requested action."""

    ...


class ExternalServiceError(DomainError):
    """Raised when an external service call fails."""

    ...
