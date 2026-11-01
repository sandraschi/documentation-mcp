---
title: "Windows Service Standards (SOTA 2026)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-10
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# Windows Service Standards (SOTA 2026)

**Established:** 2026-07-31
**Reference impl:** `fastsearch-mcp` — C++ self-installing service with named pipe IPC
**Related:** [TRAPS_AND_PITFALLS.md](./TRAPS_AND_PITFALLS.md) §14 (LocalSystem) §17 (.bat wrappers)

## Problem

Fleet servers that must run as 24/7 Windows background services currently use a mix of NSSM, sc.exe, pywin32, and self-installing C++ — with no consistent pattern. The two dominant failure modes are:

1. **`.bat` wrapper fragility** (Trap 17): NSSM → `cmd.exe` → `.bat` → real binary. `cmd.exe` prompts "Terminate batch job (Y/N)?" on shutdown, service never restarts.
2. **LocalSystem split-brain** (Trap 14): Service runs as `LocalSystem`, `Path.home()` resolves to `C:\WINDOWS\system32\config\systemprofile\`, silently creating a second database invisible to user-context processes.

## Three Tiers

Choose based on the server's language and complexity. Descending order of robustness.

### Tier 1: Self-Installing Binary (C++ / Rust)

The binary registers itself with the SCM via `CreateServiceW()` / `DeleteService()`. No external manager needed. Reference: `fastsearch-mcp`.

**When to use:** New C++/Rust services. The binary is the single artifact — no install script, no NSSM, no dependency on a specific tool path.

**Pattern (Rust, equivalent to fastsearch-mcp's C++):**
```rust
// --install: self-register as a Windows service
// --uninstall: self-remove
// (no args): run as service via StartServiceCtrlDispatcherW
```

**Advantages:**
- Zero external dependencies — binary at any path can install/uninstall itself
- Binary knows its own metadata (name, display name, description) — single source of truth
- Cannot point at the wrong binary or wrong args

**Disadvantages:**
- Requires Win32 API calls in the binary (service control handler, status reporting)
- No built-in log rotation (use Windows Event Log or app-level log management)

**Fleet example:** `fastsearch-mcp` — `FastSearchServiceNew.exe --install` / `--uninstall`. The binary uses `CreateServiceW`, `RegisterServiceCtrlHandlerW`, `SetServiceStatus`, and `ReportEventW` directly.

### Tier 2: NSSM (Python / uv-based servers)

Use NSSM to wrap `uv.exe` (or any `.exe`) as a service. **NEVER point NSSM at a `.bat`, `.cmd`, or `.ps1` file.**

**When to use:** Python fleet servers that need `uv run`. The binary path never changes (`C:\Users\sandr\.local\bin\uv.exe`), arguments vary per service.

**Hard requirements:**
1. `Application` MUST be the real `.exe` (e.g. `uv.exe`), never a wrapper script
2. `AppParameters` carries all arguments
3. `AppDirectory` set to the repo root (or the subdirectory containing `pyproject.toml`)
4. `AppEnvironmentExtra` pins `USERPROFILE`, `APPDATA`, `LOCALAPPDATA`, `HOME` (Trap 14 fix)
5. `AppExit Default Restart` for crash recovery
6. `AppRotateFiles` + `AppRotateSeconds` + `AppRotateBytes` for log management

**Pattern:**
```powershell
$NSSM = "C:\Program Files\Jellyfin\Server\nssm.exe"
$UV   = "C:\Users\sandr\.local\bin\uv.exe"
$REPO = "D:\Dev\repos\aiwatcher-mcp"
$USER = "C:\Users\sandr"

