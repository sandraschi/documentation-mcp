# GitHub Actions — no CI on private repositories

**Status:** Active (fleet mandatory)  
**Version:** 1.0 (2026-06-02)  
**Reason:** Private-repo Actions minutes bill to the account card; public repos use free standard runners. A 2025–2026 CI runaway produced a large Actions backlog.

## Rule

| Repo visibility | GitHub Actions |
|-----------------|----------------|
| **Private** | **Disabled** — no workflows, no `workflow_dispatch`, no scheduled runs |
| **Public** | Allowed when needed — prefer **one** job, **Windows or Linux** (not both), no macOS, no Tauri/PyInstaller in CI unless explicitly approved |

## Account settings (do once after card update)

1. GitHub → **Settings** → **Billing and plans** — pay backlog, set a **monthly spending limit** (e.g. $0–10).
2. GitHub → **Settings** → **Actions** → **General**:
   - Under *Actions permissions*, choose **Disable actions** for **private repositories** (or “Disable actions for all repositories” if you only use public fleet repos for CI).
3. Optional org equivalent if repos live under an organization.

## Per-repo enforcement (API)

```powershell
# Fleet script (idempotent):
pwsh -File D:\Dev\repos\mcp-central-docs\scripts\disable-actions-on-private-repos.ps1
```

Sets `PUT /repos/{owner}/{repo}/actions/permissions` → `enabled: false` for every **private** repo you own.

Workflow files may remain in git for reference; **GitHub will not run them** while disabled.

## Agents and new repos

- **Do not** add `.github/workflows/*.yml` to new **private** `*-mcp` repos.
- **Do not** re-enable Actions on a private repo without explicit user request.
- Quality gates: run **locally** — `just check`, `uv run pytest`, `just build-native` (Windows), `just mcpb-pack`.
- When a repo must have CI: make it **public** or use an external runner (self-hosted on your PC, not GitHub-hosted).

## Public repo CI hygiene (when CI is allowed)

- Single workflow job per event where possible.
- Tag-only release builds; no Windows Tauri in CI (build locally, upload to Releases).
- See `speech-mcp` `.github/workflows/` as a minimal Windows-only example.

## Related

- [GIT_REPOSITORY_SAFETY.md](./GIT_REPOSITORY_SAFETY.md)
- [AGENT_INSTALL_REFERENCE.md](./AGENT_INSTALL_REFERENCE.md) — local install tiers, Tauri local build
