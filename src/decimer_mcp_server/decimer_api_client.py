from __future__ import annotations

import base64
from dataclasses import dataclass

import httpx


@dataclass
class APIResult:
    ok: bool
    status_code: int
    smiles: str | None = None
    message: str | None = None
    reason: str | None = None
    classifier_score: float | None = None
    classifier_threshold: float | None = None
    classifier_decision: str | None = None


class DecimerAPIClient:
    def __init__(
        self, base_url: str, timeout_seconds: float, max_image_bytes: int
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.max_image_bytes = max_image_bytes

    def _validate_image_size(self, encoded_image: str) -> None:
        decoded = base64.b64decode(encoded_image, validate=True)
        if len(decoded) > self.max_image_bytes:
            raise ValueError(
                f"Decoded image size exceeds limit of {self.max_image_bytes} bytes"
            )

    async def health(self) -> APIResult:
        url = f"{self.base_url}/"
        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.get(url)
        except httpx.TimeoutException:
            return APIResult(
                ok=False,
                status_code=504,
                message="DECIMER API request timed out",
                reason="timeout",
            )
        except httpx.HTTPError as exc:
            return APIResult(
                ok=False,
                status_code=503,
                message=f"DECIMER API unreachable: {exc}",
                reason="unreachable",
            )

        message = None
        try:
            payload = response.json()
            message = payload.get("Message") or payload.get("message")
        except ValueError:
            message = response.text

        return APIResult(
            ok=response.status_code == 200,
            status_code=response.status_code,
            message=message,
            reason=None if response.status_code == 200 else "http_error",
        )

    async def image_to_smiles(
        self,
        encoded_image: str,
        is_hand_drawn: bool,
        classify_image: bool,
    ) -> APIResult:
        self._validate_image_size(encoded_image)
        url = f"{self.base_url}/image2smiles/"
        json_payload = {
            "encoded_image": encoded_image,
            "is_hand_drawn": is_hand_drawn,
            "classify_image": classify_image,
        }
        form_data = {
            "encoded_image": encoded_image,
            "is_hand_drawn": str(is_hand_drawn).lower(),
            "classify_image": str(classify_image).lower(),
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.post(url, json=json_payload)
                if response.status_code in {400, 415, 422}:
                    response = await client.post(url, data=form_data)
        except httpx.TimeoutException:
            return APIResult(
                ok=False,
                status_code=504,
                message="DECIMER API request timed out",
                reason="timeout",
            )
        except httpx.HTTPError as exc:
            return APIResult(
                ok=False,
                status_code=503,
                message=f"DECIMER API unreachable: {exc}",
                reason="unreachable",
            )

        try:
            payload = response.json()
        except ValueError:
            payload = {"message": response.text}

        if response.status_code != 200:
            return APIResult(
                ok=False,
                status_code=response.status_code,
                message=payload.get("message", "Unknown API error"),
                reason="http_error",
            )

        smiles = payload.get("smiles")
        if smiles is None:
            return APIResult(
                ok=True,
                status_code=200,
                smiles=None,
                message=payload.get("message", "No SMILES returned by API"),
                reason=payload.get("reason", "no_smiles_returned"),
                classifier_score=payload.get("classifier_score"),
                classifier_threshold=payload.get("classifier_threshold"),
                classifier_decision=payload.get("classifier_decision"),
            )

        return APIResult(
            ok=True,
            status_code=200,
            smiles=smiles,
            classifier_score=payload.get("classifier_score"),
            classifier_threshold=payload.get("classifier_threshold"),
            classifier_decision=payload.get("classifier_decision"),
        )
