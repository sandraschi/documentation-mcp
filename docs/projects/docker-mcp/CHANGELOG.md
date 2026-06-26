# Docker MCP — MCP Central mirror

**Authoritative changelog**: `D:\Dev\repos\docker-mcp\CHANGELOG.md`.

## [3.3.0] — 2026-06-02 (fleet SOTA uplift)

- **FastMCP 3.3** with sampling handler (Ollama/LM Studio), `on_duplicate=replace`, prefab-ui cards.
- **Fleet surface**: MCP prompts, `resource://docker-mcp/skills`, `docker_containers_card`, `docker_desktop_status_card`, `docker_system_info_card`.
- **Web**: `/logs` (ring buffer API), settings with LLM provider/model glom; `start.ps1` requires `/api/health` 200.
- **MCPB**: Root `manifest.json` v0.2; removed legacy `mcpb/` directory; `.mcpbignore` slim pack.
- **Tauri**: Full `just build-native` pipeline (web_sota + PyInstaller sidecar + bundle).
- **Import fix**: `docker_context.py` + `tool_registration.py` (no circular init).
- **Tests**: `tests/test_web_bridge.py` for health/logs API.

For full history (including Docker Desktop tools), read the canonical [CHANGELOG.md](file:///D:/Dev/repos/docker-mcp/CHANGELOG.md).
