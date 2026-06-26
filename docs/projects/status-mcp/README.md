# status-mcp — Goliath Status Server for Claude iOS

Minimal remote-pull MCP server. Exposes Goliath's working state — latest advanced-memory
notes, repo changelogs, recent repo activity, Claude Desktop MCP logs — over streamable-HTTP
so Claude on iOS (claude.ai custom connector) can pick up session context from anywhere.

**One file, four tools, zero database.** Reads straight from the filesystem; never touches
`memory.db`, so it cannot participate in the SQLite WAL/lock contention between IDEs.

## Tools

| Tool | Purpose |
|------|---------|
| `get_status(n=3)` | Latest *n* vault notes, newest first, 4000-char cap per note, sensitive folders excluded (see below). The "what was I doing" call at chat start. |
| `get_changelog(repo)` | First 8000 chars of `CHANGELOG.md` for a repo under `D:\Dev\repos`. Path-traversal guarded. |
| `list_recent_repos(n=10)` | Repos by directory mtime. **Caveat:** dir mtime only bumps on direct-child changes — deep edits (`src/foo.py`) won't surface. Triage-grade only. |
| `tail_mcp_log(server, lines=50)` | Tail `mcp-server-<name>.log` from Claude Desktop logs. Path-traversal guarded. |

## Paths (hardcoded, this machine)

| What | Where |
|------|-------|
| Notes vault | `C:\Users\sandr\.advanced-memory\vault` |
| Repos | `D:\Dev\repos` |
| MCP logs | `C:\Users\sandr\AppData\Roaming\Claude\logs` |

## Configuration (env vars)

| Var | Default | Purpose |
|-----|---------|---------|
| `STATUS_PORT` | `10765` | Listen port. (8765 clashes with Magenta RT on Goliath.) |
| `STATUS_PATH` | `/mcp` | Mount path. **Set to a secret path before Funnel exposure**, e.g. `/h4x9q2-mcp`. |
| `GOLIATH_STATUS_TOKEN` | unset | If set, enables bearer-token auth (`StaticTokenVerifier`). Only useful if the connecting client can send the header. |
| `STATUS_EXCLUDE` | see below | Comma-separated keywords; any note whose path component (folder or filename, case-insensitive substring) matches one is never served. |

Default exclusion keywords: `personal, private, journal, diary, reflections, travel,
security, incident, secret, credential, confidential, internal, vienna-life`. Against the
live vault this excludes 14 of 119 top-level folders (`10-personal`, `personal`, `private`,
`docs-private`, `13-journal`, `journal`, `reflections`, `11-travel`, `security`,
`security-critical`, `security-tools`, `enterprise-security`, `incidents`,
`vienna-life-assistant-updates`) plus any stray matching filenames anywhere in the tree.
Verified no false positives: `project-status`, `status-reports`, `GIT_SETUP_STATUS.md` serve normally.

## Run

```powershell
# direct
$env:STATUS_PATH = "/h4x9q2-mcp"
python status_mcp.py

# as a service (same pattern as RustDesk)
nssm install goliath-status "C:\Users\sandr\AppData\Local\Programs\Python\Python313\python.exe" "D:\Dev\repos\status-mcp\status_mcp.py"
nssm set goliath-status AppEnvironmentExtra STATUS_PATH=/h4x9q2-mcp
nssm start goliath-status
```

## Expose via Tailscale Funnel

```powershell
tailscale funnel 10765
# -> https://goliath.tailXXXX.ts.net/h4x9q2-mcp
```

Funnel requires the `funnel` node attribute in the tailnet ACL policy and Tailscale ≥ 1.38.3.
Manageable via tailscale-mcp's `manage_funnel` tool (`funnel_enable`, `funnel_disable`,
`funnel_status`, `funnel_list`, `funnel_certificate_info`).

Then: claude.ai → Settings → Connectors → Add custom connector → the Funnel URL.
On iOS, toggle the connector on in the chat's tools menu. First message "status" pulls the notes.

## Security model

This is a **public-internet endpoint to a read-only slice of the workstation**. Layers, in order
of preference:

1. **Secret path** (`STATUS_PATH`) — works with any client including the claude.ai connector UI,
   which may not offer a bearer-token field for non-OAuth servers. Obscurity, not auth, but the
   attack surface is four read-only tools.
2. **Bearer token** (`GOLIATH_STATUS_TOKEN`) — real auth, verified working (401 without/with
   wrong token). Enable if the client can send the header.
3. **Vault exclusion filter** — personal/private/journal/travel/security folders and files
   never leave the machine regardless of auth state (`STATUS_EXCLUDE`).
4. **Inherent limits** — no write operations, path-traversal guards on user-supplied names,
   per-note and per-changelog output caps.

What still leaks if the path is discovered without a token: non-excluded note contents,
changelog contents, MCP log tails (which can contain tokens echoed by misbehaving servers).

## Verification status (2026-06-11)

Tested in a Linux container against **fastmcp 3.4.2**, paths swapped to container equivalents:

- All four tools return correct results over streamable-HTTP via a real MCP client
- `mcp.run(transport="http", ...)` — `"http"` is an accepted alias across 3.x
- `StaticTokenVerifier`: 401 on missing token, 401 on wrong token, success with valid token
- Custom `path=` mount: secret path serves, default `/mcp` correctly 404s
- Exclusion filter: tested against the full live vault folder list (119 top-level dirs) —
  14 excluded, filename-level strays caught, zero false positives
- **Not yet verified on Goliath itself:** live Funnel exposure, claude.ai connector handshake,
  NSSM service operation

## Non-goals

- No write access of any kind
- No advanced-memory DB access (filesystem only, by design)
- No webapp, no dashboard — this is plumbing, not a product
