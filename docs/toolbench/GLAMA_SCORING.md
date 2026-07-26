# Glama MCP server scoring

> Source: https://glama.ai/mcp/servers/hyperspell/hyperspell-mcp/score  
> Verified: 2026-04-08

## How Glama grades servers

Glama's quality score is **entirely about docstrings**. No stars, no CI, no `llms.txt`, no `justfile`. Two components:

| Component | Weight |
|---|---|
| Tool Definition Quality (TDQS) | 70% |
| Server Coherence | 30% |

**TDQS** scores every tool 1–5 across six dimensions:

| Dimension | Weight | What it looks for |
|---|---|---|
| Purpose Clarity | 25% | First sentence states exactly what the tool does — not what it is |
| Usage Guidelines | 20% | When to call it, when not to, preconditions, call ordering |
| Behavioral Transparency | 20% | What it returns, side effects, error conditions |
| Parameter Semantics | 15% | Each param: type, allowed values, what it affects |
| Conciseness & Structure | 10% | Not a wall of text, not a one-liner; structured sections |
| Contextual Completeness | 10% | Enough context to use without reading source |

**Server-level TDQS** = 60% mean + 40% minimum across all tools.  
A single poorly described tool pulls the whole server down.

**Server Coherence** scores four dimensions equally:
- Disambiguation — can agents tell tools apart?
- Naming Consistency — consistent verb/noun patterns
- Tool Count Appropriateness — not too many, not too few
- Completeness — no obvious gaps in the tool surface

**Grade thresholds:**

| Grade | Score | Status |
|---|---|---|
| A | ≥ 3.5 | Passing |
| B | ≥ 3.0 | Passing |
| C | ≥ 2.0 | Acceptable target |
| D | ≥ 1.0 | Below par |
| F | < 1.0 | Failing |

B and above is "passing." **C is the practical target for individual devs** — A is dominated by corporate repos with 1000+ stars.

---

## What does NOT affect Glama scores

- GitHub stars / forks
- `llms.txt` / `llms-full.txt`
- `glama.json` (affects discoverability, not the quality score)
- CI badges
- `justfile`
- PyPI publication
- GitHub topics

Those affect **discoverability** (whether Glama finds and indexes the server) but not the **score**.

---

## The F→C fix: docstring quality

The most common failure patterns:

- **Too short:** one-line docstring with no Args/Returns — scores ~1.0 on Purpose Clarity only
- **Too long:** 400+ word walls of prose — Conciseness & Structure tanks
- **Missing Args:** no parameter descriptions — Parameter Semantics = 0
- **No Returns:** no description of what comes back — Behavioral Transparency suffers
- **No usage guidance:** agent can't tell when to call this vs another tool — Usage Guidelines = 0
- **Portmanteau with no sub-operation list:** "operation: str" with no explanation of valid values

Sweet spot: **80–250 words per docstring**, all six sections covered.

---

## Glama C target docstring template

This template satisfies all six Glama dimensions. Copy and adapt for every tool.

```python
async def my_tool(
    operation: Literal["read", "write", "delete"],
    path: str,
    content: str | None = None,
) -> dict:
    """One sentence: what this tool does and for whom.

    When to use: call this when you need to [specific scenario].
    When NOT to use: prefer [other_tool] for [different scenario].
    Preconditions: [path] must exist for read/delete; content required for write.

    Operations:
    - read:   Return file contents as string. Non-destructive.
    - write:  Create or overwrite file at path with content. Irreversible.
    - delete: Remove file permanently. Use dry_run=True to preview.

    Args:
        operation: Action to perform. One of: "read", "write", "delete".
        path: Absolute path to target file. Must be within allowed_directories.
            Relative paths are resolved from the server's working directory.
        content: Text to write. Required for write, ignored for read/delete.

    Returns:
        Dict with:
          success (bool): True on success.
          operation (str): Echo of the requested operation.
          data (dict): Operation-specific payload — file contents for read,
              written bytes for write, removed path for delete.
          execution_time_ms (float): Wall-clock time.
        On failure: success=False, error (str), recovery_options (list[str]).

    Errors:
        FileNotFoundError — path does not exist (read/delete).
        PermissionError  — path is outside allowed_directories.
        ValueError       — content missing for write operation.
    """
```

**Rules for the template:**
- First line: action verb + object + purpose. No "This tool..." opener.
- Keep total length 80–250 words. Count before committing.
- Operations block: one line per operation, what it does, destructive/safe.
- Args: every param, type, allowed values, which operations require it.
- Returns: name the keys, not just "a dict".
- Errors: three or fewer common failure modes with cause.

---

## Portmanteau tools: special considerations

Portmanteau tools (one tool, `operation` param selects behaviour) need extra care because Glama scores **Disambiguation** at the server level — if two portmanteau tools have overlapping descriptions, coherence suffers.

For portmanteau tools specifically:
- The one-line summary must name the domain, not the operations: `"File I/O operations for SVG and vector files via Inkscape CLI."` not `"Do stuff with files."`
- The Operations block is mandatory — without it, Parameter Semantics on `operation` scores 0
- Usage Guidelines must say which other tool to use for adjacent tasks: `"For vector editing use inkscape_vector; for analysis use inkscape_analysis."`

---

## Rescoring after fixes

Glama rescans repos automatically once per day. To force an immediate rescan:
1. Go to your server's Glama admin page (requires claiming the server with GitHub auth)
2. Click "Sync Server"

Allow a few minutes for the score to update after sync.

---

## Fleet improvement workflow

1. Paste ToolBench/Glama assessment output into a session
2. Identify which tools are pulling the minimum score down (60/40 weighting means the worst tool matters most)
3. Fix the worst 2–3 tools per repo — don't try to fix all at once
4. Sync on Glama, verify score moved
5. Log what changed in `toolbench/improvements/`

See [PROACTIVE_HARDENING.md](PROACTIVE_HARDENING.md) for the weekly loop.