& $NSSM install aiwatcher-mcp $UV
& $NSSM set aiwatcher-mcp AppParameters "run --directory $REPO python -m aiwatcher_mcp.api"
& $NSSM set aiwatcher-mcp AppDirectory $REPO
& $NSSM set aiwatcher-mcp AppEnvironmentExtra ("USERPROFILE=$USER`nAPPDATA=$USER\AppData\Roaming`nLOCALAPPDATA=$USER\AppData\Local`nHOME=$USER")
& $NSSM set aiwatcher-mcp Start SERVICE_AUTO_START
& $NSSM set aiwatcher-mcp AppExit Default Restart
& $NSSM set aiwatcher-mcp AppRotateFiles 1
& $NSSM set aiwatcher-mcp AppRotateSeconds 86400
& $NSSM set aiwatcher-mcp AppRotateBytes 10485760
& $NSSM set aiwatcher-mcp AppStdout "$REPO\data\logs\stdout.log"
& $NSSM set aiwatcher-mcp AppStderr "$REPO\data\logs\stderr.log"
```

**NSSM binary location (fleet):** `C:\Program Files\Jellyfin\Server\nssm.exe` (came with Jellyfin install). Also available via winget at `C:\Users\sandr\AppData\Local\Microsoft\WinGet\Links\nssm.exe`. The Jellyfin path is the fleet standard — hardcode it in install scripts.

**For services that need `.env` loading:** the application code MUST load `.env` itself at startup (`python-dotenv` or `pydantic-settings`). Do NOT use a wrapper script to source `.env` — that's exactly the `.bat` wrapper trap.

### Tier 3: sc.exe (simple native binaries)

Use native `sc.exe create` when the binary needs no environment setup, no working directory override, and no log rotation.

**When to use:** Simple native binaries (Rust, Go) that read their own config from a default location. The binary is self-contained.

**Pattern:**
```powershell
sc.exe create MyService binPath= "D:\path\to\binary.exe --arg1 --arg2" start= auto
sc.exe description MyService "One-line description"
sc.exe failure MyService reset= 86400 actions= restart/10000/restart/30000/restart/60000
```

**Note on `binPath=` syntax:** the `=` must be followed by a space. The path and args are a single string. Commas, semicolons, and spaces in the path/args require quoting:
```powershell
sc.exe create MyService binPath= "`"C:\Path With Spaces\bin.exe`" --flag value"

# The resolved binPath string becomes:
# "C:\Path With Spaces\bin.exe" --flag value
```

**Advantages:**
- No external tool (sc.exe is built into Windows)
- Simple, auditable config via `sc qc`

**Disadvantages:**
- No stdout/stderr capture
- No log rotation
- No working directory override (CWD is `%WINDIR%\System32`)
- Limited env var control
- `AppDirectory` equivalent requires registry editing

**When NOT to use sc.exe:**
- Binary needs a specific working directory
- Binary needs env vars set
- Binary is a `uv run` wrapper (use Tier 2 NSSM)
- You want stdout/stderr logs (use Tier 2 NSSM)

## Forbidden Patterns

| Pattern | Why forbidden |
|---------|---------------|
| NSSM → `.bat` / `.cmd` | `cmd.exe` kills on reboot (Trap 17) |
| NSSM → `powershell.exe -File wrapper.ps1` | PowerShell can hang teardown; same class as .bat |
| `sc create` with `uv.exe` via binPath | `uv run` args are too long; env vars needed; use NSSM |
| No `AppExit Default Restart` | Service crashes once, stays dead forever |
| No `AppEnvironmentExtra` for LocalSystem services | Silent split-brain (Trap 14) |
| Running as `LocalSystem` when no privileges needed | Adds split-brain risk for zero benefit |
| `sc.exe failure` without `reset=` | Default reset period is 0 (never resets); after 3 crashes the service stays dead |

## Verification Checklist

Before certifying a service as reboot-safe:

- [ ] `sc qc <service>` — `BINARY_PATH_NAME` is `.exe`, never `.bat`/`.cmd`/`.ps1`
- [ ] `START_TYPE` is `AUTO_START`
- [ ] NSSM services: `nssm status <service>` shows `SERVICE_RUNNING`
- [ ] NSSM services: `nssm dump <service> | findstr AppExit` shows `Default=Restart`
- [ ] LocalSystem services: `USERPROFILE` pinned via `AppEnvironmentExtra`
- [ ] Code-level: `Path.home()` replaced with `Path(__file__).resolve().parents[N]` or gated behind explicit config var
- [ ] Storage path logged at INFO on startup
- [ ] Service survives `Restart-Service <service> -Force`
- [ ] Port bound after restart: `Get-NetTCPConnection -LocalPort <port>`
- [ ] Service survives a full reboot (tested after script run)

## Fleet Service Inventory

