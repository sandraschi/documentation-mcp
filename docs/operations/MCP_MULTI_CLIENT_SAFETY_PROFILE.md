# MCP Multi-Client Safety Profile

**Last updated:** 2026-03-23  
**Scope:** Local stdio MCP servers used simultaneously by Cursor, Claude Desktop, Antigravity, VS Code, and other clients.

## Why this exists

Running multiple MCP clients against the same local server stack creates three practical failure classes:

1. **Process/launcher contention** (Windows `.exe` lock, uv sync/update races).
2. **State-store contention** (SQLite lock waits, transaction conflicts, stale readers).
3. **Application-level races** (simultaneous writes to shared files, cache indexes, exports).

This profile defines baseline controls for any server that is expected to survive multi-client usage.

## Baseline controls (fleet default)

- **Launch pattern:** use `uv --directory <repo> run python -m <module> ...` (avoid console-script `.exe` lock races on Windows).
- **Single stdio process guard:** server acquires a lock file in stdio mode (env opt-out only for advanced users).
- **State segregation:** if high-write workloads are expected from multiple clients, split writable state per client (separate DB/file paths) and sync explicitly.
- **SQLite hardening:** enable WAL + busy timeout + short transactions, avoid long write transactions.
- **Idempotent writes:** operations should be safe when retried or called in quick succession.
- **Fast fail diagnostics:** return actionable lock/race errors (include lock path and recovery action).

## Recommended environment flags

- `*_STDIN_SINGLE_INSTANCE=1` (default): deny a second stdio instance for the same server profile.
- `*_STDIN_SINGLE_INSTANCE=0`: explicit override for debugging.
- `PYTHONUNBUFFERED=1`: avoid buffering artifacts in stdio MCP mode.

For SQLite-backed servers:

- `SQLITE_BUSY_TIMEOUT_MS=10000` (or similar)
- `SQLITE_JOURNAL_MODE=WAL`

## Implementation template (Python, Windows-safe)

```python
from contextlib import contextmanager
from pathlib import Path
import os

@contextmanager
def stdio_single_instance_lock(lock_name: str, env_flag: str):
    if os.getenv(env_flag, "1") != "1":
        yield
        return
    lock_path = Path.home() / f".{lock_name}" / "mcp-stdio.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        import msvcrt
        f = open(lock_path, "a+b")
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            f.close()
            raise RuntimeError(f"Lock busy: {lock_path}")
        try:
            yield
        finally:
            f.seek(0)
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            f.close()
    else:
        yield
```

Wrap stdio server startup with this context manager.

## Applied notes (2026-03-23)

- `advanced-memory-mcp`: stdio lock added (`ADVANCED_MEMORY_STDIN_SINGLE_INSTANCE`).
- `davinci-resolve-mcp`: stdio lock added (`DAVINCI_MCP_STDIN_SINGLE_INSTANCE`).
- Fleet configs moved toward `python -m` launches to avoid shared `.venv\Scripts\*.exe` replacement races.

## Operational runbook

If startup fails:

1. Identify whether it is a **launcher lock** or **state lock** (error text).
2. For launcher lock: close/disable duplicate client instance, restart server.
3. For state lock: inspect DB activity; reduce concurrent writers or split state paths.
4. If repeated: enforce single-writer policy for that server and keep read-only access in secondary clients.
