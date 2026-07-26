# SOTA Docstring Protocol (June 2026)

This protocol optimizes how FastMCP tools render in modern IDEs (like Cursor) by moving parameter documentation into the generated JSON schema.

## 1. Parameter Documentation (Schema First)
The `Args:` and `Parameters:` blocks in docstrings are **deprecated**. Use Pydantic `Field` descriptions as the single source of truth.

### Standard Pattern:
```python
@app.tool()
async def db_op(
    table: Annotated[str, Field(description="Name of the table to query.")],
    limit: Annotated[int, Field(description="Max rows.", ge=1)] = 50
) -> dict:
    """Query the database.
    
    ## Return Format
    {"success": bool, "rows": list}
    """
```

## 2. Docstring Sectioning
Keep docstrings lean to prevent "floundering" and context bloat.

- **Summary**: 1-3 lines (mandatory).
- **[RATIONALE]**: (Mandatory for Industrial Portmanteaus) 1-2 lines explaining why this tool is consolidated.
- **## Return Format**: Explicit JSON structure (mandatory). Include `message` key for conversational returns — see [DIALOGIC_RETURNS.md](../DIALOGIC_RETURNS.md).
- **## Examples**: 1-3 concrete Python calls (mandatory).
- **Notes**: Prerequisite tools or sequencing info (optional).
- **Errors**: Known failure modes and recovery tips (optional).

## 3. Tool Annotations & Versioning
Explicitly signal tool behavior and maturity to the agent.

- **Safety**: Use `@mcp.tool(annotations=READ_ONLY)` or `MUTATING` / `DESTRUCTIVE`.
- **Versioning**: Always include `version="x.y.z"` in the decorator for new tools.

## 4. Implementation Rules
- **Standard String Literals**: NO f-strings in docstrings.
- **Vanish Args**: Either omit the `Args:` section entirely or use: `Args: See Parameters block.`
- **Separator Pattern**: Use `" - "` for all bulleted lists in Notes and Errors.
