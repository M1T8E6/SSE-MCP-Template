"""Domain protocols (interfaces) for dependency inversion.

This module defines the contracts that application and infrastructure
layers must implement.
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class HealthService(Protocol):
    """Protocol for health check services."""

    async def check_health(self) -> dict[str, Any]:
        """Perform a health check.

        Returns:
            Dictionary with health status information
        """
        return {}
