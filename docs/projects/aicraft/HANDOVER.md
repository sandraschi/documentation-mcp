# AICraft — Handover Document

**Last Updated**: 2026-11-10
**Current State**: Production Release `v0.1.0`
**Primary Artifact**: [sandraschi/aicraft Releases](https://github.com/sandraschi/aicraft/releases/tag/v0.1.0)

---

## 1. What Was Done
- Scaffolding of multi-crate workspace (`aicraft-core`, `aicraft-mcp`, `aicraft-app`).
- Model routing engine with Ollama `11434` local probing and tiered failover (`Local` $\rightarrow$ `Balanced` $\rightarrow$ `Frontier`).
- Token accountant tracking prompt tokens, completion tokens, latency ($t_{\text{first-token}}$), generation speed (tok/s), and cumulative USD costs.
- Versioned prompt depot and regression eval engine with fixture assertion scoring.
- Compound FastMCP 2024-11-05 server over stdio.
- Native `egui 0.37` desktop application with Model Radar, Model Arena, Telemetry, and Swarm Monitor.
- Reserved ports `11260` (Frontend) and `11261` (Backend) in `WEBAPP_PORTS.md`.
- Launchers wired into `mcp-central-docs/starts/aicraft-start.bat` and `start faves/`.
- Packaged portable release bundle `aicraft-v0.1.0-windows-x86_64.zip` and published GitHub release.

---

## 2. Immediate Next Steps
1. Wire live streaming tokens via WebSocket/SSE into the egui studio.
2. Connect real Ollama API client over local HTTP for actual local weight inference.
3. Add card entry in `craft-deck` for one-click desktop launching.

---

## 3. Deliberately NOT Done
- Did not hardcode any proprietary API keys into source (uses environment variables / MCP keychain).
- Did not add bloated web frameworks; relies purely on native Rust `egui 0.37`.
- Did not use Bash heredocs or inline python scripts (fleet rules BUG-031 and BUG-039).
