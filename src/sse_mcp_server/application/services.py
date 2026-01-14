"""Application services implementing business logic."""

from datetime import datetime, timezone
from typing import Any

from sse_mcp_server.config.settings import settings
from sse_mcp_server.domain.protocols import HealthService


class SystemHealthService(HealthService):
    """Implementation of HealthService for system status."""

    async def check_health(self) -> dict[str, Any]:
        """Check system health status.

        Returns:
            Dictionary with status, version, and timestamp
        """
        return {
            "status": "online",
            "version": settings.version,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "environment": settings.environment.value,
        }
