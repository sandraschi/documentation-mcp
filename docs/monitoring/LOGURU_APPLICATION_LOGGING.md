# Loguru and Python MCP application logging

**Purpose:** Document **in-process** logging for Python MCP servers (Loguru), and how it relates to the **infrastructure** stack in this directory (Grafana / Prometheus / Loki).

**Audience:** Server authors and operators maintaining fleet nodes (e.g. Advanced Memory, Blender MCP, web-development-mcp).

---

## Two layers (do not conflate them)

| Layer | What it is | Typical tools in this repo |
|--------|------------|----------------------------|
| **Application logging** | Lines emitted by your Python process (tools, sync, API) | **Loguru** `logger.info/debug/warning`, optional file sinks |
| **Platform / fleet logging** | Aggregate, search, and alert across hosts and containers | **Loki**, **Promtail**, **Grafana** (see `README.md`, `UNIFIED_MONITORING_STACK.md`) |

Loguru answers: *“What did this process do?”*  
Loki answers: *“What did all replicas say in the last hour?”*  
They connect when you **ship** Loguru output (stderr or log files) into Promtail → Loki.

---

## Why Loguru for MCP servers

- Readable structured messages and sensible defaults for **stderr** (TTY color when supported).
- Lower friction than stdlib `logging` for rapid tool development.
- **Canonical hub guidance:** see **`standards/AGENT_PROTOCOLS.md`** (repo root) and the bundled **`.cursor/skills/mcp-server-developer`** modules, especially:
  - `modules/minimal-mcp-server.md` — dependency and import patterns
  - `modules/architecture-and-standards.md` — structured logging expectation
- **stdio transport:** never write arbitrary text to **stdout** (it breaks JSON-RPC). Log to **stderr** via Loguru (default sink) or explicit `sys.stderr` handlers.

---

## Standards (fleet / SOTA)

1. **Levels:** `INFO` for lifecycle and outcomes, `WARNING` for degraded but continuing behavior, `ERROR` for failures users or operators must see.
2. **Hot paths:** avoid **O(n²)** or per-tick `DEBUG` in nested loops (batch or count, then one line).
3. **Noise:** damp third-party libraries (`httpx`, `watchfiles`, ORM) to `WARNING` unless debugging integrations.
4. **Secrets:** never log tokens, cookies, or raw credentials; redact paths if they contain home usernames when required by policy.

---

## Optional bridge to Loki (this `monitoring/` stack)

If you run Promtail against the host or Docker:

- Tail **log files** your server writes (e.g. under a dot-dir in user home).
- Or scrape **container stderr** with Docker logging labels.
- Label with `job`, `mcp_server`, `project` (or `instance`) so LogQL stays usable.

Start from **`HOW_TO_USE.md`**, **`promtail/promtail.yml`**, and **`SHARED_MONITORING_STACK_GUIDE.md`** in this folder.

---

## Minimal usage pattern

```python
from loguru import logger

logger.info("Invoking tool {name}", name="example_search")
logger.debug("Context: project={p}", p=project_name)
```

Prefer structured placeholders (`{name}`) over heavy f-strings for large payloads.

---

## Reference: Advanced Memory MCP

The **advanced-memory-mcp** repository uses Loguru widely (`from loguru import logger` in services, sync, API routers). Centralized setup lives in **`setup_advanced_memory_logging()`** (`advanced_memory/config.py`), invoked from API lifespan / CLI entry points (not at import time, to avoid stdio clashes).

- **Console noise:** optional env **`ADVANCED_MEMORY_CONSOLE_LOGGING`** (see that repo’s `config.py`).
- **Log level:** driven from project / app config (`log_level`).

Treat this as a **reference implementation**, not a hard dependency for every fleet server.

---

## See also

- **[`../protocol/TRANSPORTS.md`](../protocol/TRANSPORTS.md)** — HTTP vs stdio and logging cautions  
- **[`MCP_MONITORING_STANDARDS.md`](./MCP_MONITORING_STANDARDS.md)** — fleet monitoring expectations  
- **[`README.md`](./README.md)** — Grafana / Prometheus / Loki overview in this directory  
