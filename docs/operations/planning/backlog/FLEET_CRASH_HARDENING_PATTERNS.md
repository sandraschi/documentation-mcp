# Fleet crash hardening patterns

**Priority:** P1  
**Scope:** Fleet-wide audit (~30 min/repo)  
**Companion:** [FLEET_API_ENDPOINT_HARDENING_SWEEP.md](FLEET_API_ENDPOINT_HARDENING_SWEEP.md)

| Pattern | Symptom | Fix |
|---------|---------|-----|
| **Unbounded input** | POST body kills uvicorn worker | `max_body_size`; cap path depth/entries |
| **Missing timeouts** | `subprocess.run()` / HTTP client hangs | Every run/post gets timeout; `asyncio.wait_for()` |
| **Resource leaks** | Temp files, connections on crash | `try/finally`, context managers |
| **Startup fragility** | Missing `.env` → `KeyError` at import | Defaults or lifespan validation, not import-time |
| **Signal death** | Orphan backends after SIGTERM | `atexit` / lifespan shutdown; terminate children |
| **Memory bomb** | Unbounded collect-then-return | Streaming or capped collection |
| **Serialization crash** | `datetime`/`bytes` in return dict | Pydantic `model_dump()` or `default=str` |
| **Concurrent state** | SQLite lock; shared dict corruption | WAL + per-coroutine connection or locks |
| **Type confusion** | `Any` gets list not dict | `isinstance` branching or discriminated union |
| **Health endpoint crashes** | DB fail → 500 on `/health` | Catch all; return degraded, never 500 |

Flag each finding LOW (nice) or HIGH (observed prod crash).
