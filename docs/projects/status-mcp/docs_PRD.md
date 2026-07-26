# PRD — status-mcp

**Version:** 1.0 · **Date:** 2026-06-11 · **Owner:** Sandra · **Status:** core implemented, deployment pending

## 1. Problem

Claude on iOS has no view into Goliath. Picking up a work thread on mobile means
re-explaining context that already exists in the advanced-memory vault, repo changelogs,
and MCP logs. The fleet's existing servers are stdio/localhost; nothing is reachable
from claude.ai's custom-connector mechanism, which requires a public HTTPS endpoint.

## 2. Goal

A Claude iOS chat that opens with "status" and receives, within one tool round-trip,
the last few working notes from Goliath — plus on-demand changelog, repo-activity, and
MCP-log lookups. Effectively: session continuity from the couch, the train, or Tokyo.

## 3. Non-goals

- **No writes.** This server never modifies anything on Goliath.
- **No DB access.** Reads markdown from the vault directory; `memory.db` stays untouched
  (deliberate, given the SQLite WAL/lock contention history across IDEs).
- **No webapp.** No dashboard, no SOTA pages, no frontend. Exempt from WEBAPP_SOTA_STANDARDS
  by virtue of having no webapp surface.
- **No fleet federation.** Not a federation-hub member; it is a single-purpose remote endpoint.
- **No general file access.** Four fixed views, nothing else.

## 4. Requirements

### Functional

| ID | Requirement | Status |
|----|-------------|--------|
| F1 | Return latest *n* vault notes, newest first, with timestamps | done, tested |
| F2 | Return CHANGELOG.md for any repo under `D:\Dev\repos` | done, tested |
| F3 | List repos by recent modification | done, tested (mtime caveat documented) |
| F4 | Tail Claude Desktop MCP log for a named server | done, tested |
| F5 | Reachable from claude.ai custom connector (public HTTPS) | pending — Funnel + connector handshake |

### Non-functional

| ID | Requirement | Status |
|----|-------------|--------|
| N1 | Output caps to protect mobile context (4k/note, 8k/changelog, line-limited logs) | done |
| N2 | Path-traversal guards on all user-supplied path components | done |
| N3 | Auth: bearer token if client supports it; secret mount path as floor | done, tested (401/401/200) |
| N3a | Sensitive vault content (personal, private, journal, travel, security, internal, …) never served, regardless of auth state | done, tested against live folder list |
| N4 | Survive reboots unattended (NSSM service) | pending |
| N5 | No port collisions in fleet (default 10765; 8765 reserved by Magenta RT) | done |
| N6 | Single file, stdlib + fastmcp only — trivially auditable | done |

## 5. Architecture

```
iOS Claude app
   │  claude.ai custom connector (streamable-HTTP)
   ▼
Tailscale Funnel (public HTTPS, valid cert)
   │  https://goliath.tailXXXX.ts.net<STATUS_PATH>
   ▼
status_mcp.py (FastMCP 3.x, port 10765, optional StaticTokenVerifier)
   │  read-only Path operations
   ▼
vault (.advanced-memory\vault) · D:\Dev\repos\*\CHANGELOG.md · Claude MCP logs
```

Single process, single file. No persistence, no state, no background tasks.

## 6. Security analysis

Threat model: anonymous internet, since Funnel is public.

| Vector | Mitigation |
|--------|------------|
| Endpoint discovery (scanning) | Secret `STATUS_PATH`; default `/mcp` 404s when overridden |
| Credential-free read of vault/logs | `GOLIATH_STATUS_TOKEN` bearer auth where the client supports it |
| Path traversal via `repo`/`server` params | `resolve()` + parent containment checks (implemented, both tools) |
| Personal/private note exposure | `STATUS_EXCLUDE` keyword filter on every path component; 14/119 live vault folders excluded by default, env-overridable |
| Context-flooding via huge files | Hard output caps |
| Secrets leaking through MCP log tails | Residual risk — logs can echo tokens from misbehaving servers. Accepted for now; revisit with a redaction pass if it bites. |

Decision: ship with secret path as the floor because the claude.ai connector UI may not
accept a static bearer token (supports no-auth and OAuth/DCR). Token support is built and
verified for clients that can send the header.

## 7. Milestones

| # | Milestone | Effort | Status |
|---|-----------|--------|--------|
| 1 | Core server, four tools, container-verified | half a day | **done** 2026-06-11 |
| 2 | Auth + secret path, verified | same session | **done** 2026-06-11 |
| 3 | Funnel exposure + connector handshake + iOS smoke test | ~1 hour hands-on | pending |
| 4 | NSSM service + reboot test | ~30 min | pending |
| 5 | Optional: redaction filter for log tails, note-search tool | 1 day, if wanted | backlog |

## 8. Open questions

1. Does the claude.ai custom-connector UI (June 2026) offer a token/header field for
   non-OAuth servers? Determines whether layer 2 auth is usable from iOS.
2. ~~Should `get_status` filter to specific vault folders before public exposure?~~
   **Resolved 2026-06-11:** keyword exclusion filter implemented (`STATUS_EXCLUDE`),
   default set covers personal/private/journal/travel/security/internal and similar;
   verified against the live vault with zero false positives.
3. Worth adding `search_notes(query)` later, or does that recreate memops badly? Lean no.
