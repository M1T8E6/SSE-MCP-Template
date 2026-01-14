"""API v1 endpoints for SSE MCP Server.

This module contains the v1 API routes including health check and SSE endpoints.
"""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from mcp.server.sse import SseServerTransport

from sse_mcp_server.application.services import SystemHealthService
from sse_mcp_server.config.settings import settings
from sse_mcp_server.domain.protocols import HealthService
from sse_mcp_server.infrastructure.mcp_server import mcp_server

logger = logging.getLogger(__name__)

router = APIRouter()

# Create SSE transport with endpoint for POST messages
sse_transport = SseServerTransport(f"{settings.api_v1_str}/messages")


def get_health_service() -> HealthService:
    """Dependency provider for HealthService.

    Returns:
        HealthService: Health service instance
    """
    return SystemHealthService()


@router.get("/health")
async def health_check(
    service: Annotated[HealthService, Depends(get_health_service)],
) -> dict[str, str]:
    """Health check endpoint.

    Args:
        service: Health service dependency

    Returns:
        Dictionary with health status and version
    """
    health = await service.check_health()
    return {
        "status": str(health.get("status")),
        "version": str(health.get("version")),
        "environment": str(health.get("environment")),
    }


@router.get("/sse")
async def handle_sse(request: Request) -> Response:
    """Handle Server-Sent Events (SSE) connection.

    Establishes the SSE connection and manages the MCP server lifecycle.

    Args:
        request: FastAPI request object

    Returns:
        Empty response after connection closes
    """
    async with sse_transport.connect_sse(
        request.scope,
        request.receive,
        request._send,  # pyright: ignore[reportPrivateUsage]
    ) as streams:
        await mcp_server.run(
            streams[0], streams[1], mcp_server.create_initialization_options()
        )
    return Response()
