# Tool Design & Implementation (SOTA)

## 1. The Portmanteau Evolution (2026 SOTA)

To prevent "Tool Explosion" while maintaining "Searchability," the fleet has moved from **Manual Dispatchers** (Switch-Case) to **Projected Atomic Tools** (Namespacing).

- **Legacy Portmanteau**: A single tool function with an `operation` enum. (Deprecated for new work).
- **SOTA Portmanteau (Projected)**: Atomic tools grouped via FastMCP namespacing (e.g., `mount(namespace="adn_knowledge")`).
- **Industrial Portmanteau (2026 Improved)**: A high-density switch-case tool using **Strict Discriminated Unions** and **Rationale-First Docstrings**.
- **Rationale**: While "Projected" tools are preferred for searchability, "Industrial" portmanteaus are MANDATORY for servers exceeding 50+ tools in environments with strict registry limits (Antigravity/Cursor 100-tool cap).

### 1.1 The Transform Rule
For existing legacy portmanteaus, use **FastMCP Transforms** to project individual operations as atomic tools to the host. This provides the best of both worlds: centralized logic and transparent discovery.

### 1.2 The Industrial Portmanteau Standard
To satisfy static analyzers (ToolBench/Arcade) and LLM planners, the Industrial Portmanteau must follow these 4 pillars:

1.  **Strict Discriminated Unions**: Use `Annotated[Union[...], Field(discriminator="operation")]` in the Pydantic models. This ensures the analyzer sees mutually exclusive schemas instead of a "parameter blob."
2.  **Rationale-First Docstrings**: The docstring MUST begin with a `[RATIONALE]` section explaining the architectural choice for consolidation. This primes the model to treat the tool as a multi-functional controller.
3.  **Operation Mapping**: Every sub-task MUST be explicitly listed with a 1-line description and its required parameters.
4.  **High-Fidelity Examples**: Provide 1-3 Python call examples that ground the analyzer in the combined `operation + parameters` pattern.

### 2.1 The Docstring Template
Every SOTA tool MUST follow the **[Docstring SOTA Rules](./rules/docstrings_sota.md)**:
1.  **Summary**: One-line description.
2.  **Rationale**: (For Industrial Portmanteaus) The "why" behind the tool.
3.  **Vanishing Args**: All parameter docs move to `Annotated[T, Field(description="...")]`.
4.  **## Return Format**: Mandatory JSON schema description.
5.  **## Examples**: 1-3 high-fidelity Python calls.
6.  **Notes / Errors**: Use " - " bullets for prerequisites and recovery tips.

### 2.2. Args Section Formatting
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

## 3. Return Value Standards

### 3.1. The Return Rule
**All tools MUST return a value that can be represented as a string**. 
- Never return raw Pydantic models or complex objects directly.
- SOTA servers return a standard dictionary with `success`, `action`, `result`, and `error` keys.
- If an underlying library returns an object, format it as a Markdown string before returning.

### 3.2. Traceability
Include a `success` boolean and optional `suggestions` on failure to guide the agent toward recovery.

### 3.3. MCP Apps and `ToolResult` (Prefab / in-chat rich UI)

**Dependency:** **`prefab-ui>=0.14.0`** is a **core** dependency for fleet **`*-mcp`** servers ([SOTA §2.2](./SOTA_REQUIREMENTS.md)).

**Coverage rule:** For tools that primarily **list** items, report **status** / **health**, show **stats** or **dashboards**, or return **tabular** / **multi-section** structured data, you **MUST** provide a Prefab App presentation (dedicated **`@mcp.tool(app=True)`** or **`ToolResult`** with **`PrefabApp`**) in addition to any plain dict/JSON tool — see **[MCP Apps & Prefab UI](../fastmcp/mcp-apps-prefab-ui.md)** §3. **Exceptions** require an explicit **PRD** note.

For **in-conversation** rich UI (cards, images, tables) via FastMCP **MCP Apps**, tools return **`ToolResult`** with **`structured_content=PrefabApp(...)`** where applicable. Requirements:

- **Always** set **`content`** to a readable string summary for hosts that do not render Apps.
- **`@mcp.tool(app=True)`** where the tool is App-first; follow HTML/plain-text handling — **no raw HTML** in **`Text`** without stripping.

Dict/JSON tools remain valid for **thin** responses; list/status-class surfaces **add** Prefab per §3 and the §4 table **Prefab** row.

---

