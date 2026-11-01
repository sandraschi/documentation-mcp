# MCP 2026-07-28 + FastMCP 4.0 — Fleet Impact Analysis

**Date**: 2026-08-01  
**Status**: ANALYSIS — neither is final. Both are release candidates / betas.  
**TL;DR**: Do NOT convert the fleet yet. Wait for stable releases. The breaking changes are severe and affect every fleet server.

---

## Naming Clarification

What was reported as "MCP 2.0" and "FastMCP 5.0" actually refers to:

| Heard | Actual | Status |
|-------|--------|--------|
| "MCP 2.0" | MCP Python SDK v2 + MCP spec RC `2026-07-28` | Release Candidate (not final) |
| "FastMCP 5.0" | FastMCP 4.0.0b1 | Beta (not stable) |

The MCP spec does NOT use semantic versioning — it uses date-based revisions. The current stable spec is `2025-11-25`. The new RC is `2026-07-28`. FastMCP jumped from 3.4.5 to 4.0.0b1 because it was rebuilt on the MCP Python SDK v2, which aligns with the 2026-07-28 spec RC.

---

## 1. MCP Spec 2026-07-28 — Key Changes

### 1.1 Protocol Becomes Sessionless (THE BIG ONE)

- **No more `Mcp-Session-Id`** — every request is stateless
- **No more `initialize` handshake** — protocol version and capabilities carried in `_meta` on every request
- **New `server/discover` RPC** — servers advertise supported versions, capabilities, identity
- **Version negotiation per-request**, not per-connection

### 1.2 Multi Round-Trip Requests (MRTR / Guard Pattern)

- Replaces server-initiated requests (`sampling/createMessage`, `roots/list`, `elicitation/create`)
- Server returns `InputRequiredResult` (`resultType: "input_required"`)
- Client retries the original request with `inputResponses`
- ALL results now carry a required `resultType`: `"complete"` or `"input_required"`

### 1.3 Subscriptions System

- `subscriptions/listen`: single long-lived POST-response stream
- Replaces old `resources/subscribe`/`unsubscribe` and HTTP GET endpoint
- Types: `toolsListChanged`, `promptsListChanged`, `resourcesListChanged`, `resourceSubscriptions`

### 1.4 Removed Features

| Removed | Replacement |
|---------|-------------|
| `ping` | Gone — no session to ping |
| `logging/setLevel` | Per-request `io.modelcontextprotocol/logLevel` in `_meta` |
| `notifications/roots/list_changed` | Gone |
| `initialize` handshake | `server/discover` + per-request `_meta` |
| SSE stream resumability | Re-issue request with new request ID |

### 1.5 New Features

- **Cache hints**: `ttlMs` + `cacheScope` on list/read results (SEP-2549)
- **OpenTelemetry trace context**: `traceparent`, `tracestate`, `baggage` in `_meta` (SEP-414)
- **Tool ordering**: Servers SHOULD return tools deterministically
- **Standard HTTP headers**: `Mcp-Method`, `Mcp-Name` on POST (SEP-2243)
- **Extensions**: `extensions` field on capabilities for optional protocol features
- **Error code policy**: Formal allocation of `-32000` to `-32099` range

### 1.6 Deprecated (still work, scheduled for removal)

- **Roots, Sampling, Logging features** (SEP-2577)
- **HTTP+SSE transport** → migrate to Streamable HTTP
- **OAuth DCR** (RFC 7591) → Client ID Metadata Documents

---

## 2. FastMCP 4.0.0b1 — Key Changes

FastMCP 4 is built on MCP Python SDK v2. This is a ground-up rewrite of the protocol layer.

### 2.1 BREAKING: ctx.sample() REMOVED

```python
# DOES NOT EXIST in FastMCP 4
ctx.sample("Analyze this")
ctx.sample_step(...)
ctx.list_roots()
```

**Replacement**: Call an LLM directly server-side, or use the guard pattern (return `InputRequiredResult`).

