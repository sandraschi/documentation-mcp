# BUG-085 — claim_ports.py allocates live-occupied ports (no liveness check)

**Date:** 2026-10-23 | **Severity:** P2 | **Component:** `mcp-central-docs/fleet-gate/claim_ports.py`
**Status:** Open (workaround applied) — registry fixed, squatter untouched

## Symptom

`claim_ports.py --repo rust-photoprism-mcp --apply` registered backend port
11250 while a live `stable-audio-spike` uvicorn (`python -m uvicorn app:app
--port 11250`) already listened on 127.0.0.1:11250. Our backend failed to
bind at startup (`web backend cannot bind 127.0.0.1:11250`). The health check
then "passed" against the WRONG server (stable-audio JSON), a false-green one
step away from shipping against someone else's API.

## Root cause

1. `claim_ports.py` checks `WEBAPP_PORTS.md` + every `fleet-start.config.ps1`
   only. `stable-audio-spike/` has no config file and no registry row, so the
   port looked free.
2. `WEBAPP_PORTS.md` even had a live-audit row (`11250 | python (180580) |
   native process listening`) that the claim did not treat as a block.
3. Unregistered services started by hand (`python -m uvicorn ... --port X`)
   are invisible to the whole claiming system.

## Workaround applied

Claimed adjacent pair 11251/11252 (verified live-free via
`Get-NetTCPConnection`), updated our two registry rows (own rows only),
backend default, vite proxy, and docs. Did NOT touch the squatter.

## Proper fix (open)

- `claim_ports.py` should probe `Get-NetTCPConnection` liveness for
  candidates and refuse occupied ports (Windows + POSIX paths).
- Fleet policy: every long-lived listener gets a `fleet-start.config.ps1`
  (even spikes) or it is killable without notice.
- Audit: `Get-NetTCPConnection` sweep vs registry to find other squatters
  (stable-audio-spike on 11250 is squatter #1, left running — tell Sandra
  before touching it).
