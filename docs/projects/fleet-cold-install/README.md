# Fleet cold-install probe (cross-repo program)

**Status:** Phase 2b host smoke landed (2026-06-07); sandbox execute + mcpb pilot pending  
**Owners:** meta_mcp (orchestration UI + API), virtualization-mcp (sandbox execution), mcp-central-docs (manifest + reports)

## Purpose

Batch-validate fleet `INSTALL.md` paths on a **nearly naked Windows** baseline inside Windows Sandbox consumer mode. Produces JSON + markdown reports with prior-run deltas, then supports **Broken\*** reinstall-after-fix loops.

## Why separate from cold-start

Cold-start caught `start.ps1` corruption and port bugs on the dev host. Cold-install catches what first-time users hit: missing winget ids, wrong Option order, `uv` vs `pip` drift, and docs that assume tools already on PATH.

## Docs

| Doc | Role |
|-----|------|
| [FLEET_COLD_INSTALL_PROBE.md](../../docs/operations/FLEET_COLD_INSTALL_PROBE.md) | Operations spec (modes, outcomes, report schema) |
| [TODO.md](./TODO.md) | Implementation checklist — **work from this** |
| [NAKED_INSTALL_TESTING.md](../../standards/NAKED_INSTALL_TESTING.md) | Sandbox profile rules (consumer vs dev-infra) |

## Repos involved

| Repo | Role |
|------|------|
| **mcp-central-docs** | Authoring mirror: probe scripts, manifest, `scripts/out/` reports |
| **meta_mcp** | **Canonical runtime:** `fleet_probes/`, Fleet Dashboard (Cold install tab), REST + MCP tools |
| **virtualization-mcp** | Sandbox launch, `install-mcpb` / `stdio-smoke` / `install-run` APIs |

**Note:** `mcpb install` outcomes apply to **Claude Desktop only**. Multi-IDE validation uses `stdio_*` smoke (Cursor, Windsurf, Antigravity, Zed, OpenCode).

**Sibling:** Cold-start probe now parses **dirty log** on every run — fix RAG/sync gaps before trusting install smoke. See [FLEET_WEBAPP_PROBE.md](../../docs/operations/FLEET_WEBAPP_PROBE.md).

## Quick links

- Work tracker: [TODO.md](./TODO.md)
- Cold-start sibling: [FLEET_WEBAPP_PROBE.md](../../docs/operations/FLEET_WEBAPP_PROBE.md)
- Memops note: [operations/memops-import/fleet-cold-install-2026-06-07.md](../../operations/memops-import/fleet-cold-install-2026-06-07.md)
