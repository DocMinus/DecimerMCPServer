from __future__ import annotations

import argparse
import asyncio
import base64
import os
from pathlib import Path

from .decimer_api_client import DecimerAPIClient


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a DECIMER API smoke test with one image."
    )
    parser.add_argument(
        "--image",
        required=True,
        help="Path to an image file to send to /image2smiles/",
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("DECIMER_API_BASE_URL", "http://localhost:8099"),
        help="DECIMER API base URL (default: DECIMER_API_BASE_URL or http://localhost:8099)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="HTTP timeout in seconds (default: 60)",
    )
    parser.add_argument(
        "--max-image-bytes",
        type=int,
        default=10_000_000,
        help="Maximum decoded image bytes (default: 10000000)",
    )
    parser.add_argument(
        "--is-hand-drawn",
        action="store_true",
        help="Set hand-drawn mode for DECIMER",
    )
    parser.add_argument(
        "--no-classify",
        action="store_true",
        help="Disable classifier pre-check",
    )
    return parser.parse_args()


async def run() -> int:
    args = parse_args()
    image_path = Path(args.image)
    if not image_path.exists() or not image_path.is_file():
        print(f"ERROR: Image path not found or not a file: {image_path}")
        return 2

    encoded_image = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    client = DecimerAPIClient(
        base_url=args.base_url,
        timeout_seconds=args.timeout,
        max_image_bytes=args.max_image_bytes,
    )

    health = await client.health()
    print(f"health.ok={health.ok} status={health.status_code} message={health.message}")
    if not health.ok:
        return 1

    result = await client.image_to_smiles(
        encoded_image=encoded_image,
        is_hand_drawn=args.is_hand_drawn,
        classify_image=not args.no_classify,
    )
    print(
        "inference."
        f"ok={result.ok} status={result.status_code} smiles={result.smiles} "
        f"reason={result.reason} message={result.message}"
    )

    if not result.ok:
        return 1
    return 0


def main() -> None:
    exit_code = asyncio.run(run())
    raise SystemExit(exit_code)
