# P7 — ms-graph-mcp: Microsoft personal-cloud gateway (SPEC)

**Status**: ✅ **BUILT 2026-08-04** — repo live at `D:\Dev\repos\ms-graph-mcp` (v0.1.0, ports 11148/11149 registered). This spec is the historical record; implementation details live in the repo docs.
**Date**: 2026-08-04
**Proposed repo**: `D:\Dev\repos\ms-graph-mcp` (name free — verified no fleet repo or doc uses it)
**Cross-refs**: [integrations/office365-oauth.md](../../integrations/office365-oauth.md) (auth pattern) · [PARKING_LOT.md](../PARKING_LOT.md) (teams-mcp parked) · `projects/email-mcp` + `projects/onenote-mcp` (reference impls)

---

## 1. Goal

A FastMCP server exposing the **Microsoft Graph API surfaces that work with a
personal Microsoft account** as MCP tools, using the fleet-proven
`office365-oauth.md` pattern (Azure app registration + MSAL device-code flow,
no redirect URI, no subscription).

It is the Microsoft counterpart to `git-github-mcp` wrapping the GitHub API:
one server, one OAuth consent, one token store — covering the four gaps the
fleet has no Microsoft story for today: **Calendar, Tasks/To-Do, Contacts,
OneDrive**.

## 2. Why this is genuinely useful (honest assessment)

| Claim | Verdict |
|-------|---------|
| Fills a real fleet gap | **Yes.** No server today can read/write Outlook calendar, To-Do tasks, or OneDrive files. Only mail (`email-mcp`) and OneNote (`onenote-mcp`) are covered. |
| One auth for four domains | **Yes.** Calendar + Tasks + Contacts + OneDrive share one delegated consent (`offline_access` + 4 scopes). Four per-domain servers would duplicate auth infra 4x. |
| Works for Sandra's personal account | **Yes.** Graph supports personal Microsoft accounts for mail, calendar, contacts, tasks, ToDo, OneDrive, profile. (Teams/SharePoint/Entra admin do NOT — see §4.) |
| Free | **Yes.** App registration is free; Graph has generous free limits for personal accounts (throttle ~10k req / 10 min — same as onenote-mcp). |
| Fleet-compatible | **Yes.** Local FastMCP server, dual-transport, MCPB + Tauri NSIS, webapp on reserved ports. |
| Not duplicating existing repos | **Yes.** Scope explicitly EXCLUDES mail and OneNote (owned by email-mcp / onenote-mcp). No tool overlap. |

**Limits (why not a silver bullet):** no Teams, no SharePoint, no Exchange
admin, no Entra ID — personal accounts can't reach them. Those stay parked
(see `PARKING_LOT.md` → `teams-mcp (business accounts only)`).

## 3. Name

`ms-graph-mcp` (user-preferred) — agreed over `graph-mcp`:

- Disambiguates from graph databases / graph-viz tooling in registries.
- Matches fleet naming: `git-github-mcp` precedent for two-part vendor names.
- No conflict in fleet (grep across `D:\Dev\repos` finds zero repos/docs using
  `ms-graph-mcp` or a standalone `graph-mcp`).

Community Microsoft Graph MCP servers exist on public registries, but none are
first-party from Microsoft, and none ship the fleet's OAuth+webapp+packaging
stack. A fleet-native build on the proven pattern is the SOTA choice.

## 4. Scope

### In scope (personal-account Graph endpoints)

| Domain | Graph surface | Example tools |
|--------|---------------|---------------|
| Calendar | `/me/events`, `/me/calendar` | list week, create, update, cancel, find free slots |
| Tasks/To-Do | `/me/todo/lists`, `/me/todo/lists/{id}/tasks` | list lists, list tasks, add, complete, delete |
| Contacts | `/me/contacts` | list, search, create, update, delete |
| OneDrive | `/me/drive/root`, `/me/drive/items` | list folder, read text, upload, download, share link |
| Profile | `/me` | profile card, photo |

### Out of scope (explicit)

- **Mail** — email-mcp owns it (IMAP XOAUTH2 + Graph service).
- **OneNote** — onenote-mcp owns it.
- **Teams, SharePoint, Exchange admin, Entra ID, Intune** — require a
  work/school tenant; rejected by personal accounts. Parked.
- **Power Automate / Power Platform** — see comparison doc
  `not-mcp-related/comparisons/MS_GRAPH_MCP_VS_POWER_AUTOMATE.md`.

## 5. Auth design (reuse `office365-oauth.md`)

1. **Azure app registration** (free): personal Microsoft accounts only,
   no redirect URI, **Allow public client flows = Yes** (mandatory for
   device code).
