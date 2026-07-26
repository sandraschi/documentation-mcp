# Changelog

## [0.3.0] - 2026-04-04

### Changed
- **FastMCP 3.2**: Bumped dependency to `fastmcp>=3.2`, `prefab-ui>=0.14.0`.
- **Starlette backend**: Replaced FastAPI + Pydantic with plain Starlette + dicts (fleet STARLETTE_NO_PYDANTIC_STANDARD).
- **Prefab fix**: Removed base64 image embedding (`fetch_image_data_uri`) — `Image()` now uses direct `https://imgs.xkcd.com/...` URLs. Eliminates "waiting for content" hang in Claude Desktop.
- **Decorator cleanup**: `@mcp.tool(app=HAS_PREFAB)` → `@mcp.tool()` — 3.2 renders `structured_content` automatically when present; decorator arg not needed.
- Version bump: `0.2.0` → `0.3.0`.

## [0.2.0] - 2026-03-30

### Added
- **FastMCP 3.1 Prefab UI**: Rich in-chat comic rendering (Card + Image + Alt Text).
- **Discrete Tools**: Replaced the `xkcd_comic` portmanteau with `xkcd_latest`, `xkcd_get`, and `xkcd_random` to improve tool discovery and flexibility.
- **Help System**: Added `xkcd_help` tool providing a formatted guide, port assignments, and usage instructions.
- **Image Pipeline**: SOTA-standard base64 image fetching with 512KB cap for efficient rendering.

### Changed
- **Tool Result Alignment**: All tools now return `ToolResult` objects for modern host compatibility.
- **Documentation**: Updated `README.md` and fleet registry to reflect the new tool surface.

### Removed
- `xkcd_comic` portmanteau tool.

## [0.1.0] — 2026-03-20

### Added

- **FastMCP 3.1** tool `xkcd_comic` (current / by_number / random).
- **FastAPI** on **10778**, MCP at `/mcp`, `POST /api/comic`.
- **Vite** SPA on **10779** (`web_sota/start.ps1`).
- **`justfile`**, **`glama.json`**, `uv`, ruff, pytest.
