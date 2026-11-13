# CoderCraft

**Version**: v0.1.0 — Local-First Agentic IDE & Universal MCP Server.
**Repository**: [`d:\Dev\repos\codercraft`](file:///d:/Dev/repos/codercraft) | [GitHub: sandraschi/codercraft](https://github.com/sandraschi/codercraft)
**Parent Suite**: Sovereign Craft Suite

---

## Ports

| Port | Service | Assigned Date |
|------|---------|---------------|
| `14128` | Control & UI Port (`codercraft --control 14128`) | 2026-10 |

---

## Architecture

```
                               codercraft-core
              (File Tree / AST Symbols / Linter Abstraction / Diff Bus)
                                       ^
                 ┌─────────────────────┴─────────────────────┐
                 │                                           │
        codercraft-mcp (L1/L2)                      codercraft-app (L3 GUI)
     (FastMCP Stdio Server & CLI)                   (egui 0.37 Native Studio)
```

- **`crates/codercraft-core`**: File tree scanning, instruction discovery (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`), linter abstraction (Clippy, Ruff, Biome), shell runner.
- **`crates/codercraft-agent`**: Dual-mode agent loop (`Plan` for exploration, `Build` for active code synthesis).
- **`crates/codercraft-mcp`**: MCP 2024-11-05 stdio server (`codercraft-cli --mcp`).
- **`crates/codercraft-app`**: Native immediate-mode egui desktop studio with chat stream, collapsible thinking blocks, and diff inspector.

---

## Quick Start

```powershell
# Headless smoke test
.\start.ps1 -Build

# Launch native desktop studio
.\start.ps1

# Launch FastMCP stdio server
cargo run -p codercraft-mcp -- --mcp
```
