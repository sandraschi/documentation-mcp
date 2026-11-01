# BUG-062 - Stdio Proxy Wedge via Timeout-less `create_proxy()` (2026-10-04)

- **Severity:** P1 (full MCP tool outage for the affected server, silent)
- **Found in:** calibre-mcp (stdio instance pid 30484, child of OpenCode, proxying HTTP daemon 127.0.0.1:10720)
- **Fleet scope:** every repo using the HTTP-Daemon + Stdio-Proxy pattern with bare
  `create_proxy(url)` - confirmed same call shape in aiwatcher-mcp (server.py:58,
  :1376), arxiv-mcp (__main__.py:90), depot-mcp (__main__.py:38), plex-mcp
  (server.py:186), pywinauto-mcp (transport.py:216), bluesky-mcp (__main__.py:51),
  scraper-mcp (server.py:43), glama-status-mcp (server.py:448),
  mcp-studio (mcp_server.py:1530), advanced-memory-mcp (cli/commands/mcp.py:177),
  obsidian-mcp (transport.py:217), jellyfin-mcp (transport.py:111),
  overte-mcp, plus ~40 `add_provider(create_proxy(url))` bridge sites
  (lower priority: in-process, same stall class). Fix repo-by-repo, not blind-swept.

## Symptom

All MCP tool calls to the server time out (`MCP error -32001`), including static
calls that touch no database (`show_api_docs`, metadata search). The HTTP daemon
itself is healthy (direct `tools/call` answers in 0.07s). Killing the wedged
stdio instance removes the server's tools from the host session until respawn.

Signature in process list: a `python.exe -m <pkg>.__main__` stdio child with a
sub-worker burning 100+ seconds of CPU while the daemon idles near 0%.

## Root cause (verified in venv FastMCP 3.4.4 source)

1. `create_proxy(url)` builds `_create_client_factory(url)` = plain `Client(url)`
   with NO read timeout. `ProxyTool.run` calls `client.call_tool_mcp(...)` with
   no timeout of its own.
2. `Client(timeout=)` DOES bound forwarded calls despite first appearances: it
   lands in `_session_kwargs["read_timeout_seconds"]` (client.py:318-323) and
   becomes the httpx read timeout on the stream (transports/http.py:164-168).
3. One stalled daemon call (here: SQLite read under Calibre-GUI WAL pressure on
   the 5.6 TB archive drive, metadata.db 34 MB + 1.3 MB uncheckpointed WAL)
   therefore wedges the stdio session forever. Every later call queues behind
   the stuck one - even static tools - while the host fires 60s timeouts that
   change nothing server-side.
4. Trap inside the trap: `StreamableHttpTransport(sse_read_timeout=)` is a
   deprecated no-op in 3.4.x (warns, ignored). documentation-mcp's 4.0.5
   assessment confirms: `StreamableHttpTransport(sse_read_timeout=)` removed,
   use `Client timeout=`. An attempted fix with `sse_read_timeout` passes tests
   against a healthy daemon and silently fixes nothing.

## Fix (calibre-mcp, 2026-10-04, verified)

`src/calibre_mcp/server.py`, 1 file, 3 small edits (import + 2 proxy sites:
stdio `main()` probe block and `MCP_BRIDGE_URLS` block):

```python
from fastmcp import Client, FastMCP
from fastmcp.server.providers.proxy import FastMCPProxy

# stdio probe block (was: create_proxy(_probe_url, name="CalibreMCP"))
_proxy = FastMCPProxy(
    client_factory=lambda: Client(_probe_url, timeout=55),
    name="CalibreMCP",
)

# bridge block (was: mcp.add_provider(create_proxy(url)))
mcp.add_provider(
    FastMCPProxy(
        client_factory=lambda u=url: Client(u, timeout=55),
    )
)
```

55s sits just under the host's 60s MCP timeout: a stall surfaces as a clean
proxy error instead of a hung session. Fresh Client per call mirrors lib
`_create_client_factory` behaviour.

## Verification (prove-it-or-it-didn't-happen)

- `ruff check` clean, `py_compile` clean, `pytest tests/test_minimal.py` 1 passed.
- Scratch e2e (temp dir, not committed):
  `C:\Users\<user>\AppData\Local\Temp\opencode\calibre-proxy-verify.py` builds the
  exact factory, asserts `_session_kwargs["read_timeout_seconds"] == 55s` with
  warnings-as-errors (catches the `sse_read_timeout` deprecation trap), then
  proxies `list_tools` (41 tools) + `query_books list limit 1` against the live
  daemon: VERIFY PASS.
- Direct-daemon isolation probes that located the fault:
  `calibre-probe{,2,3,4}.ps1` in the same temp dir (initialize 0.15s, session
  handshake via lowercase `mcp-session-id` header, stateless `tools/call`
  rejected with "Missing session ID" as expected).
- Live ingest still pending: wedged instance was killed (pids 27384/30484);
  OpenCode respawn is lazy, and calibre tools are currently absent from the
  host session. Fix is committed to source; user action on respawn: restart the
  OpenCode session or wait for host health-check retry, then re-run any one
  calibre tool.

## Audit notes for the repo-by-repo rollout

- Stdio-proxy sites (`proxy = create_proxy(...)` after a daemon probe) are the
  outage class: same wedge, same kill-the-patient symptom. Fix first.
- `add_provider(create_proxy(url))` bridge sites stall only the bridged tools,
  not the whole session. Fix on touch.
- Do NOT "fix" with `sse_read_timeout` - deprecated no-op, silent false green.
- Bare `sqlite3.connect()` without `timeout=`/`busy_timeout` still exists in
  calibre-mcp (config_discovery.py:445, extended_library_ops.py:504/537,
  library_utils.py:67, metadata_rag.py:155, chunking.py:110, fts_utils.py:252/451,
  3 viewers). Default 5s timeout raises OperationalError rather than hanging,
  so secondary to the proxy wedge; sweep separately in <=5-file commits.
- Calibre GUI holding `metadata.db` open (WAL + `-shm` present) while the MCP
  daemon serves the same file is the stall source that exposed this. Consider a
  startup warning when `-wal` is non-empty at daemon boot.

## SOTA impact

- Propose for TOOL_DESIGN_STANDARDS / SOTA_REQUIREMENTS: stdio-proxy pattern
  MUST construct the forwarded client with `Client(url, timeout=<host-5s)`;
  bare `create_proxy(url)` is banned in new code (assfix check:
  `rg "create_proxy\(" src/` must show zero bare-URL call sites).
- Related: BUG-038 (lifespan wiring), BUG-047 (hand-rolled HTTP without
  handshake). Same family: proxy/bridge plumbing that fails silently.
