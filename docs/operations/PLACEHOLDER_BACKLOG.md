---
title: "Placeholder / Coming-Soon Backlog"
category: operations
status: active
audience: mcp-dev
last_updated: 2026-08-06
---

# Placeholder / Coming-Soon Backlog

**Established**: 2026-08-06 (gaslight sweep after immich-mcp audit)

Tracks every advertised-but-unimplemented feature found in the fleet gaslight
sweep. These are "coming soon" / "not yet implemented" points that must be
implemented or de-advertised. Each row links its GitHub issue.

Status legend: `OPEN` (issue filed, not started) · `IMPLEMENTED` · `REMOVED`
(honestly de-advertised)

| Repo | Item | Current state | Issue | Status |
|------|------|---------------|-------|--------|
| bookmarks-mcp | `ai_bookmark_portmanteau` ops `recommend` / `analyze` / `evolve` / `score` | Honest `not_implemented` errors (fixed from fake success) | [#1](https://github.com/sandraschi/bookmarks-mcp/issues/1) | OPEN |
| fullstack-demo | `query_database` tool | Honest `not_implemented` (fixed from fake success) | [#1](https://github.com/sandraschi/fullstack-demo/issues/1) | OPEN |
| fullstack-demo | `analyze_logs` tool | Honest `not_implemented` | [#1](https://github.com/sandraschi/fullstack-demo/issues/1) | OPEN |
| fullstack-demo | `execute_workflow` tool | Honest `not_implemented` (was claiming `status: executed`) | [#1](https://github.com/sandraschi/fullstack-demo/issues/1) | OPEN |
| myvrworlds | Unity integration page | Placeholder "coming soon" page | [#1](https://github.com/sandraschi/myvrworlds/issues/1) | OPEN |
| myvrworlds | OSC control page | Placeholder "coming soon" page | [#1](https://github.com/sandraschi/myvrworlds/issues/1) | OPEN |
| myvrworlds | Blender integration page | Placeholder "coming soon" page | [#1](https://github.com/sandraschi/myvrworlds/issues/1) | OPEN |
| audiotool-nexus-mcp | P2P telemetry in SettingsView | Visible "coming soon" copy | [#1](https://github.com/sandraschi/audiotool-nexus-mcp/issues/1) | OPEN |
| devices-mcp | `web-sota/backend/Dashboard.tsx` + `energy/EnergyDashboard.tsx` | Dead files, not imported anywhere | [#11](https://github.com/sandraschi/devices-mcp/issues/11) | OPEN |
| blender-mcp | Animation rendering (`render_tools.py`) | Returns "not yet implemented - use render_turntable" | [#5](https://github.com/sandraschi/blender-mcp/issues/5) | OPEN |
| blender-mcp | Sketchfab asset import | Returns "not yet implemented" | [#5](https://github.com/sandraschi/blender-mcp/issues/5) | OPEN |
| advanced-memory-mcp | Prefab graph view card | "Graph view coming soon..." card | [#18](https://github.com/sandraschi/advanced-memory-mcp/issues/18) | OPEN |
| avatar-mcp | WS `subscribe` / `unsubscribe` | Return "Subscription not yet implemented" | repo `sandraschi/avatarmcp` is **archived** - tracked here only | OPEN |
| avatar-mcp | Parameter tracking tool | `NotImplementedError` | repo archived - tracked here only | OPEN |

## Fixed during the sweep (no longer pending)

- immich-mcp: chat stub ("being industrialized") -> real Ollama chat (aad2bb7)
- immich-mcp: fake map UI -> real Leaflet map (aad2bb7)
- immich-mcp: placeholder logs -> ring buffer (aad2bb7)
- immich-mcp: fake /llm/models fallbacks -> dynamic lists (aad2bb7)
- bookmarks-mcp: fake success stubs -> honest errors (0092bcd)
- fullstack-demo: fake success stubs -> honest errors (4d53c0b)
- myai/plex_plus: fake model lists -> dynamic /api/tags (0ccc4b4)
- myai: bandit pre-commit hook repaired (utf8, toml, staged-only) (0ccc4b4)

## Scan command

Re-run the sweep with:

```powershell
rg -l "coming soon|not yet implemented|not implemented yet" D:\Dev\repos -g "*.py" -g "*.ts" -g "*.tsx" -g "*.js" -g "!*.venv" -g "!node_modules" -g "!.git" -g "!mcpb" -g "!dist" -g "!*.bak*"
```