2. **Scopes**: `User.Read`, `Calendar.ReadWrite`, `Tasks.ReadWrite`,
   `Contacts.ReadWrite`, `Files.ReadWrite`, `offline_access`.
3. **Flow**: MSAL device-code (`authenticate` tool + Settings page button),
   token cached in the repo data dir (per-family token store — copy
   email-mcp/onenote-mcp pattern).
4. **Dev fallback**: Graph Explorer shared client ID
   (`14d82eec-204b-4c2f-b7e8-296a70dab67e`) like onenote-mcp — zero setup,
   consent shows "Graph Explorer". Private registration is the prod default
   (revocable, scoped).

## 6. Tool design (SOTA portmanteau + Prefab)

| Portmanteau | Operations |
|-------------|-----------|
| `calendar_ops` | `list_week`, `list_range`, `create`, `update`, `cancel`, `find_free_slots` |
| `todo_ops` | `list_lists`, `list_tasks`, `add`, `complete`, `delete` |
| `contacts_ops` | `list`, `search`, `create`, `update`, `delete` |
| `onedrive_ops` | `list`, `read_text`, `upload`, `download`, `create_share_link` |
| `profile_ops` | `me`, `photo` |
| `auth_ops` | `status`, `login` (device code), `logout` |

- `operation: Literal[...]` discriminator first param, Annotated Field
  descriptions, docstring SOTA (no `Args:`, `## Return Format`, `## Examples`).
- **Prefab App surfaces** (`ToolResult` + `PrefabApp`) for list/status tools
  (calendar week view, task lists, folder listing) — `prefab-ui>=0.14.0` core
  dep per SOTA.
- **Pagination**: Graph `@odata.nextLink` → `next_link`/`has_more` contract;
  `limit` cap documented per tool (TOOL_DESIGN_STANDARDS §6.2).
- Annotation hints: `READ_ONLY` for reads, `MUTATING` for create/update,
  `DESTRUCTIVE` for delete/cancel.
- Returns: `{"success", "message", "data"}` + `error`/`suggestions` on failure.

## 7. Webapp (SOTA AppLayout, 7+ pages)

`ms-graph-mcp` webapp: **Dashboard** (KPIs: events this week, open tasks,
drive storage — all from `/api/*`), **Calendar** (week view + create dialog),
**Tasks** (lists + checkboxes), **Contacts** (search + cards), **Drive**
(file browser + upload), **Chat** (skill-first, personalities, local LLM),
**Settings** (device-code login, token status, provider probe), **Help**.

- Vite + React + Tailwind + Zustand + lucide-react; `data-testid` on primary
  controls; dark default; health dot + exponential-backoff health poll;
  `GET /api/health` + `GET /api/v1/diagnostics` (CUA-NSIS gate).
- Sidebar nav with accessible labels for the CUA title-matching nav walk.

## 8. Ports (proposed, register in WEBAPP_PORTS.md at scaffold time)

| Port | Service |
|------|---------|
| 11148 | ms-graph-mcp Frontend (Vite) |
| 11149 | ms-graph-mcp Backend (FastAPI + MCP HTTP `/mcp`) |

Both free in the registry as of 2026-08-04 (after safety-mcp 11146/11147).

## 9. Packaging (dual-track per PACKAGING_STANDARDS)

- **MCPB**: `.mcpb` bundle for Claude Desktop (assets/prompts 3-4-100).
- **Tauri NSIS**: `native/` embedded backend, `run_server.py` dual transport
  (MCP_PORT → HTTP, fallback → stdio), spec `strip=False, upx=False`,
  `just cua-nsis-test` + `just cua-webapp-test` mandatory.
- **uv + justfile + llms.txt + llms-full.txt + glama.json** per fleet bar.

## 10. Open questions

1. Should the token store live in ms-graph-mcp only, or become a shared
   `secrets-mcp` credential (cross-server reuse by future MS servers)?
   → Default for v1: private token store (email-mcp precedent); revisit when a
   third MS-connected server exists.
2. OneDrive file *content* ops (read/upload): text-first in v1, binary via
   Prefab/download tool in v2?
   → Default: text + download-to-path in v1, keep `download` returning a
   local file path (filesystem access is fleet-local anyway).

## 11. Decision gate

Build if: (a) Sandra has a personal Microsoft account she wants calendar/tasks/
contacts/drive automation for, and (b) the team wants one OAuth consent instead
of per-domain servers. Estimated build: 2-3 days on the email-mcp/onenote-mcp
OAuth base.
