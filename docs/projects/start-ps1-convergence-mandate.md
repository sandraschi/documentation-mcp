# Fleet launcher convergence mandate — end the start.ps1 lottery

**Status:** Mandate adopted 2026-10-04 · not yet built · highest-leverage unsexy work in the fleet
**Tags:** [fleet, start-ps1, services, nssm, tauri, dx, mandate]
**Trigger:** calibre-mcp `start.ps1` called phantom `Invoke-FleetFreePort` (zero definers fleet-wide) — silent restart death, found 2026-10-04 during backbone repair. Same shape as the daily failures.

## Measurement (2026-10-04, rg over D:\Dev\repos excl. _archives/_upstream/externals)

- ~200+ repos carry `start.ps1`; **231 vendored `FleetStartMode.ps1` copies in 6 variants** (207 converged, 24 drifted across 24 repos incl. mcd itself).
- Every fleet-wide launcher "fix" is a ~231-file mutation — 46x over the 5-file safety limit. Sync scripts cannot see per-repo mitigations, so they pave over them. The daily lottery is structural, not moral.

## Decision 1: single-source the launcher

- Repos keep a **5-line shim**: dot-source the canonical `mcp-central-docs/scripts/FleetStartMode.ps1`, declare ports, declare backend command. No logic in the shim.
- Vendored copies become frozen shims; drift is deleted, not merged. The 207-converged majority proves content is stable enough to freeze.
- Sync scripts are henceforth **banned from editing shims**; they may only bump the canonical file + conformance list.

## Decision 2: conformance probe before every sync (Test-FleetStarts)

- Static check, no launches: parse each `start.ps1` for called `Verb-Fleet*` functions, verify each exists in the canonical launcher. Report phantoms (today's bug class) as gate failures.
- Dynamic check (opt-in per repo): headless probe run (`FLEET_PROBE_RUN=1`) asserting port-bind → health-200 → clean exit, Session noted.
- No sync ships with a red probe. (`mcd scripts/Test-FleetStarts.ps1` is the seed — promote it to gate.)

## Decision 3: mitigation registry the sync must consult

- `operations/LAUNCHER_MITIGATIONS.md`: per-repo rows (repo, symptom, local fix, date, fixed-by). Sync author must attest "consulted, none overwritten" — a fix that deletes a row without resolving its symptom fails review.
- Today's calibre row is entry #1 (phantom call → Stop-FleetPortSquatters + Session-0 note).

## Decision 4: tiered daemon model — complications only where they pay

The honest answer to "are backends-as-services worth the hassle": **only for repos that own heavy persistent state.** Rest is cargo-culted complexity. Three tiers:

- **Tier 0 — stdio-only (default for new repos).** No daemon, no port, no service, no elevation story. SQLite WAL absorbs concurrent clients; LanceDB optional-local. Kills the entire failure class.
- **Tier 1 — on-demand daemon.** First client starts it (headless, user session), last client stops it, idle timeout reaps it. For medium state (caches, watchers). No boot autostart, no SYSTEM, restart = kill process you can see.
- **Tier 2 — always-on service (earned, not default).** Only for proven heavy state: calibre 13k books + RAG index, memops vault, fleet-hub. NSSM + sc.exe + Session-0 handling documented per-repo, restart runbook tested, Tauri builds bind a *different* port profile so NSIS installs never fight the service (see below).

New repos start at Tier 0 and graduate with evidence (contention logs, not vibes). Existing Tier-2 residents get audited down unless they prove the state need.

## Decision 5: Tauri/NSIS port truce

- Service daemons and Tauri-embedded backends **never share a port profile**: services on fleet registry ports, Tauri-embedded on loopback-ephemeral or registry+100 discipline, recorded in `operations/WEBAPP_PORTS.md` per repo.
- NSIS installer (user context) must detect a running service daemon and offer reuse-or-replace — never silent double-bind. Tauri production-pitfalls checklist gains a launcher-conformance item.

## Non-goals

No "all repos green always" promise (unachievable, stop bleeding for it) · no new sync that edits 200 files · no elevation-requiring routine ops · no watchdog that respawns what a human just killed on purpose.

## v0 (when picked up)

1. Freeze canonical `FleetStartMode.ps1`; generate thin shims; delete drift (one repo at a time, tested, ≤5 files per commit).
2. Promote Test-FleetStarts to pre-sync gate; first full run = baseline phantom list.
3. Open `operations/LAUNCHER_MITIGATIONS.md` with the calibre entry.
4. Tier-label every NSSM service + headless daemon (audit down the unjustified).
5. Port-truce rows in WEBAPP_PORTS.md for all Tauri repos with Tier-2 daemons.
