# Gitignore & VCS hygiene (SOTA)

> **Mandatory for all MCP repos** (Python + optional Node/webapp + Rust + Docker). Prevents bloated remotes, leaked secrets, and broken clones.

## 1. Never commit these paths

| Category | Patterns (non-exhaustive) | Why |
|----------|----------------------------|-----|
| **Node** | `node_modules/`, `**/node_modules/` | Huge, reproducible via `npm install` / `pnpm i`; **Vite** may write `node_modules/.vite/` — still under `node_modules/`. |
| **Python** | `.venv/`, `venv/`, `env/`, `__pycache__/`, `*.py[cod]`, `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/` | Env + bytecode + tool caches. |
| **Rust** | `target/` | Build output. **Fleet:** include this even in **Python-only** repos — **Zed** (and other editors running **rust-analyzer** / LSP) may create a root `target/` directory for workspace metadata; it must not be committed. |
| **Secrets** | `.env`, `.env.*`, `*.pem`, key stores | **Never** in git; use `.env.example` only. |
| **OS / IDE** | `.DS_Store`, `Thumbs.db`, `.idea/`, `.vscode/` (optional team policy) | Noise; align per repo. |
| **Build / dist** | `dist/` (when generated), `build/`, `*.egg-info/` | Regenerable; exception: **committed** `dist/` only if project policy explicitly requires it (rare). |
| **Logs / caches** | `*.log`, `logs/`, project-specific cache dirs | Unbounded size. |

**Rule:** If it is **installable** or **regenerable** from a lockfile or package manifest, it does **not** belong in Git.

## 2. Root `.gitignore` requirements

- Every repo MUST have a **root** `.gitignore` covering at least **Python + Node** if the tree contains both (e.g. `web_sota/`, `frontend/`).
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
