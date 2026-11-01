# BUG-025: FastMCP private tool attributes (`_tools` / `_tool_manager`) removed in 3.4.x

- **ID**: BUG-025
- **Severity**: P1 (High — tool_count/health endpoints broken fleet-wide; several servers crash)
- **Date**: 2026-08-17
- **Component**: Fleet-wide (26 repos) — FastMCP 3.4.2/3.4.4/3.4.5 migration

## Symptom

- `GET /health` / `/api/v1/diagnostics` return `tool_count: 0` (or a hardcoded fake
  number) despite tools being registered.
- Some servers raise `AttributeError: 'FastMCP' object has no attribute '_tools'`
  (or `_tool_manager`) on health/tools endpoints, returning HTTP 500.
- Webapp dashboards show "Tools: 0" / empty tool lists; CUA-NSIS diagnostics report
  zero tools while MCP clients see the full tool surface.

## Root Cause

FastMCP removed the private tool-manager attributes in the 3.4.x line
(verified absent on 3.4.2, 3.4.4, and 3.4.5):

- `mcp._tools` — removed
- `mcp._tool_manager` / `mcp._tool_manager._tools` — removed
- `mcp.get_tools()` (sync plural) — never existed; only `get_tool(name)` (sync)

The public API is `await mcp.list_tools()` (returns `FunctionTool` objects with
`.name`, `.description`, `.parameters`, `.fn`) and sync `mcp.get_tool(name)`.
Code reading the private attrs was written for FastMCP 2.x/3.1-3.3 and never
migrated; the fleet template (`mcp-server-template`) shipped the broken pattern
in `src/llms_docs.py` + `src/help_tool.py`, so every scaffold inherited it.

Special cases found during the sweep:

- `pdf-mcp` and plex webapp: `else 42` / `else 22` hardcoded fallback counts —
  fake data on every health call.
- `qcad-mcp`: guarded `_tool_manager` then fell through to nonexistent
  `mcp.get_tools()` → AttributeError in the `else` branch.
- `mixx-dj-mcp`: tool dispatch map built from `_tool_manager._tools` → the
  `/api/v1/tools/call` + `/api/v1/effects` REST surface silently stopped working.
- `myai` bridge: tool call path silently disabled.
- Tests in `mcp-server-template` (example server) and `publictransport-mcp` used the
  attrs directly → AttributeError or fake-pass (body never executed).

## Resolution (fleet sweep 2026-08-17)

26 repos + template fixed to the public API:

- Async routes/helpers: `tools = await mcp.list_tools()`; counts `len(tools)`;
  names `[t.name for t in tools]`; metadata via `t.description` / `t.parameters`
  / `t.fn`.
- Sync contexts (module-level logging, registration verification, sync helpers):
  loop-guard `asyncio.run()` helper (returns [] when a loop is running) instead
  of private attrs.
- Single-tool lookups: `mcp.get_tool(name)` (sync) with `getattr(t, "fn", t)`.
- `pdf-mcp` hardcoded 42 and plex webapp hardcoded 22 fallbacks removed.
- Template `llms_docs.py` / `help_tool.py` rewritten; example-server tests
  converted (`await app.list_tools()`); pre-existing failing tests fixed
  (patch-target bug: string-path `mock.patch` hit a second module instance when
  pytest imports the package as `src.example_mcp_server.*` — use `patch.object`).
- Test files with the pattern (calibre, gimp, moltbot, publictransport-mcp) converted.

Repos fixed: browser-mcp, calibre-mcp, plex-mcp, notion-mcp, moltbot-mcp,
qcad-mcp, unsloth-mcp, avatar-mcp, blender-mcp, inkscape-mcp, pdf-mcp,
comfyops-mcp, freecad-mcp, publictransport-mcp (src + frontend copies), mixx-dj-mcp,
pywinauto-mcp, devices-mcp, system-admin-mcp, robotics-mcp, reversing-mcp,
osc-mcp, virtualization-mcp, myai, ai-games-collection, database-operations-mcp,
mcp-server-template.

## Log Snippet

```
health: {"status":"ok","service":"browser-mcp","version":"0.3.0","port":10780,"tool_count":0}
AttributeError: 'FastMCP' object has no attribute '_tool_manager'
```

## SOTA Impact / Prevention

- `repo-assess-and-fix.md` 1I "FastMCP 3.4.3+ Features" — add a check row:
  `rg '\._tools\b|_tool_manager|get_tools\(' src/` must return zero hits;
  tool counts MUST use `await mcp.list_tools()` (async) or the loop-guard
  pattern (sync), never private attrs, never hardcoded fallback numbers.
- New-repo gate: template ships only the public API.
- Status: ✅ Fixed (fleet sweep complete 2026-08-17; verify with
  `rg -n '\._tools\b|_tool_manager' <repo>/src`)
