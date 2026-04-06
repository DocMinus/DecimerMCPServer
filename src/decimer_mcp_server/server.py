from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .config import settings
from .decimer_api_client import DecimerAPIClient
from .schemas import (
    AnalyzeChemicalImageInput,
    AnalyzeChemicalImageOutput,
    ServerHealthOutput,
)


mcp = FastMCP("decimer-mcp-server")
api_client = DecimerAPIClient(
    base_url=settings.decimer_api_base_url,
    timeout_seconds=settings.decimer_api_timeout_seconds,
    max_image_bytes=settings.decimer_max_image_bytes,
)


@mcp.tool()
async def server_health() -> dict:
    """Check DECIMER FastAPI server availability."""
    result = await api_client.health()
    output = ServerHealthOutput(
        ok=result.ok,
        api_status_code=result.status_code,
        message=result.message or "No response message",
    )
    return output.model_dump()


@mcp.tool()
async def analyze_chemical_image(
    encoded_image: str,
    is_hand_drawn: bool = False,
    classify_image: bool = True,
) -> dict:
    """Analyze a base64 image and return a predicted SMILES string when available."""
    parsed = AnalyzeChemicalImageInput(
        encoded_image=encoded_image,
        is_hand_drawn=is_hand_drawn,
        classify_image=classify_image,
    )

    try:
        result = await api_client.image_to_smiles(
            encoded_image=parsed.encoded_image,
            is_hand_drawn=parsed.is_hand_drawn,
            classify_image=parsed.classify_image,
        )
    except ValueError as exc:
        output = AnalyzeChemicalImageOutput(
            ok=False,
            smiles=None,
            reason="image_too_large",
            api_status_code=413,
            api_message=str(exc),
        )
        return output.model_dump()

    output = AnalyzeChemicalImageOutput(
        ok=result.ok,
        smiles=result.smiles,
        reason=result.reason,
        api_status_code=result.status_code,
        api_message=result.message,
        classifier_score=result.classifier_score,
        classifier_threshold=result.classifier_threshold,
        classifier_decision=result.classifier_decision,
    )
    return output.model_dump()
