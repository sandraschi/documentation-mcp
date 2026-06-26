# Agentic IDE / MCP Client Capability Matrix

**Last Updated:** 2026-03-23  
**Status:** Current  
**Context:** Which clients support which FastMCP 3.1 capabilities

---

## The Core Question

Not all MCP clients are equal. A server with `ctx.sample()` agentic loops does nothing
useful in Claude Desktop. CodeMode servers work everywhere but look different in each
client. Knowing this matrix is essential for designing tools that behave correctly across
the fleet.

---

## Full Capability Matrix

| Capability | Claude Desktop | Cursor | Windsurf | Antigravity | Claude Code CLI |
|-----------|:--------------:|:------:|:--------:|:-----------:|:---------------:|
| **Basic tool calls** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **CodeMode / tool_search** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **MCP Prompts** | ✅ | Partial | Partial | ✅ | ✅ |
| **Skills resources** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Sampling (ctx.sample)** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Streaming sampling** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Multi-agent loops** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **MCP reliability** | Good | Good | Good | Good | Excellent |
| **Context window pressure** | High | Medium | Medium | Low | Low |
| **Red error visibility** | High | Low | Low | Low | Terminal |

**As of March 2026. Sampling support may expand to other clients during 2026.**

---

## Config File Locations

| Client | MCP Config Path | Notes |
|--------|----------------|-------|
| Claude Desktop | `C:\Users\sandr\AppData\Roaming\Claude\claude_desktop_config.json` | Standard |
| Cursor | `C:\Users\sandr\.cursor\mcp.json` | Standard |
| Windsurf | Windsurf settings → MCP | GUI-configured |
| Antigravity | `C:\Users\sandr\.gemini\antigravity` | ⚠️ Non-standard — NOT AppData |
| Claude Code | `~/.claude/mcp.json` or per-project `.mcp.json` | CLI-managed |

---

## What Sampling Changes

**Without sampling (Claude Desktop, Cursor, Windsurf):**
```
User → Tool executes → Returns result → User sees result
```
Tools are functions. No inner loop. No autonomous decision-making mid-execution.
Every decision point surfaces to the user.

**With sampling (Antigravity, Claude Code):**
```
User → Tool starts → Tool asks LLM mid-execution → LLM reasons → Tool continues
       ↑___________________inner loop___________________↑
       (user never sees this — happens inside the tool)
```
Tools can be agents. The server drives the loop. The user sees a final result, not
every intermediate step. This is what "agentic" actually means at the implementation level.

---

## Designing for Mixed Clients

Tools that use `ctx.sample()` should degrade gracefully when sampling isn't supported:

```python
@mcp.tool
async def smart_rename_functions(binary_path: str, ctx: Context) -> dict:
    """Analyze binary and rename functions. Agentic in Antigravity, static in Claude Desktop."""
    functions = get_functions(binary_path)
    renamed = {}

    for fn in functions:
        decompiled = decompile(fn.address)
        try:
            # Agentic path: ask LLM for reasoning
            suggestion = await ctx.sample(
                f"Decompiled:\n{decompiled}\n\nSuggest a descriptive snake_case name."
            )
            new_name = suggestion.text.strip()
        except NotImplementedError:
            # Fallback: heuristic rename
            new_name = f"fn_{fn.address:08x}"

        renamed[fn.name] = new_name

    return {"renamed": renamed, "mode": "agentic" if "suggestion" in dir() else "heuristic"}
```

Alternatively: flag tools that require sampling with a clear convention:

```python
@mcp.tool
async def agentic_analysis(data: str, ctx: Context) -> str:
    """
    Deep analysis using LLM reasoning loop.
    
    REQUIRES SAMPLING SUPPORT — use in Antigravity or Claude Code.
    Returns limited results in Claude Desktop / Cursor (sampling not supported).
    """
```

---

## CodeMode: How It Looks Per Client

All clients handle the `tool_search` call — but it surfaces differently:

**Claude Desktop:** Visible tool-use block in the conversation thread. User sees it.
Looks like: `tool_search { "query": "file operations" }`. Can seem confusing without context.

**Cursor/Windsurf:** Appears in Agent/Composer output pane. Less prominent, fast, user
rarely notices it. Fits IDE workflow naturally.

**Antigravity:** Similar to Cursor — agent output, not primary chat. Gemini's large
context window means less urgency, but CodeMode still keeps context clean.

**Claude Code:** Visible in terminal output. Most transparent of all clients.

In all cases: the tool_search call happens once per server per topic area per conversation.
After schemas are loaded, subsequent calls to that server's tools are direct.

---

## Practical Workflow Split (March 2026)

Given the capability matrix, the optimal workflow assignment:

| Task type | Best client | Why |
|-----------|-------------|-----|
| Conversational dev, memory queries, file ops | Claude Desktop | Stable, great UX |
| Code editing, refactoring, debugging | Cursor / Windsurf | IDE integration |
| Agentic analysis, autonomous loops, RE workflows | Antigravity | Sampling support |
| Batch processing, CI/CD, scripted analysis | Claude Code CLI | Full sampling, scriptable |
| Ghidra headless RE (ReVa) | Claude Code | ReVa designed for it |

---

## The Red Error History (Claude Desktop)

Through most of 2025, Claude Desktop had a visible red error overlay (top-right corner)
whenever an MCP tool call failed. Causes:

1. **Context overflow** — too many tool schemas loaded at session start, no room for
   actual content. Server response truncated or dropped → red error.

2. **Parameter hallucination** — LLM didn't have the schema in context, guessed parameters,
   server rejected them → red error.

3. **Protocol errors** — early FastMCP versions had edge cases in error serialization
   that produced malformed MCP responses → red error.

4. **Slow/hanging tools** — tools with no timeout that blocked the message loop → spinner
   then red error.

**What fixed it:**
- Portmanteau pattern → fewer tools in catalog, smaller schemas
- CodeMode → schemas loaded on demand, not upfront
- FastMCP 3.0/3.1 better error handling and serialization
- Fleet standardization → consistent patterns, predictable behavior

By February 2026 the red error rate dropped dramatically. Not zero, but from
"happens constantly" to "occasional edge case."

---

## Next Likely Inflection Points

**Sampling coming to Claude Desktop:** Anthropic has not shipped this as of March 2026.
When they do, Claude Desktop will become a full agentic client. Likely 2026.

**Multi-agent coordination:** FastMCP MCPClientProvider lets servers proxy other servers,
but true multi-agent (agent A spawning agent B, coordinating results) needs protocol-level
support. Nascent as of March 2026.

**Persistent session state:** FastMCP 3.1 has `ctx.set_state()` for within-session state.
Cross-session persistence still requires external tools (advanced-memory-mcp). Native
persistent agent state would be a significant unlock.

---

## Related Docs

- `research/agentic-ide/INFLECTION_2026.md` — the historical analysis
- `fastmcp/code-mode.md` — CodeMode full reference  
- `integrations/claude-desktop/README.md`
- `integrations/cursor-ide/README.md`
- `integrations/antigravity-ide/README.md`
- `standards/HOST_APP_LIFECYCLE.md` — for host-app-dependent servers
