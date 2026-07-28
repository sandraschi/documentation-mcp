# Tool Design & Implementation (SOTA)

## 1. The Portmanteau Pattern (2026 SOTA)

To prevent "Tool Explosion" while maintaining discoverability, the fleet standard is the **Industrial Portmanteau**: a single tool function with an `operation` enum discriminator. This is mandatory for servers exceeding ~20 tools where a flat tool list would overwhelm agent context.

- **Pattern**: One `@mcp.tool()` function per domain, with `operation: Literal["op1", "op2", ...]` as the first parameter.
- **Rationale**: Portmanteaus stay within IDE/registry tool limits (Cursor 100-tool cap) while keeping related operations grouped.
- **Discovery**: The operation enum serves as a built-in catalog — agents see all valid operations in the schema.

### 1.0 No "planned" stubs (HARD — new-repo gate)

Every operation listed in the portmanteau schema, README, or `docs/TOOLS.md` MUST be implemented before the repo is called done.

| Forbidden | Required |
|-----------|----------|
| `planned: true` / "stubbed in v0.x" returns | Real behavior for every advertised op |
| README section titled "MCP tools (planned)" | Document **implemented** ops only |
| Empty `NotImplementedError` for listed ops | Dry-run short-circuit is OK when credentials absent |

Webhooks: if the product has inbound events or the host API supports webhooks, ship receive/list (and create/delete when applicable) in the same pass — do not defer to "v0.2".

### 1.1 The Transform Rule
For existing legacy portmanteaus, use **FastMCP Transforms** to project individual operations as atomic tools to the host. This provides the best of both worlds: centralized logic and transparent discovery.

### 1.2 The Industrial Portmanteau Standard
To satisfy static analyzers (ToolBench/Arcade) and LLM planners, the Industrial Portmanteau must follow these 4 pillars:

1.  **Strict Discriminated Unions**: Use `Annotated[Union[...], Field(discriminator="operation")]` in the Pydantic models. This ensures the analyzer sees mutually exclusive schemas instead of a "parameter blob."
2.  **Rationale-First Docstrings**: The docstring MUST begin with a `[RATIONALE]` section explaining the architectural choice for consolidation. This primes the model to treat the tool as a multi-functional controller.
3.  **Operation Mapping**: Every sub-task MUST be explicitly listed with a 1-line description and its required parameters.
4.  **High-Fidelity Examples**: Provide 1-3 Python call examples that ground the analyzer in the combined `operation + parameters` pattern.

## 2. FastMCP 3.4+ Features Relevant to Tool Design

Every tool implementation should leverage or be aware of these FastMCP 3.4 capabilities:

### 2.1. Sampling (`ctx.sample()`)
Tools can use `ctx.sample()` to call back to the connected LLM for autonomous reasoning, multi-step planning, or content generation within a tool. See [SOTA_REQUIREMENTS.md §2.1](./SOTA_REQUIREMENTS.md) and [FASTMCP_FEATURES.md](./FASTMCP_FEATURES.md).

```python
@mcp.tool()
async def analyze(query: str, ctx: Context) -> dict:
    result = await ctx.sample(f"Analyze: {query}")
    return {"success": True, "data": result}
```

### 2.2. Prompts (`@mcp.prompt()`)
Register reusable prompt templates that clients can fetch and inject into conversations. Use for contextual instructions, system prompts, or guided workflows.

```python
@mcp.prompt()
def database_help(topic: str) -> str:
    return f"Help on {topic}..."
```

### 2.3. SkillsProvider
FastMCP 3.4 supports `SkillsDirectoryProvider` / `ClaudeSkillsProvider` / `CursorSkillsProvider` for exposing skill directories as `skill://` resources. Configure via `mcp_config.py`.

### 2.4. MCPB Bundling
For Claude Desktop distribution, tools are packaged as `.mcpb` bundles. The bundle includes `src/`, `manifest.json`, `assets/icon.png`, and `assets/prompts/`. The `mcpb pack` output goes to `dist/{name}-v{version}.mcpb`. See **[MCPB_PACKAGING_STANDARDS.md](./MCPB_PACKAGING_STANDARDS.md)** for full layout, `.mcpbignore` rules, and what must be included/excluded.

