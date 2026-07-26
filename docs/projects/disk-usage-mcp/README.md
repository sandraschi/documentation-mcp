# disk-usage-mcp

Multi-drive disk usage analysis for Windows. Wraps `dua-cli` and `czkawka_cli` behind FastMCP 3.4+ tools + a FastAPI REST backend + React dashboard.

Built for a 20 TB media library split across 5 TB and 2.5 TB spinners, 3-2-2 backup sprawl, and model download duplication (Ollama, Pinokio, HuggingFace).

## Tools (5 MCP)

| Tool | What | Backend |
|------|------|---------|
| `scan_path` | JSON hierarchy via dua | dua-cli |
| `get_drive_overview` | Aggregate stats across drives | dua-cli |
| `find_duplicates` | Duplicate file groups | czkawka_cli |
| `find_large_files` | Files above size threshold (deep tree walk) | dua-cli |
| `disk_usage` | Portmanteau: scan/tree/drive_overview | dua-cli |

## Future Tools (Planned)

| Tool | What | Why |
|------|------|-----|
| `find_model_duplicates` | Cross-directory model dedup (GGUF, .safetensors, .bin) | Pinokio, Ollama, HF downloads often duplicate the same 10 GB model across different tool dirs |
| `find_backup_duplicates` | Detect redundant backup copies | 3-2-2 sprawl — same archive on multiple spinners |
| `scan_media_library` | Media-type breakdown (video/audio/image archives) | Plex + Calibre + raw files overlap |

## Architecture

```
MCP Client ←→ FastMCP 3.4 ←→ FastAPI (REST + /mcp) ←→ dua-cli / czkawka_cli
                              ↑
                         React / Vite / Tailwind v4 webapp (web_sota/)
```

## Ports

| Service | Port |
|---------|------|
| Backend (FastAPI + MCP HTTP) | 11114 |
| Frontend (Vite dev) | 11115 |

## Stack

- **FastMCP** 3.4.4 — dual transport (stdio + HTTP)
- **FastAPI** — REST layer with snapshot CRUD + diagnostics
- **React 19** + **Vite 6** + **Tailwind v4** + **Zustand** + **Framer Motion** + **recharts**
- **uv** + **ruff** + **justfile**
- **pytest** — 10 tests (HTTP smoke, config, import verification)
- **Session context injection** — `.claude-plugin/` + `hooks/hooks.json`

## Repo Layout

```
disk-usage-mcp/
├── src/disk_usage_mcp/
│   ├── server.py      # FastMCP entry point
│   ├── http_app.py     # FastAPI REST (health, scan, snapshots, duplicates)
│   ├── runner.py       # Async subprocess wrappers
│   ├── config.py       # Ports, paths, logging
│   └── tools/
│       ├── scan.py     # scan_path, find_large_files
│       ├── overview.py # get_drive_overview
│       ├── duplicates.py # find_duplicates (czkawka)
│       └── disk_usage.py # portmanteau
├── web_sota/           # React/Vite/Tailwind v4 dashboard
├── tests/              # 10 pytest tests
├── hooks/              # SessionStart injection
├── skills/             # disk-usage SKILL.md
├── .claude-plugin/     # Claude Code plugin
├── .mcpbignore         # MCPB packaging
├── run_server.py       # PyInstaller entry point
├── start.ps1 / .bat
└── justfile
```

## Data Flow

Scans run via async subprocess (`asyncio.create_subprocess_exec`). Results are returned as JSON and optionally snapshotted to `data/snapshots/*.json` for offline comparison. No database — filesystem-only for maximum compatibility with terabyte-scale trees.

## Session Context

Claude Code users get automatic tool-awareness prompt at session start via `.claude-plugin/` + `hooks/hooks.json`:

```
## Session Context (Disk Usage MCP)
5 tools: scan_path, find_large_files, get_drive_overview, find_duplicates, disk_usage.
Before working: check drive overview, scan specific paths.
At end: report reclaimable space.
```

## Related

- `mcp-central-docs/operations/WEBAPP_PORTS.md` — port registration (11114/11115)
- `mcp-central-docs/standards/TOOL_DESIGN_STANDARDS.md` — portmanteau pattern
- `mcp-central-docs/standards/rules/session_context_injection.md` — Claude Code hooks
