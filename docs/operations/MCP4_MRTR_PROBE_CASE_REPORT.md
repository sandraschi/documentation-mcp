---
title: "MCP4 MRTR Probe — Successful Case Report"
category: operations
status: active
audience: mcp-dev
skill_candidate: true
related:
  - operations/MCP_SERVER_SAGA_INDEX.md
  - patterns/CUA_DRIVER_AND_PYWINAUTO.md
  - standards/TAURI_PRODUCTION_PITFALLS.md
  - troubleshooting/BUGS_DEPOT.md
last_updated: 2026-08-02
---

# Case Report: FastMCP 4 / MRTR Feasibility Probe Against Claude Desktop

**Date:** 2026-08-02
**Status:** COMPLETE — empirical verdict recorded, probe retained for re-testing
**Result:** ⚠ **Claude Desktop 1.24012.9.0 does NOT implement the SEP-2322 MRTR client loop.** All ~55 fleet RED repos stay pinned to `fastmcp<4`.
**Artifacts:** `C:\temp\mcp4_audit_20260802-1301.md` (full audit) · `C:\temp\mcp4_probe\` (probe server + verifiers + logs + screenshots)

---

## 1. TL;DR

The fleet's 190-repo MCP 2026-07-28 / FastMCP 4 migration audit found ~55 repos calling
`ctx.sample()` — removed outright in FastMCP 4.0.0b1. The replacement, MRTR
(SEP-2322), requires the **client** to answer a `CreateMessageRequest` embedded in an
`InputRequiredResult` and re-issue the tool call. Whether Claude Desktop implements that
client half is the single question that gates the entire migration. We answered it
empirically with a throwaway probe server + CUA-driven desktop automation:

**It does not. Round 1 fires, round 2 never arrives.**

---

## 2. Background

### The spec (MCP 2026-07-28, final)

- Removes protocol-level sessions, the `initialize` handshake, and `Mcp-Session-Id`.
- List endpoints gain `ttlMs` and `cacheScope`.
- Missing-resource error code moves from `-32002` to `-32602`.

### FastMCP 4.0.0b1 (harsher than the spec)

- `ctx.sample()` and `ctx.sample_step()` are **removed**, not deprecated.
- Replacement is **MRTR** (SEP-2322): a tool returns an `InputRequiredResult` whose
  `input_requests` map carries a `CreateMessageRequest`; the client completes it and
  re-issues the same tool call with the answer in `ctx.input_responses`.

### Fleet state (from the audit, 2026-08-02)

| Bucket | Count | Meaning |
|--------|-------|---------|
| RED | ~55 | Call `ctx.sample()` — must stay on `fastmcp<4` |
| AMBER | ~16 | Sampling handlers, SSE fallbacks, heavy prompt/resource usage |
| GREEN | ~130 | Clean, could attempt 4.x |
| SSE overlap | 6 | Deprecated SSE transport option present |

Also discovered: every repo pins `fastmcp>=3.4.4,<4` already, so 4.x is blocked by
version pins regardless of code.

---

## 3. What we built

`C:\temp\mcp4_probe\` — a throwaway FastMCP 4.0.0b1 stdio server with two tools:

| File | Purpose |
|------|---------|
| `probe_server.py` | `mrtr_probe` returns `InputRequiredToolResult(input_required=InputRequiredResult(input_requests={"clarify": CreateMessageRequest(...)}))` on round 1; reads `ctx.input_responses["clarify"]` on round 2. `mrtr_noop` = control tool. Every round logged to `rounds.log`. |
| `verify_client.py` | Raw JSON-RPC stdio client — proves legacy-handshake era raises the documented SEP-2322 era error cleanly. |
| `verify_client2.py` | Native `fastmcp.Client` with `sampling_handler` — proves the full MRTR loop end-to-end. |

### Key API facts learned (fastmcp 4.0.0b1 / mcp-types)

- `InputRequiredToolResult` lives in `fastmcp.tools.base`; wraps `mcp_types.InputRequiredResult`.
- `InputRequiredResult` fields: `meta`, `result_type`, `input_requests`, `request_state`
  (at least one of `input_requests`/`request_state` required by validator).
- `InputResponses = dict[str, CreateMessageResult | CreateMessageResultWithTools | ListRootsResult | ElicitResult]`.
- `ctx.input_responses` is a property: `None` on round 1, populated on round 2.
- The SDK ships a full client loop: `mcp.client._input_required.run_input_required_driver`
  (dispatches all `input_requests` concurrently, retries with responses, echoes
  `request_state` byte-exact, caps at `max_rounds`, exponential backoff for state-only legs).
- **Era negotiation:** the `initialize` handshake tops out at `2025-11-25`
  (`LATEST_HANDSHAKE_VERSION`). The 2026-07-28 era is reached only via the
  `server/discover` probe; `fastmcp.Client(mode="auto")` does this automatically
  (even over stdio). A tool returning `InputRequiredResult` on a handshake-era
  connection gets a clean MCPError: *"SEP-2322 only exists at MCP 2026-07-28; this
  connection negotiated '2025-11-25'. Use ctx.elicit()..."*
- `ctx.elicit()` still exists in 4.0.0b1 (only `sample`/`sample_step` are removed) —
  the one server-initiated-input path that works with handshake-era clients.

### Server mechanics verification — both paths PASS

```
[A] legacy handshake -> negotiated 2025-11-25
[A] PASS: era error raised cleanly (SEP-2322 only exists at MCP 2026-07-28...)
[B] negotiated protocol: 2026-07-28
[B] full MRTR loop: round 1 asks -> sampling_handler receives CreateMessageRequest
    -> round 2 re-issues call -> tool reads ctx.input_responses["clarify"] -> PASS
