# meta-hypertools (project page)

Fleet control center: operate MCP server fleets from one process. Local
repo: `D:\Dev\repos\meta_mcp`. Public GitHub:
https://github.com/sandraschi/meta-hypertools (`meta-mcp` redirects there).

> Build, study, check, and run MCP servers - from one place.

Two doors: **people** use the web dashboard (`start.ps1`,
http://127.0.0.1:10719) or the desktop installer (Meta Hypertools setup,
bundled backend on 11220); **agents and IDEs** use the MCP server over
stdio (`uv run meta-mcp-server`) or the REST API on port 10718.

## Current state (2026-09-29)

- Agentic chat loop with confirm gate on mutating tool calls (42 tools,
  Ollama/OpenAI wire formats, trace + approval UI).
- Fleet Standards browser, Repo Inspiration discovery (GitHub search proxy
  with popularity markers, presets, faves), session-docs prune with
  shared-log guard, Assess Reports with search/filter/sort/paginate.
- Windows desktop app (Tauri 2.0 + NSIS, v0.5.1 release with MCPB +
  installer attached); operator backend on claimed port 11220, dev stack
  untouched on 10718/10719.
- Portable installs (`FLEET_REPOS_ROOT`/`REPOS_DIR` + repo-relative
  defaults); relaxed pre-commit biome gate (lint only).
- Repo is public; README split (short welcome + `docs/WORKFLOWS.md`).

Full history: [CHANGELOG.md](CHANGELOG.md) (mirrored from the repo).
Tool surface: [llms.txt](llms.txt) (mirrored from the repo).

## Links

- Repo README: `D:\Dev\repos\meta_mcp\README.md`
- Missions: `D:\Dev\repos\meta_mcp\docs\WORKFLOWS.md`
- Architecture: `D:\Dev\repos\meta_mcp\docs\ARCHITECTURE.md`
- Ports: backend 10718, dashboard 10719, desktop operator backend 11220
  (see `operations/WEBAPP_PORTS.md`)
