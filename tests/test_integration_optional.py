"""Optional integration tests.

Run with a live DecimerServerAPI instance listening on DECIMER_API_BASE_URL.
"""

import os

import pytest

from decimer_mcp_server.decimer_api_client import DecimerAPIClient


@pytest.mark.anyio
async def test_health_live() -> None:
    base_url = os.getenv("DECIMER_API_BASE_URL")
    if not base_url:
        pytest.skip("DECIMER_API_BASE_URL not set")

    client = DecimerAPIClient(
        base_url=base_url, timeout_seconds=5.0, max_image_bytes=1_000_000
    )
    result = await client.health()
    assert result.status_code in (200, 503, 504)
