# GitHub Actions — no billable CI on private repositories

**Status:** Active (fleet mandatory)  
**Version:** 1.1 (2026-07-26)  
**Reason:** Private-repo Actions minutes bill to the account card; public repos use free standard runners.

## Rule

| Repo visibility | Workflow **file** in repo | GitHub runs it? |
|-----------------|---------------------------|-----------------|
| **Private** | **Mandatory** — lightweight Windows-only `ci.yml` | **No** — keep Actions **disabled** for private repos (account setting / `disable-actions-on-private-repos.ps1`) |
| **Public** | **Mandatory** — same Windows-only template | **Yes** — single job, no macOS, no Tauri in CI |

Agents MUST still ship `.github/workflows/ci.yml` and a local **`just ci`** (or equivalent) that runs the same checks. Private = no cloud minutes; quality gate is local.

## Lightweight Windows-only CI (mandatory shape)

One job on `windows-latest`:

1. `uv sync` (+ dev extras)
2. `ruff check` + `ruff format --check`
3. `pytest` (mocks / dry-run; no live network secrets)
4. webapp `npm ci` + `tsc --noEmit` + `biome check` (when webapp exists)

No Ubuntu dual matrix. No Codecov required. No Tauri/NSIS/PyInstaller in CI.

Canonical template: `mcp-central-docs/templates/ci.yml.template`  
Reference: `speech-mcp` / `mastodon-mcp` `.github/workflows/ci.yml`

## Account settings (do once)

1. GitHub → Settings → Billing — spending limit (e.g. $0–10).
2. Actions → General → **Disable actions for private repositories**.
3. Enforce: `mcp-central-docs/scripts/disable-actions-on-private-repos.ps1`

## Agents and new repos

- **Do** add Windows-only `.github/workflows/ci.yml` to every new `*-mcp` (public or private).
- **Do** add `just ci` and document it in `docs/DEVELOPMENT.md`.
- **Do not** re-enable Actions on a private repo without explicit user request.
- **Do not** add Linux+Windows matrices or release-build jobs without approval.
- Before "done": **`just ci` must be green locally**.

## Related

- [GIT_REPOSITORY_SAFETY.md](./GIT_REPOSITORY_SAFETY.md)
- [AGENTS.md](./AGENTS.md) §4.1 New Repo Gate ship checklist
- [AGENT_INSTALL_REFERENCE.md](./AGENT_INSTALL_REFERENCE.md)
