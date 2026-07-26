# REPO_SOTA_BASH: Industrial Modernization Recipe (June 2026)

> [!IMPORTANT]
> **SOTA v13.1 Compliance**: This document is the authoritative guide for "bashing" a legacy or 2.x repository into June 2026 compliance. It prioritizes FastMCP 3.2, `uv`, and high-fidelity Markdown outputs.

---

## 1. The Preamble: What is a SOTA Bash?

A **SOTA Bash** is a high-density modernization sprint. It is not "maintenance"; it is a systemic architectural upgrade to ensure a repository meets the floor requirements for the **2026 April Fleet Standard**.

**Core Philosophy:**
- **Materialist**: Data and logs are the only reality.
- **Reductionist**: Purge complexity that doesn't serve the agentic loop.
- **Industrial**: Strict formatting, locked dependencies, and automated verification.

---

## 2. Phase 1: The uv Pivot (Dependency Anchoring)

Legacy package managers (pip, conda) are deprecated for SOTA work.

1.  **Initialize uv**: `uv init` (if not already managed).
2.  **FastMCP 3.2**: `uv add "fastmcp>=3.4.4,<4"`.
3.  **Modern Dev Stack**: `uv add --dev ruff pyright pytest`.
4.  **Lockfile**: Always commit `uv.lock`.

---

## 3. Phase 2: The Ruff 120 Standard (Industrialized Logic)

All SOTA repositories MUST adhere to the **120-character line length** to accommodate complex agentic logic and descriptive docstrings.

### 3.1. `pyproject.toml` Configuration
```toml
[tool.ruff]
line-length = 120
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "N", "S", "A", "C4", "T20", "RET", "SIM", "ARG", "PTH", "TRY"]
ignore = ["E501", "B008"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### 3.2. The Formatting Bash
- `uv run ruff check . --fix`
- `uv run ruff format .`

---

## 4. Phase 3: FastMCP 3.2 Feature Injection

### 4.1. Host LLM Sampling (`ctx.sample`)
Replace "mock" reasoning with native host sampling.
```python
@app.tool()
async def agentic_refactor(code: str, ctx: Context) -> str:
    """Refactor code using high-power host sampling."""
    res = await ctx.sample(
        messages=[{"role": "user", "content": f"Refactor this: {code}"}],
        max_tokens=2048
    )
    return res.text
```

### 4.2. Native Prompt Templates (`@mcp.prompt`)
Standardize expert personas and starting points.
```python
@app.prompt()
def sota_expert(repo_name: str) -> str:
    return f"You are the SOTA expert for {repo_name}. Adhere to REPO_SOTA_BASH standards."
```

### 4.3. Background Task Protocol (SEP-1686)
For long-running operations (indexing, generation), use the background context.
```python
@app.tool()
async def start_long_operation(ctx: Context):
    # SEP-1686 implementation
    ctx.run_in_background(my_long_task())
    return "Operation started in background."
```

---

## 5. Phase 4: Output Quality (Mud-to-Gold)

**CRITICAL**: Tools MUST NOT return "muddy" JSON blobs to the user. All non-trivial tool returns MUST be formatted as high-fidelity Markdown strings.

### 5.1. The Formatting Helper Pattern
Implement a internal `_to_markdown` helper to ensure consistency.
```python
def _to_markdown(data: dict, operation: str) -> str:
    # Convert structured data to human/agent-readable Markdown
    ...
```

### 5.2. Markdown Requirement
- Headers for sections.
- Code blocks for data/logs.
- Bullet points for metrics.
- Actionable **Next Steps** at the bottom of every return.

---

## 6. Phase 5: The Discovery Layer (Manifests)

1.  **`llms.txt`**: Minimal index for LLM crawlers.
2.  **`llms-full.txt`**: Complete repository context for RAG.
3.  **`glama.json`**: Standardized discovery manifest.
4.  **`.mcpb` Config**: Packaging configuration for specialized host distribution.

---

## 7. Phase 6: Deployment Scaffolding (Force Alignment)

Every SOTA webapp or server MUST include:
1.  **`start.ps1`**: PowerShell launcher with port cleanup (10700-11500 range).
2.  **`start.bat`**: Generic Windows double-click launcher.
3.  **Adjacent Ports**: If frontend is `10750`, backend MUST be `10751`.

---

## 8. SOTA-Certified Checklist

- [ ] `uv.lock` is committed.
- [ ] `ruff` (120 chars) check + format passes.
- [ ] All tool returns are structured Markdown ("Mud-to-Gold").
- [ ] FastMCP 3.2 `ctx.sample()` is used for reasoning steps.
- [ ] `llms.txt` and `glama.json` exist in root.
- [ ] `start.ps1` manages port squatter clearance.
- [ ] README includes a "SOTA v13.1 Compliance" badge.
