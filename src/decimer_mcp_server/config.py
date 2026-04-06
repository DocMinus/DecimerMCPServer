from __future__ import annotations

import os


def _get_env_str(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return value.strip()


def _get_env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(f"Environment variable {name} must be an integer") from exc
    if parsed <= 0:
        raise ValueError(f"Environment variable {name} must be greater than 0")
    return parsed


def _get_env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ValueError(f"Environment variable {name} must be a float") from exc
    if parsed <= 0:
        raise ValueError(f"Environment variable {name} must be greater than 0")
    return parsed


class Settings:
    def __init__(self) -> None:
        self.decimer_api_base_url = _get_env_str(
            "DECIMER_API_BASE_URL", "http://localhost:8099"
        )
        self.decimer_api_timeout_seconds = _get_env_float(
            "DECIMER_API_TIMEOUT_SECONDS", 60.0
        )
        self.decimer_max_image_bytes = _get_env_int(
            "DECIMER_MAX_IMAGE_BYTES", 10_000_000
        )
        self.decimer_mcp_log_level = _get_env_str("DECIMER_MCP_LOG_LEVEL", "INFO")


settings = Settings()
