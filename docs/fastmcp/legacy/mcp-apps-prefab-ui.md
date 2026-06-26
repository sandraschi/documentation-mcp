# MCP Apps, Prefab UI, and FastMCP — Fleet Standard

**Last updated:** 2026-04-17  
**Audience:** Python MCP server authors (FastMCP 3.1+), fleet maintainers  
**Status:** Active — **Prefab is fleet-mandatory** for **list / status / stats**-class tools; see [SOTA §2.2](../standards/SOTA_REQUIREMENTS.md#22-mcp-apps-and-prefab-ui-fleet-mandatory)

This document defines how **MCP Apps** (rich tool surfaces) and **Prefab UI** (Python → structured UI for MCP clients) fit into the **MCP Central Docs** / **SOTA** stack, how to implement them with **FastMCP**, and operational lessons from production work (e.g. **calibre-mcp** book cards).

---

## 1. Concepts

### 1.1 MCP Apps

An **MCP App** is a structured UI payload attached to a tool result so a **capable MCP host** can render more than plain text — cards, layouts, images — **inside the conversation**. The wire format is defined by the MCP ecosystem; hosts that do not implement Apps still receive **text** (and often JSON) fallbacks.

### 1.2 Prefab UI (`prefab-ui`)

**Prefab** is a **Python DSL** that describes UI as data (components, layout). It ships as the **`prefab-ui`** package (PyPI). FastMCP integrates with it so tools can return a **`PrefabApp`** as **structured content** alongside human/model-facing **content** (summary string).

- **Not** a replacement for fleet **standalone webapps** (Vite + FastAPI on ports **10700–10800**). Prefab is **in-conversation** only.  
- **Comparison and boundaries:** [prefab-vs-webapps.md](./prefab-vs-webapps.md).

### 1.3 What the user sees

| Host | Typical experience |
|------|---------------------|
| **Claude Desktop** | Often the **reference** for MCP Apps / Prefab. Rich output may appear **inline** and/or in a **side panel / App surface** (layout varies by version) so users can **read structured output while continuing the conversation**. Some builds support **interactive** App surfaces (buttons, forms) — treat as **progressive enhancement**; see [use cases doc](./mcp-apps-prefab-use-cases-and-examples.md) §1. |
| **Cursor** | Support evolves; same tool may show **rich card** or **text only** depending on build and settings. |
| **Other IDEs / Antigravity** | Treat as **unknown** until verified; always ship a clear **text** `content` on `ToolResult`. |

### 1.4 When Prefab is worth it (not just a “gadget”)

Prefab is easy to use as a **demo** (“pretty book list in chat”). That still helps **onboarding**. **Sustained** value is when the card **replaces** opening another app, **merging** several tool results in your head, or **previewing** risky operations — e.g. **library stats**, **fleet member status**, **health**, **diffs**, **delete previews**.

**Rule of thumb, example ideas, Claude Desktop side/interaction notes:** **[mcp-apps-prefab-use-cases-and-examples.md](./mcp-apps-prefab-use-cases-and-examples.md)** (including **§3.8** questionnaires and **pre-scaffolding checklists**).

### 1.5 Client matrix — recheck weekly

Official **MCP Apps** behavior is anchored in **[modelcontextprotocol.io — Apps extension](https://modelcontextprotocol.io/docs/extensions/apps)** and **[MCP blog](https://blog.modelcontextprotocol.io/)** announcements (e.g. production Apps extension, **2026-Q1**). **Per-host** rendering (inline vs side panel, interactivity, Prefab) changes faster than central docs.

**Fleet rule:** **Weekly**, re-verify **§1.3** against each target client’s **release notes / changelog** (Claude, Cursor, VS Code, Antigravity, etc.). Treat the table as **hints** until confirmed on a build you ship against.

---

## 2. FastMCP mechanics

### 2.1 Tool registration

Register the tool with the **`app=True`** flag so FastMCP marks it as an MCP App tool:

```python
@mcp.tool(app=True)
def show_book_prefab_card(book_id: int, ctx: Context | None = None) -> Any:
    ...
```

### 2.2 Return shape: `ToolResult`

Use **`ToolResult`** from **`fastmcp.tools`** (FastMCP 3.1+):

```python
from fastmcp.tools import ToolResult
from prefab_ui.app import PrefabApp

return ToolResult(
    content="Short summary for the model and plain-text clients.",
    structured_content=PrefabApp(view=view, title="Card title"),
)
```

- **`content`**: Always set. Used when structured UI is not rendered or for accessibility.  
- **`structured_content`**: `PrefabApp` wrapping the component tree.

### 2.3 Building the view: `prefab_ui.components`

Import layout primitives from **`prefab_ui.components`**. Typical building blocks:

| Component | Role |
|-----------|------|
| **`Card`** | Outer container; often `css_class="max-w-lg"` (Tailwind-style classes). |
| **`CardHeader`** | Header region. |
| **`CardTitle`** | Title string. |
| **`CardContent`** | Body region. |
| **`Text`** | Plain text; **does not interpret HTML**. |
| **`Image`** | `src` URL or **data URI** (`data:image/jpeg;base64,...`); `alt`, optional `width` / `height`. |

**Context-manager style** (common in Prefab examples):

```python
from prefab_ui.components import Card, CardContent, CardHeader, CardTitle, Image, Text

with Card(css_class="max-w-lg") as view:
    with CardHeader():
        CardTitle("My title")
    with CardContent():
        Text("Line one")
        Text("Line two")
```

After the `with` block, `view` is the root component passed to `PrefabApp(view=view, ...)`.

### 2.4 Styling props: `css_class` vs `cssClass`

The underlying Pydantic models often expose **`cssClass`** in JSON schema; **Python accepts `css_class`** via validators. Prefer **`css_class`** in server code for consistency with Ruff-friendly snake_case.

---

## 3. Fleet standard: packaging, coverage, toggles

### 3.1 Core dependency (mandatory)

**`prefab-ui>=0.14.0`** MUST appear under **`[project.dependencies]`** in every fleet **`pyproject.toml`** — not hidden behind an optional **`[apps]`** extra only. A normal **`uv sync`** / **`pip install`** must install it. This matches **[SOTA Requirements §2.2](../standards/SOTA_REQUIREMENTS.md#22-mcp-apps-and-prefab-ui-fleet-mandatory)**.

### 3.2 List / status / stats tools (mandatory coverage)

Servers MUST provide **Prefab App** tools (or **`ToolResult` + `PrefabApp`**) for operations whose main output is:

- **Lists** — collections, search results, inventories, directories, “show me what exists”
- **Status** — health, readiness, connectivity, service state
- **Stats / dashboards** — counts, aggregates, multi-field summaries, fleet snapshots

Pair the Prefab surface with the same domain data the plain JSON/dict tools expose. Document tool names in **README**, **`llms-full.txt`**, and **skills** so agents discover them. Scoped **PRD exceptions** (e.g. headless-only) are allowed but must be explicit.

### 3.3 Environment toggle (registration only)

Operators may disable **registering** App tools (CI, emergency headless) with a **per-server** env flag (e.g. **`CALIBRE_PREFAB_APPS=0`**, **`YOURSERVER_PREFAB_APPS=0`**). **Imports** of **`prefab_ui`** still succeed — the process **skips** `@mcp.tool(app=True)` registration and logs at **INFO**. Do not use a toggle to avoid the **core** dependency in **`pyproject.toml`**.

### 3.4 Registration wiring

- Call **`register_prefab_tools()`** (or equivalent) from **`register_tools()`** without swallowing **ImportError** for **`prefab_ui`** in production code paths — a missing package is a **install / environment failure**, not a silent skip (legacy optional-extra behavior is **deprecated** for new fleet work).

### 3.5 Module export for webapp / dynamic import

If the repo has a **Python webapp** that invokes MCP tools by import path, expose each App tool on the module namespace (e.g. **`show_book_prefab_card`**) and map dynamic-import tables with **`package.module:function`**:

```text
"show_book_prefab_card": "calibre_mcp.tools.prefab.book_card:show_book_prefab_card"
```

The segment after **`:`** must be the **function** name (not the module basename alone).

---

## 4. UX rules (Prefab `Text` and HTML)

### 4.1 Newlines and “run-on” text

**HTML collapses whitespace.** A single `Text("a\nb")` may render as **one line** in the client. **Fleet rule:**

- Use **one `Text(...)` per logical line or paragraph** for metadata and synopsis, **or** apply a **`css_class`** such as **`whitespace-pre-line`** if the client’s renderer supports it (verify per host).

### 4.2 Domain HTML in strings (e.g. Calibre comments)

Sources often store **HTML** (`<div>`, `<p>`). Prefab **`Text`** is **plain text** — **strip tags** before display:

- Use **`beautifulsoup4`** (already a common fleet dependency): `BeautifulSoup(html, "html.parser").get_text(separator="\n", strip=True)`, then normalize lines and truncate with a word-safe ellipsis.

---

## 5. Images and data URIs

- **Covers / thumbnails:** Read bytes from disk or API, detect **PNG / JPEG / WebP** from magic bytes, **base64-encode**, cap size (e.g. **512 KB** raw) to avoid huge tool payloads.  
- **`Image(src=..., alt=...)`** accepts `data:image/...;base64,...` URIs.

---

## 6. Reference implementation: calibre-mcp book card

**Purpose:** Rich **book card** in chat: title, authors, series, tags, **cover image**, **plain synopsis**.

**Location (illustrative):**

- `src/calibre_mcp/tools/prefab/book_card.py` — `register_book_card_tool()`, `show_book_prefab_card`  
- `src/calibre_mcp/tools/prefab/__init__.py` — `register_prefab_tools()`  
- Wired from `register_tools()`; **`prefab-ui`** core dependency; env **`CALIBRE_PREFAB_APPS`** (registration toggle)

Use this as a **copy pattern** for other repos (media, tickets, inventory, etc.): same **`ToolResult` + `PrefabApp`** shape, different **`book_service`** / domain layer.

---

## 7. Operational checklist (new repo)

**Concise procedure (numbered quick path):** **[update-mcp-server-for-prefabs.md](./update-mcp-server-for-prefabs.md)**.

1. Add **`prefab-ui>=0.14.0`** under **`[project.dependencies]`** (core).  
2. Implement **`@mcp.tool(app=True)`** + **`ToolResult`** + **`PrefabApp`** for **list / status / stats**-class surfaces (§3.2).  
3. Wire **`register_prefab_tools()`** from **`register_tools()`** (§3.4).  
4. Document env **registration** toggle (`*_PREFAB_APPS=0`) if supported.  
5. If webapp dynamic tool import exists, add **`module:function`** map entries (§3.5).  
6. **Strip HTML** from domain strings; **split** long text into multiple **`Text`** nodes.  
7. **Test** with real MCP host; assume **text** path always works.

---

## 8. Related central docs

| Document | Purpose |
|----------|---------|
| [fastmcp-31-fleet-capability-map.md](./fastmcp-31-fleet-capability-map.md) | **Full fleet map** — Prefab vs prompts, skills, CodeMode, providers, sampling (when to use what). |
| [update-mcp-server-for-prefabs.md](./update-mcp-server-for-prefabs.md) | **Quick path** — how to update an existing server for Prefabs (checklist + links). |
| [mcp-apps-prefab-use-cases-and-examples.md](./mcp-apps-prefab-use-cases-and-examples.md) | **When to use Prefab**, demo vs real value, **many examples** by domain, host UX (side panel, interaction). |
| [prefab-vs-webapps.md](./prefab-vs-webapps.md) | Prefab vs standalone webapps (tentative / strategic). |
| [prefab-web-renderer-scaffold-plan.md](./prefab-web-renderer-scaffold-plan.md) | **Deferred plan** — minimal DIY Prefab JSON renderer in a React webapp (fixtures, phases, non-goals). |
| [3.1-features.md](./3.1-features.md) | FastMCP 3.1 prompts, skills, platform features. |
| [tool-documentation.md](./tool-documentation.md) | Tool docstrings |
| [../standards/SOTA_REQUIREMENTS.md](../standards/SOTA_REQUIREMENTS.md) | SOTA hub — MCP Apps bullet |
| [../standards/TOOL_DESIGN_STANDARDS.md](../standards/TOOL_DESIGN_STANDARDS.md) | Portmanteau tools, errors |

---

## 9. External references

- **FastMCP** — [PrefectHQ/fastmcp](https://github.com/PrefectHQ/fastmcp)  
- **Prefab** (product/docs) — [prefab.prefect.io](https://prefab.prefect.io/) (verify current URLs; ecosystem moves fast).  
- **`prefab-ui`** — PyPI package used for **Python-side** component trees in fleet servers.

---

**Version history**

| Date | Change |
|------|--------|
| 2026-03-28 | **[update-mcp-server-for-prefabs.md](./update-mcp-server-for-prefabs.md)** — concise quick path for existing servers; §7 pointer. |
| 2026-03-28 | Initial fleet standard: MCP Apps, Prefab, FastMCP `ToolResult`, packaging, calibre-mcp pattern, Text/HTML UX. |
| 2026-04-17 | **Fleet mandatory:** **`prefab-ui`** core dep; **§3.2** list/status/stats coverage; optional-extra pattern superseded for new work; §3 renumbered (toggle = registration only). |
| 2026-03-28 | §1.3 Claude Desktop side panel / interaction pointer; §1.4 when Prefab is worth it; link **[mcp-apps-prefab-use-cases-and-examples.md](./mcp-apps-prefab-use-cases-and-examples.md)**. |
| 2026-03-28 | §1.5 **weekly** client-matrix verification vs modelcontextprotocol.io + host release notes. |
| 2026-03-28 | §1.4 pointer to use-cases **§3.8** (questionnaires / pre-scaffolding checklists). |
| 2026-03-28 | §8 related: **[prefab-web-renderer-scaffold-plan.md](./prefab-web-renderer-scaffold-plan.md)** (browser renderer plan, deferred). |
