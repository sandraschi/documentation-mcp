# FastMCP Fleet Changelog

**Purpose**: Track FastMCP releases, new features, fleet-relevant changes, and known problems.
**Source**: https://github.com/PrefectHQ/fastmcp/releases

---

## 3.5.0 (Jul 19 — "Caching & Storage")

| Aspect | Detail |
|--------|--------|
| **Release** | [v3.5.0](https://github.com/PrefectHQ/fastmcp/releases/tag/v3.5.0) — stable |
| **Fleet pin** | **CURRENT** `>=3.5.0,<4` |

**Changes:**
- **Pluggable Storage**: Persistent storage backends via `py-key-value-aio` (supports SQLite, file-system key-value stores).
- **Response Caching**: Middleware for caching tool execution results based on parameter hashes.
- **OAuth Upgrades**: PKCE support, Hugging Face and AzureB2C pre-configured authentication providers, RFC 7662 token introspection.
- **MCP SDK Pinning**: Restricts `mcp<1.17` to prevent `.well-known` configuration metadata route shifts and ensure reverse-proxy compatibility.
- **Input Validation**: Pydantic input refinements and better error feedback.

**Known problems:**
- None reported yet.

**Fleet recommendation:** Adopt immediately in all new repos; update dependencies in `pyproject.toml` to `"fastmcp>=3.5.0,<4"`.

---

## 3.4.4 (Jul 9 — "Host in Translation")

| Aspect | Detail |
|--------|--------|
| **Release** | [v3.4.4](https://github.com/PrefectHQ/fastmcp/releases/tag/v3.4.4) — stable |
| **Fleet pin** | `>=3.4.2,<4` (not yet bumped) |

**Changes:**
- **Relaxed** the 3.4.3 Host/Origin guard (broke existing ASGI/serverless/reverse-proxy deployments). Guard is now opt-in via explicit trusted hosts.
- Hugging Face OAuth provider (PKCE, Dynamic Client Registration, CIMD)

**Known problems:**
- None reported yet (4 days old)

**Fleet recommendation:** Wait ~2 weeks before bumping pin from `>=3.4.2` to `>=3.4.4`.

---

## 3.4.3 (Jul 5 — "The Fast and the Secure-ious")

| Aspect | Detail |
|--------|--------|
| **Release** | [v3.4.3](https://github.com/PrefectHQ/fastmcp/releases/tag/v3.4.3) — stable |
| **Fleet status** | Skipped (3.4.4 hotfix released 4 days later) |

**Changes:**
- **SSRF hardening**: blocks NAT64, 6to4, Teredo, ISATAP transition addresses (previously could smuggle private IPv4 targets past allowlist)
- **Streamable HTTP Host/Origin validation**: protects against DNS rebinding of localhost-bound servers
- **CodeMode**: real Monty sandbox E2E coverage added
- **ToolResult.is_error**: tools can now return rich structured errors (maps to `CallToolResult.isError`)
- Various auth, proxy, and caching fixes

**Known problems:**
- **WITHDRAWN**: Host/Origin guard broke existing ASGI, serverless, and reverse-proxy deployments. Fixed in 3.4.4. Do NOT use 3.4.3.

**Fleet recommendation:** Skip 3.4.3 entirely.

---

## 3.4.2 (Jun 6 — "Heads Up")

| Aspect | Detail |
|--------|--------|
| **Release** | [v3.4.2](https://github.com/PrefectHQ/fastmcp/releases/tag/v3.4.2) — stable |
| **Fleet pin** | **CURRENT** `>=3.4.4,<4` |

**Changes:**
- Allows private JWT headers (e.g. Clerk `cat` header) without rejecting before signature validation

**Known problems:**
- None reported

---

## 3.4.1 (Jun 5 — "Floor It")

| Aspect | Detail |
|--------|--------|
| **Release** | [v3.4.1](https://github.com/PrefectHQ/fastmcp/releases/tag/v3.4.1) — stable |

**Changes:**
- Floors Starlette at `>=1.0.1` (CVE-2026-48710 fix)
- OAuthProxy logs refresh-token cache misses

---

## 3.4.0 (Jun 3 — "Remote Control")

| Aspect | Detail |
|--------|--------|
| **Release** | [v3.4.0](https://github.com/PrefectHQ/fastmcp/releases/tag/v3.4.0) — stable |

**Changes:**
- `fastmcp-remote`: standalone bridge for stdio-only hosts to connect to HTTP servers
- Proxies fail loudly (initialize forwarded upstream)
- Auth survives idle time (`fastmcp_access_token_expiry_seconds`)
- **CodeMode**: safe defaults (`MontySandboxProvider` with 30s/100MB/50-tool-call caps)
- `ToolResult.is_error` (structured error returns)
- OTEL spans for sampling and tool execution

**Known problems:**
- 3.3 packaging split caused clean install failures (hotfixed in 3.3.1)

---

## 3.2.x — 3.3.x

See `fastmcp/HISTORY_OF_FASTMCP.md` for the full history. Key fleet-relevant versions:

| Version | Date | Fleet relevance |
|---------|------|----------------|
| 3.2.0 | Mar 30 | Providers, transforms, CodeMode, Prefab UI GA |
| 3.0.0 | Feb 18 | FastMCP 3.x rewrite |
| 2.x | 2025-2026 | Legacy (no longer used in fleet) |

---

## Fleet Version Policy

- **Remove `_strptime` hack** from `run_server.py` once we hit FastMCP 4.x (the workaround for a frozen-exe datetime import bug is no longer needed)
- Pin format: `fastmcp>=3.4.4,<4` in `pyproject.toml`
- Bump only after testing: `uv sync && uv run pytest tests/ -q`
