# Daemon tiering plan — complications only where they pay (implement later)

**Status:** Plan written 2026-10-04 · NOT started · implement in calm water, not during fires
**Tags:** [fleet, tiering, daemon, stdio, nssm, dx, plan]
**Parent mandate:** [start-ps1-convergence-mandate](start-ps1-convergence-mandate.md) (Decision 4)

## Usage patterns (the only taxonomy that matters)

- **Daily grind:** invoked most days, or runs background loops on a schedule. Owns state that must survive restarts. Examples: calibre (13k books + RAG), memops (live vault), aiwatcher (04:55 UTC digest job + fleet-event ingest), speech-mcp during voice periods, arxiv triage, fleet-agent.
- **Blue moon:** invoked a few times a month or less, stateless, wraps an external tool. Examples: notepadpp (Notepad++ ops), handbrake (transcode runs), blender, freecad, reaper, virtualdj. Long *jobs*, zero *memory* — the job needs a babysitter, not a landlord.
- **Early days:** scaffolded, no users, no traffic, no evidence yet. Most of the ~200. Gets Tier 0 by default until it proves otherwise — no pre-emptive daemons for hypothetical load.

## Tier criteria (graduate with evidence, not vibes)

| Question | Yes → |
|---|---|
| Must state survive process death (DB, index, ledger)? | Tier 1 minimum |
| Background loops on a schedule even with no client attached? | Tier 2 |
| Heavy model/device load (seconds to warm, VRAM, exclusive mic)? | Tier 1 (session-scoped warm pool) |
| Concurrent clients contend on one resource (SQLite writes, LanceDB)? | Tier 1 minimum (single owner) |
| None of the above? | Tier 0, no daemon, no port, no service |

- **Tier 0 — stdio-only.** No port, no service, no elevation story. SQLite WAL absorbs concurrent readers; single writer per call. New repos start here.
- **Tier 1 — on-demand daemon.** First client starts it (headless, user session), idle timeout reaps it, jobs/state persisted so death is boring. No boot autostart, no SYSTEM, restart = kill a process you can see.
- **Tier 2 — always-on service (earned).** NSSM + runbook + Session-0 discipline + Tauri port-truce row. Only with contention logs or schedule proof.

## Worked exemplars (audited 2026-10-04)

- **notepadpp-mcp → Tier 0.** Stateless Notepad++ op executor, no data dir, no loops. Carries full uvicorn+vite scaffold today (10815/10814) for nothing. Strip to stdio; keep webapp as `just web` opt-in, not boot.
- **handbrake-mcp ("hmdbrake-c") → Tier 0.** 2025 completist wrapper, ~1 job/month (10GB badly-released historical anime that needs proper compression). No daemon at all: persist job state to disk so any fresh stdio instance can report progress on the running HandBrakeCLI child; watch-folder stays disabled until monthly usage says otherwise. The `watch/` + `processed/` dirs are aspiration, not load.
- **aiwatcher-mcp → Tier 2 (earned).** SQLite (`database.py`, upsert_item), `data/` + `logs/` + `reports/`, scheduled 04:55 UTC digest, fleet-event ingest with Grafana dashboard, Tauri shell. Daily grind with background schedule — the textbook Tier-2 resident. Keep service; write the restart runbook; add the Tauri port-truce row.
- **speech-mcp → Tier 1 (session warm pool).** `models/` + lazy Kokoro/whisper extras ("honest-extra pattern"), exclusive mic, background wake threads. Always-on wastes VRAM and the mic 20h/day; cold-start costs seconds per session. Daemon starts on first voice op, stays warm while wake is armed, reaps on idle. Tier 2 only if house-wide always-listening becomes an explicit requirement.
- **openbci-mcp → Tier 0 (poster child).** EEG-DIY-skullcap wrapper: no .venv (never installed), no data dir, no logs, no users outside sf daydreams — yet holds a full uvicorn+vite port pair (10759/10758). Fantasy hardware gets stdio + on-demand webapp like everything else; if neuralink-for-the-masses ever arrives, the tier flips with the traffic.

## Iron rule: tiering never deletes webapps

Downgrading a repo's *daemon tier* touches boot behavior only — never the webapp, never features. Every repo keeps its full UI; Tier 0/1 repos launch it on demand (`just web` / start-on-first-use) instead of at boot. Rationale: usage is per-user, not per-repo. Sandra's handbrake runs once a month; a cloner with 300 oversize disk-destroyers runs it daily — same code, same webapp, different tier *for that user*. Tier labels live in per-install config, and promoting Tier 0 → 1 is a config flip plus the documented prerequisite (e.g. handbrake's job persistence), never a fork. No audit wave removes a single page, button, or endpoint.

## Rollout (waves, not stampedes)

1. Freeze tiers for the 4 exemplars above (pilot, proves the pattern).
2. Audit waves of ~10 repos: classify grind/moon/early-days from evidence (data dirs, loops, schedules, model weights — not README claims). ≤5 files per commit, per repo testing.
3. Downgrades (daemon → on-demand/stdio) ship with a revert note; any regression reverts the single repo, never a fleet patch.
4. Upgrades require a one-paragraph evidence note in the repo (contention log, schedule, weights). No note, no daemon.
5. Early-days repos are never audited up — they graduate when usage says so.

## Done looks like

~12 Tier-2 services with runbooks, ~30 Tier-1 on-demand daemons, everything else stdio. Boot time down, Session-0 footprint minimal, elevation needed only for the Tier-2 dozen, Tauri builds never fight a daemon for a port. The daily start.ps1 lottery becomes a weekly glance at the probe dashboard.