Official guidance: *"If borrowing the caller's model IS your server — stay on FastMCP 3.x rather than migrate."*

### 2.2 BREAKING: ctx.elicit() is Era-Gated

```python
# Raises on modern (2026-07-28) connections:
ctx.elicit("Approve this action?", response_type=bool)
# ToolError: elicitation via server-initiated requests is unavailable on 2026-07-28 connections.
```

**Replacement**: Guard pattern — return `InputRequiredResult` with the input you need.

### 2.3 BREAKING: No More Sessions

```python
# No longer persists across calls:
ctx.set_state("user_id", 42)
# Later call:
ctx.state.get("user_id")  # None — fresh connection
```

**Replacement**: `UserSession` / `SessionId` — server-minted state handles (SEP-2567), or per-request auth checks.

### 2.4 BREAKING: No Middleware.on_initialize

```python
# NEVER runs on modern connections
class MyMiddleware:
    async def on_initialize(self, ctx):
        # Won't fire — no initialize handshake
```

**Replacement**: Per-request auth checks, guard patterns.

### 2.5 Dependency Changes

| Old | New |
|-----|-----|
| `httpx` | `httpx2` (drop-in fork, same API) |
| `pydantic >= 2.0` | `pydantic >= 2.12` |
| FastAPI any | FastAPI `>= 0.133.0` (for Starlette 1.x compat) |
| camelCase fields | `snake_case` (with bridge for now) |
| `mcp` SDK 1.x | `mcp` SDK 2.0.0 (stable) + `mcp_types` |

### 2.6 Background Tasks Moved to Extension

```python
# FastMCP 3 — worked out of the box:
@mcp.tool(task=True)
async def slow_work(duration: int) -> str: ...

# FastMCP 4 — needs explicit extension:
from fastmcp_tasks import TasksExtension
mcp.add_extension(TasksExtension())

@mcp.tool(task=True)
async def slow_work(duration: int) -> str: ...
# Also: install fastmcp[tasks] extra
```

### 2.7 New Features in FastMCP 4

| Feature | Description |
|---------|-------------|
| **Multi-era serving** | One server serves both handshake-era and modern clients simultaneously |
| **Interactive tools** | Guard pattern — tools ask follow-up questions across request-response rounds (SEP-2322) |
| **Stateless session state** | `UserSession` / `SessionId` — explicit per-user state keys (SEP-2567) |
| **Background tasks extension** | `fastmcp-tasks` package, same `@mcp.tool(task=True)` surface |
| **Server extensions API** | `add_extension()` — capability-negotiated plugins (SEP-2133) |
| **Enterprise auth** | Identity assertion (SEP-990), `require_roles`, step-up challenges (SEP-2350), DCR `application_type` (SEP-837), routable transport headers (SEP-2243) |
| **Argument completion** | `@mcp.completion` — autocomplete for prompt args and resource-template parameters |
| **Cache hints** | `KeyValueResponseCacheStore` for distributed client response caching (SEP-2549) |
| **httpx2** | Next-gen httpx fork with OS trust store TLS |
| **Snake_case protocol types** | `input_schema`, `mime_type`, `is_error`, `next_cursor` (camelCase bridge active) |

### 2.8 Removed Imports (will break on upgrade)

```
fastmcp.server.proxy          → fastmcp.server.providers.proxy
fastmcp.server.openapi        → fastmcp.server.providers.openapi
fastmcp.server.apps           → fastmcp.apps
fastmcp.tools.tool            → fastmcp.tools
fastmcp.resources.resource    → fastmcp.resources
fastmcp.prompts.prompt        → fastmcp.prompts
fastmcp.server.tasks          → fastmcp.utilities.tasks
fastmcp.server.sampling       → REMOVED (no replacement)
SkillsProvider                → SkillsDirectoryProvider
CachableToolResult            → CacheableToolResult (spelling fix, no alias)
PromptToolMiddleware          → PromptsAsTools transform
```

---

## 3. Fleet Audit Results (2026-08-01)

