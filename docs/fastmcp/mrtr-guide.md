# MRTR — Multi Round-Trip Requests (SEP-2322) Fleet Guide

> **Status (verified 2026-08-14):** Spec stable in MCP **2026-07-28**. Both official SDKs implement it (Python 2.0.0, TypeScript 2.0.0). **No shipping client implements it.** FastMCP support requires **FastMCP 4** — nothing on 3.x.
> **Fleet posture:** do not use until FastMCP 4 stable AND a real client ships it. Direct local LLM calls remain the default replacement for sampling (see §6).

---

## 1. What MRTR is

Multi Round-Trip Requests (SEP-2322) is the MCP 2026-07-28 mechanism that replaces **server-initiated requests** — `roots/list`, `sampling/createMessage`, `elicitation/create` — with a **server-returned interim result** that the client fulfills on a retry of the original request.

Instead of the server asking the client "do this for me" mid-call, the tool call returns:

```json
{
  "resultType": "input_required",
  "inputRequests": {
    "clarify": {
      "type": "sample",
      "purpose": "LLM analysis of the tool output",
      "arguments": { "maxTokens": 500 }
    }
  },
  "requestState": { "round": 1 }
}
```

The client inspects `inputRequests`, gathers the requested information (runs its own LLM, asks the user, etc.), and **re-issues the original tool call** with:

```json
{
  "params": {
    "inputResponses": {
      "clarify": { "type": "sample", "content": [{ "type": "text", "text": "..." }] }
    }
  }
}
```

The server reads `ctx.input_responses["clarify"]` and completes normally with `resultType: "complete"`.

## 2. Protocol facts (2026-07-28 stable)

- All results now carry a required **`resultType`**: `"complete"` or `"input_required"`. Clients MUST treat results from older-protocol servers that omit the field as `"complete"`.
- `input_requests` is a map of request objects; the client responds with a parallel `input_responses` map on the retry.
- **`requestState`** is the server's own correlation token — the protocol itself is stateless (sessions removed), so servers encode any cross-retry state they need in `requestState` (e.g. round number, partial results).
- Removed alongside: `notifications/elicitation/complete` and the `elicitationId` field — the client learns the outcome of out-of-band interactions by retrying; a completion signal no longer fits.
- MRTR requests are NOT the same as `subscriptions/listen` (opt-in server→client change notifications on a long-lived stream). MRTR is strictly request/response with client retry.

## 3. What MRTR replaces (and what doesn't need it)

| Old server-initiated feature | 2026-07-28 status | MRTR replacement? |
|---|---|---|
| `sampling/createMessage` | Deprecated (SEP-2577, 12-month window) | Yes — `input_requests` with `type: "sample"` |
| `roots/list` | Deprecated | Partially — MRTR can request paths, but passing dirs via tool args or server config is simpler |
| `elicitation/create` | Removed from core (moved to elicitation pattern) | Yes — `input_requests` for user confirmation/clarification |
| `logging/setLevel` | Removed | No — per-request `io.modelcontextprotocol/logLevel` in `_meta` |
| Server→client notifications (progress/message) | Kept | No — flow on the request's own response stream |

## 4. SDK & framework support matrix

| Layer | Version | MRTR | Notes |
|---|---|---|---|
| MCP Python SDK | **2.0.0** (stable 2026-07-28) | ✅ | Server: `mcp.server.mcpserver.tools.base` (`InputRequiredResult`); Client: `mcp.client._input_required.run_input_required_driver` — full client loop works even over stdio |
| MCP TypeScript SDK | **2.0.0** (stable 2026-07-27) | ✅ | core/node/server packages all shipped 2.0.0 |
| FastMCP | **4.0.0b1** (beta) | ✅ | First-class: tools may return `InputRequiredResult`; retry exposes `ctx.input_responses` (fleet probe confirmed the shapes) |
| FastMCP | **3.4.x** (fleet pin today) | ❌ | Not available — `InputRequiredToolResult`/`InputRequiredResult` live on the FastMCP 4 / SDK v2 line |

Python SDK example story: `examples/stories/mrtr/` (server + client), `examples/stories/refund_desk/`; tutorial `docs_src/mrtr/tutorial002.py`.

## 5. Client implementation status (verified 2026-08-14, GitHub code search)

