from __future__ import annotations

import base64
import binascii

from pydantic import BaseModel, Field, field_validator


class AnalyzeChemicalImageInput(BaseModel):
    encoded_image: str = Field(
        ..., description="Base64-encoded image content (PNG/JPEG recommended)."
    )
    is_hand_drawn: bool = Field(
        default=False,
        description="Whether the depicted chemical structure is hand-drawn.",
    )
    classify_image: bool = Field(
        default=True,
        description="Whether to run image classification before DECIMER OCR.",
    )

    @field_validator("encoded_image")
    @classmethod
    def validate_base64(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("encoded_image must not be empty")
        try:
            base64.b64decode(stripped, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError("encoded_image is not valid base64") from exc
        return stripped


class AnalyzeChemicalImageOutput(BaseModel):
    ok: bool
    smiles: str | None
    reason: str | None = None
    api_status_code: int
    api_message: str | None = None
    classifier_score: float | None = None
    classifier_threshold: float | None = None
    classifier_decision: str | None = None


class ServerHealthOutput(BaseModel):
    ok: bool
    api_status_code: int
    message: str
