# CLI-Anything → meta-mcp Integration Plan

**Status**: Track A done, Track B1-B3 done | **Date**: 2026-07-01

## Overview

Two parallel tracks that converge. Track A (inspire_repo improvements) is the
prerequisite — it's the reconnaissance layer that Track B (harness generation)
feeds from. Ship Track A first, then Track B can rely on richer source analysis.

Paper: [CLI-Anything: Towards Agent-Native Computer Use](https://arxiv.org/abs/2606.03854)
Repo: [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything) — Apache 2.0, 44.4k stars

---

## Track A: inspire_repo Hardening (Days 1-3)

### Motivation

`inspire_repo` is already good — 1,845 lines, 7 tools, smart noise filtering,
semantic chapter output. But it has concrete gaps that block the harness-generation
use case. Each gap is surgical (30-90 min), not architectural.

### A1. Repository Metadata (highest leverage)

Right now `inspire_repo` reads zero repository metadata. It gets the file tree
and stops. For a "should I study/reuse this?" tool, that's the first question.

**Add**: One REST call to `GET /repos/{owner}/{repo}` at tree-fetch time.
Cache it alongside the tree (same TTL). Expose in response:

| Field | Source | Why |
|-------|--------|-----|
| `description` | `repo.description` | What is this project? |
| `topics` | `repo.topics` | Self-tagged categories |
| `stars` | `repo.stargazers_count` | Community signal |
| `license` | `repo.license.spdx_id` | Legal safety gate |
| `language` | `repo.language` | Primary language |
| `updated_at` | `repo.pushed_at` | Is it maintained? |
| `archived` | `repo.archived` | Is it dead? |
| `default_branch` | Already fetched, just expose it | — |

**Impact**: Before reading 15 source files, the agent knows if the repo is
archived, unlicensed, or has 2 stars. Saves wasted API calls.

**Files to touch**: `github_inspiration.py` (add `fetch_repo_meta()`),
`repo_inspiration_service.py` (call it in `_load_context`),
`repo_inspiration_profiles.py` (add metadata chapter kind).

### A2. File Content Caching

Tree is cached (300s TTL). File contents are fetched fresh every call.
If `inspire_repo_workflow` reads 5 files across 4 sub-calls, that's 20
requests — and 15 are duplicates.

**Add**: Per-session in-memory cache for file contents. Keyed by
`{owner}/{repo}@{branch}/{path}`. Same 300s TTL. Tiny change:

```python
# github_inspiration.py
_file_cache: dict[str, tuple[float, str]] = {}

async def get_file_content_cached(session, owner, repo, branch, path):
    cache_key = f"{owner}/{repo}@{branch}/{path}"
    now = time.monotonic()
    if cache_key in _file_cache:
        cached_at, content = _file_cache[cache_key]
        if now - cached_at < CACHE_TTL:
            return content
    content = await get_file_content(session, owner, repo, branch, path)
    _file_cache[cache_key] = (now, content)
    return content
```

**Files to touch**: `github_inspiration.py` (add cache dict + wrapper),
`repo_inspiration_service.py` (route through cache).

### A3. `operation` as `Literal` (SOTA compliance)

The portmanteau's `operation` parameter is raw `str`. The agent gets no
autocomplete or constraint. This fails TOOL_DESIGN_STANDARDS.md §4.

**Fix**: Change to `Literal["structure", "files", "patterns", "help"]`
in `repo_inspiration.py` tool registration.

**Files to touch**: `registries/repo_inspiration.py` (4x tool signatures).

### A4. Structured Error Types

All failures return `success: false` with English `message`. Agent must
parse prose to decide recovery. Standard says: include `error_type`.

**Add**: `error_type` field to failure responses. Enum:

`auth` | `not_found` | `rate_limited` | `network` | `invalid_input` | `truncated` | `unknown`

**Files to touch**: `repo_inspiration_service.py` (wrap all error returns),
`github_inspiration.py` (classify API errors by status code).

### A5. Multi-Manifest Detection

`inspire_repo_patterns` finds the first manifest and stops. Monorepos
(frontend `package.json` + backend `pyproject.toml`) lose the most
architecture-revealing signal.

**Fix**: Scan ALL manifests, not just the first. Return as a list in
`data.manifests[]`. The primary manifest gets the `manifest` chapter;
additional manifests get `manifest_secondary` chapters.

**Files to touch**: `repo_inspiration_service.py` (loop instead of
`next()`), `repo_inspiration_profiles.py` (manifest count in profile).

### A6. Rate Limit Tracking for Raw Fetches

Only the REST tree call exposes `X-RateLimit-Remaining`. Raw content
fetches from `raw.githubusercontent.com` don't report rate limits.
The service is blind to how many raw fetches it's burning.

**Fix**: Track raw fetch count in `_load_context()`. Return it as
`data.raw_fetches` in response metadata. Simple counter, no API changes.

### A7. Output Schema (nice-to-have)

None of the 7 tools set `output_schema=`. The response shape is stable.
Add `output_schema` to `inspire_repo` and `inspire_repo_structure`
as the two most-called tools.

**Files to touch**: `registries/repo_inspiration.py`.

### A8. API Surface Extraction (new capability, for Track B)

`inspire_repo` tells you *what files exist*. A harness generator needs
to know the *API surface* — function signatures, CLI flags, class hierarchies.

**Add**: New `operation="surface"` on `inspire_repo`. For Python repos,
runs `ast.parse()` against key source files and extracts:

- Function signatures (name, args, return type hint if present)
- Class definitions (name, base classes, public methods)
- Click/argparse CLI argument definitions
- Decorator usage (`@mcp.tool()`, `@app.get()`, etc.)

This is a **remote AST analysis** — fetch raw files, parse with `ast`,
return structured surface. No local clone needed. For non-Python repos,
return a language hint and suggest manual `inspire_repo_files`.

**Files to touch**: New file `utils/repo_inspiration_surface.py`,
new tool registration, profile limit for surface extraction.

**Why this matters for Track B**: This is the bridge. `harness_analyze`
feeds `surface` output into the `ToolSurfaceSpec` generation.

---

## Track B: Harness Generation (Days 4-10)

Track B assumes Track A items A1-A8 are done. It depends on:
- `inspire_repo(operation="surface")` (A8) — API surface extraction
- Structured error types (A4) — reliable pipeline orchestration
- File content caching (A2) — multi-phase generation without redundant fetches

### B1. `harness_analyze` — Source Analysis (Days 4-6)

New meta-mcp tool that wraps the reconnaissance into a structured spec.

```
harness_analyze(source_path: str | github_url: str, full: bool = False)
  → ToolSurfaceSpec
```

**Pipeline**:
1. If GitHub URL: call `inspire_repo(operation="structure")` + `(operation="surface")`
2. If local path: walk directory, `ast.parse()` key files directly
3. Group extracted functions/methods by domain (heuristic: same file = same domain, or class-based grouping)
4. Map domains to portmanteau tool names (verb-led snake_case per fleet standard)
5. Apply curation: `full=False` → drop internal/private methods, `_`-prefixed, test utilities, boilerplate getters/setters
6. Detect backend engine type (subprocess wrapper, REST API, Python import, CLI wrapper)
7. Output `ToolSurfaceSpec` dict

**Curation rules** (the key differentiator from CLI-Anything's dump-everything approach):

| Rule | What it drops |
|------|---------------|
| `_`-prefix methods | Internal/private |
| Single-line getters/setters | `def get_foo(self): return self._foo` |
| Test files | `test_*`, `*_test`, `conftest` |
| `__init__`, `__repr__`, `__str__` | Python dunders |
| Methods with no docstring AND no type hints AND < 5 lines | Undocumented stubs |
| Methods in `migrations/`, `scripts/`, `fixtures/` | Infrastructure, not API |

**`ToolSurfaceSpec` schema**:
```python
{
    "software_name": str,
    "source_type": "github" | "local",
    "source_path": str,
    "backend_engine": "subprocess" | "rest_api" | "python_import" | "cli_wrapper",
    "backend_details": {"command": str | None, "api_base": str | None, ...},
    "language": str,
    "tool_groups": [
        {
            "name": str,            # e.g. "blender_scene"
            "domain": str,          # e.g. "Scene management"
            "curated": bool,        # True = passed curation filter
            "operations": [
                {
                    "name": str,         # e.g. "add_object"
                    "signature": str,    # "add_object(type: str, location: tuple[float,float,float]) -> str"
                    "params": [...],     # extracted from AST
                    "docstring": str | None,
                    "is_mutating": bool,
                },
                ...
            ],
        },
        ...
    ],
    "state_model": "session" | "stateless" | "project_file",
    "warnings": [str],  # missing dependencies, unparseable files, etc.
}
```

### B2. `harness_generate` — Server Generation (Days 7-9)

Consumes `ToolSurfaceSpec` and generates a fleet-conformant FastMCP server.

```
harness_generate(spec: ToolSurfaceSpec, target_path: str, include_nsis: bool = False)
  → dict
```

**Architecture**: Extends `server_builder_sota.py`, does NOT fork it.

Instead of generating `example_portmanteau.py`, it takes the spec's
`tool_groups` and generates one portmanteau tool per group. Each tool:

1. Has the `operation: Literal[...]` discriminator from the spec's operations
2. Has a proper SOTA docstring (summary, `[RATIONALE]`, `## Return Format`, `## Examples`)
3. Uses `Annotated[T, Field(description=...)]` for all parameters
4. Has `annotations=MUTATING` or `READ_ONLY` based on spec analysis
5. Implements:
   - For `backend_engine="subprocess"`: `subprocess.run()` wrapper with proper error handling
   - For `backend_engine="rest_api"`: `httpx` async client
   - For `backend_engine="python_import"`: direct import + call
   - For `backend_engine="cli_wrapper"`: Click/argparse invocation

**Also generates**:
- `SKILL.md` from tool groups (replacements for `skill_generator.py` logic)
- Prefab status card (`show_{name}_status_card`)
- Domain-specific test stubs (unit + integration) per tool group
- `{repo}-backend.spec` for PyInstaller (if backend is Python)
- Port registration in WEBAPP_PORTS.md (allocates next available pair)

**Template strategy**: `server_builder_sota.py` gets a new entry point:

```python
def generate_from_surface_spec(spec: dict, target_path: str) -> dict:
    """Generate a full FastMCP server from a ToolSurfaceSpec.
    
    Uses the same building blocks as generate_sota_package_files()
    but parameterizes tool generation from the spec instead of
    generating example_portmanteau.py.
    """
```

### B3. `harness_refine` — Iterative Improvement (Day 10)

```
harness_refine(
    operation: Literal["gap", "add", "test"],
    repo_path: str,
    spec_focus: str | None = None,
) → dict
```

- **`gap`**: Re-run `harness_analyze` against the original source, diff against
  the current MCP server's tool surface. Returns added/removed/changed operations.
- **`add`**: Add missing operations from gap analysis (non-destructive — never
  removes existing tools). Only adds `curated=True` operations.
- **`test`**: Regenerate test stubs for added operations. Does NOT overwrite
  existing test implementations.

### B4. `scaffold_questionnaire` Extension

Add a "Harness from Source" tab to the existing Prefab questionnaire card:

- Source input: GitHub URL or local path
- Show derived tool groups (preview before generation)
- Toggle `include_nsis`, `include_mcpb`, curation level
- Calls `harness_analyze` → preview → `harness_generate` on confirm

---

## Dependency Graph

```
Track A (inspire_repo hardening)
│
├── A1: Repo metadata ───────────── independent
├── A2: File content caching ────── independent
├── A3: operation as Literal ────── independent
├── A4: Structured error types ──── independent
├── A5: Multi-manifest detection ── independent
├── A6: Rate limit tracking ─────── independent
├── A7: Output schema ───────────── independent
└── A8: API surface extraction ──── depends on: A2, A4
                                     │
                                     ▼
Track B (harness generation) ─────── depends on: A2, A4, A8
│
├── B1: harness_analyze ──────────── depends on: A8 (surface extraction)
├── B2: harness_generate ─────────── depends on: B1 (ToolSurfaceSpec)
├── B3: harness_refine ───────────── depends on: B1, B2
└── B4: questionnaire extension ──── depends on: B1, B2
```

## Derisking Test

Before building anything, validate the approach with a concrete end-to-end:

1. Run `inspire_repo(operation="surface")` against `HKUDS/CLI-Anything` itself
   (or a smaller target like `httpie/cli` or `pandoc`).
2. Manually inspect the extracted `ToolSurfaceSpec` — does it capture the
   real API surface? What does curation drop that it shouldn't?
3. If the spec looks right, run `harness_generate` against it.
4. Verify: generated server starts, `/health` returns 200, tools are registered.

**Target for derisking**: `pandoc` (well-defined CLI surface, no existing fleet
server, easy to verify with `pandoc --version`).

## License Compliance

CLI-Anything is Apache 2.0. Our usage:

- Methodology adaptation (HARNESS.md principles → Python logic): no license issue
- `skill_generator.py` adaptation: requires Apache 2.0 attribution in meta-mcp NOTICE
- Test patterns (subprocess CLI testing): requires attribution
- No code fork, no vendored files — all new implementation

Attribution file to add: `meta-mcp/NOTICE` referencing `HKUDS/CLI-Anything`
(Apache 2.0, 2026) as inspiration source.

## Effort

| Track | Items | Days |
|-------|-------|------|
| A1-A3 | Metadata, caching, Literal fix | 1 |
| A4-A7 | Error types, multi-manifest, rate tracking, output schema | 1 |
| A8 | API surface extraction (new capability) | 1 |
| B1 | `harness_analyze` | 2 |
| B2 | `harness_generate` | 3 |
| B3 | `harness_refine` | 1 |
| B4 | Questionnaire extension | 0.5 |
| **Total** | | **9.5** |

Conservative estimate: **10 days** (2 weeks with testing/buffer).
