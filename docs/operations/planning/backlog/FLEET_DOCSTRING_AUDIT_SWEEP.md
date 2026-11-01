# Fleet docstring audit (FastMCP 3.4 standard)

**Priority:** P2  
**Standard:** `standards/docstrings_sota.md`

## Required shape

- No `Args:` blocks — use `Annotated[T, Field(description="...")]`
- `## Return Format` mandatory
- `## Examples` — 1–3 concrete calls
- `[RATIONALE]` for portmanteau tools
- No f-strings or em dashes in docstrings

## Audit commands (per repo)

```powershell
rg -n "Args:" src/
rg -n "## Return" src/
rg -n "f'" src/ --glob "*.py"
```

**Priority repos:** fastsearch-mcp, meta_mcp, advanced-memory-mcp.  
**Batch limit:** 5 files per commit.
