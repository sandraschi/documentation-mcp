---
title: "June 2026 Standards Bar"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-18
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# June 2026 Standards Bar (snapshot — see living [STANDARDS_BAR.md](./STANDARDS_BAR.md))

**Status:** Fleet snapshot, superseded as canonical by the living bar above
**Effective:** 2026-06-17
**Hub:** [AGENT_PROTOCOLS.md](./AGENT_PROTOCOLS.md) (SOTA v12.2)

---

## Non-negotiables (June 2026)

| Topic | Bar |
|-------|-----|
| **FastMCP** | **3.4.4+** — `fastmcp>=3.4.4,<5`, `prefab-ui>=0.14.0` core dep. Current SOTA: **4.0.5** (verified against PyPI 2026-09-18; 3.4.3 had Host/Origin guard regression — skip it, 3.4.4 is the fix; 4.x is now the live major). **New repos MAY target 4.0.x** with MRTR awareness, or stay on 3.4.4+ — both pass the gate. Existing repos on 3.2.x may stay until active work touches their deps. ⚠️ **MCP 2026-07-28 spec** released — stateless core, sampling/roots formally deprecated with a ~12-month grace window (removal ~2027-07). **Fleet stance (2026-09-18): sampling stays permitted.** `ctx.sample()` keeps working, Claude still supports it, and gates MUST NOT fail a repo merely for using it — flag at most INFO. New work should know the MRTR replacement exists but is not forced onto it during the grace window. See `fastmcp/2026-07-28-spec-migration.md`. |
| **Packaging** | **MCPB** (`mcpb pack`) — **no DXT** — [DXT_DEPRECATION.md](./DXT_DEPRECATION.md) |
| **Python** | **uv** + `pyproject.toml` + committed `uv.lock` |
| **Automation** | Root **justfile**; `uv run python` never naked `python` |
| **LLM manifests** | **`llms.txt` + `llms-full.txt`** pair |
| **Discovery** | **`glama.json`** at repo root |
| **Webapp ports** | Adjacent FE/BE pair from the reservoir — **do not restate the range here**, it drifts as the fleet grows (caught stale at 10700-10800 on 2026-09-10 when the real reservoir was already 10700-12000). Check the actual current range and register your pair in [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md), the sole source of truth. |
| **UI in chat** | Prefab for list / status / stats tools — [SOTA_REQUIREMENTS.md §2.2](./SOTA_REQUIREMENTS.md) |
| **Concurrency** | [fastmcp-3.2-concurrency.md](./fastmcp-3.2-concurrency.md) universal connect pattern |
| **JS package manager** | **Bun** replaces npm — [BUN_STANDARDS.md](./BUN_STANDARDS.md) |
| **Linting** | **Ruff 0.16.x** — the pinned `ruff-pre-commit` rev in `.pre-commit-config.yaml` MUST equal the ruff version `uv run ruff` resolves from the venv (dev dependency), and both are updated together. Never run a bare global `ruff.exe` against a repo as the source of truth — only the repo's own pinned version (`just lint` = `uv run ruff check .`, or the pre-commit hook) counts as the gate. Version drift between the two caused false-positive "ruff failures" fleet-wide on 2026-08-20 (global 0.15.16 vs pinned 0.11.0/0.16.0). |

---

## Retired (do not scaffold or cite as current)

- **FastMCP 2.12 / 2.14.x / any 2.x** as minimum version (superseded; do not use)
- **DXT** packaging (`.dxt`, `dxt.json`, `@anthropic/dxt`)
- **Poetry** for new MCP repos
- **FastMCP 3.1.0** as fleet minimum (superseded by 3.2+)

---

## Public publish slice (`sandraschi-collected-docs`)

**Mandatory IN after update** (see [PUBLISH_UPDATE_CHECKLIST.md](../PUBLISH_UPDATE_CHECKLIST.md)):

| Shelf | Path |
|-------|------|
| **Projects** | `projects/` — entire fleet tree |
| **Integrations** | `integrations/` — refresh for new releases |
| **AI** | `not-mcp-related/general-ai/`, `not-mcp-related/development/`, `protoconsciousness/` |

Plus BUILD/SAGA: `standards/`, `fastmcp/`, `tools/`, `skills/`, `operations/`, `patterns/`, `ecosystem/`.

See [WEED_MANIFEST.md](../WEED_MANIFEST.md) for exclude/slim rules.

---

## Doc update checklist (June 2026 pass)

- [ ] README badges: FastMCP **3.4.4+** (matches the floor declared above; this line
      said 3.2+ until 2026-09-18, contradicting the same file's own version table)
- [ ] Remove DXT install options — [DXT_DEPRECATION.md](./DXT_DEPRECATION.md)
- [ ] `integrations/README.md` — service catalog current
- [ ] `skills/**` — no 2.14.3 minimums
- [ ] `projects/robofang/mcp-servers/*.md` — purge 2.12 references
- [ ] CHANGELOG new entries reference **3.2+** and MCPB only

---

**Version:** 2026-09-18 (September refresh: FastMCP SOTA 4.0.5 verified against PyPI, pin widened to `<5`, sampling confirmed permitted through grace window ~2027-07, ports row left pointing at WEBAPP_PORTS.md as sole truth; snapshot otherwise unchanged from 2026-06-17) · Owner: Sandra Schipal
