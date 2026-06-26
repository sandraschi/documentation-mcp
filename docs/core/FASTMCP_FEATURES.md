# FastMCP 3+ Features — Fleet Standard

**Status:** Active
**Audience:** All fleet MCP server repos
**Purpose:** Reference for which FastMCP 3.x features exist and how to use them. Every fleet repo should have a copy of this or link to it.

---

## Quick Reference

| Feature | FastMCP version | Our usage |
|---------|----------------|-----------|
| Dual transport (stdio + HTTP) | 3.0+ | `--stdio` / `--serve`, `http_app` mount in FastAPI |
| Portmanteau tools | 3.2+ | Consolidated operations with `operation` param |
| Skills (bundled docs) | 3.1+ | `SkillsDirectoryProvider` |
| Prefab / MCP Apps | 3.1+ | `@mcp.tool(app=True)` + `prefab-ui` components |
| Prompts | 3.1+ | `@mcp.prompt()` with typed params |
| Context injection | 3.2+ | `ctx: Context = None` for sampling + logging |
| Sampling | 3.1+ | `ctx.sample()` for LLM generation inside tools |
| Lifecycle | 3.0+ | `@lifespan` for async setup/teardown |
| http_app (ASGI mount) | 3.0+ | Mount MCP inside FastAPI alongside REST routes |
| Conversational returns | 3.2+ | Typed dicts with `success`, `message`, `data` |
| Pydantic v2 | 3.2+ | `Annotated[T, Field(...)]`, `model.model_dump()` |
| CodeMode (experimental) | 3.1+ | BM25 keyword search over tools+prompts |
| Safety boundary wrapping | fleet pattern | `wrap_untrusted()` on all external text |

---

## 1. Dual Transport

Every fleet server should support both transports:

```python
# __main__.py
import sys
from arxiv_mcp.server import mcp

if "--stdio" in sys.argv:
    mcp.run(transport="stdio")
else:
    mcp.run()  # defaults to streamable HTTP
```

Or via the ASGI mount pattern for combined REST+MCP processes:

```python
# app.py
from my_mcp_server import mcp

mcp_http = mcp.http_app(path="/mcp")
app = FastAPI()
app.mount("/mcp", mcp_http)
```

**Discovery endpoint:** `GET /.well-known/mcp/manifest.json` should list both transports.

---

## 2. Portmanteau Tools

Consolidate related operations into a single tool to reduce context token usage:

```python
@app.tool()
async def tasks(
    operation: Annotated[Literal["list", "get", "create", "update", "delete"], Field(description="Operation to perform.")],
    task_id: Annotated[str | None, Field(description="Required for get/update/delete.")] = None,
    title: Annotated[str | None, Field(description="Required for create/update.")] = None,
) -> dict:
    """Unified task management tool.

    ## Return Format
    {"success": bool, "message": str, "data": dict | list}
    """
    match operation:
        case "list": ...
        case "get": ...
        case "create": ...
        case "update": ...
        case "delete": ...
```

---

## 3. Skills (Bundled Agent Guidance)

Skills are markdown documents injected into the LLM's context. They survive context resets unlike system instructions.

```python
from fastmcp.server.providers.skills import SkillsDirectoryProvider

skills_dir = Path(__file__).resolve().parent / "skills"
if skills_dir.is_dir():
    mcp.add_provider(SkillsDirectoryProvider(roots=[skills_dir]))
```

Skills directory structure:
```
skills/my-skill/
  SKILL.md          # loaded via skill://my-skill
  reference.md      # sub-docs, not auto-loaded
  scripts/
    example.py
```

---

## 4. Prefab / MCP Apps

Rich UI rendering inside chat via `prefab-ui` components:

```python
from prefab_ui.app import PrefabApp
from prefab_ui.components import Card, CardContent, CardHeader, CardTitle, Markdown, Badge

@mcp.tool(app=True)
async def show_card(item_id: str) -> PrefabApp:
    ...
    with Card() as view:
        with CardHeader():
            CardTitle("Title")
        with CardContent():
            Markdown("Body text")
    return PrefabApp(view=view, title="Card Title")
```

Make this an optional extra:
```toml
[project.optional-dependencies]
apps = ["prefab-ui>=0.14.0"]
```

Guard the registration:
```python
try:
    from my_tools.prefab import register_prefab_tools
    register_prefab_tools(mcp)
except Exception:
    pass
```

---

## 5. Prompts

Structured prompt templates that guide agent workflows:

```python
@mcp.prompt()
async def analysis_prompt(
    mode: Literal["quick", "deep"] = "quick",
    paper_id: str | None = None,
) -> str:
    """Template description. Tags: keyword1, keyword2"""
    text = "You are an analyst..."
    if paper_id:
        text += f"\nFocus: {paper_id}"
    return text + MODES[mode]
```

---

## 6. Context Injection + Sampling

```python
from fastmcp import Context

@mcp.tool()
async def my_tool(query: str, ctx: Context) -> dict:
    await ctx.info(f"Processing: {query}")
    result = await ctx.sample(
        messages=[{"role": "user", "content": query}],
        system_prompt="Be concise.",
        max_tokens=500,
    )
    return {"result": result.text}
```

---

## 7. Conversational Returns

Always return consistent dict shapes:

```python
# Success
{"success": True, "message": "Found 12 papers.", "papers": [...]}

# Error (structured)
{"success": False, "error": str(e), "error_type": type(e).__name__,
 "recovery_options": ["Retry after a delay.", "Check input."]}
```

---

## 8. Safety Boundary Wrapping

Mandatory for any server that ingests external text. See `mcp-central-docs/standards/PROMPT_INJECTION_HARDENING.md`.

Two layers:
1. **Zero-width Unicode strip** — service layer, never skip
2. **`wrap_untrusted(text, source)`** — MCP tool boundary, wraps every external string with a safety preamble telling the LLM it's data, not instructions

Applied at every ingest point: arXiv titles/abstracts, RSS feed items, blog posts, email, Discord messages, DOI metadata, PDF text.

**Does NOT apply to REST API responses** (human-facing UIs).

---

## 9. Lifecycle Management

```python
from fastmcp.server.lifespan import lifespan

@lifespan
async def my_lifespan(server):
    db = await init_db()
    yield {"db": db}
    await db.close()
```

---

## 10. Pydantic v2 Patterns

```python
from typing import Annotated
from pydantic import Field

@app.tool()
async def search(
    query: Annotated[str, Field(description="Search query.")],
    limit: Annotated[int, Field(ge=1, le=100)] = 10,
) -> dict:
    """Search tool.

    ## Return Format
    {"success": bool, "results": list}
    """
```

---

## Reference implementations

| Feature | Best example repo |
|---------|------------------|
| Full dual transport + REST | `arxiv-mcp` |
| Portmanteau tools | `robofang-mcp` |
| Prefab cards | `arxiv-mcp`, `aiwatcher-mcp` |
| Safety wrapping | `arxiv-mcp` (`sanitize.py`) |
| Prompts + Skills | `arxiv-mcp` (10 prompts, 1 skill) |
| Sampling | `arxiv-mcp` (`arxiv_agentic_assist`) |
