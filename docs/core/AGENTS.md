# AGENTS.md — Fleet-Wide Agent Instructions
# sandraschi / mcp-central-docs
# Last updated: 2026-05-28

> This file is the canonical source of truth for AI coding agents working in ANY repo
> in the D:\Dev\repos\ fleet. Per-repo AGENTS.md files are thin overrides only.
> Full standards: D:\Dev\repos\mcp-central-docs\standards\AGENT_PROTOCOLS.md

---

## 1. Environment

- **Host**: Windows 11, Goliath (AMD Ryzen 9 5900X, RTX 4090 24GB, 64GB RAM)
- **Repos root**: `D:\Dev\repos\`
- **Fleet hub (mcd)**: `D:\Dev\repos\mcp-central-docs\`
- **Python**: `C:\Users\sandr\AppData\Local\Programs\Python\Python313\python.exe`
- **uv**: `C:\Users\sandr\.local\bin\uv.exe` — ALWAYS use full path, never naked `uv`
- **Run Python**: `uv run python` — NEVER naked `python` or `python3`
- **Node**: available via scoop; use `npx` for one-offs
- **Shell**: PowerShell 7 (`pwsh`) — never `cmd`, never `bash` for Windows paths
- **Git**: `C:\Program Files\Git\cmd\git.exe` — NOT the scoop shim (swallows stdout)

---

## 2. Build & Test

Most MCP servers follow this pattern:

```powershell
# Install deps
uv sync

# Run MCP server (stdio)
uv run python server.py

# Run webapp (if present)
cd webapp; npm install; npm run dev

# Tests (if present)
uv run pytest
# or
just test
```

Check `start.ps1` or `start.bat` at the repo root for the actual startup sequence.
Port assignments: `D:\Dev\repos\mcp-central-docs\operations\WEBAPP_PORTS.md`

---

## 3. FastMCP Standards (MANDATORY)

- **Current SOTA**: `fastmcp>=3.4.2,<4` (fleet target; minimum `>=3.2.0` until bump) — see `mcp-central-docs\fastmcp\3.4-features.md`
- **Never downgrade** a server's FastMCP version
- **Startup probes**: every server with a lifespan MUST include a shallow connectivity probe
  (see `mcp-central-docs\standards\SOTA_REQUIREMENTS.md` §2.1)
- **Prefab UI**: list/status/stats tools MUST expose `@mcp.tool(app=True)` Prefab cards
- **Portmanteau pattern**: group related ops into one tool with an `operation` enum param;
  do NOT create 40 individual tools
- **`ctx.sample()`**: use for autonomous reasoning steps, not direct LLM calls
- **No stubs**: never implement a tool as a stub and claim it's done — mark explicitly
  as `not_implemented` or raise `NotImplementedError` with a clear message

---

## 3.1 Voice Command Bus (fleet speech)

When work touches **wake word**, **spoken commands**, or **mic/STT routing** across MCP servers:

- **Normative standard:** `mcp-central-docs/standards/VOICE_COMMAND_BUS.md`
- **Registry:** `mcp-central-docs/config/voice_command_bus.yaml`
- **Ingress:** speech-mcp (wake + utterance STT) → **fleet-agent-mcp** `POST /api/voice/intent`
- **Members** (alexa-mcp, yahboom-mcp, …) expose domain tools only — no duplicate wake listeners

---

## 4. PowerShell Rules

```powershell
# CORRECT
New-Item -ItemType Directory -Path "D:\Dev\repos\myrepo"
Remove-Item -Path "D:\Dev\repos\temp\file.txt" -ErrorAction SilentlyContinue
Get-ChildItem -Path "D:\Dev\repos\" -ErrorAction SilentlyContinue

# WRONG — never use these
mkdir   # use New-Item
del     # use Remove-Item
dir     # use Get-ChildItem
&&      # use ; or separate statements
```

- Always quote paths with spaces
- Always use `\` for Windows paths, never `/`
- Redirect long output to temp file: `D:\Dev\repos\temp\op_$(Get-Date -Format 'HHmmss').txt`
- Refresh PATH when needed:
  `$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")`

---

## 5. Git / GitHub

**ALWAYS use `gitops` MCP tools. NEVER use fileops or winops for git.**

| Task | Tool |
|---|---|
| Local git operations | `gitops:git_ops` |
| GitHub operations | `gitops:github_ops` |
| Multi-step git/GitHub | `gitops:git_agentic_workflow` |

If gitops is not available, use: `C:\Program Files\Git\cmd\git.exe` directly.
GitHub user: `sandraschi`. All fleet repos are on GitHub under this account.

---

## 6. Webapp Stack

All new webapps MUST use (see `WEBAPP_SOTA_STANDARDS.md` for full spec):

