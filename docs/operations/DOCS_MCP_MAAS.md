# Docs MCP as MaaS (MCP as a Service)

**Status**: Active  
**Audience**: Other repos that need central-docs capabilities without running their own MCP server.

## Purpose

Docs MCP can be used as a **shared service** for the fleet: one running instance (mcp-central-docs backend) exposes tools over HTTP so that other repositories (e.g. robofang, email-mcp, ocr-mcp) can call semantic search, document fetch, and Q&A without embedding the full docs stack.

## Service endpoint

| Environment | Base URL | Notes |
|-------------|----------|--------|
| Local (webapp) | `http://localhost:10795` | Backend only; use this when calling from scripts or other repos. |
| Local (via frontend) | `http://localhost:10794/api` | Vite proxies `/api` → 10795; same backend. |
| Deployed | `https://<your-host>/api` | Use your deployed backend base URL. |

**Health**: No dedicated `/health` today; `GET /api/tools` returning 200 indicates the service is up.

## Pertinent tools for other repos

These tools are intended for **cross-repo consumption** (standards lookup, semantic search, doc fetch). Admin/operational tools (e.g. `start_webapp`, `reindex_docs`) are not part of the MaaS subset.

| Tool | Purpose | Typical use from another repo |
|------|----------|--------------------------------|
| `search_docs` | Semantic search over indexed central docs | "Find SOTA patterns for FastMCP", "Where is port allocation documented?" |
| `get_document` | Fetch full markdown by relative path | After search, retrieve `standards/AGENT_PROTOCOLS.md` |
| `ask_docs` | Q&A with synthesis (uses server-side sampling) | "Summarize MCP server first-time success requirements" |
| `chunk_stats` | Index health and source count | Observability, checking that docs are indexed |

**Curated list**: `GET /api/maas/tools` returns only these tools (same JSON shape as `/api/tools`). Use it for discovery when building a client that should only call the MaaS subset.

## Calling the service

### List MaaS tools (curated)

```http
GET http://localhost:10795/api/maas/tools
```

Response: JSON array of `{ "name", "description", "parameters" }` for `search_docs`, `get_document`, `ask_docs`, `chunk_stats`.

### List all tools

```http
GET http://localhost:10795/api/tools
```

### Execute a tool

```http
POST http://localhost:10795/api/execute
Content-Type: application/json

{
  "name": "search_docs",
  "arguments": {
    "query": "FastMCP portmanteau pattern",
    "limit": 5
  }
}
```

Response: `{ "result": "<string or JSON-serialized result>" }`. On error: `{ "error": "..." }` (and possibly HTTP 4xx/5xx).

### Example: search then get document

1. **Search**  
   `POST /api/execute` with `name: "search_docs"`, `arguments: { "query": "AGENT_PROTOCOLS", "limit": 3 }`.  
   Parse `result` (JSON); take `relative_path` from the snippet you need.

2. **Get full doc**  
   `POST /api/execute` with `name: "get_document"`, `arguments: { "relative_path": "standards/AGENT_PROTOCOLS.md" }`.

### Example: PowerShell

```powershell
$body = @{ name = "search_docs"; arguments = @{ query = "MCP server first-time success"; limit = 3 } } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:10795/api/execute" -Method POST -Body $body -ContentType "application/json"
```

## Authentication and security

- Current implementation has **no auth**; the backend is intended for local or trusted-network use.
- For a deployed MaaS instance, put the backend behind a reverse proxy (e.g. Traefik, Authentik) and add API keys or OAuth as needed.
- `get_document` enforces path containment under the configured docs root; paths that escape are rejected.

## Cursor / IDE configuration

Other repos can call Docs MCP as a **remote HTTP service** from scripts or agents. For Cursor/clients that expect an MCP server over stdio, run docs_mcp in stdio mode in that repo’s config, or use an MCP-to-HTTP bridge that forwards to `http://localhost:10795/api/execute` and `/api/maas/tools`.

## Summary

| Item | Value |
|------|--------|
| **MaaS role** | Central docs semantic search, document fetch, Q&A for the fleet |
| **Pertinent tools** | `search_docs`, `get_document`, `ask_docs`, `chunk_stats` |
| **Discovery** | `GET /api/maas/tools` (curated) or `GET /api/tools` (all) |
| **Execution** | `POST /api/execute` with `name` and `arguments` |
| **Backend port** | 10795 (local) |
