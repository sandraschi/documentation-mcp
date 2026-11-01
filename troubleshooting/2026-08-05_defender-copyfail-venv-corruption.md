# Postmortem: Intel Reports Hub 404 / Fleet Agent Silent Outage (2026-08-05)

**Severity:** P1 (long-running infrastructure down 2+ days, invisible to user)
**Affected:** `fleet-agent-mcp` (backend + Intel Reports Hub :11027), 5 other fleet venvs (agy, fleetwatcher, git-github, learnbot, mcp-agent-session-summaries)
**Discovered:** 2026-08-05 11:10 via `http://localhost:11027/` returning 404

## Symptoms

- `localhost:11027` (Tailscale `goliath...ts.net:11027`) returned 404 while the port showed as "listening"
- `fleet-agent-mcp` NSSM service showed Running, but `/api/health` on 10996 refused connections
- Report files in `~/.fleet-intel` kept updating (last write 11:29) while the HTTP hub was dead
- Daily job at 07:04 crashed on `ModuleNotFoundError: No module named 'pydantic_core.core_schema'`
- No log file anywhere - the crash was invisible

## Root Cause Chain (3 independent layers)

### Layer 1 - Defender false positive nuked venv files
A new signature family `Exploit:Python/CopyFail.A` (+ Linux variants, threat IDs 2147968233-2147968270) shipped ~2026-07-31. The daily scheduled Defender scan (08:28) quarantined 8+ `.py` files out of Python `site-packages` on 08-01, more on 08-02 (12x event 1011 purge). The pattern: `.py` modules deleted, `__init__.py`, compiled `.pyd`, and `dist-info` left intact - so uv considered the package installed and `uv sync` did NOT repair it.

Known false-positive family (has hit `python-dotenv` before). In fleet-agent-mcp it took `pydantic_core/core_schema.py` + `dotenv/dotenv.py`.

**6 repos affected:** agy-mcp, fleet-agent-mcp, fleetwatcher-mcp, git-github-mcp, learnbot-mcp, mcp-agent-session-summaries

### Layer 2 - Stale NSSM service paths
`fleet-hub` NSSM service pointed at `C:\dev\repos\fleet-agent-mcp\run-fleet-hub.bat` - repos had moved to `D:\Dev\repos`, so the service could never start. **Audit found 5 more stale services:** `aiwatcher-frontend`, `mcp-federation-hub`, `mcp-fleet-agent-mcp`, `mcp-pywinauto-mcp` (all `C:\dev\repos`).

### Layer 3 - Watchdog tasks disabled + hang blind spot
All 5 `Fleet-*` watchdog tasks (fleet-watchdog.ps1, every 20 min, HTTP health check) were disabled 2026-07-07 01:07. The watchdog would have detected the dead hub within 20 minutes. Additionally the watchdog's restart logic had a footgun: with `processMatch` unset, the empty regex matched ALL python processes - mass-killing every fleet server before spawning an orphan process outside NSSM (port conflict). This was very likely why the tasks were disabled.

## Why it looked alive

1. `tailscaled` holds the external `:11027` listener (`tailscale serve`) - port shows Listening, `start-intel-hub.ps1`'s `Get-NetTCPConnection` check false-positived ("already listening")
2. `intel_hub/client.py` falls back to writing report files directly to disk when the HTTP hub is down - publishers kept writing, masking the outage
3. NSSM services crash-restart on exit but cannot detect a hung-but-alive process

## Code-Level Failure Chain (why every link was silent)

The outage was invisible not just because of infra gaps - the servers themselves had no
defense against dying quietly. This is the part to internalize:

1. **No logging configuration anywhere.** `logger.*` calls across the package (e.g. the
   hub-unreachable notice in `client.py`) hit the root logger with no handlers - dropped.
   Python's fallback `lastResort` handler only surfaces WARNING+ to stderr, which NSSM
   discarded by default. `info`-level diagnostics were pure no-ops.
2. **Bare `uvicorn.run` with no crash boundary.** Both `run_server.py` and
   `intel_hub/server.py` called `uvicorn.run(...)` directly. Import-time failures
   (the `ModuleNotFoundError`) happen BEFORE any logging exists; startup failures after
   import print to stdout/stderr only. Either way: trace goes nowhere persistent.
3. **Silent success instead of loud fallback.** `client.py`'s filesystem fallback was
   logged at `info` and returned `success: True` with `via: "filesystem"` - the pipeline
   looked healthy while the hub was dead. A fallback that hides the primary failure is a
   masking layer, not a resilience feature.
4. **No watchdog alarm on staleness.** The hub's own report files kept getting timestamps,
   so even "check the last report time" looked fine.

**Hardening applied (2026-08-05):**

