# BUG-034: NSSM Service Runs Dual-Transport `run_server.py` in Silent STDIO Mode, Causing Backend Hang and Launcher Restart Loop

**Discovered:** 2026-09-10 (`email-mcp`, `tvtropes-mcp`)  
**Severity:** P1 (High — backend never opens HTTP port; launcher loops indefinitely restarting service; frontend blocked by Session 0 zombie)  
**Component:** Python MCP servers migrated to NSSM services using PyInstaller/dual-transport `run_server.py`, consumed by `mcp-central-docs/scripts/Invoke-FleetWebappStart.ps1` (`Start-FleetNssapp`)  
**Status:** Fixed in `email-mcp`, `tvtropes-mcp`, and `Invoke-FleetWebappStart.ps1`

---

## Symptom

When launching `<repo>-start.bat` (or `start.ps1`):

```text
email-mcp service not healthy - restarting via NSSM
Backend restarted
[email-mcp] Clearing port listeners on 10812 ...
  could not stop PID 81060 (node, session 0)
[email-mcp-retry] Clearing port listeners on 10812 ...
  could not stop PID 81060 (node, session 0)
Waiting for backend on :10813 ...
```

The launcher hangs at `Waiting for backend on :<port> ...` for 30 seconds, fails the health check, and restarts the NSSM service again in an endless loop. Even after NSSM restarts the service, the port is never opened. Concurrently, `Stop-FleetPortSquatters` repeatedly reports `could not stop PID <PID> (node, session 0)`.

---

## Root Cause

This bug is an architectural trap formed by **three interlocking gaps**:

### 1. Dual-Transport Fallback Trap (`run_server.py`)
`run_server.py` was authored for PyInstaller desktop binaries with the dual-transport pattern:
```python
port = os.environ.get("MCP_PORT") or os.environ.get("PORT")
if port:
    # Run uvicorn HTTP
    sys.argv = ["run_server.py", "--http", "--host", host, "--port", str(port)]
main()
```
If neither `MCP_PORT` nor `PORT` is found in the environment, `run_server.py` assumes the caller is Claude Desktop / Cursor over a stdio pipe and falls back to **`run_stdio_async()`** (`sys.stdin`).

### 2. Incomplete NSSM Service Setup (Drift from BUG-033 Migration)
Following the BUG-033 migration, NSSM services were installed pointing to `python.exe run_server.py` as `LocalSystem`, but **without** passing `--http --port <port>` in `AppParameters` and **without** setting `+PORT=<port>` in `AppEnvironmentExtra`.
Because NSSM runs as `LocalSystem`, `PORT` was `None`. Python silently booted FastMCP into STDIO mode inside Session 0, waiting indefinitely on `sys.stdin` and **never binding to the HTTP port**.

### 3. Missing `-ElevatedFallback` in `Start-FleetNssmWebapp` (BUG-007 Regression)
`Invoke-FleetWebappStart.ps1`'s `Start-FleetNssmWebapp` called:
```powershell
if ($frontendPort -gt 0) {
    Stop-FleetPortSquatters -Ports @($frontendPort) -Label $svcName
}
```
It omitted `-ElevatedFallback`. When a previous run, watchdog, or system task left a Vite/Node process alive in Session 0 on the frontend port, unelevated `taskkill` failed with `Access is denied`. The launcher could neither clear the frontend port nor reach the backend.

---

## Resolution

1. **`run_server.py` Guard**:
   Updated `run_server.py` to check `MCP_PORT`, `PORT`, `WEB_PORT`, and fall back to the repo's assigned fleet port (e.g. `10813` for `email-mcp`, `10964` for `tvtropes-mcp`) unless `--stdio` is explicitly passed in `sys.argv`.
2. **LocalSystem Zombie Cleanup**:
   Added cleanup on service startup in `run_server.py` so the service uses its own `LocalSystem` / `SeDebugPrivilege` context to terminate any Session 0 orphaned processes holding the frontend port.
3. **Environment Hardening**:
   Added `PORT=<port>` and `MCP_PORT=<port>` to `.env`.
4. **Engine Hardening (`Invoke-FleetWebappStart.ps1`)**:
   Added `-ElevatedFallback` to `Stop-FleetPortSquatters` inside `Start-FleetNssmWebapp` line 636 per BUG-007 standards.

---

## Fleet Repos Audited & Fixed

| Repo | Backend Port | Status | Notes |
|---|---|---|---|
| `email-mcp` | 10813 | Fixed | Port 10813 responding, zombie PID 81060 killed, frontend operational |
| `tvtropes-mcp` | 10964 | Fixed | Had exact same STDIO trap; updated `run_server.py`, service responding `200 OK` |