Scanned fleet repos for `ctx.sample()`, `ctx.sample_step()`, `sampling_handler`, and `SamplingTool`:

| Repo | Severity | Details |
|------|----------|---------|
| **advanced-memory-mcp** | CRITICAL | 28+ hits. `ctx.sample()` is the core of inter_server_tools, agentic_content_workflow, intelligent_batch_processor, make_skill_advanced. This server IS sampling. |
| **arxiv-mcp** | CRITICAL | 3 tools use `ctx.sample()`: arxiv_agentic_assist, arxiv_sampling_hint, deep_analyze_paper_epistemics. Also has epistemic_job background task. |
| **calibre-mcp** | HIGH | agentic_workflow, media_agentic tools, help tools all reference `ctx.sample()`. |
| **blender-mcp** | HIGH | agentic.py, chat_tools, construct_tools, repository_tools all use `ctx.sample()`. |
| **discord-mcp** | HIGH | DiscordSamplingHandler + sampling_handler config on server init. |
| **autohotkey-mcp** | HIGH | dual_llm.py uses `ctx.sample()` for dual-model orchestration. |
| **arr-mcp** | HIGH | ArrSamplingHandler + agentic cross-arr workflow via `ctx.sample()`. |
| **beyondcompare-mcp** | MEDIUM | agentic.py uses `ctx.sample()`. |
| **avatar-mcp** | MEDIUM | avatar_sampling_tool uses `ctx.sample()`. |
| **alexa-mcp** | MEDIUM | 1 direct `ctx.sample()` call. |
| **bumi-mcp** | MEDIUM | agentic.py uses `ctx.sample()`. |
| **yahboom-mcp** | MEDIUM | agentic.py uses `ctx.sample()`. |
| **home-assistant-mcp** | MEDIUM | agentic.py uses `ctx.sample()`. |
| **aiwatcher-mcp** | LOW | `distill_pending()` uses sampling conceptually but search shows no direct `ctx.sample()` call. May use server-side LLM already. |
| **learnbot-mcp** | CLEAR | No hits. Server-side LLM already. |
| **resolveops** | HIGH | `conversational_resolve_assistant` and `intelligent_video_processing` — sampling-heavy but possibly abstracted. Needs deeper check. |

**Total**: At least **13 repos** with direct `ctx.sample()` usage. The "sampling-heavy" tier (advanced-memory, arxiv, calibre, blender, discord, autohotkey) are the hardest to migrate.

Additional concerns not caught by this search: `ctx.elicit()`, `Middleware.on_initialize`, `ctx.set_state()`, and camelCase field access — all require separate audits.

---

## 4. Fleet Impact — Per-Pattern Breakdown

| Fleet Pattern | Status in FastMCP 4 | Severity | Affected repos |
|---------------|---------------------|----------|----------------|
| `ctx.sample()` for agentic reasoning | **REMOVED** | CRITICAL | 13+ repos |
| `ctx.elicit()` for user confirmations | **Era-gated** (raises on modern) | CRITICAL | Needs separate audit |
| `ctx.list_roots()` for file paths | **REMOVED** | HIGH | blender-mcp, filesystem-mcp, others |
| `Middleware.on_initialize` for auth | **Never fires** on modern | HIGH | discord-mcp, others |
| `ctx.set_state()` cross-call | **Does not persist** | HIGH | advanced-memory-mcp, others |
| `@mcp.tool(task=True)` background | **Needs extension** | MEDIUM | arxiv-mcp (epistemic_job) |
| camelCase field access | **Bridge active, will be removed** | MEDIUM | All repos (eventually) |
| `httpx` in tool code | **FastMCP uses httpx2 now** | MEDIUM | All repos using custom HTTP |
| `SamplingTool` patterns | **REMOVED** | CRITICAL | advanced-memory-mcp |

---

## 5. Usage Examples — FastMCP 4

### 5.1 Guard Pattern (replaces ctx.elicit / ctx.sample)

