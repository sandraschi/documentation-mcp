# chitchat — Conversation Starters & Fleet Docs Crosslink

**Canonical source repo:** `D:/Dev/repos/chitchat`
**Ports:** **10974** (FastAPI + MCP `/mcp`) · **10975** (Vite dashboard)
**Stack:** FastMCP 3.2 · FastAPI · React 18 · Vite 5 · TypeScript
**Start:** `web_sota/start.ps1`

---

## What it does

- **Conversation Starters** — 64 curated topics across 8 categories (Ice Breakers, Tech & Tools, Deep Thoughts, Vienna & Local, Creative & Weird, Work & Life, Food & Drink, Hypotheticals)
- **Conversation Archive** — JSON-backed CRUD for saving conversations with topic, response, and tags. Filter by tag, delete, stats.
- **Fleet Docs Crosslink** — Semantic search across `mcp-central-docs` via docs_mcp backend (port **10795**). Discover fleet standards, patterns, and port registries.

## MCP Tools

| Tool | Access | Description |
|------|--------|-------------|
| `chitchat_welcome` | Read-only | Random conversation starter + warm welcome |
| `chitchat_topics` | Read-only | Browse topics by category or get random |
| `chitchat_archive` | Read-write | CRUD for saved conversations (add/list/get/delete/stats) |
| `chitchat_search_docs` | Read-only | Semantic search across fleet documentation |

## REST API (10 endpoints)

`/api/health`, `/api/welcome`, `/api/topics`, `/api/archive` (CRUD + stats), `/api/docs/search`, `/api/docs/health`

---

## Fleet Integration

| Related | Role |
|---------|------|
| [mcp-central-docs](../mcp-central-docs/) | Docs source for crosslink search |
| [hermes-agent](../hermes-agent/) | Hermes can use chitchat tools for social interactions |
| [uitars-mcp](../uitars-mcp/) | Companion GUI agent — chitchat can delegate desktop tasks |
| [robofang](../robofang/) | Fleet supervisor routing |

---

*Tags: #chitchat #social #conversation #mcp #fleet #fastmcp3.2*