| Service | Tier | Binary | Pinned? | Bat-free? |
|---------|------|--------|---------|-----------|
| `aiwatcher-mcp` | 2 (NSSM) | `uv.exe` | Yes | Yes (fixed 2026-07-31) |
| `arxiv-mcp` | 2 (NSSM) | `pwsh.exe` (`uv.exe`) | Yes | Yes (fixed 2026-09-10) |
| `advanced-memory-mcp` | 2 (NSSM) | unknown | Yes | Unknown |
| `devices-mcp` | 2 (NSSM) | `uv.exe` | Yes | Yes (fixed 2026-07-31) |
| `fleet-agent-mcp` | 2 (NSSM) | `uv.exe` | Yes | Yes (fixed 2026-07-31) |
| `fleet-hub` | 2 (NSSM) | unknown | Yes | Unknown |
| `mcp-federation-hub` | 2 (NSSM) | `pwsh.exe` | Yes | Yes (.ps1 → pwsh.exe is acceptable if non-interactive) |
| `mcp-fleet-agent-mcp` | 2 (NSSM) | unknown | Yes | Unknown |
| `mcp-pywinauto-mcp` | 2 (NSSM) | unknown | Yes | Unknown |
| `tvtropes-mcp` | 2 (NSSM) | `uv.exe` | Yes | Yes (fixed 2026-07-31) |
| `RustDeskHbbs` | 2 (NSSM) | `hbbs.exe` | N/A | Yes (fixed 2026-07-31) |
| `RustDeskHbbr` | 2 (NSSM) | `hbbr.exe` | N/A | Yes (fixed 2026-07-31) |
| `FastSearchMCP` | 1 (Self-installing) | `FastSearchServiceNew.exe` | N/A | N/A (native) |

## Reference Implementations

| Pattern | Repo | File |
|---------|------|------|
| Tier 1: Self-installing C++ | `fastsearch-mcp` | `fastsearch_service.cpp` |
| Tier 1: C++ service bridge (Python) | `fastsearch-mcp` | `src/fastsearch_mcp/service_client.py` |
| Tier 2: NSSM + uv.exe (Python) | `mcp-central-docs/scripts` | `fleet-fix-nssm.ps1` |
| Tier 3: sc.exe (Rust) | `rustdesk-server` | `install-server.bat` |
| Fleet pinning script | `mcp-central-docs/scripts` | `fix-nssm-pins-and-arxiv.ps1` |
| Fleet audit script | `mcp-central-docs/scripts` | `audit-nssm-env.ps1` |

---

## Post-2026-08-05 Hardening (fleet-agent outage)

Incident: [2026-08-05 postmortem](../troubleshooting/2026-08-05_defender-copyfail-venv-corruption.md) - Defender CopyFail false-positive nuked venvs, stale NSSM paths kept the hub down 2+ days, no logs existed.

### 1. Stale Path Audit (MANDATORY after any repo move)

A NSSM service whose `Application` / `AppDirectory` / `AppParameters` point at a moved/renamed path fails silently - service state stays `Stopped`, no error, no log. After `fleet-agent-mcp` moved `C:\dev\repos` -> `D:\Dev\repos`, **5 of 14 NSSM services** were stale.

**Audit command:**
```powershell
Get-CimInstance Win32_Service | Where-Object { $_.PathName -match "nssm" } | ForEach-Object {
    $name = $_.Name
    $app = (nssm get $name Application 2>&1) -join ";"
    $dir = (nssm get $name AppDirectory 2>&1) -join ";"
    if ($app -match "C:\\dev" -or $dir -match "C:\\dev") { "STALE: $name | $app | $dir" }
}
```
Fix: `nssm set <svc> Application/AppDirectory/AppParameters <new path>` (elevated), then `Start-Service`.

### 2. Log Capture (MANDATORY for every NSSM service)

A service that writes nowhere is undebuggable. The 2026-08-05 crash (ModuleNotFoundError at startup) produced zero traces - NSSM discards stdout/stderr by default. Every NSSM service MUST configure:

```powershell
nssm set <svc> AppStdout "<repo>\logs\<svc>-stdout.log"
nssm set <svc> AppStderr "<repo>\logs\<svc>-stderr.log"
nssm set <svc> AppRotateFiles 1
nssm set <svc> AppRotateBytes 10485760   # 10 MB
nssm set <svc> AppRotateOnline 1          # rotate without service restart
Restart-Service <svc>
```

### 3. Hang Detection (NSSM's blind spot)

NSSM restarts the app **only when the process exits**. A hung-but-alive process (deadlocked listener, stuck event loop) sits dead forever - service shows Running, health check fails. Every long-running NSSM service MUST pair with a health-check watchdog task:

- Script: `mcp-central-docs/scripts/fleet-watchdog.ps1` (every 20 min)
- Config: `fleet-watchdog-config.json` - add `"RestartService": "<service-name>"` so the watchdog calls `Restart-Service` instead of spawning an orphan process (which would conflict on the port and escape NSSM supervision)
- The `processMatch` kill path is only for non-service repos; it now falls back to matching the repo cwd (never an empty pattern - that matches every python process)

### 4. Tailscale Serve vs Local Listener

`tailscale serve` keeps the external listener alive even when the backend is dead - `Get-NetTCPConnection -LocalPort X` will match the tailscaled socket. Any port-check must filter `-LocalAddress 127.0.0.1` (see `fleet-agent-mcp/scripts/start-intel-hub.ps1`).
