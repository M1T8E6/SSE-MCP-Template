# pylint: disable=import-error

from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from sse_mcp_server.main import app


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Fixture for async HTTP client."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Fixture for synchronous TestClient."""
    with TestClient(app) as c:
        yield c