| File | Change |
|------|--------|
| `run_server.py` | Rotating file logging to `logs/server.log` (10 MB x3) + top-level `except BaseException` writing traceback to `logs/crash.log`. Import crashes now leave a trace on disk. |
| `src/fleet_agent/intel_hub/server.py` | Same: `logs/intel-hub.log` + `logs/intel-hub-crash.log` |
| `src/fleet_agent/intel_hub/client.py` | Hub-unreachable fallback raised to `logger.warning` - visible on stderr (captured by NSSM) and in the hub log |

**Fleet rule (from this incident):** a long-running server that writes nowhere is
undebuggable. Every entrypoint MUST (a) configure rotating file logging at startup,
(b) wrap startup in a crash boundary that writes the traceback to disk, and (c) log
fallbacks/masking layers at WARNING or above. See also
`standards/TOOL_DESIGN_STANDARDS.md` §7.1 (Server Hardening Patterns).

**Naked print prohibition (already fleet law, was violated anyway):** ruff rule
`T20` (flake8-print) is enabled fleet-wide - "Forbidden in Production Modules"
(`standards/RUFF_STANDARDS.md`). Exceptions: `tests/*` only. A pre-existing
`print(f"[health] db error: {exc}")` in `fleet_agent/server.py:396` had shipped
under this rule; it is now `logger.warning`. Audit finding: run
`uv run ruff check src/ --select T20` on every touched repo before commit - a
naked print in an error path is a silent-failure ticket waiting to be written.

## Timeline

| When | What |
|---|---|
| 2026-07-04 | Watchdog tasks installed |
| 2026-07-07 01:07 | All 5 watchdog tasks disabled (batch) |
| 2026-07-31 18:40 | First Defender CopyFail detection (signature push) |
| 2026-08-01 08:28 | Scheduled scan quarantines 8+ venv files (6 repos) |
| 2026-08-02 08:28 | More quarantine purges |
| 2026-08-03 ~21:53 | Hub stops serving; reports continue via filesystem fallback |
| 2026-08-05 07:04 | Daily job crashes on broken pydantic_core |
| 2026-08-05 11:10 | User hits 404 on :11027 |

## Fixes applied (2026-08-05)

1. **Venv repair:** `uv sync --reinstall` in fleet-agent-mcp + 5 other affected repos (verified pydantic imports OK)
2. **Defender exclusion:** `D:\Dev\repos` added to Defender exclusion path list (elevated)
3. **`UV_LINK_MODE=copy`** set via `setx` - protects venvs from sharing corrupted cache entries via hardlinks
4. **NSSM stale paths:** repointed `fleet-hub` (and `aiwatcher-frontend`, `mcp-federation-hub`, `mcp-fleet-agent-mcp`, `mcp-pywinauto-mcp`) to `D:\Dev\repos`; started `fleet-hub` service (hub back on :11027)
5. **NSSM log capture:** `AppStdout`/`AppStderr` + `AppRotateFiles`/`AppRotateBytes 10MB`/`AppRotateOnline` for `fleet-agent-mcp` and `fleet-hub` -> `D:\Dev\repos\fleet-agent-mcp\logs\*.log`. Future crashes land in a file.
6. **Watchdog fixes (`mcp-central-docs/scripts/fleet-watchdog.ps1`):**
   - New `RestartService` config field: health check fail -> `Restart-Service <name>` (NSSM owns the restart, no orphans, no port conflict)
   - Safe `processMatch` fallback: empty pattern no longer kills every python process; falls back to matching the repo cwd
   - Config: `RestartService` added for 5 NSSM-managed repos + new `fleet-hub` entry
7. **Watchdog tasks:** all 5 re-enabled + new `Fleet-fleet-hub` task registered (20-min interval)

## Prevention / Standards

- **Defender:** CopyFail family is a known false-positive on real Python packages. Fleet venv dirs are now excluded. If a new signature wave hits: symptom is `ModuleNotFoundError` for a package that `uv sync` refuses to repair -> `uv sync --reinstall` (or `--force-reinstall` per package).
- **NSSM services:** MUST audit `Application`/`AppDirectory`/`AppParameters` against the current repo layout after any repo move (see `standards/WINDOWS_SERVICE_STANDARDS.md` "Stale Path Audit").
- **NSSM services:** MUST configure `AppStdout`/`AppStderr` + rotation. A service that writes nowhere is undebuggable.
- **Hang detection:** NSSM restarts on process exit only. Every NSSM-managed long-runner needs a health-check watchdog task (`RestartService` mode) to catch hung-but-alive processes.
- **start-intel-hub.ps1:** port check now filters `-LocalAddress 127.0.0.1` (tailscaled listener no longer false-positives).

## Verification

- `http://127.0.0.1:11027/` -> HTTP 200 (hub service)
- `http://127.0.0.1:10996/api/health` -> HTTP 200 (agent service)
- Both NSSM services Running; 6 watchdog tasks Ready
- Log files present in `D:\Dev\repos\fleet-agent-mcp\logs\` (rotating)
