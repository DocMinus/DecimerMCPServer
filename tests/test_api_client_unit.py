import base64

from decimer_mcp_server.decimer_api_client import DecimerAPIClient


def test_validate_image_size_allows_small_payload() -> None:
    client = DecimerAPIClient(
        base_url="http://localhost:8099",
        timeout_seconds=1.0,
        max_image_bytes=20,
    )
    encoded = base64.b64encode(b"12345").decode("utf-8")
    client._validate_image_size(encoded)


def test_validate_image_size_rejects_large_payload() -> None:
    client = DecimerAPIClient(
        base_url="http://localhost:8099",
        timeout_seconds=1.0,
        max_image_bytes=4,
    )
    encoded = base64.b64encode(b"12345").decode("utf-8")

    try:
        client._validate_image_size(encoded)
        assert False, "Expected ValueError for oversized image payload"
    except ValueError as exc:
        assert "exceeds limit" in str(exc)
