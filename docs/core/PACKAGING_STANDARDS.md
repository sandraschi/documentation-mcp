# Packaging & Discovery Standards (SOTA)

## 0. Two-Track Distribution (READ FIRST)

Every fleet server has **two distinct install surfaces** that solve different problems:

| Track | Artifact | Solves | Does NOT solve |
|---|---|---|---|
| **Claude Desktop MCP install** | `.mcpb` bundle | Single-click server registration in Claude Desktop; env var prompting; curated directory listing | Python runtime; webapp; scheduler; naked-PC prereqs |
| **Full app install (webapp + backend)** | `start.bat` + `start.ps1` | Everything — prereqs, deps, ports, webapp, scheduler, browser open | Nothing extra needed |

**Both tracks are mandatory.** They are complementary, not alternatives.

- `.mcpb` is for developer users installing via Claude Desktop. It does not replace `start.bat`.
- `start.bat` is for running the full stack (Starlette backend + Vite webapp). It does not replace `.mcpb`.
- For Python servers, `.mcpb` still requires the user to have Python — the single-click promise is partial. Anthropic recommends Node.js for fully self-contained bundles, but FastMCP Python is the fleet standard and we accept this tradeoff.
- **Steve-class users** (non-dev, naked PC) need `start.bat` with the `Require-Command` pattern from [NAKED_PC_INSTALL_STANDARD.md](./NAKED_PC_INSTALL_STANDARD.md). mcpb alone will not help them.

**What native installers bundle:** MCP server + webapp only. **Never** host apps (Blender, Unity Editor), LLM runtimes (Ollama, vLLM), or model weights. See **[LLM_AND_INSTALL_TIERS.md](./LLM_AND_INSTALL_TIERS.md)** and [tauri_godot_sota.md](./rules/tauri_godot_sota.md).

---



The official standard for Claude Desktop.

- **Source Code**: Must be self-contained in `src/`.
- **Assets**: 
    - `assets/icon.png`: 256x256px identifying icon.
- **NO Dependencies**: Do not bundle external libraries in the package.
- **FORBIDDEN**: Never use `mcpb init` or `mcpb create` (generates broken manifests).

## 2. SOTA Prompting (3-4-100 Rule)

A SOTA package is defined by its prompts:
- **system.md**: 3,000+ words of core capabilities.
- **user.md**: 4,000+ words of natural language tutorials.
- **examples.json**: 100+ structured tool call mappings.

## 3. Global Discovery

### 3.1. Glama (`glama.json`)
Placed in repository root. Enables indexing in the Glama MCP registry. **Exclude** from the `.mcpb` build.

### 3.2. LobeHub
Expose machine-readable manifest at `/.well-known/mcp/manifest.json`.

## 4. Stability & Isolation

Use `@mcp.lifespan()` to manage long-running processes and ensuring resource persistence across restarts.

---

## 5. Python MCP repo: **uv**, **justfile**, **llms.txt** + **llms-full.txt**, **Glama**, **MCPB pack**

These are **fleet build standards** for new and maintained **Python** MCP servers. Together they cover day-to-day dev, LLM discovery, registry indexing, and Claude Desktop bundles.

| Artifact | Requirement |
|----------|-------------|
| **uv** | Use **[Astral uv](https://docs.astral.sh/uv/)** for installs and lockfile: `pyproject.toml`, committed **`uv.lock`**, workflows use `uv sync` and `uv run …`. Legacy pip-only setups are discouraged unless explicitly grandfathered. |
| **justfile** | Root **`justfile`** with discoverable recipes (e.g. `serve`, `test`, `lint`, `fmt`; optional **`mcpb-pack`** or `pack-mcpb`). Same commands CI should invoke where possible. |
| **llms.txt** | Root **`llms.txt`** (**required**): tight LLM **index** (links + summary); must reference **`llms-full.txt`**. [integrations/llms-txt-manifest.md](../integrations/llms-txt-manifest.md). |
| **llms-full.txt** | Root **`llms-full.txt`** (**required**): long-form LLM doc — tools, env, architecture, troubleshooting. See [DOCUMENTATION_STANDARDS.md](./DOCUMENTATION_STANDARDS.md) §1. |
| **glama.json** | Root **`glama.json`** per **§3.1** (Glama / discovery). Required for registry visibility. |
| **MCPB pack** | For **`.mcpb`** releases: run **`mcpb pack . dist/<name>.mcpb`** from a layout that satisfies **[MCPB_PACKAGING_STANDARDS.md](./MCPB_PACKAGING_STANDARDS.md)** (`manifest.json`, assets, `src/`, no `mcpb init`). Optional in CI on version tags. **`glama.json` stays in the repo only** — exclude from the bundle per MCPB rules. |

**Gitingest (optional, not a build artifact):** [Gitingest](https://gitingest.com) is **recommended agent ergonomics** when you need a **one-shot, live** text bundle of **any** public GitHub tree (or a subpath) — e.g. auditing a dependency, onboarding to a third-party MCP, or quick context without a clone. It is **not** part of the **required** fleet bar above: your own repos still ship **`llms.txt` + `llms-full.txt`** as the **versioned, curated** LLM entry points. Use **both** roles intentionally — comparison and automation hooks in **[integrations/llms-txt-manifest.md](../integrations/llms-txt-manifest.md)** § Gitingest (e.g. git-github-mcp `gitingest_*` operations).

**Full MCPB layout, manifest fields, CI examples, and forbidden commands** → [MCPB_PACKAGING_STANDARDS.md](./MCPB_PACKAGING_STANDARDS.md).

**Documentation file list (README, CHANGELOG, …)** → [DOCUMENTATION_STANDARDS.md](./DOCUMENTATION_STANDARDS.md) (includes **llms.txt** + **llms-full.txt**, both required).

---

## 6. Optional ergonomics: **pre-commit (Ruff)**, **`ty` in CI (non-blocking)**

| Practice | Requirement |
|----------|-------------|
| **Pre-commit + Ruff** | Repos SHOULD include **`.pre-commit-config.yaml`** with **[astral-sh/ruff-pre-commit](https://github.com/astral-sh/ruff-pre-commit)** (`ruff`, `ruff-format`). After clone: `pre-commit install` (or run `pre-commit run --all-files` in CI). Keeps format/lint consistent without relying on memory. Details → [CODE_QUALITY_STANDARDS.md](./CODE_QUALITY_STANDARDS.md). |
| **`ty` (Astral)** | Add **`ty`** as an optional dev dependency; run **`ty check`** (e.g. `uv run ty check src`) in **CI** with **`continue-on-error: true`** (or equivalent) until diagnostics are clean — then flip to **blocking**. Do not block shipping on `ty` during adoption. Same file → [CODE_QUALITY_STANDARDS.md](./CODE_QUALITY_STANDARDS.md). |
