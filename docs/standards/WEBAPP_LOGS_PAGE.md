# Webapp Logs Page Standard (Fleet v1.0)

**Status:** Official fleet pattern (June 2026)  
**Extends:** [WEBAPP_STANDARDS.md](./WEBAPP_STANDARDS.md) §1.1 Logger Panel, §6.3  
**Reference implementation:** `bookmarks-mcp` `/logs`, `devices-mcp` `/logs`

---

## 1. Purpose

Every SOTA MCP webapp with a FastAPI backend MUST expose a dedicated **Logs** page (route `/logs`) in addition to any compact dashboard activity widget. The page is the operator console for tool calls, exports, auth events, and server log lines.

---

## 2. Backend API (mandatory)

Prefix: **`/api/logs`**

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/api/logs` | Paginated query |
| `GET` | `/api/logs/stats` | Ring buffer / file stats |
| `GET` | `/api/logs/export` | Download filtered logs (`json` or `csv`) |
| `DELETE` | `/api/logs` | Clear buffer (auth-gated in production) |

### 2.1 Query parameters (`GET /api/logs`)

| Param | Type | Default | Notes |
|-------|------|---------|-------|
| `limit` | int | 50 | Max 500 |
| `offset` | int | 0 | Pagination |
| `level` | string | — | Minimum level: DEBUG, INFO, WARNING, ERROR |
| `kind` | string | — | e.g. `tool_call`, `export`, `server` |
| `search` | string | — | Substring match on detail + meta |
| `sort` | asc \| desc | desc | By timestamp |
| `after_id` | string | — | Tail mode: only entries newer than id |

### 2.2 Response shape

```json
{
  "entries": [
    {
      "id": "1717234567.123456",
      "timestamp": "2026-06-01T12:00:00+00:00",
      "level": "INFO",
      "kind": "tool_call",
      "detail": "browser_bookmarks (ok)",
      "meta": { "tool": "browser_bookmarks" }
    }
  ],
  "total": 42,
  "limit": 50,
  "offset": 0,
  "max_entries": 2000,
  "sort": "desc"
}
```

### 2.3 Rotation

- In-memory repos: **`collections.deque(maxlen=N)`** with `N` from env (e.g. `BOOKMARKS_LOG_MAX_ENTRIES`, default 2000).
- File-based repos: rotate on size via `logging.handlers.RotatingFileHandler`; expose file path in `/api/logs/stats`.

Legacy **`GET /api/activity`** MAY remain for dashboard widgets; new UIs MUST use `/api/logs`.

---

## 3. Frontend page (mandatory)

Route: **`/logs`** — sidebar label **Logs** (icon: `ScrollText` or `FileText`).

| Feature | Required |
|---------|----------|
| Live tail toggle | Poll `after_id` every 1–2s when ON |
| Pagination | Page size selector + prev/next |
| Level filter | DEBUG → ERROR |
| Kind filter | tool_call, export, server, … |
| Search | Debounced text filter |
| Sort | Newest / oldest first |
| Export | JSON + CSV download |
| Clear logs | Confirm dialog → `DELETE /api/logs` |
| Auto-scroll pause | When user scrolls up during tail (§6.3 WEBAPP_STANDARDS) |

Visual: dark monospace stream, level color chips, glass card chrome matching Iron Shell.

---

## 4. Logging integration

On backend startup, attach an `ActivityLogHandler` (or equivalent) to the root logger so uvicorn/app INFO+ lines appear with `kind: server`.

Tool calls MUST log with `kind: tool_call`, level ERROR on failure.

---

## 5. Checklist

- [ ] `/api/logs` + stats + export + clear
- [ ] Ring buffer max documented in README / settings
- [ ] `/logs` page with tail, pagination, filters, export
- [ ] Sidebar nav entry
- [ ] Tests for query + export + clear
