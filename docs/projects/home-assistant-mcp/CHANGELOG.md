# Changelog

## [2.5.1] — 2026-07-21

### Fixed
- E501 line-too-long lint errors in `portmanteau.py` and `prompts.py`
- `ruff format` applied to `server.py`

### Packaging
- MCPB bundle rebuilt: `dist/home-assistant-mcp-2.5.0.mcpb` (29.9 kB)

## [2.5.0] — 2026-07-14

### Fixed
- CORS `["*"]` replaced with fleet-standard allowlist (localhost, Tauri, Tailscale, LAN)
- Missing glama.json added
- Missing .cursorrules added
- Missing CHANGELOG.md added
- Missing .opencode/skills/ directory added
- Ruff lint cleanup
- MCPB pack updated to match current version

### Changed
- Updated __version__ to match pyproject.toml
