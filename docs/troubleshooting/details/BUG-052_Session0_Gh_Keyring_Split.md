# BUG-052 -- Session-0 `gh` Keyring Split (service sees stale auth, terminal is fine)

- **ID**: `BUG-052`
- **Severity**: `P1` (all `github_ops` + `gitops` pushes fail; the terminal works, so it masks as "already fixed" and burns re-auth loops)
- **Date**: 2026-09-27
- **Repo/Component**: `git-github-mcp` daemon on :10713 when hosted under the `mcp-federation-hub` NSSM service (LocalSystem, session 0). Applies to ANY session-0 `gh` consumer.
- **Status**: Fixed

## Symptom

- `github_ops(operation="auth_status")` via MCP: `Failed to log in ... The token in default is invalid`, `authenticated: false`.
- `git_core(operation="push")` via MCP: `remote: Invalid username or token. Password authentication is not supported for Git operations.` / `fatal: Authentication failed`.
- Same box, user terminal: `gh auth status` green, fresh token, `workflow` scope present. `gh auth login` and `gh auth refresh -s workflow` change nothing for the daemon.
- `gh auth login --with-token` (fed from `gh auth token`) also changes nothing: modern `gh` stores it in the keyring again, `hosts.yml` stays token-free (verified: file mtime bumped, still no `oauth_token`).

## Root Cause

Two credential stores, one `gh`:

1. Interactive-terminal `gh` reads the Windows Credential Manager (keyring) entry, which every browser-flow login/refresh updates.
2. The session-0 daemon (LocalSystem under NSSM -- even with `USERPROFILE`/`APPDATA`/`HOME` redirected to the user profile via `nssm set ... AppEnvironmentExtra`) cannot unlock the interactive-logon keyring entry, so `gh` falls back to `%APPDATA%\GitHub CLI\hosts.yml`, which contains only `user:` + `git_protocol:` and no `oauth_token`.
3. Result: terminal and daemon permanently disagree. Every terminal-side re-auth is invisible to the daemon.

Aggravator found during diagnosis: a dead hardcoded `GH_TOKEN` in the Claude Desktop config `gitops` `env` block. Env beats keyring everywhere, so one stale value poisons every host that reads that config. (Claude Desktop was not running in this session; fixed anyway as hygiene.)

Diagnosis chain that proved it on 2026-09-27 (Goliath):

- `Get-NetTCPConnection -LocalPort 10713` owner PID 27024 (`python`) -> parent 36560 -> 39004 (`git-github-mcp`) -> 36784 (`uv.exe`) -> ... -> 8808 (`uvicorn.exe`) -> 6572 (`nssm.exe`, service `mcp-federation-hub`) -> `services.exe`. All session 0.
- `sc.exe qc mcp-federation-hub` -> `SERVICE_START_NAME: LocalSystem`.
- `nssm get mcp-federation-hub AppEnvironmentExtra` -> profile redirected to `C:\Users\<user>`, but no token in env.
- `%APPDATA%\GitHub CLI\hosts.yml` -> user present, `oauth_token` absent.
- Terminal `gh auth status` -> green with `workflow` scope. Daemon `auth_status` -> invalid. QED.

## Resolution

- Backed up `hosts.yml`, inserted the current fresh token (scopes `repo`, `read:org`, `workflow`) as `oauth_token:` under `github.com:`. No service restart needed -- `gh` re-reads the file per invocation.
- Verified end to end via MCP: `auth_status` green (`hosts.yml` source listed) + no-op `push` (`Everything up-to-date`).
- Removed the dead hardcoded `GH_TOKEN` from `claude_desktop_config.json` `gitops` env (backup `claude_desktop_config.json.20260927_013700.bak`) so future keyring refreshes are not shadowed there.
- Fleet audit per protocol: fleet-wide grep for hardcoded `GH_TOKEN`/`GITHUB_TOKEN` values found no live instances -- only docs placeholders (`ghp_your_token_here`, `ghp_...`) in `git-github-mcp` docs, a clean `opencode.json`, and ~25 stale `.bak` copies of the Claude config holding the same dead token (inert, API-rejected). One live-adjacent copy remains: `claude_desktop_config2.json` still carries the dead token -- flagged, not edited (unknown reader).

## Never-again rules

- Never hardcode `GH_TOKEN` in MCP client configs. Let `gh` use the keyring; treat any stored token copy as rot-prone.
- Triage shortcut: `hosts.yml` without `oauth_token` + green terminal + red service = this bug. Check consumer session (`SessionId`, parent chain ending in `nssm.exe`/`services.exe`).
- Re-authing in the terminal does NOT fix session-0 consumers, and this file copy does NOT auto-rotate. After the next browser re-auth, repeat the `gh auth token` -> `hosts.yml` step.
- Long-term hardening (open): mint a dedicated fine-grained PAT for service contexts (separable, revocable) instead of copying the interactive OAuth token into a plaintext file. NSSM alternative: `nssm set <svc> AppEnvironmentExtra "GH_TOKEN=..."` + `sc.exe stop/start` (children inherit env).

## Log Snippet

```text
remote: Invalid username or token. Password authentication is not supported for Git operations.
fatal: Authentication failed for 'https://github.com/sandraschi/sandraschi.git/'
```

```text
github.com
  X Failed to log in to github.com account sandraschi (default)
  - Active account: true
  - The token in default is invalid.
```
