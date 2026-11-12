# DevCraft — Handover Document

**Last Updated**: 2026-11-10
**Current State**: Production Release `v0.1.0`
**Primary Artifact**: [sandraschi/devcraft Releases](https://github.com/sandraschi/devcraft/releases/tag/v0.1.0)

---

## 1. What Was Done
- Scaffolding of multi-crate workspace (`devcraft-core`, `devcraft-mcp`, `devcraft-app`).
- Live recursive fleet scanner auditing git status across 280+ repositories.
- Time machine backup engine saving rolling snapshots under `.devcraft/snapshots`.
- Real-time port sentinel cross-referencing sockets against `WEBAPP_PORTS.md`.
- Windows NSSM service watchdog with safe restart validation.
- Ephemeral Docker container test execution.
- Compound FastMCP 2024-11-05 server over stdio.
- Native `egui 0.37` desktop application with multi-panel layout.
- Reserved ports `11258` (Frontend) and `11259` (Backend) in `WEBAPP_PORTS.md`.
- Launchers wired into `mcp-central-docs/starts/devcraft-start.bat` and `start faves/`.
- Packaged portable release bundle `devcraft-v0.1.0-windows-x86_64.zip` and published GitHub release.

---

## 2. Immediate Next Steps
1. Add git commit and branch switching directly from the egui Selected Repo pane.
2. Integrate Podman desktop detection alongside Docker.
3. Add card entry in `craft-deck` for one-click desktop launching.

---

## 3. Deliberately NOT Done
- Did not kill child processes of NSSM directly (enforces rule: `sc.exe stop/start` only).
- Did not bypass the port registry (all ports allocated via `claim_ports.py`).
