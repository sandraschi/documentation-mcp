# ToolBench — scraper / analyzer (third party)

For a **deeper** write-up (Arcade business context, stdio score cap, stars, “single dev or not?”), see [ARCADE_TOOLBENCH_ASSESSMENT.md](ARCADE_TOOLBENCH_ASSESSMENT.md).

**ToolBench** ([toolbench.arcade.dev](https://toolbench.arcade.dev/)) is an Arcade.dev product that publishes **trust / quality reports** for MCP servers listed in its directory. It is **not** part of FastMCP or the MCP spec; it is an **external benchmark** our fleet uses as one signal among many.

## What gets analyzed

From public pages and report cards (e.g. [methodology](https://toolbench.arcade.dev/methodology)):

1. **Definition quality** — Tool definitions: descriptions, parameter schemas (types, enums, bounds), whether outputs are described well enough for chaining.
2. **Protocol readiness** — Static signals that the server is suitable for agent use (structured tools, reasonable surface area).
3. **Supportability** — Repository health proxies (stars, activity, releases) — **not** fully under repo control.

Reports often note: summary text may be **generated from README + source analysis**, not necessarily the author’s own marketing copy.

## “Scraper” in practice

We say **scraper/analyzer** informally:

- **Ingestion**: discover server metadata (e.g. GitHub, PyPI, MCP registry links) and tool listings.
- **Static analysis**: inspect tool definitions (names, parameters, docstrings/schemas as visible to the analyzer).
- **Heuristic scoring**: map findings to rubric items (e.g. constrained inputs, response shape, verb-led names, recovery guidance).

Exact pipelines are **Arcade’s**; they can change. Do not treat a single report as permanent truth — use **Rescan** when the product offers it after you ship fixes.

## Grades (typical report card)

Reports show a **letter grade** and a **numeric trust score** derived from weighted criteria. Low grades often combine:

- Weak or missing **JSON Schema** detail (free `string` instead of `Literal`, no min/max on numbers).
- **Generic** tool names (`foo_bar` noun piles vs `list_*` / `get_*`).
- **Portmanteau** tools flagged when the benchmark prefers one-action-per-tool (fleet may still choose portmanteau for [tool explosion](../standards/HISTORY_OF_FASTMCP.md) reasons — document the tradeoff in [FLEET_ALIGNMENT.md](FLEET_ALIGNMENT.md)).
- Missing **error/recovery** hints and **output** documentation.

## How to use ToolBench in the fleet

1. Find or submit the server; open the **tool report**.
2. Read **Top issues** and map them to [TOOL_DESIGN_STANDARDS.md](../standards/TOOL_DESIGN_STANDARDS.md) §4–§9.
3. Fix in-repo (schemas, docstrings, `annotations`, optional `output_schema`).
4. Request **rescan** if available; record outcomes under [improvements/](improvements/README.md).

## Limits

- Third-party **methodology** may disagree with **fleet** choices (e.g. portmanteau tools).
- **Supportability** scores reward popular repos — small private projects start at a disadvantage.
- Analysis may **lag** the latest commit until rescanned.