### 2.4. Prefab UI / MCP Apps ($3.3)
Rich in-chat UI via `@mcp.tool(app=True)` and `ToolResult` with `PrefabApp` — see §3.3 below and [MCP Apps & Prefab UI](../fastmcp/mcp-apps-prefab-ui.md).

### 2.5. Resources (`@mcp.resource()`)
Dynamic data streams exposed via `resource://` URIs. Useful for live status, streaming logs, or file contents.

### 2.6. Tool Annotations (READ_ONLY / MUTATING / DESTRUCTIVE)
See §9 below.

## 3. Docstring Standards

### 3.1 The Docstring Template
Every SOTA tool MUST follow the **[Docstring SOTA Rules](./rules/docstrings_sota.md)**:
1.  **Summary**: One-line description.
2.  **Rationale**: (For Industrial Portmanteaus) The "why" behind the tool.
3.  **Vanishing Args**: All parameter docs move to `Annotated[T, Field(description="...")]`.
4.  **## Return Format**: Mandatory JSON schema description.
5.  **## Examples**: 1-3 high-fidelity Python calls.
6.  **Notes / Errors**: Use " - " bullets for prerequisites and recovery tips.

### 3.2. Args Section Formatting
The `Args` section is the "Schema Bridge." It must be formatted precisely:
- **One parameter per line**: No exceptions.
- **Explicit Type Hints**: Must match the code (e.g., `(str | None)`, `(list[str])`).
- **Required/Optional**: Explicitly state if a parameter is required for specific operations.

**Example**:
```python
Args:
    operation (Literal, required): The operation to perform. Must be one of: "list", "add", "remove".
    name (str | None): Target item name. Required for: add, remove operations.
```

## 4. Return Value Standards

### 4.1. The Return Rule
- Never return raw Pydantic models or complex objects directly.
- SOTA servers return a standard dictionary with `success`, `action`, `result`, and `error` keys.
- If an underlying library returns an object, format it as a Markdown string before returning.

### 4.2. Dialogic Returns & Conversational Style

Every tool SHOULD return a `message` key with a natural-language summary alongside structured `data`. This enables FastMCP's automatic conversational wrapping and gives the agent something to present to the user without rephrasing.

```python
{"success": True, "message": "Found 3 running MySQL connections.", "data": [...]}
```

On failure, include a `dialogic` metadata block with `suggestions` and `recovery_options` — see **[DIALOGIC_RETURNS.md](./DIALOGIC_RETURNS.md)** for the full standard.

### 4.3. Traceability
Include a `success` boolean and optional `suggestions` on failure to guide the agent toward recovery.

### 4.4. MCP Apps and `ToolResult` (Prefab / in-chat rich UI)

**Dependency:** **`prefab-ui>=0.14.0`** is a **core** dependency for fleet **`*-mcp`** servers ([SOTA §2.2](./SOTA_REQUIREMENTS.md)).

**Coverage rule:** For tools that primarily **list** items, report **status** / **health**, show **stats** or **dashboards**, or return **tabular** / **multi-section** structured data, you **MUST** provide a Prefab App presentation (dedicated **`@mcp.tool(app=True)`** or **`ToolResult`** with **`PrefabApp`**) in addition to any plain dict/JSON tool — see **[MCP Apps & Prefab UI](../fastmcp/mcp-apps-prefab-ui.md)** §3. **Exceptions** require an explicit **PRD** note.

For **in-conversation** rich UI (cards, images, tables) via FastMCP **MCP Apps**, tools return **`ToolResult`** with **`structured_content=PrefabApp(...)`** where applicable. Requirements:

- **Always** set **`content`** to a readable string summary for hosts that do not render Apps.
- **`@mcp.tool(app=True)`** where the tool is App-first; follow HTML/plain-text handling — **no raw HTML** in **`Text`** without stripping.

