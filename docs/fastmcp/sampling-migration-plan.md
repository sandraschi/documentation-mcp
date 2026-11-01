# Sampling Migration Plan: `ctx.sample()` → Direct Local LLM

**Status**: Planning
**Driver**: MCP 2026-07-28 deprecated `sampling/createMessage` (SEP-2577). FastMCP 4 will remove `ctx.sample()`.
**Fleet constraint**: No cloud API keys — use Ollama or LM Studio exclusively. Zero per-token cost.

## Why NOT MRTR

MRTR (`InputRequiredResult`) is the protocol-level replacement for sampling, but it requires FastMCP 4 and has a round-trip overhead. The simpler, cheaper, and more accessible pattern is **direct local LLM calls**: the server holds an httpx client and calls Ollama/LM Studio directly. No protocol support needed, works with every MCP client today, zero cost.

```python
# BEFORE: ctx.sample() — deprecated, only works with Claude Desktop / hosts that support sampling
result = await ctx.sample("Analyze this trope")

# AFTER: direct Ollama call — works with every client, zero cost
import httpx
async with httpx.AsyncClient() as client:
    r = await client.post("http://localhost:11434/api/chat", json={
        "model": "qwen2.5:27b",
        "messages": [{"role": "user", "content": "Analyze this trope"}],
    })
    result = r.json()["message"]["content"]
```

## Fleet Audit: 15 Servers Affected

| Server | `ctx.sample()` calls | Test priority | Complexity |
|--------|---------------------|---------------|------------|
| devices-mcp | 1 | **1st** — simple, isolated, low risk | Low |
| multi-backup-mcp | 1 | 2nd | Low |
| home-assistant-mcp | 1 | 3rd | Low |
| obsidian-mcp | 1 | 4th | Low |
| discord-mcp | 1 | 5th | Low |
| email-mcp | 2 | — | Medium |
| calibre-mcp | 2 | — | Medium |
| pywinauto-mcp | 3 | — | Medium |
| freecad-mcp | 3 | — | Medium |
| tvtropes-mcp | 3 | — | Low (falls back to plan) |
| blender-mcp | 4 | — | Medium |
| arxiv-mcp | 7 | — | High (many calls) |
| filesystem-mcp | 4 | — | Medium |
| advanced-memory-mcp | 8 | — | High (many calls) |

## Migration Pattern

### For simple text generation (no tools passed):

```python
# Add to server.py imports
import httpx

# Tool function
async def _call_local_llm(prompt: str, system: str = "", model: str = "") -> str:
    """Call local Ollama or LM Studio."""
    base = os.getenv("LLM_BASE_URL", "http://localhost:11434")
    model_name = model or os.getenv("LLM_MODEL", "qwen2.5:27b")
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    async with httpx.AsyncClient(timeout=120) as client:
        if "11434" in base:
            r = await client.post(f"{base}/api/chat", json={
                "model": model_name, "messages": messages, "stream": False,
            })
            return r.json()["message"]["content"]
        else:
            r = await client.post(f"{base}/v1/chat/completions", json={
                "model": model_name, "messages": messages,
            })
            return r.json()["choices"][0]["message"]["content"]
```

### For agentic flows (tools passed to LLM):

These need the LLM to understand which tools are available. The pattern is to inject tool descriptions into the system prompt instead of passing tool definitions:

```python
# BEFORE: ctx.sample() with tools= parameter
result = await ctx.sample(
    messages=[{"role": "user", "content": user_msg}],
    system_prompt="You have these tools: ...",
    tools=[tool1, tool2],  # MCP-specific, only works with sampling hosts
)

# AFTER: tool descriptions in system prompt (works everywhere)
system = (
    "You have access to these tools. Call them by returning JSON:\n"
    "- search_notes(query): search notes by keyword\n"
    "- read_note(id): get full note content\n\n"
    "When you want to call a tool, respond with JSON like: {\"tool\": \"search_notes\", \"args\": {\"query\": \"...\"}}"
)
async with httpx.AsyncClient() as client:
    r = await client.post(f"{base}/api/chat", json={
        "model": model_name,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user_msg},
        ],
    })
    response = r.json()["message"]["content"]
    # Parse JSON tool calls from response, execute, feed back...
```

## Test Plan (devices-mcp canary)

1. Clone devices-mcp
2. Replace `ctx.sample()` with `_call_local_llm()` using Ollama
3. Run `uv run pytest` — confirm no regressions
4. Start the server and exercise the affected tool
5. Check logs for latency/token usage
6. If clean — promote pattern to next server

## Config

Add to each server's `.env.example`:

```env
# Local LLM for agentic tools (replaces MCP sampling)
LLM_BASE_URL=http://localhost:11434
LLM_MODEL=qwen2.5:27b
LLM_TIMEOUT=120
```

No cloud keys, no per-token cost. Uses the RTX 4090 that's already running.

## Timeline

| Phase | When | What |
|-------|------|------|
| 1 — Canary | This week | Migrate devices-mcp, analyze logs |
| 2 — Low complexity | Next week | multi-backup-mcp, home-assistant-mcp, obsidian-mcp, discord-mcp |
| 3 — Medium complexity | Within 2 weeks | email-mcp, calibre-mcp, pywinauto-mcp, freecad-mcp, blender-mcp, tvtropes-mcp |
| 4 — High complexity | Within 3 weeks | arxiv-mcp, filesystem-mcp, advanced-memory-mcp |
| 5 — assfix update | After canary | Update assfix checklist: `ctx.sample()` → direct LLM recommended |
