# Tailscale MCP — product requirements (index)

**Mirror folder:** This `projects/tailscale-mcp/` copy tracks the upstream repo for discovery in MCP Central Docs.

**Canonical PRD (full):** [docs/PRD.md in tailscale-mcp](https://github.com/sandraschi/tailscale-mcp/blob/main/docs/PRD.md) — or locally: `D:\Dev\repos\tailscale-mcp\docs\PRD.md`

**Snapshot (2026-03-22):**

- **Runtime:** FastMCP **3.1+**, Tailscale Admin API (`TAILSCALE_API_KEY`, `TAILSCALE_TAILNET`); optional SEP-1577 `tailscale_agentic_workflow` with sampling env vars.
- **Web (`Webapp`):** `/my-tailnet` (Mermaid + CSS orbit), `/partner-tailnets` (`tailscale_partner_tailnets` — members vs shared users, devices-by-login).
- **Dev tooling:** **Ruff** for lint, format, and import sorting; **pre-commit** uses `ruff` / `ruff-format` (Black and isort hooks removed upstream).
- **Version:** **2.0.2** — see upstream [CHANGELOG](https://github.com/sandraschi/tailscale-mcp/blob/main/CHANGELOG.md).