```python
from fastmcp import FastMCP
from fastmcp.server.results import InputRequiredResult

mcp = FastMCP("MyServer")

@mcp.tool()
async def dangerous_operation(target: str, confirmed: bool = False) -> str:
    """Delete a critical resource. Requires confirmation."""
    if not confirmed:
        return InputRequiredResult(
            message="Confirm deletion",
            input_requests=[{
                "type": "elicitation",
                "message": f"Are you sure you want to delete '{target}'?",
                "response_type": bool,
            }]
        )
    # Client retries with confirmed=True
    return f"Deleted {target}"
```

### 5.2 Server-Side LLM (replaces ctx.sample)

```python
from fastmcp import FastMCP
import httpx2

mcp = FastMCP("MyServer")

@mcp.tool()
async def analyze_code(code: str) -> str:
    """Analyze code by calling Ollama directly."""
    async with httpx2.AsyncClient() as client:
        r = await client.post(
            "http://localhost:11434/api/generate",
            json={"model": "codellama", "prompt": f"Analyze:\n{code}", "stream": False}
        )
        return r.json()["response"]
```

### 5.3 Session State (replaces ctx.set_state)

```python
from fastmcp import FastMCP, SessionId, UserSession

mcp = FastMCP("MyServer")

@mcp.tool()
async def start_workflow(session: UserSession) -> str:
    session.state["step"] = 1
    return "Workflow started"

@mcp.tool()
async def continue_workflow(session: UserSession) -> str:
    step = session.state.get("step", 0)
    session.state["step"] = step + 1
    return f"Step {step + 1} complete"
```

### 5.4 Tasks Extension (replaces built-in task=True)

```python
from fastmcp import FastMCP
from fastmcp_tasks import TasksExtension

mcp = FastMCP("MyServer")
mcp.add_extension(TasksExtension())

@mcp.tool(task=True)
async def train_model(epochs: int) -> str:
    """Long-running training job."""
    for epoch in range(epochs):
        await asyncio.sleep(1)
    return f"Trained {epochs} epochs"
```

### 5.5 Argument Completion

```python
@mcp.completion()
async def suggest_models(argument: str, value: str) -> list[str]:
    models = ["llama3:8b", "codellama:13b", "mistral:7b"]
    return [m for m in models if value.lower() in m.lower()]
```

---

## 6. Recommendation: DO NOT CONVERT YET

### Why Wait

1. **Both are pre-release.** MCP spec 2026-07-28 is an RC. FastMCP 4.0.0b1 is a beta. The spec itself says: *"this specification is not final. Changes may be introduced between the RC and the final release."*

2. **Massive breaking change for the fleet.** `ctx.sample()` is the backbone of 13+ fleet servers. The official upgrade guide says: *"If borrowing the caller's model IS your server — stay on FastMCP 3.x rather than migrate."*

3. **No upgrade path for sampling-heavy servers.** The recommendation to "call an LLM directly" requires massive architectural changes — every server that uses `ctx.sample()` needs a full redesign of how it does agentic reasoning.

4. **The tooling ecosystem hasn't caught up.** Claude Desktop, Cursor, opencode — none have shipped support for the 2026-07-28 spec yet. FastMCP serves both eras, but the modern era is untested in production.

5. **FastMCP 3.x is still maintained.** v3.4.5 is the current stable release. The v3→v4 migration is one-way — there's no downgrade path for a server once converted.

### Recommended Timeline

| Phase | When | Action |
|-------|------|--------|
| **Now** | Immediate | Pin `fastmcp>=3.4.5,<4.0.0` fleet-wide. Audit for `ctx.elicit()` and `on_initialize`. |
| **Beta** | When FastMCP 4.0 stable ships | Convert ONE canary server (learnbot-mcp — zero sampling hits, already server-side LLM). Run it in production for 2 weeks. |
| **Pilot** | ~4 weeks after stable | Convert 3-5 servers of increasing complexity. Test with all tools, webapps, CUA smoke tests, Playwright E2E. |
| **Fleet** | ~8 weeks after stable | Mechanical rollout across remaining non-sampling servers. Use the upgrade checklist and automated migration prompts. |
| **Sampling servers** | ~12 weeks after stable | Redesign sampling-heavy servers for server-side LLM or guard pattern. This is the long pole. |

