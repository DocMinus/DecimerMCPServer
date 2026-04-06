SMOKE_IMAGE ?= /Users/a/dev/DecimerServerAPI/example_usage/structure.png

.PHONY: sync test run smoke

sync:
	uv sync --extra dev

test:
	uv run pytest

run:
	uv run --env-file .env decimer-mcp-server

smoke:
	uv run --env-file .env decimer-mcp-smoke-test --image "$(SMOKE_IMAGE)"
