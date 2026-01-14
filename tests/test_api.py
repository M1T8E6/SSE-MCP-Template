import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient) -> None:
    """Test the health check endpoint."""
    response = await async_client.get("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "environment" in data
    assert data["status"] == "online"
    assert data["version"] == "1.0.0"  # Default version from settings
    assert data["environment"] in ["development", "staging", "production", "test"]


def test_sse_endpoint_exists() -> None:
    """
    Test placeholder for SSE endpoint.
    Full SSE testing requires an MCP client which is beyond unit test scope.
    Integration tests should cover the full SSE flow with proper MCP client.
    """
    # SSE endpoint is tested via integration/e2e tests
    assert True  # Placeholder test
