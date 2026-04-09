# FastMCP 3.2+ Startup Connectivity Probes

## Pattern: Fail Fast in Lifespan

MCP servers that depend on external resources (databases, APIs, filesystems) should
probe connectivity during the lifespan startup hook — before the `yield` — so that
host clients (Claude Desktop, IDE integrations) see a hard failure with an actionable
message rather than a zombie server that accepts connections but silently errors on
every tool call.

---

## Why Lifespan, Not Elsewhere

| Location | Verdict | Reason |
|---|---|---|
| Module-level (top of server.py) | ❌ | No event loop yet; must use sync I/O; too early |
| `main()` before `run_server_async()` | ⚠️ | Works, but splits startup logic across two places |
| `server_lifespan` before `yield` | ✅ | Designed for this; async I/O available; clean abort |
| First tool call (lazy) | ❌ | Silent fail — exactly what probes prevent |

A `RuntimeError` raised before the `yield` in `server_lifespan` causes FastMCP to abort
startup. The process exits non-zero. Claude Desktop marks the server as failed in its
UI. The error message lands in the MCP log file.

**Important:** In stdio transport, `__main__.py` typically redirects stderr to devnull
for JSON-RPC cleanliness. The probe's error message is therefore in the log
(`logs/<server>.log`), not surfaced inline in the client. This is still far better than
silent failure — the log is the first place to check when a server won't start.

---

## Standard Probe Template

```python
import asyncio
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastmcp import FastMCP


async def _probe_connectivity(log: logging.Logger) -> None:
    """Probe all required external dependencies at startup.

    Raises RuntimeError with a human-readable, actionable message if
    any required dependency is unreachable.
    """
    failures: list[str] = []

    # --- 1. Local filesystem probe ---
    data_path_str = os.environ.get("MY_DATA_PATH", "").strip().strip('"')
    if data_path_str:
        data_path = Path(data_path_str)
        if not data_path.exists():
            failures.append(
                f"MY_DATA_PATH '{data_path}' does not exist"
            )
            log.warning("STARTUP PROBE: %s", failures[-1])
        else:
            log.info("STARTUP PROBE: filesystem OK — %s", data_path)

    # --- 2. Remote HTTP service probe ---
    api_url = os.environ.get("MY_SERVICE_URL", "").strip()
    if api_url:
        probe_url = api_url.rstrip("/") + "/health"
        log.info("STARTUP PROBE: probing %s", probe_url)
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    probe_url, timeout=aiohttp.ClientTimeout(total=5)
                ) as resp:
                    if resp.status < 500:
                        log.info("STARTUP PROBE: service OK (HTTP %d)", resp.status)
                    else:
                        failures.append(
                            f"MY_SERVICE_URL returned HTTP {resp.status}"
                        )
        except asyncio.TimeoutError:
            failures.append(
                f"MY_SERVICE_URL '{api_url}' timed out after 5s — is the service running?"
            )
        except Exception as exc:
            failures.append(
                f"MY_SERVICE_URL '{api_url}' unreachable: {type(exc).__name__}: {exc}"
            )

    # --- 3. Decision ---
    if failures:
        detail = "; ".join(failures)
        raise RuntimeError(
            f"<ServerName> startup failed — required dependencies unreachable. "
            f"{detail}. "
            f"Fix the issue and restart Claude Desktop / your MCP client."
        )


@asynccontextmanager
async def server_lifespan(mcp_instance: FastMCP):
    log = logging.getLogger("<servername>.lifespan")
    log.info("SERVER LIFESPAN: starting")

    await _probe_connectivity(log)

    log.info("SERVER LIFESPAN: all probes passed, server ready")
    yield
    log.info("SERVER LIFESPAN: shutdown complete")


mcp = FastMCP(
    "<ServerName>",
    lifespan=server_lifespan,
    # ...
)
```

---

## Decision Logic Reference

Three outcomes are useful:

### Hard fail — something configured but unreachable
The server was pointed at a resource and can't reach it. Abort with a message
telling the user what to fix.

```python
# Something was configured but nothing is reachable
if configured and not reachable:
    raise RuntimeError(
        "Server startup failed — <resource> is not reachable. "
        "<detail>. Fix: <what to do>, then restart."
    )
```

### Warn and continue — nothing configured at all
The server can operate in a degraded mode (e.g. user will pass paths directly
to tools). Don't hard-fail; do log a clear warning.

```python
if not configured:
    log.warning(
        "STARTUP PROBE: <resource> not configured. "
        "Server will start in degraded mode — most tools will error "
        "until a valid path or URL is provided."
    )
    return
```