### What To Do Now

1. **Run this fleet audit** to understand the blast radius:

```powershell
rg -l "ctx\.sample\(|ctx\.sample_step\(|ctx\.list_roots\(|ctx\.elicit\(|on_initialize|ctx\.set_state|SamplingTool" D:\Dev\repos\*\src\ --include "*.py" | ForEach-Object { $_ -replace '.*repos\\([^\\]+).*', '$1' } | Sort-Object -Unique
```

2. **Read the full upgrade guide**: `https://gofastmcp.com/getting-started/upgrading/from-fastmcp-3`

3. **Pin FastMCP 3.x** in all fleet `pyproject.toml` files:
   ```toml
   dependencies = ["fastmcp>=3.4.5,<4.0.0"]
   ```

4. **Subscribe** to the FastMCP and MCP spec repos for stable release announcements.

---

## 7. What They Replaced It With — The Real Answer

They didn't just delete sampling. They inverted the architecture.

### Why Sampling Had to Go

The new protocol is **sessionless** (SEP-2575 + SEP-2567). No `initialize` handshake, no `Mcp-Session-Id`, no persistent connection. Every request is an independent HTTP call. This was the **#1 most-requested feature** from enterprise developers who wanted to put MCP servers behind plain round-robin load balancers.

`ctx.sample()` was impossible in this model because it was a **server-initiated push**: the server sent a `sampling/createMessage` request *down* an open bidirectional stream back to the client and blocked for the answer. No stream = no push = no sampling.

### The Replacement: MRTR (Multi Round-Trip Requests)

```
OLD (push model, session-based):
  Client tool call ──→ Server
  Server ──ctx.sample()──→ Client's LLM (server pushes, blocks)
  Client's LLM → answer → Server
  Server → result → Client

NEW (pull model, sessionless):
  Client tool call ──→ Server
  Server → InputRequiredResult("I need LLM analysis of this") → Client
  Client calls its own LLM → gets answer
  Client RETRIES same tool call with answer attached → Server
  Server → result → Client
```

The server doesn't *push* a request. It *returns* one. The **client** runs the retry loop. Each round is a separate HTTP request — load-balanceable, no sticky sessions.

### What This Means for Tool Code

```python
# BEFORE — push model, dead in FastMCP 4
@mcp.tool()
async def analyze(paper_id: str, ctx: Context) -> dict:
    text = fetch(paper_id)
    result = await ctx.sample(f"Analyze: {text}")  # PUSHES to client
    return {"analysis": result}

# AFTER — pull/guard model, FastMCP 4
@mcp.tool()
async def analyze(paper_id: str, llm_response: str | None = None) -> dict:
    text = fetch(paper_id)
    if llm_response is None:
        return InputRequiredResult(
            message="LLM analysis needed",
            input_requests={"analysis": CreateMessageRequest(
                messages=[SamplingMessage(role="user", content=TextContent(text=f"Analyze: {text}"))],
                max_tokens=1000,
            )}
        )
    return {"analysis": llm_response}
```

### The Cruel Irony

The official blog post says: *"the most highly-requested features from developers who were eager to get better reliability and scalability."*

Translation: enterprise developers with 10,000-server deployments wanted load balancing. They got it. Your 13 sampling-heavy fleet servers? Collateral damage.

Even the FastMCP 4 upgrade guide is blunt: *"If borrowing the caller's model IS your server — stay on FastMCP 3.x rather than migrate."*

---

## 8. Community Reaction

### SEP-2577 Discussion (GitHub PR #2577)

**SamMorrowDrums** (MCP contributor) — approved the deprecation but flagged the elephant in the room:

> "servers can no longer use inference without either paying for it or finding a way to charge the user, doesn't change the decision but it matters."

**PederHP** (MCP member) — the most nuanced take:

> "sampling as it exists now adds a lot of complexity for a feature that has almost no adoption. It should be said that almost all of this complexity still exists in order to support elicitation which is not being deprecated. [...] It is my hope it will eventually return in a more flexible and usable format — perhaps as a compatibility feature with an emerging model invocation standard."

He also proposed deprecating **Prompts** too:

> "The Prompts capability mostly serves as a source of confusion for models when they work with MCP right now."

**kziemski** — nervous about feature creep removal:

> "So just tools, resources and mcp apps? resources next to go?"

### Core Maintainer Meeting (Discussion #2536, April 1, 2026)

Internal consensus was blunt. From the meeting notes:

> "Roots and sampling move to an extension. [...] This is part of a wider intent to keep the core spec minimal and push optional capabilities outward."

> "The group reached consensus that transport-level sessions [...] should be eliminated entirely. The confusion they introduce outweighs any benefit at that layer."

No public dissent recorded. The meeting was between core maintainers at the MCP Dev Summit — Anthropic, Microsoft, Prefect (FastMCP), Zed, and others. This was an insider decision.

### SDK Ecosystem Reaction

The SDK ecosystem is already moving:

- **MCP Python SDK v2**: Stable release on 2026-07-28, removes sampling from server API
- **MCP TypeScript SDK**: Deprecated sampling in v1.28+
- **FastMCP 4.0.0b1**: Removes `ctx.sample()` entirely from `Context`
- **Pydantic AI** (pydantic/pydantic-ai#6738): Preparing `MCPToolset` for FastMCP 4
- **Dozens of .NET repos**: Already bumping `ModelContextProtocol` from 1.4.1 to 2.0.0 via Dependabot (visible as automatic PRs triggered by SEP-2577 references)

### The Overall Picture

| Group | Position |
|-------|----------|
| **Core maintainers** (Anthropic, MS, Prefect) | Deprecate. Stateless is the future. Low adoption, high complexity. |
| **Enterprise devs** | Wanted this. Load balancing, no sticky sessions, simpler infrastructure. |
| **Server authors using sampling** | Collateral damage. Official advice: stay on v3. |
| **SDK maintainers** | Already shipped. Python, TS, Go, C# all on v2 with sampling removed from server API. |
| **Downstream consumers** | Auto-upgrading via Dependabot. Most won't notice until their servers break. |

The consensus isn't "sampling is bad" — it's "sampling is powerful but almost nobody implemented it, and the architecture it requires (persistent bidirectional streams) blocks the #1 requested feature (stateless load balancing)."

---

## 9. The Fleet's Position — Honest Assessment

Your fleet is an outlier. You're one of the few server authors who **actually used sampling heavily**. The maintainers' argument that "nobody adopted it" doesn't apply to a fleet with 13+ servers built around `ctx.sample()`.

You have options:

1. **Pin FastMCP 3.x** and keep serving the old protocol. Clients (Claude Desktop, Cursor, opencode) will continue negotiating the old era for at least 12 months, probably longer. This buys time.

2. **Convert sampling servers to server-side LLM** (Ollama on RTX 4090). Works now, works forever, zero protocol dependency. But you lose the "borrow the caller's model" capability — your tokens, your bill.

3. **Convert to the MRTR guard pattern**. Works on the new protocol, architecturally clean. But no major client supports the retry loop yet, so you're building for a future that doesn't exist.

4. **Fork FastMCP 3.x** and maintain your own fork with `ctx.sample()` preserved. Drastic but viable if the fleet's entire value proposition IS sampling.

The honest recommendation: **Option 1 for the next 12 months, option 2 as the long-term target.** The protocol is moving away from server-initiated LLM calls. Adapting to that reality now, on your own timeline, beats being forced to adapt later.

---

## 10. Advantages Worth the Pain

Once stable, the 2026-07-28 era brings genuine improvements:

| Advantage | Why It Matters |
|-----------|---------------|
| **Stateless by default** | No session management. Load-balance freely. No sticky sessions. |
| **Multi-era serving** | One deployment serves all clients. No migration flag day. |
| **Guard pattern** | Cleaner than `ctx.elicit()` — the tool returns what it needs, client provides it. |
| **Cache hints** | `tools/list` results are cacheable. Reduces latency on every connection. |
| **Enterprise auth** | `require_roles`, identity assertion, step-up challenges — production-grade. |
| **Extensions API** | Capability-negotiated plugins instead of monkey-patching core. |
| **Argument completion** | Autocomplete for prompt/resource parameters — native IDE integration. |
| **httpx2** | OS trust store, no certifi dependency, same API surface. |

---

**Bottom line**: This is the biggest protocol change in MCP's history. The fleet is heavily dependent on the features being removed. Wait for stable releases, audit the blast radius now, and plan a phased rollout — not a flag-day conversion.

---

## 11. FastMCP 4.0 — Judged on Its Own Merits

Strip away the MCP spec politics. Evaluate FastMCP 4.0 purely as a Python framework. How good is it?

### The Good — Genuine Engineering Improvements

**Multi-era serving is real work.** One server process handles old-protocol clients (with `ctx.sample()`, `ctx.elicit()`, sessions) and new-protocol clients (stateless, MRTR) simultaneously. This is non-trivial — the SDK negotiates per-connection and FastMCP abstracts the difference. You get a migration path without a flag day.

**Server extensions API.** `mcp.add_extension(TasksExtension())` is a clean plugin system. No more monkey-patching internals. This enables modular fleet servers — compose auth, tasks, telemetry, skills as extensions. The extension advertises its capability (`io.modelcontextprotocol/tasks`) and clients negotiate. Proper plugin architecture in a Python MCP framework is genuinely new.

**Snake_case protocol types.** `tool.input_schema` instead of `tool.inputSchema`. This sounds trivial but it's a massive quality-of-life improvement for Python developers. Every MCP SDK v2 object is properly Pythonic now — autocomplete works, type checkers are happy, no more cognitive dissonance between Python conventions and protocol camelCase.

**Cleaner middleware dispatch.** In v3, middleware only saw routable requests. In v4, every message passes through: `notifications/cancelled`, `notifications/initialized`, `notifications/progress`, unknown methods, validation failures. This is the right design — middleware as a universal interceptor, not a selective hook. The old behavior was a source of silent bugs.

**Path security on templated resources.** `..` traversal, absolute paths, and null bytes are screened at the server's read choke point before your handler runs. A rejected read returns a generic "resource not found" — no information leak. Per-parameter exemptions available. This is security infrastructure you'd have to write yourself otherwise.

**Deterministic tool ordering.** `tools/list` returns in stable order, not Python's hash-order randomization. This matters: LLM prompt caches key on the tools block. Deterministic order = higher cache hit rate = cheaper API calls. Small thing, real impact.

**UserSession pattern.** Server-minted state handle passed as a tool argument. The model sees it, threads it between calls. More explicit than `ctx.set_state()` hidden in transport magic. This is evolution, not replacement — the old way was fragile and opaque.

**Argument completion.** `@mcp.completion()` — autocomplete for prompt arguments and resource template parameters. This enables IDE-like suggestions in MCP clients. Genuinely new functionality that didn't exist in v3.

### The Bad — What You Lose

**`ctx.sample()` removed from Context entirely.** Not deprecated, not era-gated — removed. `AttributeError` on every era. For a fleet built around this capability, this is fatal.

**`ctx.elicit()` era-gated.** Raises on modern connections. Since `Client` defaults to `mode="auto"` which negotiates the modern era, the default path is broken. You must explicitly set `mode="legacy"` or rewrite tools.

**`Middleware.on_initialize` never fires on modern connections.** Any auth gating, setup, or initialization you did in `on_initialize` is gone. Must be ported to per-request checks or guard patterns.

**Session state doesn't persist.** `ctx.set_state()` values evaporate between calls. The replacement (`UserSession`) is a different model requiring tool signature changes.

**Background tasks need a separate package.** `fastmcp[tasks]` extra + `fastmcp_tasks` import + `TasksExtension()` registration. For something that was built-in in v3, this is busy work.

**Import path reorganisation.** `fastmcp.server.proxy` → `fastmcp.server.providers.proxy`, `fastmcp.tools.tool` → `fastmcp.tools`, `SkillsProvider` → `SkillsDirectoryProvider`, `CachableToolResult` → `CacheableToolResult` (spelling fix, no alias). Dozens of mechanical changes. Every fleet server needs import surgery.

**httpx2 migration.** FastMCP uses `httpx2` exclusively now. If your tools catch `httpx.ConnectError` around FastMCP calls, those handlers are dead code — silently, because `httpx` is still installed transitively. No type checker catches this. Grep for `except httpx.` or wait for production failures.

**camelCase bridge is temporary.** `tool.inputSchema` still works today but emits `FastMCPDeprecationWarning`. The bridge will be removed in a future release. Every field access in every fleet server needs eventual migration.

**Dependency churn.** `pydantic >= 2.12` (up from 2.0), `FastAPI >= 0.133.0` (for Starlette 1.x compat). These force unrelated upgrades across the fleet. FastAPI 0.115 → 0.133 is a non-trivial jump.

### The Ugly — Framework Quality Issues

**Beta quality.** "This is a beta released for testing ahead of 4.0. Pin an exact version and expect sharp edges." The release notes say it directly. This is not production-ready.

**Breaking change density.** 12-item upgrade checklist, 28 removed imports, removed server methods, removed parameters, removed context methods, behavior changes that compile fine but break at runtime. The upgrade guide is 463 lines. This is not a minor version bump — it's a full rewrite.

**httpx2 is a fork.** httpx2 is maintained by a single developer as a "next-generation" fork. httpx has 14k stars and hundreds of contributors. httpx2 has... neither. The entire FastMCP HTTP stack now depends on a fork of uncertain longevity. This is a single-point-of-failure architectural risk that didn't exist in v3.

**The snake_case migration was avoidable.** MCP Python SDK v2 moved protocol types to `mcp_types` with snake_case fields. FastMCP could have wrapped them to preserve camelCase indefinitely. Instead they built a temporary bridge with scheduled removal. This creates forced migration work for zero user-facing benefit — the wire format never changed.

**Server-side LLM is the recommended path, but FastMCP provides zero helpers for it.** "Call an LLM directly from your server" — but there's no `LLMClient`, no provider abstraction, no Ollama/Anthropic/OpenAI integration in FastMCP itself. You're on your own with raw `httpx2.AsyncClient`. Contrast with `ctx.sample()` which was one line. The replacement is more work for less functionality.

### The Verdict

| Aspect | Score (0-10) | Notes |
|--------|-------------|-------|
| Engineering quality | 7 | Rewrite is solid, test suite passes MCP conformance. |
| Pythonic design | 8 | Snake_case, clean extensions API, proper typing. |
| Migration experience | 3 | 12-step checklist, 28 moved imports, silent runtime breaks. |
| Feature parity with v3 | 4 | Sampling gone, elicitation gated, sessions gone, tasks moved. |
| Stability | 2 | Beta. "Expect sharp edges." |
| Dependency hygiene | 4 | httpx2 fork risk, pydantic/Starlette version churn. |
| Fleet suitability | 2 | 13+ servers broken by sampling removal. Official advice: stay on v3. |
| **Overall** | **4/10** | Good framework, wrong time, wrong audience. |

FastMCP 4 is well-engineered for a developer starting a new server today who never used sampling. For the fleet, it's a downgrade that removes more than it adds. The one genuinely useful feature — multi-era serving — exists precisely because the protocol break is so severe that you need it.

The framework isn't bad. The timing and the protocol it's built on are the problem. FastMCP 4 would be a 7/10 release if it shipped on a protocol that kept `ctx.sample()`. On the 2026-07-28 protocol, for a sampling-heavy fleet, it's a 4.