| Client | MRTR | Notes |
|---|---|---|
| Official SDK client drivers | ✅ | Both SDKs — this is the "library-ready" layer |
| Claude Desktop | ❌ | Fleet probe 2026-08-02: `InputRequiredResult` received, then ignored (no retry) |
| Zed | ❌ | Still speaking 2025-11-25 — not even on the new protocol yet |
| opencode | ❌ | No `InputRequiredResult` / `input_required` code |
| Cline | ❌ | No MRTR code |
| Cursor, Copilot, JetBrains, Cody | ❌ (no signals) | Closed-source or no surfaced implementation |

Global search: 2640 `InputRequiredResult` hits, all from the modelcontextprotocol org or SDK-derived side projects. **Zero mainstream clients.**

**Reading:** MRTR is *library-ready, product-empty*. It is one dependency bump away for any client adopting SDK v2 (TypeScript 2.0.0 already shipped) — the gap is adoption, not feasibility.

## 6. When to use MRTR vs alternatives (fleet decision table)

| Situation | Best pattern | Why |
|---|---|---|
| Server tool needs an LLM judgment call | **Direct local LLM call** (httpx → Ollama/LM Studio; `fleet-llm` post-sampling design) | Works on every client TODAY, protocol-independent, zero cost, no round-trip overhead. MRTR requires client support that doesn't exist yet |
| Tool needs user clarification / confirmation | **MRTR** (`input_requests`) when clients support it; **two-step tools** (draft → confirm) today | MRTR is the protocol-blessed shape; until clients ship it, explicit `confirm=True` args or a separate confirm tool work everywhere |
| Server needs filesystem roots | **Tool args / server config** | Deprecated anyway; simplest path |
| Interop with a third-party client that DOES implement MRTR | MRTR | Use it — but gate on §5 status before building |

**FastMCP 4 note:** the 4.0.0b1 upgrade guide is blunt — *"If borrowing the caller's model IS your server — stay on FastMCP 3.x rather than migrate."* For the fleet, direct local LLM calls make that caveat moot: we never borrow the caller's model.

## 7. Fleet posture & triggers

1. **Stay on `fastmcp>=3.4.4,<4`** — MRTR is a FastMCP 4 feature; adopting it requires the v4 upgrade path (canary learnbot-mcp → mechanical fleet upgrade) first.
2. **No new `ctx.sample()` usage** in P6/P7 work (sampling is Deprecated, still functional through the 12-month window).
3. **Re-check §5 quarterly** (or when a client release notes "MCP 2026-07-28 support"): MRTR becomes adoptable when a client you actually run implements it.
4. MRTR is an **optimization/interop path, never a dependency** — the fleet's intelligence layer must keep working on clients that never ship it.

## 8. The sampling lesson (why the hype is tempered)

Sampling was the same story in 2025: protocol-blessed, SDK-first-class, "the future of agentic servers" — the fleet built 13+ servers on `ctx.sample()`. Then SEP-2577 deprecated it in the very next protocol revision, and every one of those servers became migration debt. The pattern:

1. Spec feature ships, SDKs implement it, servers adopt eagerly
2. Protocol revision removes/rebrands it, servers eat the migration
3. Replacement (MRTR) repeats step 1

MRTR looks genuinely useful — interaction patterns are the missing piece of stateless MCP — but it has the same lifecycle risk, and today it has worse adoption than sampling ever had (sampling at least shipped in Claude Desktop). Mitigation: **default to protocol-independent patterns** (direct LLM calls, tool-arg state), treat MRTR as a *nice interop shape to be ready for*, not a foundation to build on. If it wins, adopting it is a small, reversible change — exactly the shape of the fleet-llm design.

## 9. Resources

- Spec: [MRTR pattern](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/mrtr) · [SEP-2322](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2322) · [2026-07-28 changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- Fleet probe (Claude Desktop round-trip test, 2026-08-02): *(fleet-internal, mcp-central-docs)* `operations/MCP4_MRTR_PROBE_CASE_REPORT.md`
- Migration plan (sampling → direct LLM): `sampling-migration-plan.md`
- FastMCP 4 decision: `fastmcp-4-assessment.md`
- Spec migration (stateless core, deprecations): `2026-07-28-spec-migration.md`
