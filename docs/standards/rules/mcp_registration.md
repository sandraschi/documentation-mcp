# FastMCP 3.4+ Tool Registration & CodeMode (SOTA 2026)

## 1. Tool Registration Protocol
> [!CAUTION]
> FastMCP registers tools AT IMPORT TIME via `@mcp.tool` decorator. No import = no tool.

- **Portmanteau Imports**: Mandatory in `src/*/mcp/tools/__init__.py`. Re-exporting portmanteaus ensures registration during server boot.
- **Provider Conflicts**: `FileSystemProvider` is for schema-based discovery. DO NOT use it documented functions; it will result in an empty tool list.

## 2. Context Injection & Legacy Bridge
FastMCP 3.2+ re-exports `Context` for a cleaner API, but legacy servers may still require the internal path.

### Standard Import (3.2+):
```python
from fastmcp import Context
```

### Legacy Compatibility Bridge:
```python
try:
    from fastmcp import Context
except ImportError:
    from fastmcp.server.context import Context
```

- **Usage**: Always type-hint as `ctx: Context = None` in tool functions. FastMCP 3.2 will automatically inject the active sampling context.

## 3. Pydantic v2 Mandate
FastMCP 3.2 is built on Pydantic v2. Legacy v1 patterns are prohibited.

- **REJECT**: `model.dict()`, `model.json()`, `parse_obj()`.
- **REQUIRE**: `model.model_dump()`, `model.model_dump_json()`, `model.model_validate()`.

## 4. CodeMode (Experimental BM25 Discovery) — fastmcp 3.4.2+
- **Import Path**: `from fastmcp.experimental.transforms.code_mode import CodeMode` (not re-exported from `transforms.__init__`).
- **Signature**: `CodeMode(*, sandbox_provider=None, discovery_tools=None, execute_tool_name="execute", execute_description=None, max_tool_calls=50)` — keyword-only arguments.
- **Placement**: Apply only in CLI orchestration (e.g. `cli/commands/mcp.py`) via the `--agentic` flag, never as default.

## 5. Conversational Returns
Tools should return typed objects (BaseModel) or `dict` to enable 3.2's automatic natural language wrapping.

### Standard Return Schema:
```python
{
    "success": bool,
    "message": "Natural language summary for the user",
    "data": { ... } # Structured data for follow-up tool calls
}
```

## 6. Docstring SOTA
All tool registration MUST follow the **[Docstring SOTA](./docstrings_sota.md)**:
- Abolish `Args:` in docstrings.
- Use `Annotated[T, Field(description="...")]` for all parameters.
- Mandatory `## Return Format` and `## Examples`.
