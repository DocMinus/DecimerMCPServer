# Project Agent Rules

## Image Attachment Handling

User attaches image → execute:

1. Call `decimer_analyze_chemical_image` on attached image
2. Return compact JSON only:

```json
{"is_structure": <true|false>, "smiles": <string|null>, "reason": <string|null>}
```

Requirements:
- No markdown fences
- No explanation/prefix/suffix
- `smiles: null` when no structure detected
- `reason: null` when classification succeeds

## MCP Registry Publishing

Trigger: Tag push (`v*`) or manual dispatch.

Workflow:
1. Validate `server.json` against schema
2. Publish via `modelcontextprotocol/registry-action@v1`
3. Verify registry listing

Manual publish:
```bash
# Validate
uv pip install jsonschema
python -c "import json, jsonschema, urllib.request; schema = json.loads(urllib.request.urlopen('https://static.modelcontextprotocol.io/schemas/2025-09-29/server.schema.json').read()); data = json.load(open('server.json')); jsonschema.validate(data, schema); print('Valid!')"

# Publish (requires auth token in secrets)
```

Registry: https://registry.modelcontextprotocol.io
