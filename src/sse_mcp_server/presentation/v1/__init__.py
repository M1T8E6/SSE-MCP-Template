"""Presentation layer - API endpoints and HTTP handling."""

from .api import get_message_handler, router

__all__ = ["get_message_handler", "router"]
