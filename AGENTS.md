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
