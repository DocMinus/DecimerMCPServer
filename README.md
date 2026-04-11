# DecimerMCPServer

mcp-name: io.github.DocMinus/decimer-mcp-server

MCP server that exposes DECIMER image-to-SMILES functionality as tool calls.

This project is a thin adapter over the existing FastAPI service in `DecimerServerAPI`.
It does not run DECIMER models directly.
The adapter sends JSON requests by default, with automatic fallback to form payloads for compatibility.

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
  "api_message": null,
  "classifier_score": 0.0000012,
  "classifier_threshold": 0.3,
  "classifier_decision": "structure_like"
}
```

When no SMILES is returned by API classifier behavior:

```json
{
  "ok": true,
  "smiles": null,
  "reason": "not_chemical_structure",
  "api_status_code": 200,
  "api_message": "No SMILES returned by API",
  "classifier_score": 0.99999,
  "classifier_threshold": 0.3,
  "classifier_decision": "not_structure_like"
}
```

## Development tests

```bash
uv sync --extra dev
uv run pytest
```

Make targets:

```bash
make sync
make test
```

## Smoke test helper

Run one health check + one inference call against your DECIMER API:

```bash
cd /Users/a/dev/DecimerMCPServer
DECIMER_API_BASE_URL=http://chitchat:8099 uv run decimer-mcp-smoke-test --image /Users/a/dev/DecimerServerAPI/example_usage/structure.png
```

If you keep settings in `.env`, load it with:

```bash
uv run --env-file .env decimer-mcp-smoke-test --image /Users/a/dev/DecimerServerAPI/example_usage/structure.png
```

or use make:

```bash
make smoke
```

Override the image path if needed:

```bash
make smoke SMOKE_IMAGE=/absolute/path/to/image.png

## MCP Registry publishing

Tags matching `v*` trigger `.github/workflows/publish-mcp.yml`.

Workflow steps:
- installs `mcp-publisher`
- validates `server.json`
- calls registry publish using secret `MCP_REGISTRY_TOKEN`
- publishes slug `io.github.DocMinus/decimer-mcp-server` (case sensitive; must match registry grant)

Before tagging:
1. Update `pyproject.toml` + `server.json` versions
2. Ensure `server.json` stays valid (`uv pip install jsonschema && python validate snippet from AGENTS.md`)
3. Add GitHub repo secret `MCP_REGISTRY_TOKEN` (GitHub PAT with `repo`, `workflow` scopes)

Release flow:
```bash
git tag v0.1.1
git push origin v0.1.1
```

Monitor Actions tab. If publish fails, rerun using workflow dispatch after fixing issues.
```

## Contribution
This project was built by DocMinus with AI-assisted coding support (OpenCode/Copilot-style tooling), then reviewed and tested by the author.

## AI usage policy

- AI assistance was used for scaffolding, implementation drafts, and documentation edits.
- Final technical decisions, validation runs, and acceptance were performed by the maintainer.
- Runtime behavior should be validated with local tests (`make test`) and smoke tests (`make smoke`) before release.
