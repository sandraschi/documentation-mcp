# Fleet alignment — escaping D / E / F on ToolBench

Purpose: turn external ToolBench findings into **actionable repo work** aligned with [TOOL_DESIGN_STANDARDS.md](../standards/TOOL_DESIGN_STANDARDS.md), without treating the grade as the only metric.

## Priority order (what moves “definition” scores fastest)

1. **Parameters** — Replace untyped `operation: str` with `Literal[...]` (or enums). Add `Annotated[..., Field(ge=, le=, description=)]` for numbers and strings that need bounds or format notes.
2. **Docstrings** — First line + **Returns** with stable keys; **Errors** / recovery; for portmanteau tools, bullet **operations** list.
3. **Tool names** — Verb-led `snake_case` ([TOOL_DESIGN_STANDARDS.md](../standards/TOOL_DESIGN_STANDARDS.md) naming row): `get_help`, `manage_tailnet_devices`, `list_*`, `run_*`. Omit redundant product prefix when the **server only does one product** (see improvements notes).
4. **FastMCP** — Use `@mcp.tool(name="...")` if the Python function name stays internal for legacy reasons. Set **`annotations`** (read-only vs mutating) where applicable; optional **`output_schema`** when the success shape is stable.
5. **Destructive / high-impact** — Document dry-run / confirm patterns per §6–§7 in tool design standards.

## Rescan workflow

See **[TOOLBENCH_ECOSYSTEM.md](TOOLBENCH_ECOSYSTEM.md)** for the full loop (Glama contrast, Arcade MCP product vs ToolBench, step-by-step rescoring).

1. Merge fixes on the default branch (or the branch ToolBench tracks).
2. **[Submit for rescoring](https://toolbench.arcade.dev/submit)** — sign in; the report card shows **Sign in to request rescan** when auth is required ([Improve](https://toolbench.arcade.dev/improve) links the same flow).
3. Wait for the async re-analysis (scores can lag commits).
4. Paste the new report link and date into the server’s [improvements/](improvements/README.md) entry.

## When ToolBench conflicts with fleet rules

| Benchmark preference | Fleet position |
|---------------------|----------------|
| One tool per action | We allow **portmanteau** tools with a typed `operation` to avoid tool explosion; mitigate with Literals + clear docstrings ([HISTORY_OF_FASTMCP.md](../standards/HISTORY_OF_FASTMCP.md)). |
| Verb-prefixed names | We align — prefer `get_help` over `tailscale_help` when the server is already Tailscale-only. |
| GitHub stars | Not controllable — document in TOOLBENCH_ANALYSIS; focus on definition quality. |

## Per-server log

Add or update a file under [improvements/](improvements/README.md) for each server that completes a meaningful pass.
