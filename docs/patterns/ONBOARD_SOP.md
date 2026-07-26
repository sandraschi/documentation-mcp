# Onboard New Repo — SOP

**Trigger**: `onboard <repo-name>`
**Reference macro**: `agentic_macros.md` → `onboard`
**Scope**: First-time setup for a repo you've never run before. Install deps, start backend, open browser.

---

## Why onboard

Every fleet repo has a different startup sequence despite the shared conventions. `start.ps1` exists in most repos but may need `.env` configured, specific Python/Node versions, or port-clearing. This SOP gets a dev from zero to running dashboard in under 2 minutes.

---

## Phase 1 — Verify & context

```powershell
Test-Path "D:\Dev\repos\{repo-name}"
```

If the repo doesn't exist, stop and report. Do not clone — the repo should already be local.

Read the repo type from `pyproject.toml` (or `docker-compose.yml`, or `package.json`) and the startup script from `start.ps1` or `start.bat` to understand the expected ports.

---

## Phase 2 — Install deps

```powershell
cd D:\Dev\repos\{repo-name}

# Python deps
uv sync

# Webapp deps (if webapp exists)
if (Test-Path webapp/package.json) {
    cd webapp
    if (Test-Path bun.lock) { bun install } else { npm install }
    cd ..
}
```

If `uv sync` fails, report the error and stop — don't proceed with a broken environment.

---

## Phase 3 — Configure .env

```powershell
if (-not (Test-Path .env)) {
    if (Test-Path .env.example) {
        Copy-Item .env.example .env
        Write-Host "Created .env from .env.example" -ForegroundColor Yellow
        Write-Host "WARNING: .env contains placeholder values — edit before using API-dependent features" -ForegroundColor Yellow
    }
}
```

Do NOT create a `.env` from scratch. If neither `.env` nor `.env.example` exists, warn that the server may require env vars and proceed.

---

## Phase 4 — Start backend

Run the backend in a way that lets us poll for health:

```powershell
# Port clearing
Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue |
    ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }

# Start
Start-Process powershell -ArgumentList "-NoProfile -Command uv run python -m {package}.server --http --port {port}" -WindowStyle Normal

# Poll health
for ($i = 0; $i -lt 30; $i++) {
    try {
        $r = Invoke-WebRequest -Uri "http://127.0.0.1:{port}/health" -TimeoutSec 2 -UseBasicParsing
        if ($r.StatusCode -eq 200) { "Backend ready"; break }
    } catch { Start-Sleep 1 }
}
```

If health never returns 200: check `start.ps1` for the correct startup command, try `uv run python -m {package}.main --http`, or run the script manually in a visible window to see errors.

---

## Phase 5 — Start frontend

```powershell
cd D:\Dev\repos\{repo-name}\webapp
Start-Process powershell -ArgumentList "-NoProfile -Command npm run dev -- --port {fe-port} --host 127.0.0.1" -WindowStyle Normal
```

---

## Phase 6 — Open & report

```powershell
Start-Process "http://127.0.0.1:{fe-port}"
```

Report:

```
=== Onboard complete: {repo-name} ===
Backend:  http://127.0.0.1:{be-port}/health (200)
MCP HTTP: http://127.0.0.1:{be-port}/mcp
Frontend: http://127.0.0.1:{fe-port}/
Dashboard: http://127.0.0.1:{fe-port}/
.env: {configured / missing / created from example — WARN}
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `uv sync` fails | Python version mismatch | Check `requires-python` in `pyproject.toml`, ensure 3.12+ |
| Backend starts then exits | Missing `run_server.py` or wrong entry point | Read `pyproject.toml` `[project.scripts]` for the correct command |
| Health endpoint 404 | Wrong port or wrong path | Try `/api/health`, `/api/v1/health`, or check the server code |
| Frontend shows blank page | Vite proxy not configured for this backend port | Check `vite.config.ts` proxy target — may need updating |
| Port collision | Zombie from previous session | Run `stop.bat` or kill manually |

---

## Anti-patterns

| Anti-pattern | Why it fails |
|-------------|-------------|
| **Starting without reading the repo's startup script** | Every repo has quirks — `start.ps1` encodes them |
| **Assuming ports are free** | Zombie processes from crashed sessions are the #1 startup failure |
| **Skipping .env check** | Server starts but all API calls fail because of missing keys |
| **Not reporting the actual health response** | "Backend is up" is less useful than "Backend returned: soffice not found" |
