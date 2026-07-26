# obsidian-mcp — Status

Last verified: June 2026

| Metric | Status |
|--------|--------|
| **Gateway** | FastAPI on 10915 |
| **Webapp** | Vite fleet SOTA on 10890 |
| **Framework** | FastMCP 3.2+ |
| **Python** | 3.12+ |
| **Tools** | 24+ (vault, search, links, canvas, RAG) |
| **MCPB** | v0.2 manifest + `scripts/build-mcpb.ps1` |
| **CI** | ruff, pytest, biome, vitest, playwright e2e |
| **Overall** | Beta |

## Recent (2026-06)

- Fleet webapp conformance: AppLayout, proxy, ports 10915/10890
- LoggerContext + Playwright e2e
- MCPB staging build with prompts and `.mcpbignore`
- Multi-vault, Settings API, LanceDB RAG, plugin bridge (see repo CHANGELOG)

## Known issues

- Pydantic V1 `@validator` in `config.py` (migrate to `@field_validator`)
- `mcp-server/src/` copy may lag repo `src/` — build script stages from `src/obsidian_mcp` at pack time
