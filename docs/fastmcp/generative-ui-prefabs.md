# FastMCP Generative UI: Prefabs

**Last Updated:** 2026-06-06  
**Standard:** FastMCP 3.4.2 (GA target)

**Generative UI (Prefabs)** allows MCP servers to push rich, interactive components directly into the conversation surface. Instead of raw JSON or text, servers can return formatted cards, tables, and images that are rendered natively by the host (Claude Desktop, Cursor, etc.).

---

## 1. The Prefab DSL

FastMCP uses a Python DSL provided by `prefab-ui` to define components.

### Core Primitives
| Component | Usage |
|---|---|
| `Card` | The primary layout container for atomic entities. |
| `Table` | Best for list-based data or fleet status. |
| `Image` | Supports `src` URLs and Base64 Data URIs. |
| `Text` | Markdown-friendly text rendering. |

---

## 2. Implementation: `ToolResult`

To return a Prefab, your tool must return a `ToolResult` object containing both a text fallback (for RAG) and the structured UI.

### Pattern: The Entity Card
```python
from mcp.types import ToolResult
from prefab_ui import PrefabApp, Card, Text, Image

@mcp.tool(app=True)
async def show_book_card(book_id: str) -> ToolResult:
    """Display a rich book card."""
    book = await get_book(book_id)
    
    app = PrefabApp(
        title=book.title,
        root=Card(
            content=[
                Image(src=book.cover_url),
                Text(f"Author: **{book.author}**"),
                Text(book.summary)
            ]
        )
    )
    
    return ToolResult(
        content=f"Book: {book.title} by {book.author}", # Text fallback
        structured_content=app
    )
```

### Pattern: Prefab + explicit error (3.4+)

When the card shows a failure state, set **`is_error=True`** so the host marks the tool call as failed while still rendering the Prefab:

```python
return ToolResult(
    content=summary,
    structured_content=PrefabApp(view=error_card, title="Error"),
    is_error=True,
)
```

See [3.4-features.md](3.4-features.md) §4.

---

## 3. Fleet Requirements

Following **SOTA 2026**, Prefab is **MANDATORY** for tools belonging to the following categories:

1. **Lists**: Search results, inventories, and "show me" tools.
2. **Status**: Health checks, server readiness, and telemetry.
3. **Dashboards**: Financial summaries, fleet snapshots, or project overviews.

---

## 4. Host Rendering & Fallbacks

Capable hosts render the `structured_content` in a dedicated "App Surface" (Claude side-panel) or inline (Cursor).
- **Graceful Degradation**: If a host does not support Prefabs, it will only see the `content` string.
- **Accessibility**: Always ensure the `content` fallback is high-fidelity for RAG consumption.

---

## 5. Security Note: UI Sanitization

- **HTML Injection**: Prefab components sanitize basic text. However, ensure that domain-specific HTML (e.g., Calibre comments) is stripped using `BeautifulSoup` before passing it to a `Text` component.
- **Data URIs**: Limit Base64 image sizes to **512KB** to prevent transport timeouts.

---

## References
- [tool-documentation.md](./tool-documentation.md)
- [fastmcp-32-fleet-capability-map.md](./fastmcp-32-fleet-capability-map.md)
- [prefab-vs-webapps.md](./prefab-vs-webapps.md)
