# Memops import — Fleet cold-install probe program

**Created:** 2026-06-07  
**Tags:** fleet, meta_mcp, virtualization-mcp, naked-install, sandbox, cold-install  
**Status:** active program — scaffold phase

## Summary

Today's project: **cold install all fleet repos in Windows Sandbox (consumer / nearly naked)**, orchestrated by **meta_mcp**, executed via **virtualization-mcp** sandbox tools, with JSON + markdown reports and **Broken\*** reinstall-after-fix loops.

Complements the **cold-start probe** (start.ps1 on dev host). Cold-install answers whether `INSTALL.md` works for first-time users.

## Key decisions

- Sandbox profile: **consumer only** (`Launch-ConsumerSandbox.ps1`) — never dev-infra for naked tests.
- Separate outcomes from cold-start: `install_ok`, `install_failed`, `doc_gap`, `verify_failed`, `skip`.
- Batch 10–20 repos per session (sandbox relaunch is expensive).
- Reports: `fleet-cold-install-report.json`, `fleet-cold-install-{stamp}.md`, `comparison.install_failed_delta`.
- Artifact dir: `D:\Dev\repos\_sandbox_runs\<run_id>\`.

## Work tracker

Primary: `mcp-central-docs/projects/fleet-cold-install/TODO.md`  
Spec: `mcp-central-docs/docs/operations/FLEET_COLD_INSTALL_PROBE.md`

## Implementation map

| Layer | Repo | What |
|-------|------|------|
| Orchestrator | meta_mcp | Fleet Dashboard **Cold install** tab, REST API, progress poll |
| Sandbox | virtualization-mcp | Consumer WSB launch, fleet install script API (needs INSTALL.md alignment) |
| Reports | mcp-central-docs | `fleet-cold-install-probe.ps1`, manifest, `scripts/out/` |

## Related context

- Cold-start probe got `root_order_failed` + parse_failed delta (2026-06-07).
- NAKED_INSTALL_TESTING standard already documents consumer vs dev-infra.
- virtualization-mcp `POST /api/v1/fleet/install-script` exists but uses pip/`&&` — must align with fleet INSTALL.md / uv.

## Next actions (P0)

1. Implement `fleet-cold-install-manifest.json` sync from `INSTALL.md` presence.
2. meta_mcp `FleetColdInstallService` + UI tab (mirror cold-start).
3. Pilot 10 repos in consumer sandbox.
4. Broken\* reinstall after INSTALL.md fixes.

## Memops sync note

Import this file when memops MCP is online. Suggested memory title: `Fleet cold-install probe program 2026-06-07`.
