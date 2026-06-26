---
title: "FastMCP Sampling Anti-Patterns"
category: pattern
status: active
audience: mcp-dev
skill_candidate: true
related:
  - fastmcp/sep-1577-sampling-with-tools.md
  - ecosystem/mcp-protocol/MCP_CLIENT_CAPABILITIES.md
last_updated: 2026-02-22
---

# FastMCP Sampling Anti-Patterns

**Status:** Production-confirmed bugs (found 2026-02-22 in `advanced-memory-mcp` and `filesystem-mcp`)
**FastMCP version:** 3.1.1+.1+
**Reference:** [SEP-1577 Sampling with Tools](../fastmcp/sep-1577-sampling-with-tools.md)

---

## Quick Summary

The correct pattern is `ctx.sample(tools=[plain_python_fn, ...], result_type=PydanticModel)` where `ctx` is a `Context` parameter FastMCP auto-injects into the tool function.

Everything else described below is wrong.

---

## Anti-pattern 1: Accessing `app.state` or `mcp.ctx`

```python
# âŒ BROKEN â€” FastMCP has no .state and no .ctx
sampling_ctx = app.state.get("sampling_context")
result = await mcp.ctx.sample(...)
```

**Error:** `AttributeError: 'FastMCP' object has no attribute 'state'`

**Fix:**
```python
# âœ… CORRECT â€” FastMCP injects ctx via the parameter
@mcp.tool
async def my_tool(prompt: str, ctx: Context = None) -> dict:
    result = await ctx.sample(messages=prompt, ...)
```

---

## Anti-pattern 2: Wrong parameter name for Context injection

```python
# âŒ BROKEN â€” FastMCP looks for 'ctx' by convention
async def my_tool(prompt: str, context: Context = None) -> dict:
    result = await context.sample(...)
```

FastMCP injects the live session context into a parameter typed as `Context`. While technically it finds it by type annotation, the conventional name is `ctx`. Using `context` may work in some versions but is undocumented and fragile.

**Fix:** Always name it `ctx`.

---

## Anti-pattern 3: Dict-formatted tools

```python
# âŒ BROKEN â€” pre-3.1.1+.1 pattern; LLM gets mock strings not real results
tools = [
    {
        "name": "search",
        "description": "...",
        "function": lambda query: f"Searched for {query}"  # mock!
    }
]
result = await ctx.sample(tools=tools, ...)
```

Two problems: dict format is not the 3.1.1+.1 API, and lambdas returning strings are mocks.

**Fix:**
```python
# âœ… CORRECT â€” real function, plain callable
async def search_knowledge_base(query: str) -> str:
    """Search the knowledge base. Returns markdown list of results."""
    from myserver.services.search import do_real_search
    return await do_real_search(query)

result = await ctx.sample(tools=[search_knowledge_base], ...)
```

---

## Anti-pattern 4: Custom sample_step() loop

```python
# âŒ BROKEN â€” pre-3.1.1+.1 manual loop, replaced by ctx.sample(tools=[...])
class AgenticWorkflow:
    async def run(self, prompt, tools):
        messages = [{"role": "user", "content": prompt}]
        for _ in range(self.max_iterations):
            step = await ctx.sample_step(messages=messages, tools=self._format_tools(tools))
            if step.stop_reason == "end_turn":
                break
            # manually call tools, append results ...

    def _format_tools_for_sampling(self, tools):
        return [{"name": t.__name__, "description": ..., "input_schema": ...} for t in tools]
```

**Fix:** Delete the class. `ctx.sample(tools=[fn1, fn2])` does the loop internally, handles tool calls, and returns when done.

---

## Anti-pattern 5: Wrapper class around the MCP instance

```python
# âŒ BROKEN
class SamplingClient:
    def __init__(self, mcp_instance):
        self._client = mcp_instance.ctx   # AttributeError
```

There is no need for a wrapper. Context is available only inside a tool function during an active client session. It cannot be stored or passed around.

---

## Rule: Leaf tools vs Meta-tools

| Type | Calls LLM? | Passed to ctx.sample? | Example |
|---|---|---|---|
| Leaf tool | No | Yes (as `tools=`) | `search_notes`, `read_note`, `write_note` |
| Meta-tool | Yes (via `ctx.sample`) | No | `agentic_content_workflow`, `intelligent_batch_processor` |

Leaf tools are plain Python async functions. FastMCP generates their JSON schema from type hints and docstrings automatically.

---

## Naming Convention

Meta-tools that use `ctx.sample()` should be prefixed: `agentic_`, `workflow_`, `batch_`, `orchestrate_`. This makes it obvious at a glance which tools coordinate vs which tools do actual work.

---

**Date:** 2026-02-22
**Status:** Reference â€” production-confirmed
**Owner:** Sandra Schi

