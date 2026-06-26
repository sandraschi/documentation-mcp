---
title: "SEP-1577 - Sampling with Tools - The Agentic Revolution"
category: architecture
status: active
audience: mcp-dev
skill_candidate: true
related:
  - patterns/FASTMCP_SAMPLING_ANTIPATTERNS.md
  - ecosystem/mcp-protocol/MCP_CLIENT_CAPABILITIES.md
last_updated: 2026-01-27
---

# SEP-1577: Sampling with Tools - The Agentic Revolution

## Executive Summary

**SEP-1577** represents the most significant advancement in MCP (Model Context Protocol) technology since its inception. This groundbreaking feature transforms MCP from a traditional client-server protocol into an intelligent, autonomous processing framework where servers can borrow the client's LLM to orchestrate complex workflows without round-trip communication bottlenecks.

## The Problem SEP-1577 Solves

### Traditional MCP Limitations

**Workflow Bottleneck:**
- Every decision requires client round-trip
- Complex workflows become exponentially expensive
- Client becomes scalability bottleneck
- 10-step workflow = 10 API calls minimum

**Example Pain Point:**
```
User → Client → "analyze this document" → Server → Client → "should I summarize?" → Server → Client...
```
- **Problem**: Client bottleneck for complex workflows
- **Cost**: 100 papers × 5 decisions = 500 API calls
- **Time**: Hours of processing due to network latency
- **Scalability**: Fails completely at scale

## SEP-1577: The Solution

### Revolutionary Agentic Architecture

**SEP-1577 Workflow:**
```
User → Server → LLM autonomously orchestrates: analyze → summarize → categorize → validate
```
- **Advantage**: Server borrows client's LLM for autonomous decision-making
- **Efficiency**: Single orchestrated call replaces dozens of round-trips
- **Scalability**: Handles arbitrarily complex workflows

### Core SEP-1577 Features

#### 1. `ctx.sample()` with Tools Parameter

```python
# SEP-1577 sampling with tools
response = await ctx.sample(
    messages=[{"role": "user", "content": "Process this document intelligently"}],
    tools=[analyze_relevance, extract_metadata, generate_summary, cross_reference]
)
```

**Execution Flow:**
1. **Server** passes prompt + tools to **client's LLM**
2. **LLM** autonomously decides tool sequence and parameters
3. **Server** executes tools automatically (no client round-trips)
4. **Results** fed back to LLM for next decisions
5. **Loop** continues until LLM produces final answer

#### 2. `ctx.sample_step()` - Fine-Grained Control

```python
step_result = await ctx.sample_step(
    messages=[{"role": "user", "content": current_prompt}],
    tools=available_tools
)
if step_result.tool_calls:
    for tool_call in step_result.tool_calls:
        if is_safe_to_execute(tool_call):
            execute_tool(tool_call)
```

#### 3. Structured Output Validation

```python
class ProcessingResult(BaseModel):
    sentiment: str
    confidence: float
    key_topics: List[str]
    summary: str

result = await ctx.sample(
    messages=[{"role": "user", "content": "Analyze this article"}],
    tools=analysis_tools,
    result_type=ProcessingResult  # Automatic validation
)
```

## Performance & Economic Analysis

| Operation Scale | Traditional MCP | SEP-1577 | Savings |
|----------------|-----------------|----------|---------|
| Simple workflow (5 steps) | 5 API calls | 1 call | 80% reduction |
| Medium workflow (15 steps) | 15 API calls | 1 call | 93% reduction |
| Large batch (1000 items × 10 ops) | 10,000 calls | ~50 calls | 99.5% reduction |

## Implementation Roadmap

### Phase 1: Core SEP-1577 (✅ Complete)
- [x] ctx.sample() with tools parameter
- [x] ctx.sample_step() fine-grained control
- [x] Structured output validation
- [x] Sampling handlers (Anthropic, OpenAI)

### Phase 2: Advanced Orchestration (🚧 In Progress)
- [ ] Multi-agent coordination framework
- [ ] Workflow persistence and resumption
- [ ] Real-time progress streaming

---

## Production Anti-Patterns (2026-02-22)

These bugs were found in production in `advanced-memory-mcp` and `filesystem-mcp`.

| Anti-pattern | Error | Fix |
|---|---|---|
| `app.state.get("sampling_context")` | AttributeError | Use `ctx: Context` parameter |
| `mcp.ctx.sample(...)` | AttributeError | Use injected `ctx` inside tool |
| `tools=[{"name": "x", "function": lambda ...}]` | Mock results | Pass plain callables: `tools=[fn1, fn2]` |
| `context: Context = None` | Injection fails | Rename to `ctx: Context = None` |

### Correct minimal example

```python
from fastmcp import Context
from pydantic import BaseModel

class Result(BaseModel):
    summary: str
    success: bool

async def my_leaf_tool(query: str) -> str:
    """Do real work. FastMCP generates schema from type hints + docstring."""
    return "real result from real service"

@mcp.tool
async def my_meta_tool(prompt: str, ctx: Context = None) -> dict:
    result = await ctx.sample(
        messages=prompt,
        tools=[my_leaf_tool],   # plain callables, not dicts
        result_type=Result,
    )
    r: Result = result.result
    return {"summary": r.summary, "ok": r.success}
```

### Rule: meta-tools vs leaf tools

Only **meta-tools** call `ctx.sample()`. **Leaf tools** are passed as `tools=` arguments.
Naming convention for meta-tools: prefix with `agentic_`, `workflow_`, `batch_`, `orchestrate_`.

---

**Date:** 2026-01-27 (anti-patterns added 2026-02-22)
**Status:** Active reference
**Owner:** Sandra Schi
