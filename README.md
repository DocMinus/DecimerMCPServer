# DecimerMCPServer

MCP server that exposes DECIMER image-to-SMILES functionality as tool calls.

This project is a thin adapter over the existing FastAPI service in `DecimerServerAPI`.
It does not run DECIMER models directly.

## Tools

- `server_health`: Checks whether the DECIMER FastAPI server is reachable.
- `analyze_chemical_image`: Sends a base64-encoded image to `/image2smiles/` and returns structured output.

## Requirements

- Python 3.10+
- Running DECIMER API server (default: `http://localhost:8099`)

## Install

```bash
cd /Users/a/dev/DecimerMCPServer
uv venv
uv sync
```

## Configuration

Copy `.env.example` values into your environment:

- `DECIMER_API_BASE_URL` (default `http://localhost:8099`)
- `DECIMER_API_TIMEOUT_SECONDS` (default `60`)
- `DECIMER_MAX_IMAGE_BYTES` (default `10000000`)
- `DECIMER_MCP_LOG_LEVEL` (default `INFO`)

## Run (stdio transport)

```bash
uv run decimer-mcp-server
```

or

```bash
uv run python -m decimer_mcp_server
```

## Example MCP client config

```json
{
  "mcpServers": {
    "decimer": {
      "command": "uv",
      "args": ["run", "python", "-m", "decimer_mcp_server"],
      "env": {
        "DECIMER_API_BASE_URL": "http://localhost:8099"
      }
    }
  }
}
```

## Output shape

`analyze_chemical_image` returns:

```json
{
  "ok": true,
  "smiles": "CCO",
  "reason": null,
  "api_status_code": 200,
  "api_message": null
}
```

When no SMILES is returned by API classifier behavior:

```json
{
  "ok": true,
  "smiles": null,
  "reason": "no_smiles_returned",
  "api_status_code": 200,
  "api_message": "No SMILES returned by API"
}
```

## Development tests

```bash
uv sync --extra dev
uv run pytest
```

## Smoke test helper

Run one health check + one inference call against your DECIMER API:

```bash
cd ~/Users/a~/dev/DecimerMCPServer
DECIMER_API_BASE_URL=http://localhost:8099 uv run decimer-mcp-smoke-test --image ~/dev/DecimerServerAPI/example_usage/structure.png
```

## Contribution
OpenCode based creation by DocMinus.