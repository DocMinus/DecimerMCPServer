# Project Agent Rules

## Image Attachment Handling Rule

When a user attaches an image, follow this template exactly:

1. Use the `decimer` MCP tool only.
2. Call `analyze_chemical_image` on the attached image.
3. Return compact JSON only, with no extra text:

```json
{"is_structure": <true|false>, "smiles": <string|null>, "reason": <string|null>}
```

Additional requirements:
- No markdown fences in final output.
- No explanation, prefix, or suffix text.
- Keep `smiles` as `null` when no structure is detected.
- Keep `reason` as `null` when classification succeeds without an error reason.

## MCP Registry Publishing Reference

When asked about publishing this MCP server to the MCP Registry, follow this baseline workflow:

1. Ensure `server.json` exists at the repository root with complete, current metadata.
2. Validate `server.json` against the official schema:
   `https://static.modelcontextprotocol.io/schemas/2025-09-29/server.schema.json`.
3. Prefer automated publishing via GitHub Actions using
   `modelcontextprotocol/registry-action@v1`.
4. Verify the server appears in the registry after publishing.

Reference article:
- `https://mcpplaygroundonline.com/blog/how-to-publish-your-mcp-server-to-registry`
