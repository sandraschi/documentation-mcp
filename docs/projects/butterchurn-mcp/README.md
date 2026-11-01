# butterchurn-mcp

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/jberg/butterchurn"><img src="https://img.shields.io/badge/butterchurn-2.6-ff6b35?style=flat-square" alt="Butterchurn"></a>
</p>

> Universal visualizer toolbox — modern WebGL2 GLSL shaders + legacy MilkDrop presets (butterchurn). FastMCP server with BPM sync for [mixx-dj-mcp](https://github.com/sandraschi/mixx-dj-mcp).

## Release

**v0.1.0-beta.1** (prerelease, 2026-08-28) — [GitHub release](https://github.com/sandraschi/butterchurn-mcp/releases/tag/v0.1.0-beta.1)

Install: drag `butterchurn-mcp-0.1.0-beta.1.mcpb` onto Claude Desktop, or `mcpb install <file>`.

## Engines

| Engine | What | When to use |
|--------|------|-------------|
| **GLSL Shaders** | 6 bundled WebGL2 scenes (gyroid, tunnel, plasma, …) | Modern look, no `.milk` baggage |
| **Butterchurn** | ~2,000 MilkDrop presets (butterchurn packs + projectM collections) | Retro Winamp nostalgia |

Open **Toolbox** in the webapp to switch engines, preview, and go fullscreen.

## How it works

The webapp fills the entire browser window with a WebGL canvas running MilkDrop preset visualizations. The built-in beat generator pulses to the current BPM (default 128). Presets cycle through the butterchurn library — click or use arrow keys to switch.

**mixx-dj-mcp integration:** Send `POST /api/bpm { "bpm": 140 }` to the backend at 10878 to sync the visualizer's beat to a DJ set.

## Quick start

```powershell
uv sync
cd webapp; bun install; cd ..
just serve     # backend on :10878 + MCP HTTP at /mcp
```

In another terminal:
```powershell
just web       # Vite dev on :10879
```

Or use `start.ps1` for both at once.

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Server status, version, uptime |
| `/api/bpm` | GET | Current BPM value |
| `/api/bpm` | POST `{ "bpm": 140 }` | Set BPM (mixx-dj-mcp sync) |

## MCP tools

| Tool | Description |
|------|-------------|
| `get_bpm` | Read current BPM |
| `set_bpm` | Set BPM for visualizer sync |

## Ports

| Role | Port |
|------|------|
| Backend (FastAPI + MCP HTTP) | 10878 |
| Frontend (Vite dev) | 10879 |
