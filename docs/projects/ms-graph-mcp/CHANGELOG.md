# Changelog

## 0.1.0 (2026-08-04)

Initial release.

- **MCP tools** (8): `auth_ops` (device-code login/status/logout),
  `calendar_ops` (week/range list, create, update, cancel, free-slot search),
  `todo_ops` (lists, tasks, add, complete, delete), `contacts_ops` (list,
  search, CRUD), `onedrive_ops` (list, read, upload, download, share links),
  `profile_ops` (me, photo), `ms_graph_health`, `show_health_prefab`.
- **Auth**: MSAL device-code flow, Graph Explorer public client default,
  optional private Azure app registration (`MSG_CLIENT_ID`), atomic token
  store in `%LOCALAPPDATA%\ms-graph-mcp\tokens.json`.
- **Graph client**: httpx with 401 retry + forced refresh,
  `@odata.nextLink` pagination, typed errors with recovery suggestions.
- **Webapp** (11148/11149): Dashboard KPIs with MOCK-until-onboarded state,
  Calendar, Tasks, Contacts, Drive pages, Chat (local LLM), Settings with
  device-code UI, Help, Logs, Tools, Skills. Dark theme, data-testid,
  e2e suite green (6 tests).
- **REST**: health, diagnostics, auth lifecycle, calendar/todo/contacts/
  drive read+write, skills/tools discovery, LLM provider probe. All data
  endpoints guarded by `api_guard`.
- **Docs**: README, INSTALL, docs/ stack, llms.txt + llms-full.txt,
  glama.json, skill `ms-graph-expert`.
