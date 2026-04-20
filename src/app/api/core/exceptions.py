"""Map domain exceptions to HTTP responses."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
    DuplicateResourceError,
    ExternalServiceError,
    ResourceNotFoundError,
    ValidationError,
)


def register_exception_handlers(app: FastAPI) -> None:
    """Register domain exception handlers with the FastAPI application."""

    @app.exception_handler(ResourceNotFoundError)
    async def not_found_handler(
        request: Request, exc: ResourceNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"error": exc.message, "detail": exc.detail},
        )

    @app.exception_handler(AuthenticationError)
    async def authentication_handler(
        request: Request, exc: AuthenticationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={"error": exc.message, "detail": exc.detail},
        )

    @app.exception_handler(AuthorizationError)
    async def authorization_handler(
        request: Request, exc: AuthorizationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=403,
            content={"error": exc.message, "detail": exc.detail},
        )

    @app.exception_handler(DuplicateResourceError)
    async def duplicate_handler(
        request: Request, exc: DuplicateResourceError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"error": exc.message, "detail": exc.detail},
        )

    @app.exception_handler(ValidationError)
    async def validation_handler(
        request: Request, exc: ValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"error": exc.message, "detail": exc.detail},
        )

    @app.exception_handler(ExternalServiceError)
    async def external_service_handler(
        request: Request, exc: ExternalServiceError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=502,
            content={"error": exc.message, "detail": exc.detail},
        )
