# AICraft

**Version**: v0.1.0 (2026-11-10) — Sovereign AI Ops, Model Routing & Token Telemetry Studio.
**Repository**: [`d:\Dev\repos\aicraft`](file:///d:/Dev/repos/aicraft) | [GitHub: sandraschi/aicraft](https://github.com/sandraschi/aicraft)
**Parent Suite**: Sovereign Craft Suite / Craft Bundlers

---

## Ports

| Port | Service | Assigned Date |
|------|---------|---------------|
| `11260` | Frontend (egui 0.37 Native Studio / Web) | 2026-11-10 |
| `11261` | Backend (FastMCP 2024-11-05 JSON-RPC / Control) | 2026-11-10 |

---

## Architecture

```
                                  aicraft-core
              (Router & Failover / Telemetry Accountant / Prompt Depot)
                                       ^
                 ┌─────────────────────┴─────────────────────┐
                 │                                           │
         aicraft-mcp (L1/L2)                         aicraft-app (L3 GUI)
  (FastMCP Stdio Server & CLI)                     (egui 0.37 Native Studio)
```

- **`crates/aicraft-core`**:
  - `router`: Probes local Ollama (`http://127.0.0.1:11434`), manages tier routing (`Local` $\rightarrow$ `Balanced` $\rightarrow$ `Frontier`), and handles automated failover.
  - `telemetry`: Token consumption tracker, tokens/sec speed calculator, latency recorder, and exact USD spend accountant.
  - `prompts`: Local versioned prompt storage and regression eval runner with keyword/schema assertions.
  - `swarm`: Agent hierarchy visualizer and tool-call trace recorder.
- **`crates/aicraft-mcp`**:
  - FastMCP 2024-11-05 stdio server (`aicraft-mcp --mcp`).
  - Universal CLI with subcommands: `status`, `models`, `telemetry`, `route`, `eval`.
- **`crates/aicraft-app`**:
  - Native immediate-mode egui 0.37 desktop studio with Model Radar, Model Arena, Token Telemetry, and Agent Swarm Monitor.

---

## Compound FastMCP Tools

| Tool | Ops | Purpose |
|------|-----|---------|
| `aicraft_route_completion` | Execute | Route prompt to optimal tier with automatic fallback and latency/cost tracking |
| `aicraft_get_telemetry` | Query | Return real-time token spend, latency, speed (tok/s), and cache hit ratios |
| `aicraft_inventory_models` | Query | List active local Ollama models and cloud endpoints with health status |
| `aicraft_eval_prompt` | Test | Run automated regression test suite on prompt templates against fixtures |

---

## Quick Start

```powershell
# Headless smoke test
.\start.ps1 -Smoke

# Launch native desktop studio
.\start.ps1

# Launch FastMCP stdio server
cargo run -p aicraft-mcp -- --mcp
```
