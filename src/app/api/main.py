"""FastAPI application factory and entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.core.exceptions import register_exception_handlers
from app.api.routes import auth, chat, health


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(title="AI Agent Blueprint")

    # CORS middleware for local frontend development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Domain exception → HTTP response mapping
    register_exception_handlers(app)

    # Routes
    app.include_router(health.router)  # /health (no prefix)
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

    return app


app = create_app()
