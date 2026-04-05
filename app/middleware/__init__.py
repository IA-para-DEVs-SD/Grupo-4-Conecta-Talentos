"""Middleware do sistema."""

from app.middleware.error_handler import ErrorHandlerMiddleware, handle_exception

__all__ = ["ErrorHandlerMiddleware", "handle_exception"]