## 4. Agentic tool quality (fleet + external benchmarks)

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
| **Destructive / high-impact ops** | Deletes, overwrites, sends, money-like, or irreversible actions require **explicit agent-visible guardrails**: `confirm=True`, separate dry-run/preview, or a two-step pattern — documented in Args. | Set MCP **`destructiveHint`** / **`readOnlyHint`** (§8) so hosts can reason about risk. |
| **Naming** | One **verb-led** `snake_case` name per tool; portmanteau name matches domain (`resolve_timeline`, not `do_stuff`). | Same casing and verb patterns across a server (`list_*`, `get_*`, `set_*`). |
| **MCP tool annotations** | — | Every tool sets **`annotations=`** on `@mcp.tool()` (§8) with accurate **read-only vs mutating** hints. |
| **Prefab (list / status / stats)** | Tools in §3.3 **coverage rule** ship a **Prefab App** surface (`ToolResult` + `PrefabApp` or `app=True` tool); **`prefab-ui`** in core deps ([SOTA §2.2](./SOTA_REQUIREMENTS.md)). | Card/table layout matches the dict tool’s fields; document both in skills / `llms-full.txt`. |

---

## 5. Pagination — how it works for MCP tools

**Problem:** A single tool call that returns an unbounded list (emails, files, rows, log lines) can **fill the model context**, slow the host, and hide the fact that more data exists. Benchmarks flag “no pagination guidance” when neither the **schema** nor the **docstring** explains how to pull the next chunk.

**Rule:** If the result set can grow without a fixed small bound, the tool **MUST** implement **one** of the following patterns and document it under **Args** and **Returns**.

### 5.1. Limit + offset (simple)

- Parameters: e.g. `limit: int = 50`, `offset: int = 0`.
- Enforce: `1 <= limit <= max_page` (e.g. `max_page` 100–500 depending on row size).
- Response: include **`has_more: bool`** and optionally **`total`** if cheap to compute; return **`items`** (or your standard key) as only the current page.

### 5.2. Cursor / page token (preferred for large or live data)

- Parameters: e.g. `limit: int = 50`, `cursor: str | None = None` (opaque token from a previous response).
- Response: include **`next_cursor: str | None`** (or `next_page_token`) and **`has_more: bool`**.
- The docstring MUST say: “Pass `cursor` from the previous response to get the next page.”

### 5.3. What does *not* need pagination

- A **single object** by id, fixed small structs, or **bounded** outputs (e.g. “status”, “health”, “counts under 20 fields”) — state that the result is **bounded** in the docstring so evaluators do not flag it.

### 5.4. Docstring contract

For paginated tools, **Returns** MUST mention: default `limit`, max allowed, which keys carry **`items`**, **`has_more`**, and how to obtain the **next** page (`offset` or `cursor`).

---

## 6. Structured errors and recovery (agent-visible)

Align tool failures with [error-handling.md](./error-handling.md).

- On failure, return a dict that includes at least **`success: False`** and **`error`** (string the agent can read).
- **SHOULD** include **`suggestions`** or **`recovery_options`** (list of strings), and when useful **`error_type`**, **`diagnostic_info`** (non-secret).
- For HTTP-backed services, map status codes into **clear messages**; do not return empty bodies for 4xx/5xx without translating into `error` + recovery text.

This addresses “no error handling guidance” in external reviews: the **model** must see what to do next, not only that something failed.

---

## 7. Output schema (documentation + optional MCP schema)

- **Docstring (MUST):** §2 **Returns** documents the success dict shape: keys, types, and nested structure of `result`.
- **MCP schema (SHOULD):** FastMCP 3.1+ supports `@mcp.tool(..., output_schema={...})` — use it when the success payload is stable so clients and benchmarks see a **machine-readable** output shape.
- Keep §3.1: values must remain JSON-serializable / stringifiable; do not leak raw non-JSON objects.

---

## 8. MCP `ToolAnnotations` (FastMCP)

MCP defines optional **tool [annotations](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)** (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`). Hosts use them as **hints** for planning and risk display — not as a security boundary (see spec: clients must treat annotations as untrusted unless the server is trusted).

Fleet servers **SHOULD** pass **`annotations=`** on every `@mcp.tool()` using `mcp.types.ToolAnnotations`:

```python
from mcp.types import ToolAnnotations

@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
async def list_items(...) -> dict:
    ...
```

**Guidance:**

- **`readOnlyHint=True`**: tool does not mutate persistent state (queries, list, get status).
- **`destructiveHint=True`**: tool may delete, overwrite, or otherwise irreversibly change data (only meaningful when not read-only).
- **`idempotentHint`**: repeated calls with the same arguments do not compound damage (safe retries).

---

## 9. Implementation honesty (no fake green)

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

## 9. External references (non-normative)

- [ToolBench methodology](https://toolbench.arcade.dev/methodology) — how third-party scoring weights definition quality, protocol, supportability.
- [Arcade patterns](https://arcade.dev/patterns) — detailed pattern pages (paginated result, recovery guide, constrained input, etc.).
