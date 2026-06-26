# FastMCP 3.1 Features Guide

**Status:** Active  
**Applies to:** `fastmcp>=3.1.0`  
**Last updated:** 2026-03-15  
**Supersedes:** FASTMCP_3.1.1+_FEATURES_GUIDE.md (outdated; do not use for new development)

---

## 1. Scope and version

- **Fleet standard:** `fastmcp>=3.1.0`. All new MCP servers and existing fleet alignment target 3.1.
- **Package:** PyPI `fastmcp`; repo: [PrefectHQ/fastmcp](https://github.com/PrefectHQ/fastmcp). Do not use `from mcp.server.fastmcp import FastMCP` (Anthropic frozen 1.0); use `from fastmcp import FastMCP`.
- **3.1 is additive over 3.0:** No new breaking changes. Upgrading from 3.0 is a version bump and optional adoption of new features.
- **Coming from 2.x:** You must migrate 2.x â†’ 3.0 first (see [Upgrading from FastMCP 2](https://gofastmcp.com/development/upgrade-guide)), then 3.0 â†’ 3.1 (this guide and `fastmcp/3.0-to-3.1-improvements.md`).

---

## 2. FastMCP 3.0 foundation (relevant to 3.1)

These are 3.0 behaviors that 3.1 builds on. Servers must comply with 3.0 before adding 3.1 features.

### 2.1 Server construction and transport

- **Constructor:** `FastMCP(name, ...)` â€” identity and behavior only. No `host`, `port`, `sse_path`, etc. in the constructor; those are passed to `run()`, `run_http_async()`, or `http_app()`.
- **Running:**
  - Stdio: `mcp.run()` or `run_stdio_async()` (replaces deprecated `run_standalone()`).
  - HTTP: Use `mcp.http_app(transport=...)` to get an ASGI app; mount it in your FastAPI/Starlette app (e.g. at `/mcp`). Do not treat the FastMCP instance as the main FastAPI app (no `@app.get` on the MCP object).
- **Single-backend pattern:** One FastAPI app for custom routes (e.g. `/health`); mount the MCP HTTP app from `mcp.http_app()` at a fixed path (e.g. `/mcp`).

### 2.2 Context and state

- **`Context` injection:** Tools receive `ctx: Context` by type annotation (conventional name `ctx`). Use it for sampling and state, not `mcp.ctx` or `app.state`.
- **State is async:** `await ctx.set_state(key, value)` and `value = await ctx.get_state(key)`. State is session-scoped and JSON-serializable by default; use `serializable=False` for request-scoped non-serializable values.
- **Mounted servers:** Each FastMCP instance has its own state store. For shared serializable state across mounts, pass the same `session_state_store` to both.

### 2.3 Sampling (LLM callbacks)

- **Only supported API:** `ctx.sample(...)`. `ctx.session.create_message()` is removed.
- **Usage:** `result = await ctx.sample(messages=..., tools=[...], result_type=...)`. Pass plain Python callables (or tool definitions) for `tools`; do not pass dict mocks.
- **Context parameter:** Always use a parameter named `ctx` typed as `Context` so FastMCP injects the session context.

### 2.4 Visibility and listing

- **Component control:** Use server-level `mcp.enable()` / `mcp.disable()` (by names, tags, or components). Do not call `.enable()`/`.disable()` on component objects (raises `NotImplementedError`).
- **Listing:** Use `list_tools()`, `list_resources()`, `list_prompts()`, `list_resource_templates()` â€” they return lists, not dicts.

### 2.5 Naming and deprecations (3.0)

- `mount(subserver, prefix="x")` â†’ `mount(subserver, namespace="x")`.
- `add_tool_transformation(...)` â†’ `add_transform(ToolTransform(...))`.
- `FastMCP.as_proxy(url)` â†’ `create_proxy(url)` from `fastmcp.server`.
- Prompts return `Message` or `list[Message]` (from `fastmcp.prompts`), not raw dicts or `mcp.types.PromptMessage`.

### 2.6 Security and storage (3.0)

- **OAuth storage:** Default client storage is no longer DiskStore (CVE-2025-69872). Use FileTreeStore or pass explicit `client_storage`. Existing clients re-register on first connection after upgrade.
- **Auth:** Auth providers no longer auto-load from env; pass `client_id`, `client_secret` (e.g. from `os.environ`) explicitly.

---

## 3. FastMCP 3.1 features (additive)

### 3.1 Server-side prompts (`@mcp.prompt`)

**Purpose:** Reusable, parameterized message templates. Clients call `prompts/get` with a name and arguments; the server returns one or more messages to inject into the conversation (e.g. system or user context).

**Definition:**

```python
from fastmcp import FastMCP
from fastmcp.prompts import Message

mcp = FastMCP("MyServer")

@mcp.prompt(
    name="expert_mode",
    description="Load expert-mode instructions for this server's tools.",
    tags={"guidance", "expert"},
)
def expert_mode(domain: str = "general") -> str:
    """Return guidance for working with this server in expert mode."""
    base = "You are working with MyServer tools. Use tool_x for X, tool_y for Y."
    if domain == "sql":
        return base + "\n\nPrefer parameterized queries."
    return base
```

**Return types:**

- `str` â€” single user message.
- `list[Message]` or `list[Message | str]` â€” multi-turn; strings become user messages.
- `PromptResult` â€” full control (messages, description, meta).

**Decorator options:** `name`, `description`, `tags`, `meta`, `version`. Name defaults to function name; description to docstring.

**Argument types:** MCP passes string arguments; FastMCP can accept typed parameters (e.g. `list[int]`, `dict[str, str]`, `float`) and documents JSON string format in the schema. Keep types simple for reliable coercion.

**Context in prompts:** Add `ctx: Context` to the signature to access request/session info (e.g. `ctx.request_id`).

**Async prompts:** Both `def` and `async def` are supported; async is preferred when the prompt does I/O.

**Visibility:** Use `mcp.disable(keys={"prompt:expert_mode"})` or tag-based `mcp.enable(tags={"public"}, only=True)` to control which prompts are listed.

**Duplicate behavior:** `on_duplicate` (e.g. `on_duplicate="error"`) at server init controls duplicate prompt names (ignore, replace, error, warn).

**References:** [Prompts](https://gofastmcp.com/servers/prompts), [Getting Prompts (client)](https://gofastmcp.com/clients/prompts.md).

---

### 3.2 Skills provider

**Purpose:** Expose skill directories (e.g. folders with `SKILL.md`) as MCP **resources** under the `skill://` URI scheme. Clients list and read these like any resource; format aligns with Claude/Cursor/VS Code skill directories.

**Structure:**

- Each skill = directory with a main file (default `SKILL.md`) and optional supporting files.
- YAML frontmatter in the main file can supply description and metadata.

**Bundled skills (in your package):**

```python
from pathlib import Path
from fastmcp import FastMCP
from fastmcp.server.providers.skills import SkillsDirectoryProvider

mcp = FastMCP("MyServer")
skills_dir = Path(__file__).resolve().parent / "skills"
if skills_dir.is_dir():
    mcp.add_provider(SkillsDirectoryProvider(roots=[skills_dir]))
```

**Vendor providers (userâ€™s installed skills):**

```python
from fastmcp.server.providers.skills import (
    ClaudeSkillsProvider,   # ~/.claude/skills/
    CursorSkillsProvider,   # ~/.cursor/skills/
    WindsurfSkillsProvider,
    VSCodeSkillsProvider,   # ~/.copilot/skills/
    CodexSkillsProvider,
    GeminiSkillsProvider,
    GooseSkillsProvider,
    CopilotSkillsProvider,
    OpenCodeSkillsProvider,
)
mcp.add_provider(ClaudeSkillsProvider())
```

**Resource URIs:**

- Main file: `skill://<skill-name>/SKILL.md`
- Manifest (file list, sizes, hashes): `skill://<skill-name>/_manifest`
- Supporting files: `skill://<skill-name>/<path>`

**Options:**

- `supporting_files="template"` (default): Supporting files are discoverable via manifest; not all listed as top-level resources.
- `supporting_files="resources"`: Every file appears in `list_resources()`.
- `reload=True`: Re-scan directory on each request (development only; avoid in production).

**Client utilities:** `fastmcp.utilities.skills`: `list_skills()`, `download_skill()`, `sync_skills()`, `get_skill_manifest()`.

**References:** [Skills Provider](https://gofastmcp.com/servers/providers/skills).

---

### 3.3 OpenAPI provider

**Purpose:** Generate MCP tools from an OpenAPI 3.x or Swagger 2.0 spec. One provider call can expose many REST endpoints as tools.

**Basic usage:**

```python
from fastmcp import FastMCP
from fastmcp.server.providers.openapi import OpenAPIProvider

mcp = FastMCP("MyAPI")
mcp.add_provider(
    OpenAPIProvider(
        spec="https://api.example.com/openapi.json",  # URL or path
        base_url="https://api.example.com",
        headers={"Authorization": "Bearer <token>"},
    )
)
```

**With filtering:**

- `include_tags`, `exclude_tags` â€” by OpenAPI tags.
- `include_paths`, `exclude_paths` â€” path prefix inclusion/exclusion.
- `include_methods`, `exclude_methods` â€” HTTP methods.

**Timeout:** Not on the provider. Configure `httpx.AsyncClient(timeout=...)` and pass that client if you need a custom timeout; otherwise a default client is used (e.g. 30s).

**Tool names:** From `operationId` when present; otherwise derived from method + path (e.g. `get_users_id`, `post_projects`).

**References:** [OpenAPI ðŸ¤ FastMCP](https://gofastmcp.com/integrations/openapi.md), [OpenAPIProvider](https://gofastmcp.com/servers/providers/openapi).

---

### 3.4 Streaming sampling (`ctx.sample_stream`)

**Purpose:** Stream LLM response chunks inside a tool instead of waiting for the full response.

**Usage:**

```python
@mcp.tool
async def stream_analysis(data: str, ctx: Context) -> str:
    """Analyze data and stream the reasoning back."""
    chunks = []
    async for chunk in ctx.sample_stream(
        f"Analyze this step by step: {data}",
        max_tokens=2000,
    ):
        chunks.append(chunk.text)
    return "".join(chunks)
```

**When to use:** Long responses, progress reporting, or incremental processing. For most tools, `ctx.sample()` remains the default.

---

### 3.5 Improved `fastmcp discover`

**Purpose:** List MCP servers configured in supported clients (Claude Desktop, Cursor, Windsurf, etc.) with status and detail.

**Usage:**

```powershell
fastmcp discover --client claude
fastmcp discover --client cursor
fastmcp discover
```

**JSON output (scripting / fleet audit):**

```powershell
fastmcp discover --client claude --json
```

Use this to audit tool counts, transport types, and server paths/versions across the fleet.

---

## 4. Server construction checklist (3.1)

- [ ] Dependency: `fastmcp>=3.1.0` in `pyproject.toml` (no upper bound unless required).
- [ ] Import: `from fastmcp import FastMCP` (never `from mcp.server.fastmcp`).
- [ ] No transport/host/port in `FastMCP()`; pass them to `run()` or use `http_app()` and mount in your web app.
- [ ] HTTP: Single FastAPI (or Starlette) app; mount `mcp.http_app()` at a path (e.g. `/mcp`); no `@app.get` on the MCP instance.
- [ ] State: `await ctx.set_state()` / `await ctx.get_state()` in tools.
- [ ] Sampling: `ctx.sample()` (and optionally `ctx.sample_stream()`); no `ctx.session.create_message()`.
- [ ] Mount: `mount(subserver, namespace="...")` (not `prefix=`).
- [ ] Prompts: Return `Message` or `list[Message]` (or `PromptResult`); not raw dicts.
- [ ] Optional 3.1: Add `@mcp.prompt`, `SkillsDirectoryProvider` or vendor skills provider, `OpenAPIProvider`, as needed.

---

## 5. Optional dependencies

- **Background tasks (SEP-1686):** `pip install "fastmcp[tasks]"` if you use `task=True` or `TaskConfig`.
- **OAuth DiskStore (not recommended):** `pip install 'py-key-value-aio[disk]'` only if you must keep DiskStore (diskcache CVE applies).

---

## 6. Compatibility and escape hatches

- **Decorator return value:** In 3.0+, decorators return the original function. Code that expects a component object (e.g. `.name`, `.description`) can set `FASTMCP_DECORATOR_MODE=object` for v2-style behavior (deprecated).
- **Metadata key:** Component `meta` uses the `"fastmcp"` key (not `"_fastmcp"`).
- **Banner:** `FASTMCP_SHOW_SERVER_BANNER` (replaces `FASTMCP_SHOW_CLI_BANNER`).

---

## 7. References

| Topic | Link |
|-------|------|
| Upgrade from 2 | https://gofastmcp.com/development/upgrade-guide |
| Prompts | https://gofastmcp.com/servers/prompts |
| Skills provider | https://gofastmcp.com/servers/providers/skills |
| OpenAPI | https://gofastmcp.com/integrations/openapi.md |
| Changelog | https://gofastmcp.com/changelog |
| GitHub | https://github.com/PrefectHQ/fastmcp |
| PyPI | https://pypi.org/project/fastmcp/ |

**In this repo:**

- `fastmcp/3.1-features.md` â€” Short 3.1 summary (prompts + skills).
- `fastmcp/3.0-to-3.1-improvements.md` â€” 3.0 â†’ 3.1 upgrade and examples.
- `standards/HISTORY_OF_FASTMCP.md` â€” Version history and breaking changes.
- `standards/FASTMCP3_UPGRADE_STRATEGY.md` â€” Fleet upgrade plan.
- `docs/operations/FASTMCP_3.1_ALIGNMENT.md` â€” Full alignment rules (backend, frontend, docs).
- `patterns/FASTMCP_SAMPLING_ANTIPATTERNS.md` â€” Sampling pitfalls (3.1.1+.1+; still relevant for 3.1).

---

**Last updated:** 2026-03-15  
**Owner:** mcp-central-docs