- React + Vite + TypeScript
- TailwindCSS dark theme (Slate-950 / Zinc-950 backgrounds)
- Lucide React icons
- Zustand state management
- Framer Motion for animations
- Backend: Starlette (default) or FastAPI (when REST surface warrants it)
- Adjacent port pairs: backend on N, frontend on N+1 (e.g. 10762/10763)
- `start.ps1` MUST clear port before binding; `start.bat` is the double-click wrapper

No white/light backgrounds. No Bootstrap. No jQuery. No hardcoded tool lists — always
discover dynamically from the MCP server.

---

## 7. File Routing

| Task | Use |
|---|---|
| Read/write files on Windows | `fileops:file_ops` |
| Windows system ops | `winops` (windows-operations-mcp) |
| Git operations | `gitops:git_ops` |
| GitHub operations | `gitops:github_ops` |
| Container/Docker | `fileops:container_ops` |

Never use bash_tool for Windows paths (C:\, D:\) — bash_tool runs in a Linux container.

---

## 8. Naming & Conventions

- Server repos: `{name}-mcp` (e.g. `calibre-mcp`, `plex-mcp`)
- MCP registration name (in Claude Desktop config): short alias without `-mcp`
  suffix where practical (e.g. `gitops`, `memops`, `calibreops`)
- Disabled servers in Claude Desktop config: prefix key with `_` (e.g. `_vbox-mcp`)
- Port registry: register ALL ports in `mcp-central-docs\operations\WEBAPP_PORTS.md`
  before allocating; reservoir is 10700–10999
- New repo checklist: run the pre-flight questionnaire in
  `.cursor/rules/new-mcp-server-questionnaire.mdc` before writing files
- Required files per repo: `README.md`, `INSTALL.md`, `llms.txt`, `llms-full.txt`,
  `glama.json`, `start.ps1`, `start.bat`
- Webapp repos: `docs/screenshots/` + **Preview** section in README — see
  `standards/README_WEBAPP_SCREENSHOTS.md` (wrapper MCPs: show simplified UI vs host app)
- Wrapper MCP repos: README **How it runs** (headless default explicit) + **Hands-in / Hands-out**
  — see `standards/README_WRAPPER_MCP.md`
- **Promotion / discovery:** see `standards/FLEET_PROMOTION.md` before posting on wrappee GitHub, Goodreads, forums

---

## 9. Critical Don'ts

- **Before editing INSTALL.md or README install sections:** read `standards/AGENT_INSTALL_REFERENCE.md`
- Do NOT commit `node_modules/`, `.venv/`, `__pycache__/`, `*.pyc`, `.env`
- Do NOT hardcode ports — read from config or env
- Do NOT use `pywinauto-mcp` in default IDE chains for webapp work
- Do NOT force-push to `main`
- Do NOT mix Pydantic v1 and v2 in the same server
- Do NOT publish API keys or tokens in any file, ever
- Do NOT implement stubs and describe them as complete

---

## 10. Where to Look

| Question | Answer |
|---|---|
| **Editing INSTALL.md / README install?** | **`standards/AGENT_INSTALL_REFERENCE.md`** — READ FIRST |
| **README Preview / webapp screenshots?** | **`standards/README_WEBAPP_SCREENSHOTS.md`** |
| **Wrapper MCP (headless, hands-in/out)?** | **`standards/README_WRAPPER_MCP.md`** |
| **Promotion / discovery (no spam)?** | **`standards/FLEET_PROMOTION.md`** |
| Which port does X use? | `mcp-central-docs\operations\WEBAPP_PORTS.md` |
| What's in the fleet? | `mcp-central-docs\projects\FLEET_INDEX.md` |
| Full agent protocols | `mcp-central-docs\standards\AGENT_PROTOCOLS.md` |
| Webapp spec | `mcp-central-docs\standards\WEBAPP_SOTA_STANDARDS.md` |
| FastMCP 3.2 features | `mcp-central-docs\standards\SOTA_REQUIREMENTS.md` |
| Tool design patterns | `mcp-central-docs\standards\TOOL_DESIGN_STANDARDS.md` |
| PowerShell patterns | `mcp-central-docs\standards\POWERSHELL_STANDARDS.md` |
| Backend framework choice | `mcp-central-docs\standards\STARLETTE_NO_PYDANTIC_STANDARD.md` |
| Known bugs | `mcp-central-docs\troubleshooting\BUGS_DEPOT.md` |
| Claude Desktop config | `C:\Users\sandr\AppData\Roaming\Claude\claude_desktop_config.json` |
| MCP server logs | `C:\Users\sandr\AppData\Roaming\Claude\logs\mcp-server-{name}.log` (encoding: latin-1) |
