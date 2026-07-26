# inkscape-mcp — ToolBench improvement note

**Report:** *(paste public ToolBench assessment URL after next scan — search [sandraschi + SCORED](https://toolbench.arcade.dev/?q=sandraschi&status=SCORED))*  
**Last seen grade:** *(pending rescan)* (date: 2026-03-24)

## Snapshot

- **Definition quality:** Addressed in-repo: MCP wrappers now use **`Literal[...]`** for every portmanteau `operation`, **`mcp.types.ToolAnnotations`** on each `@mcp.tool()`, and **gold-standard docstrings** (portmanteau rationale, operations list, Args, Returns, Errors) per [TOOL_DESIGN_STANDARDS.md](../../standards/TOOL_DESIGN_STANDARDS.md) §2–§4 and [FLEET_ALIGNMENT.md](../FLEET_ALIGNMENT.md).
- **Protocol / transport:** stdio and HTTP unchanged; FastMCP 3.1+ prompts/resources already registered upstream in repo.
- **Supportability:** GitHub activity / stars — not controlled in code.

## Easy wins (≤2h) — done this pass

1. Added **`src/inkscape_mcp/mcp_tool_types.py`** — single source of `Inkscape*Operation` Literals aligned with `tools/*.py`.
2. **`main.py`** — typed `operation` params; **`ToolAnnotations`** per tool (`inkscape_analysis` / `list_local_models` read-heavy; file/vector write-capable).
3. **`tools/heraldry.py`** — `generate_heraldry` annotations + expanded docstring.

## Follow-ups (optional)

1. **`output_schema=`** on `@mcp.tool()` where success dict shape is stable enough for JSON Schema (TOOL_DESIGN_STANDARDS §7).
2. **MCP wrapper** for `inkscape_system(operation="execute_extension")` — expose `extension_id` / params if ToolBench flags incomplete parameter surface.
3. **inkscape_vector** — host may need `**kwargs` passthrough for barcode/boolean extras; evaluate without breaking Literal ergonomics.

## Done / follow-up

- [x] Merged-oriented changes on default branch (apply in `D:\Dev\repos\inkscape-mcp`)
- [ ] **Request rescan** on [ToolBench Submit](https://toolbench.arcade.dev/submit) after publish
- [ ] Paste assessment URL and letter grade after rescoring
