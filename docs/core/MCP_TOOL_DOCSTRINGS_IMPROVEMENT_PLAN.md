# MCP Tool Docstrings Improvement Plan
2: 
3: **Status**: Standardized (2026-04-27)
4: **Scope**: Fleet-wide SOTA MCP servers
5: **Reference**: [TOOL_DESIGN_STANDARDS.md §1.2](./TOOL_DESIGN_STANDARDS.md#12-the-industrial-portmanteau-standard)
6: **Outcome**: Finalized the "Industrial Portmanteau" pattern to resolve IDE tool limits and static analysis friction.

---

## 1. Problem Summary

### 1.1 What users see in Cursor

- **Args block**: Comes from the tool's long description (docstring). For portmanteau tools this is often a big block of text (Operations, Parameters, Returns, Examples). It can render as one blob or be parsed loosely, so it's hard to scan.
- **Parameters block**: Comes from the MCP tool schema (`arguments.properties`). Each property has `type`, `default`, `enum`, etc., but **no `description`**. Cursor then shows something like "no description" for every parameter, so the parameter list is useless even though the docstring has the real docs.

### 1.2 Root cause

- The **JSON schema** sent to the client (e.g. from `mcps/<server>/tools/*.json` or from the server's `tools/list`) is built from the Python signature and types. FastMCP does **not** today pull per-parameter text from the docstring into `arguments.properties.<name>.description`.
- So: rich "Parameters" prose lives only in the docstring; the schema has no per-parameter descriptions, and Cursor's Parameters panel has nothing to show.

### 1.3 Preferred approach: Parameters block as single source for params

- **We cannot remove the Parameters block** — Cursor renders it from the tool schema. We can only make it useful or leave it showing "no description."
- **Recommendation: make the Parameters block the primary place for parameter docs.** Populate `arguments.properties.<name>.description` (via `Annotated` + `Field` in Python or in the JSON). Cursor then shows params in a **nicely bulleted** list. **Drop the Args section** in the docstring (vanish or one-line placeholder). The docstring focuses on: summary, operations (if portmanteau), Returns, Examples, Notes (prerequisites / "use this tool first"), Errors. Param details live only in the schema → Parameters block.

### 1.4 Why portmanteau tools are worse

- One tool, many operations; many parameters are optional and only apply to some operations.
- Docstrings tend to be long (Operations, then Parameters with "Required for: X, Y"). That makes the Args block dense and hard to read.
- The same parameters still have no schema description, so the Parameters block stays "no description" for every arg.

---

## 2. Improvement Plan (High Level)

| Phase | Goal | Outcome |
|-------|------|---------|
| **A. Schema** | Every `arguments.properties.<name>` has a `description` | Cursor Parameters block shows params in a clear, bulleted list (no more "no description"). |
| **B. Docstring** | Don't duplicate params; keep description lean | Summary, operations, Returns, Examples, Errors only; param docs live in schema → Parameters block. |
| **C. Source of truth** | Prefer Python as source; schema generated from it | Annotated + Field(description=...) so generated schema gets descriptions. |
| **D. Fleet** | Same pattern across fleet repos | One convention; optional lint/CI to enforce. |

---

## 3. Detailed Plan

### 3.1 Phase A: Add per-parameter descriptions to the schema

**Target**: Every property in `arguments.properties` has a `description` string.

**Options**:

1. **Python as source (recommended)**  
   - In tool signatures, use `Annotated[T, Field(description="...")]` for each parameter.  
   - FastMCP/Pydantic will then include that in the generated JSON schema, and Cursor will show it in the Parameters block.  
   - Example:
     ```python
     from typing import Annotated
     from pydantic import Field

     @mcp.tool()
     async def db_operations(
         operation: Annotated[str, Field(description="Operation: execute_query, batch_insert, ...")],
         connection_name: Annotated[str | None, Field(description="Registered DB connection name.")] = None,
         query: Annotated[str | None, Field(description="SQL or DB-specific query; use ? or :name placeholders.")] = None,
         ...
     ) -> dict[str, Any]:
         """Short summary. Operations: ... (keep docstring for full docs)."""
     ```
   - **Portmanteau**: For operation-specific params, one-line is enough, e.g.  
     `"Table name. Used for: batch_insert, quick_data_sample."`

2. **JSON as source**  
   - If descriptors are hand-maintained (e.g. `mcps/<server>/tools/*.json`), add a `description` key to each `arguments.properties.<name>`.  
   - Keep it one sentence; can copy from or condense the docstring.

3. **Generator**  
   - If descriptors are generated from the server (e.g. list tools → export JSON), extend the generator to parse the docstring (e.g. Google/NumPy "Parameters:" or "Args:") and set `properties.<name>.description` from the first line per param.  
   - Fallback: no description in docstring → leave empty or "(See tool description)."

**Deliverable**: No parameter in any fleet tool schema should be missing `description` (or have a placeholder that we explicitly accept until Phase C is done).

---

### 3.2 Phase B: Docstring format (Parameters block = param docs; no duplicate Args)

**Target**: The **Parameters block** (from schema) is the single, nicely bulleted place for param docs. The **Args block** in the docstring vanishes or is a one-line placeholder. The docstring stays lean: summary, operations, Returns, Examples, Notes (prerequisites), Errors.

**Principle: Keep docstrings lean.** Do not let them grow huge. Every section should earn its place. Param details live only in the schema → Cursor's Parameters block; the docstring does not repeat them (Args vanishes or is a placeholder).

**Conventions**:

1. **Summary**: First 1–3 lines = what the tool does. No parameter list here.
2. **Operations** (portmanteau): Bullet list of operation names and one-line each. Keeps the top of the docstring scannable.
3. **Args block**: **Vanish or placeholder only.** All parameter docs live in the schema → Cursor's Parameters block. In the docstring, either omit an Args section entirely or use a single placeholder line, e.g. `Args: See Parameters block.` Do not list or describe parameters in the docstring. **IFF** you keep an Args block with any real content (e.g. for docstring-only clients), use **" - " delimiters** for every option or format list so the Args block stays readable (one " - " per line); the old email-ops style applied here.
4. **Returns**: One short block (structure or key keys). No need to list every possible key for every operation.
5. **Examples**: Few but useful (see below).
6. **Notes**: When the tool has prerequisites or ordering requirements, add a short **Notes:** block so the client knows to call other tools first. Use " - " bullets. Example: "Use db_connection(operation='register') first; then db_schema(operation='list_tables') to see tables." Keeps sequencing and dependencies explicit.
7. **Errors**: When relevant, a short block (see below).

**Where param descriptions live**: Put the **one-line (or short) description per parameter** in the **schema** (`Field(description="...")` or `arguments.properties.<name>.description` in JSON). Cursor then shows them in the **Parameters block** in a clear, bulleted way. Do not duplicate that content in the docstring. (The old email-ops " - " delimiters improved the **Args** block; since we eliminate Args in favor of Parameters, that pattern is only relevant **if** you keep an Args block with content—then use " - " per option so it stays readable.)

- **Examples**: Few but useful. Include an explicit **Examples:** block with **1–3 representative calls** that help the client (LLM/user) understand how to invoke the tool—e.g. minimal call, one with key optional args, one variant (different operation or service). Do not catalog every operation or combination; keep the block short. Cursor's docstring UI renders this section well. Example:
  ```
  Examples:
      send_email(to="user@example.com", subject="Hello", body="This is a test email")
      send_email(..., service="sendgrid", html="<h1>Welcome!</h1>")
  ```
  Reference: **user-emailops** (`mcps/user-emailops/tools/*.json`).

- **Notes**: Extra info for the client—especially **prerequisites and ordering**. Use when "you must use another tool first" (e.g. register a DB connection, then get schema). Short " - " bullets. Example:
  ```
  Notes:
      - Register a connection first: db_connection(operation='register') or db_management(operation='init_database')
      - List tables: db_schema(operation='list_tables') before querying or batch_insert
  ```
  Use Notes for sequencing; use Errors for failure modes and recovery.

- **Errors**: When the tool returns structured errors or has well-known failure modes, add a short **Errors:** block so the client can recover or explain. Use " - " bullets: one line per error pattern or tip. Keep to 3–5 items. Example:
  ```
  Errors:
      - success=False, error="Connection not found": use db_connection(operation='list') first
      - success=False, error="Query is required": pass query= for this operation
      - Table not found: check table_name or use db_schema(operation='list_tables')
  ```
  Omit if the tool has no specific error semantics worth documenting.

**Portmanteau-specific**: For operation-specific params, put "Used for: op1, op2" (or similar) in the **schema** description for that param, so the Parameters block is self-contained. The docstring does not repeat it.

**Deliverable**: AGENT_PROTOCOLS or this doc updated with the above format; one or two fleet tools (e.g. database-operations-mcp `db_operations`) refactored as the reference.

---

### 3.3 Phase C: Single source of truth (Python → schema)

**Target**: Per-parameter descriptions are defined once in Python (or in JSON) and appear in the schema only. The docstring has no Args content (vanish or placeholder).

**Approach**:

1. **Primary**: Use `Annotated[T, Field(description="...")]` in the tool signature. Schema is generated by FastMCP; Cursor Parameters block is populated.
2. **Docstring**: Omit Args or use a one-line placeholder ("Args: See Parameters block."). Param docs live only in the schema. Docstring-only clients still get summary, Operations, Returns, Examples, Notes, Errors.
3. **Caching / mcps/*.json**: If Cursor or the bridge use cached descriptors under `mcps/<server>/tools/*.json`, ensure those files are regenerated from the server (or from the same Python source) so they get the new `description` fields. Document the regeneration step.

**Deliverable**: At least one fleet repo (e.g. database-operations-mcp) uses Annotated+Field for all portmanteau tool parameters; schema and docstring stay in sync; process documented.

---

### 3.4 Phase D: Fleet rollout and docs

**Target**: All fleet MCP servers follow the same pattern; new portmanteau tools get a populated Parameters block and lean docstring (no Args, optional Notes/Errors) from the start.

**Actions**:

1. **Docs**: In AGENT_PROTOCOLS (or linked from it), add a short "Tool schema and Cursor UI" subsection:
   - Use `Annotated[T, Field(description="...")]` for every tool parameter.
   - Docstring: summary, Operations (if portmanteau), no Args (or placeholder), Returns, Examples, Notes (prerequisites), Errors.
   - Reference this improvement plan for rationale and portmanteau details.
2. **Lint (optional)**: Script or CI that:
   - For Python: checks that every `@mcp.tool()` parameter has a `Field(description=...)` (or equivalent), or
   - For JSON: checks that every `arguments.properties.<name>` has a non-empty `description`.
3. **Fleet repos**: Apply the pattern to database-operations-mcp first, then other portmanteau-heavy servers (e.g. fileops, dbops, calibreops) as capacity allows.

**Deliverable**: Documented standard; optional lint; at least 2–3 fleet repos updated; new tools required to follow the standard.

---

## 4. Order of Work (Suggested)

1. **Phase A + C together** in one repo (e.g. database-operations-mcp): Add `Annotated`/`Field` to one portmanteau tool (`db_operations`), regenerate or update schema, confirm Cursor shows descriptions in the Parameters block.
2. **Phase B**: Remove Args from the docstring (or use placeholder "Args: See Parameters block."); add Notes if the tool has prerequisites (e.g. "call db_connection first"); confirm Parameters block shows all param descriptions in Cursor.
3. **Phase D**: Update AGENT_PROTOCOLS and this plan; roll out to other portmanteau tools in the same repo, then to other fleet repos; add optional lint.

---

## 5. References

- **Fleet example (db_operations)**: `database-operations-mcp` repo — long docstring, no per-param schema description.
- **Cursor schema source**: `mcps/user-dbops/tools/db_operations.json` — `description` has full prose; `arguments.properties` have no `description`.
- **Cursor-friendly docstring reference (email-ops)**: `mcps/user-emailops/tools/send_email.json`, `email_status.json`, `email_help.json` — good Examples; optional Notes. The " - " delimiters there were in the **Args** block; since we prefer no Args, that pattern is only required **IFF** an Args block is present (then use " - " per option for readability).
- **FastMCP / MCP**: Parameter descriptions in schema come from Pydantic `Field(description=...)` when using `Annotated` on the tool parameters (see [Improving MCP tool schemas](https://pamelafox.github.io/py-ai-mcp-tool-schemas), MCP Python SDK issue #566).
- **Existing standards**: [AGENT_PROTOCOLS.md](AGENT_PROTOCOLS.md) §4 (Docstring Construction Rules, Args section, Gold Standard). See also [fastmcp/tool-documentation.md](../fastmcp/tool-documentation.md) for implementation details.

---

## 6. Success Criteria

- In Cursor's tool UI, the **Parameters** block shows a short, non-empty description for every parameter (no "no description").
- The docstring has **no Args** (or a one-line placeholder); it is easy to scan: summary, operations, Returns, Examples, Notes (prerequisites), Errors.
- Portmanteau tools call out "Used for: op1, op2" in the **schema** description for the param. Tools with ordering requirements document them in a **Notes** block (e.g. use db_connection first, then db_schema).
- At least one fleet repo (database-operations-mcp) fully updated; process documented and repeatable for the rest of the fleet.
