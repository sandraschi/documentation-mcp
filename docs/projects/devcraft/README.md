# DevCraft

**Version**: v0.1.0 (2026-11-10) — Sovereign Developer Cockpit, Fleet Hygiene & Git Governance Workstation.
**Repository**: [`d:\Dev\repos\devcraft`](file:///d:/Dev/repos/devcraft) | [GitHub: sandraschi/devcraft](https://github.com/sandraschi/devcraft)
**Parent Suite**: Sovereign Craft Suite / Craft Bundlers

---

## Ports

| Port | Service | Assigned Date |
|------|---------|---------------|
| `11258` | Frontend (egui 0.37 Native Studio / Web) | 2026-11-10 |
| `11259` | Backend (FastMCP 2024-11-05 JSON-RPC / Control) | 2026-11-10 |

---

## Architecture

```
                                  devcraft-core
           (Fleet Scanner / Backup Engine / Port & Service Sentinel / Sandbox)
                                       ^
                 ┌─────────────────────┴─────────────────────┐
                 │                                           │
         devcraft-mcp (L1/L2)                        devcraft-app (L3 GUI)
  (FastMCP Stdio Server & CLI)                     (egui 0.37 Native Studio)
```

- **`crates/devcraft-core`**:
  - `fleet`: Live scanning of 280+ repositories; monitors git dirty status, branch state, and `AGENTS.md` / `CLAUDE.md` conformance.
  - `backup`: Time machine snapshot engine with rolling restore points under `.devcraft/snapshots`.
  - `ports`: Socket auditor parsing 600+ ports from `WEBAPP_PORTS.md` and reconciling active listeners.
  - `services`: Windows NSSM service watchdog enforcing strict `sc.exe stop/start` protocols without orphan processes.
  - `sandbox`: Ephemeral Docker/Podman container test runner with subprocess fallback.
  - `meta`: Fleet-wide MCP capability search and tool discovery engine.
- **`crates/devcraft-mcp`**:
  - FastMCP 2024-11-05 stdio server (`devcraft-mcp --mcp`).
  - Universal CLI with subcommands: `status`, `audit`, `ports`, `discover`, `snapshot`.
- **`crates/devcraft-app`**:
  - Native immediate-mode egui 0.37 desktop studio with Fleet Radar, Selected Repo Inspector, Time Machine, Docker Sandbox, Port Sentinel, and Windows Service Watchdog.

---

## Compound FastMCP Tools

| Tool | Ops | Purpose |
|------|-----|---------|
| `devcraft_audit_fleet` | Audit | Scan all workspace repos, git dirty status, branch state, and AGENTS.md coverage |
| `devcraft_checkpoint_worktree` | Backup | Create atomic snapshot of modified files before major edits |
| `devcraft_audit_ports` | Audit | Reconcile active listening sockets against `WEBAPP_PORTS.md` |
| `devcraft_sandbox_run` | Execute | Run tests/commands inside isolated Docker container or sandboxed subprocess |
| `devcraft_restart_service` | Manage | Safely restart Windows NSSM service adhering to fleet sc.exe protocol |
| `devcraft_discover_tools` | Query | Fleet-wide keyword search for MCP servers and tools |

---

## Quick Start

```powershell
# Headless smoke test
.\start.ps1 -Smoke

# Launch native desktop studio
.\start.ps1

# Launch FastMCP stdio server
cargo run -p devcraft-mcp -- --mcp
```
