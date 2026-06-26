# GIMP MCP Server

**By FlowEngineer sandraschi**

Professional image editing through Model Context Protocol (MCP) using GIMP 3 — **Agent Lab v4.6.0**.

[![FastMCP](https://img.shields.io/badge/FastMCP-3.2-blue)](https://github.com/jlowin/fastmcp)
[![Python](https://img.shields.io/badge/Python-3.12+-green)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## Agent Lab (v4.6.0)

Dual-mode GIMP orchestrator: **Hands-In** live bridge (`:10824`) + **Hands-Off** headless CLI.

| Port | Service |
|------|---------|
| 10772 | Webapp (Dashboard, Agent Tools) |
| 10773 | HTTP MCP + FastAPI |
| 10824 | GIMP Live Bridge (host plugin) |

### Agent Lab tools

| Tool | Purpose |
|------|---------|
| `gimp_bridge_tool` | Bridge status, execution mode, ping |
| `gimp_render_tool` | Canvas capture for vision loops |
| `gimp_validation_tool` | Texture/image QA (Unity, Gazebo) |
| `gimp_import_tool` | blender → gimp → unity handoff |
| `gimp_vision_refine_tool` | Multi-angle texture review bundles |
| `gimp_sim_art_tool` | Gazebo icons, atlases, decal UV sheets, VRChat, auto-import |
| `gimp_batch_tool` | Batch ops incl. `pbr_pack` (albedo/normal/roughness) |

### Fleet pipelines

| Pipeline | Script | Docs |
|----------|--------|------|
| Textures | `scripts/run-fleet-pipeline.ps1` | [FLEET_PIPELINE.md](https://github.com/sandraschi/gimp-mcp/blob/master/docs/FLEET_PIPELINE.md) |
| Sim art | `scripts/run-sim-art-pipeline.ps1` | [SIM_ART_PIPELINE.md](https://github.com/sandraschi/gimp-mcp/blob/master/docs/SIM_ART_PIPELINE.md) |
| E2E smoke | `scripts/fleet_e2e_smoke.py --offline --strict` | CI + fleet probe |

### Cross-fleet HTTP (no stdio mount)

| Consumer | Integration |
|----------|-------------|
| **robotics-mcp** | `robotics_sim_art` → POST `:10773/api/v1/tool` |
| **avatar-mcp** | `POST /api/v1/avatars/{id}/thumbnail` + `avatar_manager set_thumbnail` |
| **unity3d-mcp** | `gimp_import_tool push_unity` |

## Quick start

```powershell
git clone https://github.com/sandraschi/gimp-mcp
cd gimp-mcp
uv sync
.\start.ps1 -RestartGimp
```

MCPB bundle:

```powershell
uv run python build_mcpb.py
# dist/gimp-mcp-4.5.2.mcpb
```

## MCP registration (stdio)

```json
{
  "gimp-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/gimp-mcp", "run", "python", "-m", "gimp_mcp.mcp_server"],
    "env": { "PYTHONUNBUFFERED": "1" }
  }
}
```

## Portmanteau tools (core)

17 domain tools consolidating ~1000 GIMP PDB procedures: `gimp_file`, `gimp_transform`, `gimp_color`, `gimp_filter`, `gimp_layer`, `gimp_analysis`, `gimp_batch`, `gimp_system`, `gimp_pdb`, plus workspace, channel, animation, paths, G'MIC, GEGL, color management.

## Documentation

| Doc | Content |
|-----|---------|
| [INSTALL.md](https://github.com/sandraschi/gimp-mcp/blob/master/docs/readme/INSTALL.md) | MCPB, bridge, Docker, monitoring |
| [ROADMAP.md](https://github.com/sandraschi/gimp-mcp/blob/master/docs/ROADMAP.md) | Agent Lab phases 1–6 |
| [MONITORING.md](https://github.com/sandraschi/gimp-mcp/blob/master/docs/MONITORING.md) | Prometheus + Loki |
| [DOCKER.md](https://github.com/sandraschi/gimp-mcp/blob/master/docs/DOCKER.md) | Container deployment |

## Repository

- **GitHub**: [sandraschi/gimp-mcp](https://github.com/sandraschi/gimp-mcp)
- **MCPB**: `dist/gimp-mcp-*.mcpb` (build locally or GitHub Release on tag `v*`)

## License

MIT — Sandra Schipal
