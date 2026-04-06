from decimer_mcp_server.schemas import AnalyzeChemicalImageInput


def test_input_schema_accepts_valid_base64() -> None:
    valid = "aGVsbG8="
    parsed = AnalyzeChemicalImageInput(encoded_image=valid)
    assert parsed.encoded_image == valid


def test_input_schema_rejects_invalid_base64() -> None:
    try:
        AnalyzeChemicalImageInput(encoded_image="not_base64!!!")
        assert False, "Expected base64 validation failure"
    except ValueError as exc:
        assert "valid base64" in str(exc)
