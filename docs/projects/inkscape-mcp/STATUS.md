# Inkscape MCP -- Project Status

**Last Updated**: 2026-05-28
**Repo**: `D:\Dev\repos\inkscape-mcp` | [GitHub](https://github.com/sandraschi/inkscape-mcp)
**Version**: v2.6.0 (Agent Lab Phase 6 complete)
**Python**: 3.12+ | **Build**: Hatchling / uv
**Status**: PRODUCTION READY — Agent Lab roadmap active

---

## What It Is

Professional vector graphics and SVG operations for AI agents. Bridge between natural language and the Inkscape CLI (batch Actions API + extension ecosystem).

**Key Capability**: Conversational SVG generation, portmanteau vector ops, fleet `web_sota` dashboard (10899/10900).

---

## Agent Lab

| Phase | Status | Theme |
|-------|--------|-------|
| Baseline | done | 4 portmanteau tools, AI SVG, extensions, web_sota |
| 1 (2.1.0) | done | Vision exports, execution_mode |
| 2 (2.2.0) | done | `/agent-tools` webapp, inkscape_validation |
| 3 (2.3.0) | done | inkscape_fleet gimp/blender/unity handoff |
| 4 (2.4.0) | done | Telemetry, Docker, smoke test |
| 5 (2.5.0) | done | Robotics fab art, fleet E2E smoke |
| 6 (2.6.0) | done | UI icon packs, icon sheets, SVG refine loop |

Details: [ROADMAP.md](file:///D:/Dev/repos/inkscape-mcp/docs/ROADMAP.md) in repo.

---

## Port Allocation

| Service | Port |
|---------|------|
| Webapp (Vite) | 10899 |
| HTTP MCP / REST | 10900 |

---

## Fleet role

```text
inkscape (SVG) → gimp (raster QA) → unity (UI sprites)
inkscape (DXF) → robotics (fab paths)
```

Next fleet repo after gimp-mcp Agent Lab Phases 1–5.
