# forgejo-mcp

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.4.4%2B-7c5cfc?style=flat-square" alt="FastMCP"></a>
  <a href="https://forgejo.org/"><img src="https://img.shields.io/badge/Forgejo-Codeberg-BA4A00?style=flat-square" alt="Forgejo"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-GPL--3.0-blue?style=flat-square" alt="GPL-3.0"></a>
</p>

FastMCP server + React companion for **Forgejo** and **Codeberg** — multi-profile remotes, repos/issues/PRs, runners, inbox, and local-LLM chat.

**v0.2.0** · Frontend **11132** · Backend **11133**

> FastMCP 3.4.4+ · portmanteau tools (dialogic) · Actions runner health · 12-view dashboard · backend LLM proxy

## Features

- **Multi-profile** — several Forgejo/Codeberg instances; switch active profile
- **Repos** — list, search, create, read raw file contents
- **Issues & PRs** — create, comment, list, merge, review diffs
- **Runners** — forgejo-runner health/version + workflow run history
- **Inbox** — notification threads + inbound webhook receiver (HMAC)
- **Chat** — streaming local-LLM chat (Ollama/LM Studio via backend proxy)
- **Dashboard** — KPIs, repo browser, logs, tools/skills/settings/help pages

## Quick start

```powershell
git clone https://github.com/sandraschi/forgejo-mcp
cd forgejo-mcp
uv sync
Copy-Item .env.example .env
# set Forgejo/Codeberg base URL + personal access token
.\start.ps1
```

Dashboard: http://127.0.0.1:11132 · API/MCP: http://127.0.0.1:11133

Requires [uv](https://github.com/astral-sh/uv) and [Bun](https://bun.sh).

## MCP tools (portmanteau, dialogic — v0.2.0 breaking change)

- `forgejo_profiles` — list / add / set_active / remove
- `forgejo_repos` — list / create / search / file_get
- `forgejo_issues` — list / create / comment
- `forgejo_prs` — list / create / merge / diff
- `forgejo_actions` — runners / workflow_runs / notifications
- `forgejo_status` — health/version/profiles
- `forgejo_shutdown` — confirm-gated termination

## License

GPL-3.0-only