Dict/JSON tools remain valid for **thin** responses; list/status-class surfaces **add** Prefab per §3 and the §4 table **Prefab** row.

---

## 5. Agentic tool quality (fleet + external benchmarks)

**Purpose:** Tools are consumed by **LLM agents** with finite context and unreliable free-text inputs. This section codifies what external rubrics (e.g. [ToolBench](https://toolbench.arcade.dev/) / [Improve](https://toolbench.arcade.dev/improve)) and [Arcade Agentic Tool Patterns](https://arcade.dev/patterns) treat as quality signals. Third-party grades also weight **GitHub supportability** (stars, activity); **definition quality** is what we control in-repo.

**Glama scoring** is separate from ToolBench and grades purely on docstring quality. See [toolbench/GLAMA_SCORING.md](../toolbench/GLAMA_SCORING.md) for the full breakdown: 6 dimensions, grade thresholds (C ≥ 2.0 is the practical target), the C-target docstring template, and the F→C fix workflow. The key insight: **the minimum-scoring tool in a server pulls the whole server's grade down** (60% mean + 40% minimum weighting) — fix the worst tool first.

Fleet tools **MUST** satisfy §2–§3 and the **MUST** rows below. **SHOULD** rows are expected for new work and when touching existing tools.

| Topic | MUST | SHOULD |
| --- | --- | --- |
| **Descriptions** | Every tool has a **complete gold-standard docstring** (§2); sub-operations are listed for portmanteau tools. | First line matches the tool’s MCP `name`; avoid duplicate/conflicting `description=` vs docstring. |
| **Error handling guidance** | Failures return a **structured dict** with human-readable `error` (or equivalent) and **actionable** `suggestions` / `recovery_options` where applicable — see §6 and [error-handling.md](./error-handling.md). | Include `error_type` (short category) when it helps the model branch (e.g. `validation`, `auth`, `not_found`). |
| **Output shape** | **Returns** in the docstring lists **stable keys** and meaning of `result` (and nested fields). | Use FastMCP **`output_schema=`** on `@mcp.tool()` when the success shape is stable (helps hosts and benchmarks). |
| **Pagination** | Any tool that can return a **growing collection** (list/search/stream summary) implements **bounded** returns + continuation — §5. | Document default `limit` and max cap in Args + Returns. |
| **Parameter constraints** | `operation` / mode params use **`Literal[...]`** (or enums). Numeric bounds use types + validation. | Prefer constrained types over `str` for categories; document regex/format in the Arg line when `str` is unavoidable. |
| **Destructive / high-impact ops** | Deletes, overwrites, sends, money-like, or irreversible actions require **explicit agent-visible guardrails**: `confirm=True`, separate dry-run/preview, or a two-step pattern — documented in Args. | Set FastMCP annotation `DESTRUCTIVE` (§9) so hosts can reason about risk. |
| **Naming** | One **verb-led** `snake_case` name per tool; portmanteau name matches domain (`resolve_timeline`, not `do_stuff`). | Same casing and verb patterns across a server (`list_*`, `get_*`, `set_*`). |
| **FastMCP annotations** | — | Every tool sets **`annotations=`** on `@mcp.tool()` (§9) with accurate **`READ_ONLY` / `MUTATING` / `DESTRUCTIVE`** hints. |
| **Prefab (list / status / stats)** | Tools in §3.3 **coverage rule** ship a **Prefab App** surface (`ToolResult` + `PrefabApp` or `app=True` tool); **`prefab-ui`** in core deps ([SOTA §2.2](./SOTA_REQUIREMENTS.md)). | Card/table layout matches the dict tool’s fields; document both in skills / `llms-full.txt`. |

---

## 6. Pagination — how it works for MCP tools

**Problem:** A single tool call that returns an unbounded list (emails, files, rows, log lines) can **fill the model context**, slow the host, and hide the fact that more data exists. Benchmarks flag “no pagination guidance” when neither the **schema** nor the **docstring** explains how to pull the next chunk.

**Rule:** If the result set can grow without a fixed small bound, the tool **MUST** implement **one** of the following patterns and document it under **Args** and **Returns**.

### 6.1. Limit + offset (simple)

- Parameters: e.g. `limit: int = 50`, `offset: int = 0`.
- Enforce: `1 <= limit <= max_page` (e.g. `max_page` 100–500 depending on row size).
- Response: include **`has_more: bool`** and optionally **`total`** if cheap to compute; return **`items`** (or your standard key) as only the current page.

### 6.2. Cursor / page token (preferred for large or live data)

- Parameters: e.g. `limit: int = 50`, `cursor: str | None = None` (opaque token from a previous response).
- Response: include **`next_cursor: str | None`** (or `next_page_token`) and **`has_more: bool`**.
- The docstring MUST say: “Pass `cursor` from the previous response to get the next page.”

### 6.3. What does *not* need pagination

- A **single object** by id, fixed small structs, or **bounded** outputs (e.g. “status”, “health”, “counts under 20 fields”) — state that the result is **bounded** in the docstring so evaluators do not flag it.

### 6.4. Docstring contract

For paginated tools, **Returns** MUST mention: default `limit`, max allowed, which keys carry **`items`**, **`has_more`**, and how to obtain the **next** page (`offset` or `cursor`).

---

## 7. Structured errors and recovery (agent-visible)

Align tool failures with [error-handling.md](./error-handling.md).

- On failure, return a dict that includes at least **`success: False`** and **`error`** (string the agent can read).
- **SHOULD** include **`suggestions`** or **`recovery_options`** (list of strings), and when useful **`error_type`**, **`diagnostic_info`** (non-secret).
- For HTTP-backed services, map status codes into **clear messages**; do not return empty bodies for 4xx/5xx without translating into `error` + recovery text.

This addresses “no error handling guidance” in external reviews: the **model** must see what to do next, not only that something failed.

### 7.1 Server Hardening Patterns (MANDATORY for new servers)

These three patterns prevent silent crashes — discovered during filesystem-mcp postmortem (2026-07-06). Every fleet server MUST implement all three.

#### Pattern 1: No bare `except: pass` in startup/cleanup code

Any startup guard, cleanup function, or background task that uses `try/except` MUST log failures at minimum. Bare `pass` in an exception handler leaves zero breadcrumbs when the server later dies from the accumulated state.

```python
# WRONG — orphan cleanup fails silently, zombie processes accumulate
def _kill_orphaned():
    try:
        subprocess.run(["taskkill", "/F", "/PID", str(pid)], timeout=5)
    except Exception:
        pass  # NEVER

# CORRECT — failure is logged with traceback
def _kill_orphaned():
    try:
        subprocess.run(["taskkill", "/F", "/PID", str(pid)], timeout=5)
    except Exception:
        logger.warning("Failed to kill orphan PID %d", pid, exc_info=True)
```

#### Pattern 2: Module-import functions MUST raise, never `return False`

Functions that import tool modules, register providers, or initialize subsystems MUST crash the server on failure. A server running with half its tools unregistered is worse than a server that fails fast at startup.

```python
# WRONG — server starts with partial tool surface, no alarm
def _import_tools():
    try:
        importlib.import_module(".tools.foo", package=__name__)
        importlib.import_module(".tools.bar", package=__name__)
    except Exception as e:
        logger.error("Import failed: %s", e)
        return False  # NEVER — unchecked, server runs degraded

_tools_imported = _import_tools()  # result never checked

# CORRECT — server exits immediately with full traceback
def _import_tools():
    try:
        importlib.import_module(".tools.foo", package=__name__)
        importlib.import_module(".tools.bar", package=__name__)
    except ImportError as e:
        logger.warning("Optional dep missing: %s", e)  # non-fatal
    except Exception as e:
        logger.exception("Fatal import error: %s", e)
        raise  # kills the server — fix the import, don't ship degraded

_import_tools()  # raises on failure, no unchecked variable
```

#### Pattern 3: `_error_response()` auto-logging (one-line fleet fix)

Add `logger.exception()` inside your shared error response helper. Every tool caller that catches `Exception` and returns `_error_response(...)` automatically gets full traceback logging — no per-tool edits needed. This is the highest-leverage single change in any MCP server.

```python
# In your shared responses module (e.g. tools/utils.py)
def _error_response(error: str, error_type: str = "general", **kwargs) -> dict:
    """Auto-logging error response — traceback logged before returning to caller."""
    logger.exception("Tool error: %s [%s]", error, error_type)
    return {"success": False, "error": error, "error_type": error_type, ...}

# Every tool boundary now produces a traceback automatically:
# ports/file_ops.py
except Exception as e:
    return _error_response(str(e), "file_error")  # traceback auto-logged
```

**Rationale:** The `_error_response` helper is called from inside `except` blocks where `sys.exc_info()` has the active exception. `logger.exception()` captures the full stack. One line covers 50+ call sites across all tool files. No traceback is ever lost again.

---

## 8. Output schema (documentation + optional MCP schema)

- **Docstring (MUST):** §2 **Returns** documents the success dict shape: keys, types, and nested structure of `result`.
- **MCP schema (SHOULD):** FastMCP 3.4+ supports `@mcp.tool(..., output_schema={...})` — use it when the success payload is stable so clients and benchmarks see a **machine-readable** output shape.
- Keep §3.1: values must remain JSON-serializable / stringifiable; do not leak raw non-JSON objects.

---

## 9. MCP Tool Annotations (FastMCP 3.4+)

Every tool SHOULD set `annotations=` on `@mcp.tool()` to signal behavior to the agent.

### Current approach (works with all FastMCP 3.x)

```python
from fastmcp import FastMCP

_README_ONLY = {"readonly": True}
_MUTATING = {}

@mcp.tool(annotations=_README_ONLY)
async def list_items(...) -> dict:
    """..."""
```

### Future import (when the annotations module ships in fastmcp)

The `from fastmcp.tool.annotations import READ_ONLY, MUTATING, DESTRUCTIVE` import does not exist in the shipped 3.4.2 package. When it ships (expected soon), the pattern becomes:

```python
from fastmcp import FastMCP
from fastmcp.tool.annotations import READ_ONLY, MUTATING, DESTRUCTIVE

@mcp.tool(annotations=READ_ONLY)
async def list_items(...) -> dict:
    """..."""
```

The dict format and the constants format are semantically identical. Migration is mechanical (see `docs/fastmcp-annotations-upgrade.md`).

**Guidance:**

- **`READ_ONLY`** : tool does not mutate state (queries, list, get status).
- **`MUTATING`**: tool changes state but does not destroy (create, update, configure).
- **`DESTRUCTIVE`**: tool may delete, overwrite, or irreversibly change data.
- Annotations MUST match real behavior. If a tool both reads and writes, use `MUTATING` and document side effects in the docstring.

---

## 10. Implementation honesty (no fake green)

- Prototype-only placeholders are allowed only with explicit temporary marking.
- Pre-release and production code MUST NOT return simulated success or synthetic findings as real output.
- If a dependency (provider/model/integration) is missing, return explicit failure:
  - `success: False`
  - `error_type: "not_implemented"` (or equivalent)
  - clear `error` / `message`
  - actionable `suggestions` / `recovery_options`
- Webapp-backed operations MUST expose unavailable capability as visible **Under construction** state.
- Do not silently no-op when a requested action is unavailable.
- **`openWorldHint`**: tool reaches external networks/services (APIs, email, cloud) vs closed local-only state.

Annotations MUST match real behavior. If a tool both reads and writes, `readOnlyHint=False` and document side effects in the docstring.

---

## 11. External references (non-normative)

- [ToolBench methodology](https://toolbench.arcade.dev/methodology) — how third-party scoring weights definition quality, protocol, supportability.
- [Arcade patterns](https://arcade.dev/patterns) — detailed pattern pages (paginated result, recovery guide, constrained input, etc.).
