---
project: status-mcp
status: active
priority: medium
tags: [status, remote-access, ios, tailscale, funnel, advanced-memory, fastmcp, streamable-http]
created: 2026-06-11
updated: 2026-06-11
ports: [10765]
repo: D:\Dev\repos\status-mcp
github: (not yet pushed)
---

# status-mcp — Goliath Status Server for Claude iOS

Single-file FastMCP 3.x server exposing Goliath's working state (vault notes, changelogs,
repo activity, MCP logs) over streamable-HTTP via Tailscale Funnel, for the claude.ai
custom-connector on iOS. Remote session continuity: "status" as first message on mobile
pulls the latest advanced-memory notes.

## Status

`active — core implemented and container-verified 2026-06-11; Funnel exposure + NSSM service pending`

| Component | Status |
|---|---|
| Four read-only tools (status, changelog, recent repos, log tail) | done |
| Streamable-HTTP transport (fastmcp 3.4.2 verified) | done |
| Bearer auth (`StaticTokenVerifier`, 401/401/200 verified) | done |
| Secret mount path (`STATUS_PATH`, verified — default 404s) | done |
| Path-traversal guards + output caps | done |
| Vault exclusion filter (personal/private/journal/travel/security/internal) | done — 14/119 folders, zero false positives |
| Tailscale Funnel exposure | pending |
| claude.ai connector handshake + iOS smoke test | pending |
| NSSM service | pending |

## Tool Inventory

| Tool | Operations |
|------|------------|
| `get_status` | latest n vault notes, newest first, 4k-char cap/note, `STATUS_EXCLUDE` keyword filter |
| `get_changelog` | CHANGELOG.md head (8k cap) for repo under D:\Dev\repos |
| `list_recent_repos` | repos by dir mtime (direct-child changes only — documented caveat) |
| `tail_mcp_log` | tail Claude Desktop `mcp-server-<name>.log` |

## Key Decisions

1. **Filesystem, not DB** — reads markdown from `C:\Users\sandr\.advanced-memory\vault`
   directly; never opens `memory.db`. Immune to the SQLite WAL/lock contention between IDEs.
2. **Port 10765** — fleet range; 8765 collides with Magenta RT host bridge.
3. **Secret path as auth floor** — claude.ai connector UI may not accept static bearer
   tokens; token auth is built and verified for clients that can send the header.
4. **No webapp** — deliberate exemption from WEBAPP_SOTA_STANDARDS; this is plumbing.
5. **Read-only by construction** — no write tools exist.
6. **Exclusion before exposure** — sensitive vault folders (personal, private, journal,
   travel, security, incidents, vienna-life) filtered at the path-component level,
   env-overridable via `STATUS_EXCLUDE`; applies regardless of auth state.

## Related

- **tailscale-mcp** — manages the Funnel exposure (`manage_funnel`: enable, disable,
  status, list, certificate_info; CLI-backed, verified initialized 2026-06-11).
  Added to Claude Desktop config 2026-06-11.
- **advanced-memory-mcp (memops)** — the vault this reads from.
- Docs: `D:\Dev\repos\status-mcp\README.md`, `D:\Dev\repos\status-mcp\docs\PRD.md`.

## Next Steps

1. `tailscale funnel 10765` with `STATUS_PATH` set to a secret path
2. Add connector at claude.ai, toggle on in iOS chat, smoke test "status"
3. NSSM install (RustDesk pattern), reboot test
