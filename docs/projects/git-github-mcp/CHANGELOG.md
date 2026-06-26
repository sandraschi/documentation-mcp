# Changelog

## 0.2.0 (2026-05-02)

### Fixed
- **Clone/push/pull/fetch timeout too short** — `server.py` had a blanket 25s `asyncio.wait_for` wrapper
  around all git operations, killing network operations before the inner `_run_git_async` subprocess
  timeout (120s for clone) could fire. The outer wrapper now uses an operation-aware timeout:
  180s for `clone`, `push`, `pull`, `fetch`; 25s for all local operations.

### Added
- **`depth` parameter on `git_core`** — Exposes `--depth N` shallow clone support. Pass `depth=1`
  for large repos to get the current tree without full history (seconds instead of minutes for
  repos like vscode or linux kernel).
- **Context-aware clone error messages** — Timeout errors now return a specific, actionable message
  explaining the cause (large repo / slow connection) and suggesting the `depth=1` shallow clone as
  the remedy, including a ready-to-run PowerShell fallback command. Generic auth/network errors
  retain their existing messages.

### Files Changed
- `src/git_github_mcp/server.py` — Operation-aware `_wall_timeout`; `depth` param threaded through
  `_run_git_tool` wrapper and `git_core` MCP tool signature
- `src/git_github_mcp/tools/git_ops.py` — `depth` param on `git_ops()`; `--depth N` injected into
  clone args; timeout-specific error branch with actionable recovery message



- Initial release
- git_ops: clone, status, add, commit, push, pull, branch, tag, stash
- github_ops: create_issue, list_issues, create_pr, list_prs, search (via gh CLI)
- FastMCP 3.1.1+.4+, Literal enums for discoverability, dialogic response patterns