```

---

## 4. The Claude Desktop test (CUA-driven)

### Setup

1. Registered the probe in `%APPDATA%\Claude\claude_desktop_config.json`
   (`mcpServers."mcp4-mrtr-probe"` → venv python + `probe_server.py`).
   **Timestamped backup taken before every config write** (restored after).
2. Launched Claude Desktop (MSIX `Claude_1.24012.9.0_x64__pzs8sxrjxfjjc` —
   found via `Get-AppxPackage`, not the usual exe paths).
3. Verified the server was spawned by CD via `rounds.log` (`starting stdio transport`).

### The CUA interaction

- Focused the CD window, dismissed a stray context menu (Escape), clicked into the
  chat input at verified coordinates, typed the prompt, **screenshot-verified the text
  landed in the input box**, then pressed Enter.
- Automation approvals: `approve_automation(duration_minutes=10)` before mouse actions
  (HITL). DPI note: CD runs fullscreen at 1.5x scale — cursor position confirmed with
  `position()` before clicking.

### The empirical result

```
12:05:30 mrtr_probe ROUND 1: ctx.input_responses is None - issuing input_requests
12:05:35 mrtr_noop called
(ROUND 2 never arrives — waited 45+ s)
```

Claude Desktop:
1. Called `mrtr_probe` ✅
2. Received `InputRequiredResult` (server logged round 1) ✅
3. **Did NOT surface the `CreateMessageRequest` to the user** ❌
4. **Did NOT re-issue the tool call** (`ctx.input_responses` never populated) ❌
5. Degraded it to a bare `Tool execution failed` and self-invoked `mrtr_noop` to isolate.

CD's own analysis (shown in its UI): *"The client here did not surface any elicitation
prompt to me, and the error came back bare, without the documented return shape."*

### Re-run (cleanliness control)

The run was repeated from scratch with a rotated log and screenshot-verified input:
**identical result** (round 1 at 12:05:30, no round 2, `mrtr_noop` fallback).
The first result was not an input-interference artifact.

---

## 5. Pitfall discovered: stdout corruption on stdio transport

First CD launch failed to parse the server: *"Expected '/' or ']' after array element
in JSON at position 5"* — the probe's logging wrote to **stdout**, corrupting the
JSON-RPC stream (and FastMCP 4.0.0b1 prints an ASCII banner on startup).

**Fix:** route all logging to `stderr`, set `FASTMCP_BANNER=0`.

> **Rule for every stdio MCP server, now enforced:** nothing but newline-delimited
> JSON-RPC may ever be written to stdout. Log to stderr or a file.

---

## 6. Fleet consequences & actions

1. **All ~55 RED repos stay pinned to `fastmcp<4`.** No `ctx.sample()` → MRTR migration
   until Claude Desktop ships the client half. This is a client gap, not a stack gap —
   the SDK (`run_input_required_driver`), the types, and the server-side loop all work.
2. **`ctx.elicit()` is the only viable server-initiated-input path with CD today** —
   but it changes UX (visible elicitation prompts) and is a design decision, not a port.
3. **Re-test after each Claude Desktop release.** One tool call; `rounds.log` gives the
   verdict. File an issue with Anthropic if the loop remains unimplemented.
4. Audit artifacts retained: `C:\temp\mcp4_probe\` (server, verifiers, logs,
   screenshots) + `C:\temp\mcp4_audit_20260802-1301.md`.

### Uncertainty notes

- Tested against Claude Desktop 1.24012.9.0 only. Server-side negotiation to
  2026-07-28 over stdio works, so CD *could* complete the loop — it just doesn't.
- CD's UI error ("no structured error body returned") suggests it may not even
  recognize the `input_required` result shape yet.

---

## 7. What made this a success (retrospective)

| Step | Why it worked |
|------|---------------|
| **Probe self-verification first** | `verify_client2.py` proved the server mechanics before any desktop automation — CD failures were unambiguous client-side results, not server bugs. |
| **Log-to-file + stderr discipline** | `rounds.log` gave a machine-readable verdict independent of UI observation. |
| **Backup before every config edit** | CD config was restored byte-exact after the test. |
| **Screenshot-verified input** | The typed prompt was confirmed in the input box before Enter — no "did the text land?" ambiguity. |
| **Rotated log on re-run** | Zero contamination from verify-client traffic in the CD verdict. |
| **CUA with HITL approval** | `approve_automation` + verified cursor positions made the desktop drive safe and reproducible. |

---

**Owner:** Sandra S.
**Last updated:** 2026-08-02
