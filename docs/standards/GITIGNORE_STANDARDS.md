# Gitignore & VCS hygiene (SOTA)

> **Mandatory for all MCP repos** (Python + optional Node/webapp + Rust + Docker). Prevents bloated remotes, leaked secrets, and broken clones.
>
> **ALWAYS create `.gitignore` BEFORE `git add -A`.** LLMs habitually skip this step and commit node_modules, target/, and data/. It's the #1 most common and most expensive rookie mistake.
>
> **New-repo gate:** `standards/AGENTS.md` §4.1 ship checklist items **9–10** — good `.gitignore` + `.mcpbignore` are HARD. No `node_modules`, Tauri `target/`, or `.venv` on the remote.

## 1. Never commit these paths

| Category | Patterns (non-exhaustive) | Why |
|----------|----------------------------|-----|
| **Node** | `node_modules/`, `**/node_modules/` | Huge, reproducible via `npm install` / `pnpm i`; **Vite** may write `node_modules/.vite/` — still under `node_modules/`. |
| **Python** | `.venv/`, `venv/`, `env/`, `__pycache__/`, `*.py[cod]`, `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/` | Env + bytecode + tool caches. |
| **Rust** | `target/` | Build output. **Fleet:** include this even in **Python-only** repos — **Zed** (and other editors running **rust-analyzer** / LSP) may create a root `target/` directory for workspace metadata; it must not be committed. |
| **Secrets** | `.env`, `.env.*`, `*.pem`, key stores | **Never** in git; use `.env.example` only. |
| **OS / IDE** | `.DS_Store`, `Thumbs.db`, `.idea/`, `.vscode/` (optional team policy) | Noise; align per repo. |
| **MCPB staging** | `mcpb/src/`, often whole `mcpb/` | Exact copy of `src/` for `mcpb pack` — build artifact, goes stale if committed |
| **Logs / caches** | `*.log`, `logs/`, project-specific cache dirs | Unbounded size. |
| **Fleet mass-fix / sneak-in backups** | **`*.bak`** and **`*.bak.*`** (both required) | Timestamped specialist backups accumulate fast: `file.20260701_030123.bak`, `file.bak.20260701`, `*_YYYYMMDD_HHMMSS.md.bak`. Always ignore both patterns — never commit them. |

**Rule:** If it is **installable** or **regenerable** from a lockfile or package manifest, it does **not** belong in Git.

## 1b. Fleet .gitignore template (copy-paste ready)

```gitignore
# Go (not in fleet yet, but when it arrives)
*.exe
*.exe~
*.dll
*.so
*.dylib
go.work
go.work.sum

# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
env/
.mypy_cache/
.pytest_cache/
.ruff_cache/

# Node / webapp
node_modules/
**/node_modules/
.next/
*.tsbuildinfo

# Rust / Tauri (FLEET: commonly forgotten!)
target/
native/target/
web_sota/src-tauri/target/
gen/

# Build output
dist/
build/
*.spec
*.exe
!run_server.py
*.mcpb

# MCPB pack staging (exact copy of src/ for packing — never commit)
mcpb/src/
mcpb/

# Tauri resources (PyInstaller binaries — gitignored, bundled at build)
native/resources/*.exe
native/binaries/*.exe

# Data / DB
data/
*.db
*.db-shm
*.db-wal

# Secrets
.env
.env.*
!.env.example
*.pem

# OS
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/

# Logs
*.log
logs/

# Fleet backup artifacts
*.bak
*.bak.*

# Docker
.docker/
```

> Add `native/target/` and `gen/` for Tauri 2.0 repos. The `native/resources/*.exe` and `native/binaries/*.exe` patterns prevent committed PyInstaller binaries. `data/` and `*.db*` prevent committed SQLite databases.

## 2. Root `.gitignore` requirements

- Every repo MUST have a **root** `.gitignore` covering at least **Python + Node** if the tree contains both (e.g. `web_sota/`, `frontend/`).
- Include **`*.bak` and `*.bak.*`** (both) so sneak-in specialist / mass-fix timestamped backups never get committed. `*.bak` alone misses `foo.bak.20260701`; `*.bak.*` alone misses `foo.20260701.bak`.
- **Rust `target/` (mandatory on fleet):** Add **`target/`** at repo root even when the project is not a Rust crate — **Zed IDE** integration and **rust-analyzer** often emit `target/` at the repository root; without this line, `git status` fills with build artifacts.
- **Before** `git add .` on a large change, run:
  - `git status` and spot-check for `node_modules`, `venv`, `.env`.
- **Agents / automation:** Do not run blind `git add .` without verifying ignore rules exist for new ecosystems (e.g. adding a Vite app → ensure `node_modules/` is ignored **before** first commit).

## 3. Accidentally committed `node_modules` (or venv)

1. Add patterns to `.gitignore`.
2. `git rm -r --cached path/to/node_modules` (files stay on disk).
3. Commit the fix.
4. If already **pushed** and history must be clean: rewrite history, e.g.  
   `git filter-repo --path path/to/node_modules --invert-paths --force`  
   then `git push --force` (coordinate with collaborators; they must re-clone or hard-reset to `origin`).

## 4. Related central docs

- **[WEBAPP_STANDARDS.md](./WEBAPP_STANDARDS.md)** — Ports, webapp layout (frontend deps stay local).
- **[Packaging / MCPB](./PACKAGING_STANDARDS.md)** — What **is** shipped in bundles vs repo.
- Archived Git etiquette: [not-mcp-related/git-github/git/etiquette.md](../not-mcp-related/git-github/git/etiquette.md) (general `.gitignore` notes).

## 5. Review

- **Owner:** Sandra Schi  
- **Trigger:** New subproject (webapp, extension) added to a repo → extend `.gitignore` in the **same PR**.

**Version:** 1.1 (2026-03-23) — fleet `target/` + Zed / rust-analyzer note
