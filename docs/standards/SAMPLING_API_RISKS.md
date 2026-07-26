# Sampling & API Call Risks in MCP Servers

**Created:** 2026-02-28  
**Status:** Active  
**Applies to:** All MCP servers using FastMCP sampling / ctx.sample() / agentic loops

---

## The Problem

Claude Desktop does **not** fully implement the MCP sampling spec. It does not advertise `sampling.tools` capability. MCP servers that use `ctx.sample()` for tool-calling during sampling cannot use the client's model â€” they fall back to **direct Anthropic API calls**, bypassing your Claude subscription and charging against an API key.

Combined with agentic loop tools (e.g. `dbops:agentic_workflow_tool` with `max_steps=5`), a single runaway invocation can fire multiple API calls before you notice. At scale across 20+ MCP servers, this is a real cost and quota risk.

---

## FastMCP 3.1.1+ Sampling (Legacy Purged)

- **FastMCP 3.1.1+ (GA 2026-03-30):** Baseline fleet standard. Unified sampling API, stable capability negotiation, and bugfixes for parallel tool execution.
- **Legacy FastMCP 2.x:** Fully deprecated. All servers migrated to **3.2+** to ensure protocol safety and Prefab UI support.
- **Migration Policy:** No 3.1.1+.x or 3.0.x variants permitted in production.

---

## Mitigations

### 1. Rate Limiter (token bucket)

```python
from collections import deque
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_calls: int, window_seconds: int):
        self.max_calls = max_calls
        self.window = timedelta(seconds=window_seconds)
        self.calls = deque()

    def allow(self) -> bool:
        now = datetime.now()
        while self.calls and self.calls[0] < now - self.window:
            self.calls.popleft()
        if len(self.calls) >= self.max_calls:
            return False
        self.calls.append(now)
        return True
```

Recommended default: **10 API calls / hour / server**, overridable via env var `MCP_SAMPLING_MAX_CALLS_PER_HOUR`.

### 2. Hard Daily Token Budget

```python
DAILY_TOKEN_BUDGET = int(os.environ.get("MCP_DAILY_TOKEN_BUDGET", "100000"))

if token_counter.today_total >= DAILY_TOKEN_BUDGET:
    return "API budget exhausted for today. Sampling unavailable."
```

Accumulate token counts from API response `.usage` fields. Reset at midnight local time.

### 3. Explicit max_llm_calls on Agentic Tools

Any tool that loops must expose a `max_llm_calls` parameter (default: 3, hard cap: 10):

```python
async def agentic_tool(goal: str, max_llm_calls: int = 3) -> str:
    calls = 0
    while ...:
        if calls >= min(max_llm_calls, 10):
            return "Reached max_llm_calls limit. Stopping."
        calls += 1
        ...
```

### 4. Env Var Kill Switch

If `ANTHROPIC_API_KEY` is not set, fail loudly rather than silently:

```python
if not ctx.client_capabilities.sampling:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "Error: client does not support sampling and ANTHROPIC_API_KEY is not set. Cannot proceed."
```

This is the correct "refuse" pattern â€” not a blanket refusal, but a clean failure when no fallback is available.

### 5. Local Logging

Log every API fallback call with token count:

```python
with open("mcp_api_calls.log", "a") as f:
    f.write(f"{datetime.now().isoformat()} | {tool_name} | tokens={usage.total_tokens}\n")
```

Check Goliath logs periodically before the Anthropic billing cycle.

---

## Risk Assessment by Server

| Server | Risk | Reason |
|--------|------|--------|
| `dbops:agentic_workflow_tool` | **HIGH** | max_steps=5 loop, each step can call API |
| `memops:adn_external` (sampling) | Medium | Single calls mostly, but can chain |
| `memops` note ops | Low | Single API call per operation |
| Most other MCP servers | Low | No sampling, no API fallback |

---

## Action Items

- [ ] Add rate limiter to `dbops` agentic tool
- [ ] Add `max_llm_calls` parameter to all agentic loop tools
- [ ] Set `ANTHROPIC_API_KEY` only on servers that legitimately need it
- [ ] Add token budget env var to all sampling-capable servers
- [ ] Audit fleet for servers still on FastMCP < 3.0.0