### Pass silently — resource reachable
No noise needed beyond a single INFO line.

```python
log.info("STARTUP PROBE: <resource> OK")
```

---

## Probe Design Guidelines

**Keep probes cheap and bounded.**
- Always set a timeout (5s is a reasonable default for HTTP).
- For filesystems, check existence of a sentinel file (e.g. `metadata.db`) rather
  than recursing the entire tree with `rglob`. Use `iterdir()` on known parent dirs.
- Probes run synchronously from the host's perspective — slow probes delay all tool
  availability.

**Use existing dependencies.**
- HTTP probes: use `aiohttp` (already a dependency in most FastMCP servers) rather
  than adding `httpx` or `requests` just for a health check.
- Filesystem probes: `pathlib.Path`, no extra deps.

**Be consistent with `discover_*` functions.**
If your server has a `discover_libraries()` or similar function that scans for
data sources, the probe should use the same logic — not a stricter or looser version.
Divergence causes confusing behaviour where the probe passes but the tool fails.

**One probe per dependency type.**
Don't combine the local FS check and the remote API check into a single pass/fail.
Report each failure separately so the user knows exactly what to fix.

---

## Real-World Example: calibre-mcp

calibre-mcp has two data sources — local Calibre library directories (SQLite) and
an optional remote Calibre Content Server (HTTP). The probe checks both and uses the
"either is fine" pattern: if at least one is reachable, the server starts normally.

```python
async def _probe_calibre_connectivity(log: logging.Logger) -> None:
    base_path_ok = False
    remote_ok = False
    messages: list[str] = []

    # Local: check CALIBRE_BASE_PATH for at least one metadata.db
    base_path_str = os.environ.get("CALIBRE_BASE_PATH", "").strip().strip('"')
    if base_path_str:
        base_path = Path(base_path_str)
        if base_path.exists():
            # Shallow scan — don't rglob a large NAS share
            dbs = [
                item / "metadata.db"
                for item in base_path.iterdir()
                if item.is_dir() and (item / "metadata.db").exists()
            ]
            if dbs:
                base_path_ok = True
                log.info("STARTUP PROBE: local libraries OK (%d found)", len(dbs))
            else:
                messages.append(f"CALIBRE_BASE_PATH '{base_path}' has no metadata.db")
        else:
            messages.append(f"CALIBRE_BASE_PATH '{base_path}' does not exist")

    # Remote: GET /ajax/library-info
    server_url = os.environ.get("CALIBRE_SERVER_URL", "").strip()
    if server_url:
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    server_url.rstrip("/") + "/ajax/library-info",
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as resp:
                    if resp.status < 500:
                        remote_ok = True
                        log.info("STARTUP PROBE: remote server OK (HTTP %d)", resp.status)
                    else:
                        messages.append(f"Calibre server returned HTTP {resp.status}")
        except asyncio.TimeoutError:
            messages.append(f"Calibre server '{server_url}' timed out (5s)")
        except Exception as exc:
            messages.append(f"Calibre server unreachable: {exc}")

    if base_path_ok or remote_ok:
        return  # At least one data source available

    if not base_path_str and not server_url:
        log.warning(
            "STARTUP PROBE: no data source configured — server starts in degraded mode"
        )
        return

    raise RuntimeError(
        "CalibreMCP startup failed — no Calibre data source is reachable. "
        + "; ".join(messages)
        + ". Fix: start Calibre Content Server on port 8099, or ensure "
        "CALIBRE_BASE_PATH contains library directories, then restart."
    )
```

Key design choices in this example:
- **Shallow scan** (`iterdir()`) instead of `rglob()` — avoids scanning deep NAS trees.
- **"Either-or" pass logic** — two optional sources, either one is sufficient.
- **Degraded mode** for the "nothing configured" case — server still loads so the user
  can configure it via tool arguments without restarting.
- **Actionable error message** — tells the user exactly what port to check and what
  env var to set.

---

## Checklist

Before shipping a FastMCP server that depends on external resources:

- [ ] `server_lifespan` probes all required external dependencies before `yield`
- [ ] Each probe has a timeout (HTTP: 5s default)
- [ ] Filesystem probes use shallow scans, not `rglob`
- [ ] Probe logic is consistent with the server's `discover_*` / `get_*_client()` functions
- [ ] `RuntimeError` messages include: what failed, why, and how to fix it
- [ ] "Nothing configured" case uses a warning, not a hard fail, if degraded operation is valid
- [ ] Probes use existing dependencies — no new deps just for health checks
- [ ] Probe is extracted into a named `_probe_*` function, not inlined in lifespan
