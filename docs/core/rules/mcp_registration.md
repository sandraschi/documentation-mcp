# FastMCP 3.2 Tool Registration & CodeMode (SOTA 2026)

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

## 4. CodeMode (Experimental BM25 Discovery)
- **Import Path**: Mandatory `from fastmcp.experimental.transforms import CodeMode`.
- **Signature (3.2)**: `CodeMode()` — zero arguments.
- **Warning**: Using `CodeMode(mcp)` will result in a `TypeError` in 3.2.
- **Placement**: Apply only in CLI orchestration (e.g. `cli/commands/mcp.py`) via the `--agentic` flag.

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
All tool registration MUST follow the **[Docstring SOTA](file:///D:/Dev/repos/mcp-central-docs/standards/rules/docstrings_sota.md)**:
- Abolish `Args:` in docstrings.
- Use `Annotated[T, Field(description="...")]` for all parameters.
- Mandatory `## Return Format` and `## Examples`.
