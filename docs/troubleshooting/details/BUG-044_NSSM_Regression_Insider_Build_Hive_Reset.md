# BUG-044: NSSM Fleet-Wide Path Regression After Windows Insider Dev Channel Build Swap

**Discovered:** 2026-09-22 (all NSSM services, via `meta_mcp` HTTP protocol probing)
**Severity:** P1 (all 17 NSSM-managed fleet services stopped simultaneously; no dashboards, no HTTP-mode MCP servers reachable)
**Component:** All NSSM services registered under `HKLM:\SYSTEM\CurrentControlSet\Services\*\Parameters`
**Status:** Root-caused. Remediation (self-healing boot repair) tracked below; not yet applied — see Follow-up.
**Regression of:** [`2026-09-10_nssm-fleetwide-repoint-and-ram-optimization.md`](../2026-09-10_nssm-fleetwide-repoint-and-ram-optimization.md)

---

## Symptom

Every NSSM-managed fleet service (`arxiv-mcp`, `discord-mcp`, `fastsearch-mcp`,
`fleet-agent-mcp`, `tvtropes-mcp`, `advanced-memory-mcp`, `email-mcp`, `devices-mcp`,
`mcp-federation-hub`, `mcp-pywinauto-mcp`, `ollama-serve`, `LiveKitSFU`, `RustDeskHbbr`,
`RustDeskHbbs`, `aiwatcher-mcp`, `fleet-hub`, `advanced-memory-mcp-daemon` — 17 total)
was `STOPPED` on boot. `sc.exe start <svc>` would transition to `START_PENDING` and then
immediately back to `STOPPED` with no listener ever opening on the assigned port.

Discovered while probing fleet servers with a new `mcp-explorer`-backed protocol check
(`fleet_ops(operation="protocol_probe")` in `meta_mcp`) — every HTTP-mode server except
the one already running (`meta_mcp` itself, started manually) was unreachable.

## Root Cause

Confirmed via `nssm.exe get <svc> AppDirectory` — every service's `AppDirectory` /
`Application` had reverted to `C:\dev\repos\<name>`, which has not existed since the
2026-08-05 migration to `D:\Dev\repos`. This is the **exact** corruption fixed fleet-wide
on 2026-09-10 by `discord-mcp/scripts/repoint-all-services.ps1`, which directly patched
the registry `Parameters` keys under `HKLM:\SYSTEM\CurrentControlSet\Services`.

Evidence timeline (from `C:\ProgramData\nssm-boot-check.log`, written by the
`Fleet-NSSM-boot-check` logon-triggered scheduled task):

| Time | All 17 services |
|---|---|
| 2026-09-19 23:42 | RUNNING (last known-good) |
| 2026-09-22 04:51 (first boot check after reboot) | STOPPED — 17/17 |

Windows Update history (`Microsoft.Update.Session` COM object, no elevation needed)
shows the trigger:

```
9/22/2026 2:18:11 AM  Windows 11 Insider Preview 29671.1000 (rs_prerelease)
```

`HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion` confirms this host is enrolled in
the **Windows Insider Dev Channel** (`DisplayVersion=Dev`,
`BuildLabEx=29671.1000.amd64fre.rs_prerelease.260911-1426`). The machine rebooted into
the new build at 04:16 AM; the first post-boot check at 04:51 AM already shows the full
regression.

**The structural bug is not "Windows reverted a registry key."** It's that the 2026-09-10
fix was applied as a **one-time imperative registry mutation** with no durable, re-
appliable source of truth. Anything that resets or restores the `HKLM\SYSTEM` hive — an
in-place OS upgrade (this case), a System Restore, a fresh image — silently regresses it,
and nothing re-applies the fix without a human noticing the outage first. Dev Channel
in-place build swaps are known to restore portions of the SYSTEM hive from a pre-upgrade
checkpoint; this is the second time in under two weeks this host's NSSM registrations
have been wiped by exactly that mechanism.

## Resolution / Follow-up (tracked, not yet shipped)

1. Extend `Fleet-NSSM-boot-check` (currently read-only logging, see
   `mcp-central-docs/scripts/nssm-boot-check.ps1`) to **detect and repair** stale
   `C:\dev\repos` paths on every boot, not just log them.
2. Register the repair as a **SYSTEM-context scheduled task** (`-RunLevel Highest -User
   SYSTEM`), not a user script requiring an interactive UAC click — a headless agent
   session cannot complete a UAC prompt (`Start-Process -Verb RunAs` returns "operation
   was canceled by the user" with no interactive desktop to consent on).
3. Add a canary check to `fleet-gate/nightly.ps1` (`Fleet-Nightly-Gate` scheduled task)
   that greps `HKLM:\SYSTEM\CurrentControlSet\Services\*\Parameters` for `C:\dev\repos`
   fleet-wide and fails the gate if found — catches it within 24h even without a reboot.
4. Reconsider Dev Channel enrollment on hosts running production-adjacent NSSM services;
   Beta/Release Preview channels get far less full-build churn.

## SOTA Impact

Confirms `standards/WINDOWS_SERVICE_STANDARDS.md` / `TRAPS_AND_PITFALLS.md` should treat
"registry-only fixes for OS-managed state" as inherently non-durable — any fix that lives
solely in a live `HKLM` mutation needs a companion boot-time (or update-triggered)
reconciliation step, not just a one-off repair script run by hand.
