# Documentation Standards

## 1. Required Files

Every SOTA MCP repository MUST have the following at the root:

1.  **README.md**: Features, installation, quick start, and links to detailed docs. **High-risk servers** (e.g. **pywinauto-mcp**, host desktop control): MUST link prominently to **`docs/SAFETY.md`** (or equivalent) and to fleet **mcp-central-docs** patterns when isolation requires a second server (e.g. **virtualization-mcp** for Windows Sandbox).
    - **Install order (fleet bar):** If the README shows **`uv sync`** (including **`uv sync --dev`**, **`--extra …`**, etc.), it MUST also show **obtaining the source first** and working from the **repository root** — e.g. **`git clone <url>`** then **`cd`** / **`Set-Location`** into that directory (or **`gh repo clone …`**, unpack, submodules, as appropriate). **`uv` has nothing to sync until the project exists on disk.** The same idea applies to Node: **`npm install`** / **`npm ci`** only after checkout at repo root. Canonical dev flow: **[DEPLOYMENT_STANDARDS.md](./DEPLOYMENT_STANDARDS.md) §2**. **`docs/INSTALL.md`** and **`llms-full.txt`** run-command sections SHOULD follow the same order when they include `uv sync`.
2.  **CHANGELOG.md**: Version history following semantic versioning (MAJOR.MINOR.PATCH).
3.  **LICENSE**: MIT or Apache 2.0 preferred.
4.  **docs/**: Organized folder for specialized documentation.
5.  **docs-private/**: (Git-ignored) Internal dev notes, progress reports, and scratch work.
6.  **`.gitignore`**: MUST exclude dependencies and caches per **[GITIGNORE_STANDARDS.md](./GITIGNORE_STANDARDS.md)** (`node_modules/`, `.venv/`, etc.).
7.  **`llms.txt`** (repository root, **required**): LLM-facing **index** — H1, short blockquote pitch, `##` sections with links; must point to **`llms-full.txt`**. Part of the **[packaging / discovery bar](./PACKAGING_STANDARDS.md#5-python-mcp-repo-uv-justfile-llmstxt-glama-mcpb-pack)** alongside `glama.json` and MCPB. **How-to:** [integrations/llms-txt-manifest.md](../integrations/llms-txt-manifest.md).
8.  **`llms-full.txt`** (repository root, **required**): LLM-facing **full corpus** — complete tool/prompt list, env tables, architecture, ports, troubleshooting, run commands (no need to keep short; avoid duplicating-only README without structured sections). **`llms.txt`** stays the skimmable entry; **`llms-full.txt`** holds depth. Ecosystem naming per [llmstxt.org](https://llmstxt.org/) / common two-file convention.

**Gitingest:** Optional **runtime** aid for **external** or **live** repo text dumps — **not** a replacement for items 7–8 on repos you maintain. See **[PACKAGING_STANDARDS.md §5](./PACKAGING_STANDARDS.md#5-python-mcp-repo-uv-justfile-llmstxt-glama-mcpb-pack)** (Gitingest note) and **[integrations/llms-txt-manifest.md](../integrations/llms-txt-manifest.md)** § Gitingest.

## 2. Standard Structure (`docs/`)

```
docs/
├── integration-guide.md  # Claude Desktop / Client setup
├── architecture.md       # System design and data flow
├── tools-reference.md    # Complete API reference
├── configuration.md      # Environment variables and settings
├── troubleshooting.md    # Common issues and solutions
└── examples/             # Working code snippets
```

## 3. Maintenance

- **Continuous Updates**: Documentation is updated alongside every feature addition or bug fix.
- **Monthly Reviews**: Check for broken links and stale examples.
- **PRD Standards**: Large features require a PRD in the artifacts directory during PLANNING.
