# How to update an MCP server for Prefabs (quick path)

**Audience:** Maintainers adding **MCP Apps** / **Prefab UI** to an existing **FastMCP 3.1+** Python server.  
**Full reference:** [mcp-apps-prefab-ui.md](./mcp-apps-prefab-ui.md) — concepts, UX, images, fleet packaging (core dependency, list/status coverage).

---

## 1. Decide

- Prefab is **in-chat rich UI**, not a replacement for a fleet **webapp** (ports **10700–10800**). See [prefab-vs-webapps.md](../archive/fastmcp/prefab-vs-webapps.md).
- Every App tool must still return useful **plain text** via `ToolResult.content` for hosts that ignore Apps.
- **List / status / stats** tools **must** gain a Prefab surface — [SOTA §2.2](../standards/SOTA_REQUIREMENTS.md#22-mcp-apps-and-prefab-ui-fleet-mandatory), [mcp-apps-prefab-ui.md §3.2](./mcp-apps-prefab-ui.md#32-list--status--stats-tools-mandatory-coverage).

---

## 2. Dependencies

In **`pyproject.toml`**, add **`prefab-ui`** to **core** dependencies (not only an optional extra):

```toml
[project]
dependencies = [
    # ...
    "prefab-ui>=0.14.0",
]
```

Document in **README** / **`llms-full.txt`** / **skills** so agents discover **`show_*`** / App tools.

---

## 3. Implement the tool

1. **`@mcp.tool(app=True)`** on the function that returns structured UI.
2. Return **`ToolResult`** from **`fastmcp.tools`** with:
   - **`content`** — short string for the model and text-only clients (required).
   - **`structured_content`** — **`PrefabApp(view=..., title="...")`** built from **`prefab_ui.components`**.
3. Put implementation in a small module (e.g. **`your_mcp.tools.prefab.card`**) for clarity.

---

## 4. Wire registration

1. Add **`register_prefab_tools()`** (or similar) that registers Prefab **`@mcp.tool(app=True)`** handlers.
2. Call it from **`register_tools()`**. A missing **`prefab_ui`** install should **fail fast** in dev — do not silently skip (fleet standard: core dependency).
3. Optional: if **`YOURSERVER_PREFAB_APPS=0`**, **skip** registering App tools only; core JSON tools still load.

---

## 5. Webapp import maps (if applicable)

If a **Python webapp** calls tools by **`module:function`** string, add entries for each Prefab tool, e.g.:

```text
"show_item_prefab_card": "your_mcp.tools.prefab.card:show_item_prefab_card"
```

Use the **function** name after `:``.

---

## 6. Content hygiene

- **`Text`** does not render HTML — **strip tags** from domain HTML strings (e.g. BeautifulSoup).
- Prefer **one `Text(...)` per paragraph** or **`whitespace-pre-line`** if the client supports it — see [mcp-apps-prefab-ui.md §4](./mcp-apps-prefab-ui.md).

---

## 7. Verify

| Check | Done |
|-------|------|
| **`prefab-ui`** listed under **`[project.dependencies]`** | ☐ |
| **`uv sync`** installs **`prefab-ui`** without `--extra` | ☐ |
| List/status/stats domains have a **Prefab** tool or **`ToolResult`** path | ☐ |
| Same tool returns readable **text** when Apps are not rendered | ☐ |
| Optional env disables **registration** only (`*_PREFAB_APPS=0`) | ☐ |

Re-check client behavior periodically — see [mcp-apps-prefab-ui.md §1.5](./mcp-apps-prefab-ui.md).

---

## 8. Related

- [mcp-apps-prefab-ui.md](./mcp-apps-prefab-ui.md) — full standard  
- [mcp-apps-prefab-use-cases-and-examples.md](./mcp-apps-prefab-use-cases-and-examples.md) — examples  
- [../standards/TOOL_DESIGN_STANDARDS.md §3.3](../standards/TOOL_DESIGN_STANDARDS.md#33-mcp-apps-and-toolresult-prefab--in-chat-rich-ui)
