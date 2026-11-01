---
title: "Wrapture: Fleet Diagnostic & Testing Guide"
category: tools
status: active
audience: fleet-developers
last_updated: 2026-09-12
---

# Wrapture (`wrapt` + `capture`)

**Status in Fleet**: Diagnostic sidecar & targeted test utility only. **Not approved for fleet-wide production rollout.**  
**Upstream**: [Graham Dumpleton / wrapture](https://github.com/GrahamDumpleton/wrapture) (v1.0.0b1, Sept 2026)  
**Core Mechanism**: Runtime call-site binding, safe monkeypatching, deterministic unit-test assertions, and ad-hoc call-tree tracing built on `wrapt` and `autowrapt`.

---

## Fleet Verdict & Policy

> [!IMPORTANT]
> **Production Rollout: SKIP.** Do not add `wrapture` to standard server dependencies, base templates, or production `pyproject.toml` files across the 200+ FastMCP servers.  
> **Testing & Diagnostics: ADOPT SURGICALLY.** Retain `wrapture` in dev dependencies (`[dependency-groups] dev`) for hard-to-mock system boundaries, and keep it in central developer toolboxes for zero-code-change ad-hoc debugging.

---

## Why Wrapture Clashes with an MCP Production Fleet

1. **Stdio / JSON-RPC Contamination Risk**  
   FastMCP servers operating over `stdio` transport require strict byte-level protocol hygiene. Raw JSON-RPC frames are transmitted over `stdout`. While wrapture supports file sinks and OTLP backends, default terminal sinks or unconfigured formatters risk leaking diagnostic output into `stdout`, immediately corrupting JSON-RPC framing and causing Claude Desktop or local orchestrators to crash or drop connections.

2. **FastMCP Already Handles the Protocol Boundary**  
   FastMCP (3.2+) provides clean lifecycle hooks, structured logging (`structlog` directed strictly to `stderr` or rotating files), and async middleware. Tool execution timings, request arguments, and error handling are already captured at the ASGI/protocol boundary. Intercepting Python call trees underneath FastMCP via monkeypatching introduces an unnecessary abstraction layer.

3. **Maintenance at 200+ Repo Scale**  
   Managing `wrapture.toml` configurations or monkeypatch targets across hundreds of repositories causes immediate configuration drift. Because wrapture is in pre-1.0 beta (`1.0.0b1`), its API surface and companion instrumentation packages are actively evolving.

4. **Async & Event Loop Overhead**  
   In heavy async I/O environments (FastMCP tool dispatch, IMAP polling, Docker/Win32 stream monitoring), runtime method interception via dynamic wrappers adds cumulative call overhead to high-frequency event loops.

---

## High-Leverage Use Cases in Our Stack

| Use Case | Verdict | Why |
|---|---|---|
| **Fleet-wide Production Monitoring** | **Skip** | Use standard `structlog` and OpenTelemetry export via FastMCP/ASGI middleware or centralized `observability-mcp`. |
| **System Tool Testing (`windows-operations-mcp`)** | **Adopt** | Ideal for mocking un-injectable C-extensions, WMI, or `pywin32` calls without fragile, spec-less `unittest.mock` objects. |
| **Third-Party Service Stubs (`email-mcp`, Cloud APIs)** | **Adopt** | Inject simulated failures, network timeouts, and error cascades (e.g. SMTP dropouts, Graph API rate limits) to verify compensating logic deterministically. |
| **Ad-Hoc Hanging/Drift Debugging** | **Toolbox** | Running `uvx --from wrapture wrapture run -- python server.py` on an unresponsive local server to trace internal execution paths without modifying code or dirtying git status. |

---

## Core API Primitives

Wrapture operates via three composable concepts:

```
   ┌─────────────────────────────────────────────────────────────┐
   │ 1. BINDING: Points at target callable (class, module, func)  │
   │    target = wrapture.binding(TargetClass, "method_name")    │
   └──────────────────────────────┬──────────────────────────────┘
                                  │
   ┌──────────────────────────────▼──────────────────────────────┐
   │ 2. INTERVENTION (Optional): Alters behavior on call         │
   │    target.stub(...) / target.fail(...) / target.transform(...)│
   └──────────────────────────────┬──────────────────────────────┘
                                  │
   ┌──────────────────────────────▼──────────────────────────────┐
   │ 3. TIMELINE & TAPE: Records execution graph and call order    │
   │    with wrapture.timeline(target) as tape: ...              │
   │    tape.tree(), tape.calls(target)                           │
   └─────────────────────────────────────────────────────────────┘
```

* **`wrapture.binding(target, attribute)`**: Attaches a transparent observer to a class method, static function, or module-level callable.
* **`binding.stub(return_value=...)`**: Bypasses the underlying implementation and supplies a fixed result.
* **`binding.fail(exception, once=False)`**: Injects a real exception (once for transient retries, or permanently).
* **`binding.transform(func)`**: Intercepts arguments before the real code runs or mutates return values.
* **`wrapture.timeline(*bindings)`**: Context manager recording all interactions across the bound targets in chronological order.

---

## Practical Pytest Recipes

### 1. Host OS Boundary Testing (Win32 / C-Extensions)

In [`windows-operations-mcp`](file:///d:/Dev/repos/windows-operations-mcp), native C-extensions like `win32file` or `win32security` are notoriously difficult to patch with standard `unittest.mock` because C-extension module attributes frequently resist monkeypatching or produce spec mismatches:

```python
import pytest
import wrapture
from windows_operations_mcp.core import robust_file_write

def test_win32_retry_on_transient_lock(tmp_path):
    """Verify that a locked file triggers retry backoff and eventually succeeds."""
    # Bind to native C-extension call site without spec drift
    lock_call = wrapture.binding("win32file", "LockFileEx")
    
    # Inject a transient lock contention error on first attempt only
    lock_call.fail(OSError("Resource temporarily locked (ERROR_LOCK_VIOLATION)"), once=True)

    with wrapture.timeline(lock_call) as tape:
        target = tmp_path / "locked_file.txt"
        success = robust_file_write(str(target), "data payload")
        
        assert success is True
        
        # Verify the retry loop fired exactly twice (1 fail + 1 success)
        calls = tape.calls(lock_call)
        assert len(calls) == 2
```

---

### 2. Failure-Injection on Outbound Network Gateways (`email-mcp`)

When external services drop connections mid-flight, test whether compensation transactions or rollback handlers correctly execute:

```python
import pytest
import httpx
import wrapture
from email_mcp.mailer import send_transactional_notification

def test_smtp_timeout_triggers_fallback_queue():
    """Verify that an HTTP/SMTP gateway timeout enqueues the message to dead-letter storage."""
    post_call = wrapture.binding("httpx.AsyncClient", "post")
    queue_call = wrapture.binding("email_mcp.queue.DeadLetterQueue", "enqueue")

    # Inject network timeout into outgoing HTTP request
    post_call.fail(httpx.TimeoutException("Upstream gateway gateway timed out"))

    with wrapture.timeline(post_call, queue_call) as tape:
        result = send_transactional_notification(
            recipient="user@example.com",
            subject="Fleet Alert",
            body="High memory warning",
        )
        
        assert result.status == "queued_for_retry"
        assert len(tape.calls(post_call)) == 1
        assert len(tape.calls(queue_call)) == 1
        
        # Assert the queue payload preserved original message details
        queued_item = tape.calls(queue_call)[0].args[0]
        assert queued_item["recipient"] == "user@example.com"
```

---

### 3. Negative Assertions ("Verify What Did NOT Happen")

One of `unittest.mock`'s greatest weaknesses is asserting that side-effects were prevented across complex call trees. With wrapture, you assert non-execution on dangerous operations (e.g. destructive disk deletions or DB mutations in [`filesystem-mcp`](file:///d:/Dev/repos/filesystem-mcp)):

```python
import pytest
import wrapture
from filesystem_mcp.atomic_ops import atomic_batch_delete

def test_permission_failure_prevents_destructive_purge(tmp_path):
    """Verify that if validation fails on item 2, NO deletions are executed."""
    check_perm = wrapture.binding("filesystem_mcp.atomic_ops", "_check_permissions")
    unlink = wrapture.binding("os", "unlink")

    # Fail permission check on the second file
    def fail_on_second(path):
        if "forbidden" in str(path):
            raise PermissionError("Access Denied")
        return True

    check_perm.transform(fail_on_second)

    files = [tmp_path / "ok.txt", tmp_path / "forbidden.txt", tmp_path / "pending.txt"]
    for f in files:
        f.write_text("data")

    with wrapture.timeline(check_perm, unlink) as tape:
        with pytest.raises(PermissionError):
            atomic_batch_delete(files)

        # STRICT NEGATIVE ASSERTION: os.unlink was NEVER invoked
        assert len(tape.calls(unlink)) == 0
        assert all(f.exists() for f in files)
```

---

### 4. Async Coroutines & FastMCP Tool Dispatch

Wrapture transparently handles Python `asyncio` coroutines without needing separate `AsyncMock` wrappers:

```python
import pytest
import wrapture
from fastmcp import FastMCP

app = FastMCP("demo-server")

@app.tool()
async def fetch_remote_metrics(server_id: str) -> dict:
    raw_data = await external_fetch(server_id)
    return {"id": server_id, "load": raw_data["cpu"]}

async def external_fetch(server_id: str) -> dict:
    ...

@pytest.mark.asyncio
async def test_async_mcp_tool_with_wrapture():
    fetch_binding = wrapture.binding(__name__, "external_fetch")
    fetch_binding.stub(return_value={"cpu": 42.5})

    with wrapture.timeline(fetch_binding) as tape:
        result = await fetch_remote_metrics("fleet-node-01")
        
        assert result == {"id": "fleet-node-01", "load": 42.5}
        assert len(tape.calls(fetch_binding)) == 1
        assert tape.calls(fetch_binding)[0].args[0] == "fleet-node-01"
```

---

### 5. Inspecting Self-Calls (Internal Private Methods)

`unittest.mock.Mock` instances cannot observe calls an object makes to its own private methods (e.g., `self._validate()`) because mocking the object replaces the entire instance. Wrapture observes the *real* class execution:

```python
import wrapture

class DataIngester:
    def ingest(self, payload: dict):
        cleaned = self._sanitize(payload)
        return self._persist(cleaned)

    def _sanitize(self, payload: dict) -> dict:
        return {k: v.strip() for k, v in payload.items() if isinstance(v, str)}

    def _persist(self, data: dict) -> str:
        return "stored"

def test_internal_sanitization_call_tree():
    ingest_b = wrapture.binding(DataIngester, "ingest")
    sanitize_b = wrapture.binding(DataIngester, "_sanitize")
    persist_b = wrapture.binding(DataIngester, "_persist")

    with wrapture.timeline(ingest_b, sanitize_b, persist_b) as tape:
        ingester = DataIngester()
        ingester.ingest({"key": "  hello  "})

    # Print the formatted ASCII call tree
    print(tape.tree())
    # Output:
    # DataIngester.ingest(payload={'key': '  hello  '}) -> 'stored'
    #   DataIngester._sanitize(payload={'key': '  hello  '}) -> {'key': 'hello'}
    #   DataIngester._persist(data={'key': 'hello'}) -> 'stored'

    assert len(tape.calls(sanitize_b)) == 1
```

---

## Ad-Hoc Diagnostic Sidecar (Zero Code Modifications)

When a server hangs, deadlocks, or exhibits unexpected drift in development, you can attach wrapture at launch without touching git-tracked source files.

### Step 1: Create a Local `wrapture.toml`

Place this in your current working directory or a scratch folder:

```toml
[wrapture]
# Targets to intercept and trace
targets = [
    "my_mcp_server.core:execute_task",
    "my_mcp_server.storage:acquire_lock",
    "sqlite3.Connection:execute",
    "asyncio.locks.Lock:acquire",
]

# CRITICAL: Output sink must NEVER be stdout on stdio MCP servers!
[sink]
type = "file"
path = "debug_trace.log"
format = "nested_tree"
```

### Step 2: Run via `uvx` (No Virtualenv Changes Needed)

Launch your server under wrapture using `uvx`:

```powershell
# Run untouched with targeted trace output
uvx --from wrapture wrapture run --config wrapture.toml -- python -m my_mcp_server
```

Alternatively, use environment variable bootstrapping via `autowrapt`:

```powershell
$env:AUTOWRAPT_BOOTSTRAP = "wrapture"
$env:WRAPTURE_CONFIG = "wrapture.toml"
python -m my_mcp_server
```

> [!CAUTION]
> **Stdio Isolation Rule**: If the server uses stdio transport (Claude Desktop / Cursor integration), verify `wrapture.toml` points to `file://...` or `stderr`. Never route traces to `stdout`, as it will corrupt JSON-RPC frames and crash the client session.

---

## Comparison: `unittest.mock` vs `wrapture`

| Feature | `unittest.mock` | `wrapture` |
|---|---|---|
| **Spec Verification** | Spec-blind by default (accidental typos like `mock.assert_called_once_whit()` silently pass). Requires explicit `autospec=True`. | **Always adheres to real code signature**; verifies call sites against actual runtime parameters. |
| **Object Self-Calls** | Cannot observe calls an object makes to its own private methods (`self._method()`). | **Full internal visibility**: Observes and traces entire internal method call trees. |
| **C-Extension Support** | Often fails to patch C-extensions or builtins (`win32file`, `sqlite3`, etc.). | **Robust proxying** via `wrapt` call-site bindings. |
| **Call Tree Visualization** | None. Manual inspection of `mock.mock_calls`. | Built-in `tape.tree()` ASCII hierarchy of nested execution. |
| **Zero-Code Tracing** | None (requires source or test modifications). | Built-in CLI launcher (`wrapture run`) and config-driven tracing. |
| **Production Risk** | High if patches leak across tests. | High if used in production stdio MCP servers; strictly reserved for test/dev. |
