# BUG-023 — Service DACL Broken Grant (fleet-watchdog NSSM services)

- **Severity**: P1 (5 services unmanageable; service control plane locked out)
- **Date**: 2026-08-15
- **Repo/Component**: `mcp-central-docs/scripts/service-acl-setup.ps1` (v1) → **aiwatcher-mcp, fleet-agent-mcp, devices-mcp, advanced-memory-mcp, fleet-hub** (all NSSM services)
- **Status**: ✅ Fixed (service-acl-setup.ps1 rewritten; fleet-watchdog restart branch hardened)

## Symptom

After running the first version of `service-acl-setup.ps1` (which applied `sc sdset` with an `(A;;RPWPCR;;;<SID>)` DACL), **every service-control operation failed with access denied on all 5 services**:

```
sc.exe query aiwatcher-mcp      -> [SC] EnumQueryServicesStatus:OpenService FAILED 5: Access is denied.
Get-Service aiwatcher-mcp       -> (empty, silently skipped)
Restart-Service aiwatcher-mcp   -> Cannot find any service with service name 'aiwatcher-mcp'
New-Object ServiceController    -> object created, .Status blank
sc.exe sdshow aiwatcher-mcp     -> OpenService FAILED 5 (even elevated, even as SYSTEM)
sc.exe sdset aiwatcher-mcp ...  -> OpenService FAILED 5 (cannot repair via sdset)
```

The daemons themselves kept running (NSSM holds the process; health checks 200) — only the
control plane was dead. Diagnosis red herrings that burned ~40 min: "deny-all ACL",
"SeRestorePrivilege bypass", "wrong account", "RPC unavailable" (the latter two were
marshaling bugs in the diagnosis scripts — `$null` vs `""` and a swapped parameter order
producing ERROR_INVALID_NAME 123 / RPC_S_SERVER_UNAVAILABLE 1722).

## Root Cause

1. **`sc sdset` accepts the SDDL and writes it verbatim — `RPWPCR` is NOT a read/query grant.**
   In service SDDL, `RPWPCR` decodes to `RP` (SERVICE_START) + `WP` (SERVICE_STOP) + `CR`
   (SERVICE_USER_DEFINED_CONTROL) = access mask **0x130**. It grants start/stop/control but
   **no READ_CONTROL (0x20000), no SERVICE_QUERY_STATUS (0x4), no SERVICE_QUERY_CONFIG (0x1),
   no SERVICE_ENUMERATE_DEPENDENTS (0x8)**. Result: every open for query/status/config —
   which is what `Get-Service`, `sc query`, `sc sdshow`, `Restart-Service`'s status probe and
   the SCM's own enumeration all need — is denied, for **everyone including Administrators**,
   because those rights are simply not in any ACE.
2. **Repair is a chicken-and-egg**: `sc sdset` needs SERVICE_CHANGE_CONFIG + READ_CONTROL to
   even open the service handle; a DACL that lacks those rights cannot be repaired with
   `sc.exe` at all — elevated or not. `sc.exe` also never enables SeRestorePrivilege, and
   that privilege does not bypass DACLs for *service* objects (it is file-scoped), so running
   it as SYSTEM does not help either.
3. **The fixer used the wrong access mask**: `OpenService(..., 0x10000)` = **DELETE**, not
   WRITE_DAC. WRITE_DAC = **0x40000**. With DELETE requested, even the legitimate owner
   (SYSTEM) was denied — owner-implicit WRITE_DAC only covers WRITE_DAC.

## Resolution

1. **Inspect the true state via the registry** (bypasses the broken service DACL entirely —
   registry ACLs are separate):
   `HKLM\SYSTEM\CurrentControlSet\Services\<name>\Security\Security` is a REG_BINARY
   security descriptor; parse with `RawSecurityDescriptor` to see owner + ACEs.
   → owner = **S-1-5-18 (SYSTEM)**, ACEs = SY/BA/user all `access=304 (0x130)`. Not deny-all;
   just rights-starved.
2. **Repair as SYSTEM via a one-shot scheduled task** (`schtasks /ru SYSTEM`), using P/Invoke
   `SetServiceObjectSecurity`: SYSTEM owns the services → owner-implicit WRITE_DAC grants the
   handle regardless of the DACL. Applied a rich rights SDDL:
   `D:(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;SY)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)(A;;CCLCSWLOCRRC;;;AU)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;<userSID>)`
   (full management incl. CHANGE_CONFIG for the user, AU gets read/query).
3. **SCM crash recovery** on all 5: `sc failure <svc> reset= 86400 actions= restart/5000/restart/10000/restart/30000`.
4. **Rewrote `service-acl-setup.ps1`** (v2): self-elevates, embeds the SYSTEM-task + P/Invoke
   fixer, **verifies after write** (registry re-read: user ACE present + `Get-Service` works),
   idempotent. Log: `service-acl-setup.log`.
5. **fleet-watchdog.ps1** restart branch now polls the health URL after `Restart-Service`
   before claiming success (was returning `true` blind).

Log snippet (certified dead-path test):

```
2026-08-15 02:29:31 Check: aiwatcher-mcp
2026-08-15 02:29:33 DEAD: aiwatcher-mcp not responding - restarting
2026-08-15 02:29:35 Restarted service aiwatcher-mcp
2026-08-15 02:29:38 OK: aiwatcher-mcp healthy after service restart (3s)
```

## Fleet Audit

- `rg "sdset" D:\Dev\repos -g "*.ps1"` → **only** `mcp-central-docs/scripts/service-acl-setup.ps1`
  (v2 is the safe one). No other repo writes service DACLs.
- `fastsearch-mcp` uses `sc.exe failure` + `Restart-Service` (recovery config only — unaffected).
- WINDOWS_SERVICE_STANDARDS.md reviewed; this incident added the DACL-repair technique to
  the operational docs (aiwatcher-mcp `docs/OPS.md` § Watchdog Interplay).

## SOTA Impact / Hardening

- **Never grant bare `RPWPCR` on services** — if read/query rights are not already present
  from the default DACL, every status tool breaks. Use the rich rights string above or the
  spooler-style defaults (`CCLCSWLOCRRC` for AU-class access).
- **`sc sdset` cannot self-repair a rights-starved service** — the SYSTEM-task P/Invoke
  technique in `service-acl-setup.ps1` is the canonical repair path (owner-implicit WRITE_DAC).
- **WRITE_DAC = 0x40000** (0x10000 is DELETE) — verify access masks against
  `winnt.h`/docs before P/Invoking service APIs.
- Service control from scheduled (non-elevated) contexts requires the user-SID ACE with
  START/STOP **plus** QUERY rights; re-run `service-acl-setup.ps1` after any NSSM reinstall.
