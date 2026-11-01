---
title: "AGENTS.md - Fleet-Wide Agent Instructions"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-18
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# AGENTS.md - Fleet-Wide Agent Instructions
# sandraschi / mcp-central-docs
# Last updated: 2026-05-28

> This file is the canonical source of truth for AI coding agents working in ANY repo
> in the D:\Dev\repos\ fleet. Per-repo AGENTS.md files are thin overrides only.
> Full standards: D:\Dev\repos\mcp-central-docs\standards\AGENT_PROTOCOLS.md

---

## 1. Environment

- **Host**: Windows 11, Goliath (AMD Ryzen 9 5900X, RTX 4090 24GB, 64GB RAM)
- **Repos root**: `D:\Dev\repos\`
- **Fleet info depot (aka "mcd")**: `D:\Dev\repos\mcp-central-docs\`
- **Python**: `C:\Users\<user>\AppData\Local\Programs\Python\Python313\python.exe`
- **Run Python**: `uv run python` - NEVER naked `python` or `python3`
- **Node**: available via scoop; use `npx` for one-offs
- **Shell**: PowerShell 7 (`pwsh`) - never `cmd`, never `bash` for Windows paths
- **Git**: `C:\Program Files\Git\cmd\git.exe` - NOT the scoop shim (swallows stdout)
- **uv**: `C:\Users\<user>\.local\bin\uv.exe` - ALWAYS use full path, never naked `uv`
- **bun**: `C:\Users\<user>\.bun\bin\bun.exe` - JS package manager, fleet standard for webapps
- **just**: `C:\Users\<user>\scoop\shims\just.exe` (or `C:\Users\<user>\.local\bin\just.exe`) - ALWAYS use full path, never naked `just`
- **ripgrep (rg)**: `C:\Users\<user>\AppData\Local\Microsoft\WinGet\Links\rg.exe` - ALWAYS use full path, never naked `rg`
- **fd**: `C:\Users\<user>\.local\bin\fd.exe` - ALWAYS use full path, never naked `fd`
- **Ruff**: `C:\Users\<user>\AppData\Local\Programs\Python\Python313\Scripts\ruff.exe`
- **Biome**: `C:\Users\<user>\.local\bin\biome.exe`
- **actionlint**: `C:\Users\<user>\.local\bin\actionlint.exe`
- **taplo**: `C:\Users\<user>\.cargo\bin\taplo.exe`
- **yamllint**: `C:\Users\<user>\.local\bin\yamllint.exe`
- **hadolint**: `C:\Users\<user>\.local\bin\hadolint.exe`
- **shellcheck**: `C:\Users\<user>\.local\bin\shellcheck.exe`
- **markdownlint**: `C:\Users\<user>\AppData\Roaming\npm\markdownlint.cmd`
- **ollama**: `C:\Users\<user>\AppData\Local\Programs\Ollama\ollama.exe`
- **winget**: `C:\Users\<user>\AppData\Local\Microsoft\WindowsApps\winget.exe`

---

## 2. Build & Test (Two Architectural Tracks as of 2026-10-17)

### Track A: Pure-Rust ArtCraft Repos (`Cargo.toml` at root -- e.g. `rust-devices-mcp`)
Canonical standard: **[`standards/RUST_ARTCRAFT_STANDARD.md`](./RUST_ARTCRAFT_STANDARD.md)**.
Python/FastMCP/Starlette/port-claiming rules are **INVALIDATED** for Pure-Rust repos.

```powershell
$env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"

# Lint gate (deny unwrap_used, expect_used, panic, todo, unimplemented)
cargo clippy --workspace --all-targets --all-features -- -D warnings

# Unit + headless dispatch + parity tests
cargo test --workspace

# Format check
cargo fmt --all --check

# Run CLI (--json) or MCP server (stdio)
cargo run -p rust-devices-mcp -- status --json
cargo run -p rust-devices-mcp -- mcp
```

### Track B: Legacy Python / FastMCP Repos (`pyproject.toml` at root)

```powershell
# Install deps
uv sync

# Run MCP server (stdio)
uv run python server.py

# Run webapp (if present)
cd webapp; bun install; bun run dev

# Tests (if present)
uv run pytest
# or
just test
```

Check `justfile`, `start.ps1`, or `start.bat` at the repo root for the actual startup sequence.
Port assignments (Python sidecar webapps only; Pure-Rust L3 apps call L1 in-process with zero ports): `D:\Dev\repos\mcp-central-docs\operations\WEBAPP_PORTS.md`

---

## 3. FastMCP Standards (Legacy Python Track Only -- Superseded by `RUST_ARTCRAFT_STANDARD.md` for Rust Repos)

> **2026-10-17 Regime Change:** If a repo is a Pure-Rust ArtCraft workspace (`Cargo.toml` at root), **skip §3 entirely** and follow **[`standards/RUST_ARTCRAFT_STANDARD.md`](./RUST_ARTCRAFT_STANDARD.md)**.

- **Current SOTA (Python repos)**: `fastmcp>=3.4.4,<4` (minimum for NEW Python repos) - see `mcp-central-docs\fastmcp\3.4-features.md`
- **Never downgrade** a server's FastMCP version
- **Startup probes**: every server with a lifespan MUST include a shallow connectivity probe
  (see `mcp-central-docs\standards\SOTA_REQUIREMENTS.md` §2.1)
- **Prefab UI**: list/status/stats tools MUST expose `@mcp.tool(app=True)` Prefab cards
- **Portmanteau pattern**: group related ops into one tool with an `operation` enum param;
  do NOT create 40 individual tools
- **`ctx.sample()`**: use for autonomous reasoning steps, not direct LLM calls
- **No stubs**: never implement a tool as a stub and claim it's done - mark explicitly
  as `not_implemented` or raise `NotImplementedError` with a clear message

---

## 3.1 Voice Command Bus (fleet speech)

When work touches **wake word**, **spoken commands**, or **mic/STT routing** across MCP servers:

- **Normative standard:** `mcp-central-docs/standards/VOICE_COMMAND_BUS.md`
- **Registry:** `mcp-central-docs/config/voice_command_bus.yaml`
- **Ingress:** speech-mcp (wake + utterance STT) → **fleet-agent-mcp** `POST /api/voice/intent`
- **Members** (alexa-mcp, yahboom-mcp, …) expose domain tools only - no duplicate wake listeners

---

## 4. PowerShell Rules

```powershell
# CORRECT
New-Item -ItemType Directory -Path "D:\Dev\repos\myrepo"
Remove-Item -Path "D:\Dev\repos\temp\file.txt" -ErrorAction SilentlyContinue
Get-ChildItem -Path "D:\Dev\repos\" -ErrorAction SilentlyContinue

# WRONG - never use these
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

## 4.1 New Repo Gate (HARD RULE)

> **2026-10-17 Architecture Triage First:** Before creating or porting a repo, check the **4-Bucket Triage Matrix** in **[`standards/RUST_ARTCRAFT_STANDARD.md` §3](./RUST_ARTCRAFT_STANDARD.md#3-fleet-rustification-strategy-the-4-bucket-triage-matrix)**:
> - **Bucket A (REST/Cloud/SQLite/CLI/System) & Bucket B (Clean Hardware/SCPI/LAN IoT):** Build as a **Pure-Rust ArtCraft 3-Tier Workspace** following **[`standards/RUST_ARTCRAFT_STANDARD.md`](./RUST_ARTCRAFT_STANDARD.md)** (`L1 <domain>-core`, `L2 <domain>-mcp`, `L3 <domain>-app`). Do NOT apply the Python/FastMCP/Starlette checklist below.
> - **Bucket C (Embedded Host-App Python) & Bucket D (PyTorch/CUDA ML):** Follow the Python/FastMCP gate below.
>
> **Default: Rust.** Buckets A/B cover nearly every new repo (REST, cloud, SQLite, CLI,
> system, clean hardware). A new repo builds Pure-Rust unless the dossier names a Bucket
> C/D blocker (host-owned process, CUDA kernels, no native equivalent) in
> `docs/DEVELOPMENT.md` (or `HANDOVER.md`): name the bucket, name the blocker.
> "Faster to write" is not a blocker. Scaffold with `just new-rust <domain>` (zero tokens).

**North star (Python track) - assfix-zero:** The initial build must be so complete that the first
`assfix <repo>` / `assess and fix <repo>` finds **nothing CRITICAL or HIGH** to criticize.
Assfix is for drift later - not a cleanup pass for a runt scaffold.
Full target map: **`standards/NEW_REPO_BUILD_COMPLETE.md`**.

When asked to create, scaffold, or build a new Python MCP server repo from scratch:

**PAUSE. Do NOT write any files yet.** Read ALL of these FIRST:

| # | Standard | Why |
|---|----------|-----|
| 00 | `standards/RUST_ARTCRAFT_STANDARD.md` | **Check Bucket A–D triage first!** If Pure-Rust, use the ArtCraft 6-Gate DoD instead of this table |
| 0 | `standards/NEW_REPO_BUILD_COMPLETE.md` | **Assfix-zero** - build so first assess finds nothing CRITICAL/HIGH |
| 1 | `standards/AGENT_PROTOCOLS.md` | Full protocol tree |
| 2 | `standards/JUNE_2026_STANDARDS_BAR.md` | Version floor, retired tools |
| 3 | `standards/SOTA_REQUIREMENTS.md` | FastMCP 3.4.4 mandatory features |
| 4 | `standards/TOOL_DESIGN_STANDARDS.md` | Portmanteau, annotations, Prefab, pagination |
| 5 | `standards/README_STRUCTURE.md` | README, INSTALL, **docs/** stack including **ONBOARDING** (default - wrappees need install) |
| 6 | `standards/NAKED_PC_INSTALL_STANDARD.md` | start.ps1 Require-Command, winget |
| 6b | `standards/START_SCRIPT_STANDARD.md` | `start.ps1` + **`start.bat`** + **`mcp-central-docs/starts/{repo}-start.bat`** (Sandra QoL) |
| 6c | `standards/ONBOARDING_STANDARD.md` | **Default gate:** first-timer wrappee/account flow + **big red under-hero CTA** + **MOCK-until-onboarded** UI |
| 7 | `standards/WEBAPP_SOTA_STANDARDS.md` | AppLayout + **catch-them-all** pages + Local LLM + data-testid |
| 8 | `standards/BUN_STANDARDS.md` | bun / npm lockfile; Biome for JS/TS |
| 9 | `standards/PACKAGING_STANDARDS.md` | Two-track (MCPB + Tauri) |
| 10 | `standards/MCPB_PACKAGING_STANDARDS.md` | .mcpb layout, manifest, prompts 3-4-100, **`.mcpbignore` mandatory** |
| 10b | `standards/GITIGNORE_STANDARDS.md` | **`.gitignore` BEFORE first `git add`** - no node_modules, target/, .venv, data DBs |
| 11 | `standards/rules/tauri_nsis_building.md` | Tauri 2.0, embedded backend, NSIS, CORS |
| 12 | `standards/rules/chat_skills_prefab_standard.md` | Chat page, personalities, memory |
| 13 | `fastmcp/3.4-features.md` | Lifespan, prompts, resources, sampling |
| 14 | `standards/GITHUB_ACTIONS_NO_PRIVATE_CI.md` | Private: Actions disabled; still ship Windows CI file + `just ci` |
| 15 | `standards/TOOL_DESIGN_STANDARDS.md` | **No "planned" stubs** - every advertised op must work (dry-run OK) |
| 16 | `standards/TESTING_GUIDE.md` | **No undeclared mocks** - fixtures/dry-run/fakes must be named and documented |
| 17 | `standards/RAG_OPERATIONS_STANDARD.md` | RAG/Index Operations standard -- background sweeps, live polling, no 10s timeouts |
| 18 | `standards/FLEET_CROSSCONNECT_STANDARD.md` | Fleet crossconnects, companion servers, 1-hop rule, soft degradation |

Report: "Read N standards. Building to assfix-zero spec." Build the complete repo in one pass.
Do **not** leave CRITICAL/HIGH gaps for a later assfix.

**Ship checklist (HARD - before calling done):**

0. **Assfix-zero self-check** - Mentally (or actually) run `patterns/repo-assess-and-fix.md` Phase 1 against the new tree. Zero CRITICAL, zero HIGH. Residual MEDIUM/LOW only with explicit rationale. See `NEW_REPO_BUILD_COMPLETE.md`.
1. **Tools fully implemented** - README must not say "planned". Portmanteau ops return real behavior (dry-run short-circuit OK). No `planned: true` stubs.
2. **Webhooks installed** - inbound receive endpoint + secret env + list/ops (or domain-native webhook CRUD when the host API has them). Document in TOOLS.md.
3. **docs/ stack** - `CONFIGURATION.md`, `DEVELOPMENT.md`, `TOOLS.md`, `TROUBLESHOOTING.md` (+ docs/README index).
4. **Lint green** - `ruff check` + `ruff format --check` + webapp `biome check` + `tsc --noEmit`.
5. **CI** - `.github/workflows/ci.yml` Windows-only lightweight (ruff, biome, pytest, tsc). Private: Actions stay account-disabled; agents run `just ci` locally and it must pass.
6. **Webapp catch-them-all** - Dashboard hero+KPIs, Inbox, Tools, Skills, Chat, Settings LLM, Help page, Logs, domain pages.
7. **No undeclared mocks** - Test doubles, dry-run paths, and empty-without-credentials API responses MUST be declared. Undeclared fake KPIs that look live fail FakeFind. **Allowed (declared):** MOCK-badged sample UI until onboarding succeeds (`ONBOARDING_STANDARD.md` § Mock-until-onboarded).
8. **Onboarding (DEFAULT - nearly always)** - Assume onboarding is required. Wrappees must be installed/runnable for the user to get joy (**even `notepadpp-mcp` needs Notepad++**; same for Blender, Unity, Mastodon, World Labs, Plex, …). Ship all of:
   - `docs/ONBOARDING.md` (what for, money/CC, pitfalls, sanity check)
   - INSTALL link to ONBOARDING near the top
   - Webapp: **big red onboarding button under Dashboard hero** (`data-testid="onboarding-cue"`)
   - Webapp: **MOCK-until-onboarded** sample KPIs/lists (visible **MOCK** badges; fake names e.g. Joe Mocky / Sandra Mockinger) that **clear after successful onboarding**
   - Health/probe signal that flips “configured” when the wrappee/account is ready  
   **N/A only (rare):** no wrappee **and** no online account necessary - write `Onboarding: N/A` + one-line rationale in `docs/DEVELOPMENT.md`. If either a wrappee or an online account exists, onboarding is mandatory. Missing = **gate fail**.
9. **Good `.gitignore` (HARD)** - Exists **before** first `git add`. Must ignore at least: `node_modules/` / `**/node_modules/`, `.venv/`, `target/` / `**/target/` (Tauri + rust-analyzer), `webapp/dist/`, `src-tauri/target/`, `src-tauri/binaries/`, **`mcpb/src/`** (MCPB pack staging - exact copy of `src/`, never commit), `data/` or `*.sqlite3` / `*.db*`, `.env` (keep `.env.example`), `.coverage`, `*.mcpb`, **`*.bak` and `*.bak.*`** (timestamped sneak-in specialist backups accumulate - both patterns required). Copy from `GITIGNORE_STANDARDS.md` §1b. Spot-check `git status` for `node_modules` / `target` / `mcpb/src` / `*.bak*` before commit. Committing those = **gate fail**.
10. **Good `.mcpbignore` (HARD)** - Exists on every MCPB-packaged repo. Must exclude `.venv/`, `node_modules/`, `webapp/`, `src-tauri/`, `tests/`, `data/`, `target/`, build artifacts, **`*.bak` and `*.bak.*`**. Pack script **MUST wipe+recopy** `src/` → `mcpb/src/` immediately before `mcpb pack` (gitignore alone does not stop a stale local twin from shipping). See `MCPB_PACKAGING_STANDARDS.md` § Fresh copy before pack. Packing `.venv` or `node_modules` into `.mcpb` = **gate fail**.
11. **MCPB prompts 3-4-100 (HARD)** - Not a runt: `assets/prompts/system.md` **≥ 3,000 words**, `assets/prompts/user.md` **≥ 4,000 words**, `assets/prompts/examples.json` **≥ 100** tool-call example objects. Verify with word-count + JSON length before pack (see `MCPB_PACKAGING_STANDARDS.md` §2.3b). Stub/TODO prompts = **gate fail**.

**Webapp ship check:** Do **not** ship a domain-only runt. See `WEBAPP_SOTA_STANDARDS.md` §III.

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
- Zustand state management (`store/llm.ts` + `lib/provider.ts` for LLM probe)
- Framer Motion for animations
- Backend: FastAPI + Pydantic v2 (default since 2026-09-30); existing Starlette repos migrate only when their REST layer is reworked (see `STARLETTE_NO_PYDANTIC_STANDARD.md`)
- Adjacent port pairs: backend on N, frontend on N+1 (e.g. 10762/10763)
- `start.ps1` MUST clear port before binding; `start.bat` is the double-click wrapper
- **Catch-them-all pages** (not optional): Dashboard hero+KPIs, Inbox, Tools, Skills, Chat, Settings (LLM providers), Help page, Logs - plus domain pages

No white/light backgrounds. No Bootstrap. No jQuery. No hardcoded tool lists - always
discover dynamically from the MCP server. A thin "Outbox + stub Settings" webapp fails the gate.

---

## 7. File Routing

| Task | Use |
|---|---|
| Read/write files on Windows | `fileops:file_ops` |
| Windows system ops | `winops` (windows-operations-mcp) |
| Git operations | `gitops:git_ops` |
| GitHub operations | `gitops:github_ops` |
| Container/Docker | `fileops:container_ops` |
| Web search in chat | `searchstudio:searchops` first (receipts prove coverage) |

Web search in chat: `searchops` first; `fetch` / `openserp_extract` / memops
web search only as receipt-directed fallbacks for what the receipts show as
uncovered. Rationale: the fallbacks fail silently on harmless queries, while
`searchops` receipts prove what was actually searched.

Never use bash_tool for Windows paths (C:\, D:\) - bash_tool runs in a Linux container.

---

## 8. Naming & Conventions

- Server repos: `{name}-mcp` (e.g. `calibre-mcp`, `plex-mcp`)
- MCP registration name (in Claude Desktop config): short alias without `-mcp`
  suffix where practical (e.g. `gitops`, `memops`, `calibreops`)
- Disabled servers in Claude Desktop config: prefix key with `_` (e.g. `_vbox-mcp`)
- Port registry: register ALL ports in `mcp-central-docs\operations\WEBAPP_PORTS.md`
  before allocating; reservoir is 10700-15000
- New repo checklist: run the pre-flight questionnaire in
  `.cursor/rules/new-mcp-server-questionnaire.mdc` before writing files
- Required files per repo: `README.md`, `INSTALL.md`, `llms.txt`, `llms-full.txt`,
  `glama.json`, `start.ps1`, `start.bat`, `CONTRIBUTING.md` (public repos;
  private/experimental exempt until public - see `GITHUB_HYGIENE_STANDARDS.md`)
- Webapp repos: `docs/screenshots/` + **Preview** section in README - see
  `standards/README_WEBAPP_SCREENSHOTS.md` (wrapper MCPs: show simplified UI vs host app)
- Wrapper MCP repos: README **How it runs** (headless default explicit) + **Hands-in / Hands-out**
  - see `standards/README_WRAPPER_MCP.md`
- **Promotion / discovery:** see `standards/FLEET_PROMOTION.md` before posting on wrappee GitHub, Goodreads, forums

---

## 9. Critical Don'ts

- **Before editing INSTALL.md or README install sections:** read `standards/AGENT_INSTALL_REFERENCE.md`
- Do NOT commit `node_modules/`, `.venv/`, `__pycache__/`, `*.pyc`, `.env`
- Do NOT hardcode ports - read from config or env
- Do NOT hardcode author-machine paths (`C:\Users\<user>\...`, `D:\Dev\repos\...`) in runtime code or example configs - derive from `__file__`, `Path.home()`, `%LOCALAPPDATA%`/`%APPDATA%`, `shutil.which`, keep env overrides (BUG-079; gate in `patterns/repo-assess-and-fix.md` 1J)
- Do NOT use `pywinauto-mcp` in default IDE chains for webapp work
- Do NOT force-push to `main`
- Do NOT use `Test-Path ".git"` to check for git repos - PowerShell doesn't see hidden items; use `git rev-parse --git-dir` instead
- Do NOT run `git init` on any directory that already has a `.git` folder - this silently destroys all commit history
- Do NOT mix Pydantic v1 and v2 in the same server
- Do NOT publish API keys or tokens in any file, ever
- Do NOT implement stubs and describe them as complete
- Do NOT blindly execute LLM-suggested resource fetch commands (clone, install, pull) without verifying the target - **HalluSquatting** exploits LLM hallucination of repo/skill names to deliver promptware (see `standards/threats/AGENTIC_BOTNETS.md`). Prefer explicit URLs over short names.
- Do NOT author multi-line file content with a Bash heredoc (`cat > file <<'EOF'`) - it intermittently fails on this Windows/Git-Bash setup and writes nothing. Use the Write tool. See `troubleshooting/details/BUG-031_Bash_Heredoc_Intermittent_Break.md`.
- Do NOT patch files with inline Python (`python - <<'PY'`, `python -c`) - **Python's string-literal parser silently converts backslash escapes in your replacement text.** `"D:\Dev\repos\x"` becomes `D:` + `\D` + `ev` + CR + `epos` + CR + `x`, because `\r \n \t \b \f \v \a` are all *valid* escapes and convert without warning. Worst case observed: a `# noqa` insertion swallowed the rest of a line and silently deleted dict entries - valid Python, ruff clean, wrong behaviour, no error anywhere. Use **Edit** for targeted replacements and **Write** for whole files; if a script must patch, use raw strings (`r"D:\Dev\repos"`) and read the result back. See `troubleshooting/details/BUG-039_Heredoc_Python_Escape_Mangling.md`.

---

## 10. Where to Look

| Question | Answer |
|---|---|
| **Editing INSTALL.md / README install?** | **`standards/AGENT_INSTALL_REFERENCE.md`** - READ FIRST |
| **Tooling / local-vs-cloud cost model?** | **`standards/TOOLING_COST_MODEL.md`** |
| **Local LLM economics / doctrine?** | **`standards/LOCAL_LLM_FIRST_DOCTRINE.md`** |
| **README Preview / webapp screenshots?** | **`standards/README_WEBAPP_SCREENSHOTS.md`** |
| **Wrapper MCP (headless, hands-in/out)?** | **`standards/README_WRAPPER_MCP.md`** |
| **Promotion / discovery (no spam)?** | **`standards/FLEET_PROMOTION.md`** |
| **Editing README/docs/dashboard prose?** | **`standards/FLEET_HYGIENE_STANDARDS.md`** - no unearned "production-ready"/"industrialized"/emoji-train claims |
| **Wiring a new crossconnect between fleet repos?** | **`patterns/FLEET_MESHING_PHILOSOPHY.md`** + `patterns/CROSSCONNECT_PATTERN.md` - check for existing overlap first |
| **Ending a turn with source changes in a shared repo?** | **`patterns/AGENT_BRANCH_DISCIPLINE.md`** - finish and commit, or revert; never leave dirty source for "someone else" |
| **Auditing a repo's tool coverage against the software it wraps, or a competitor?** | **`patterns/WRAPPEE_CAPABILITY_DRIFT_SOP.md`** - explicit per-repo request only, report not a fix |
| Which port does X use? | `mcp-central-docs\operations\WEBAPP_PORTS.md` |
| What's in the fleet? | `mcp-central-docs\projects\FLEET_INDEX.md` |
| **Is X installed / cloned on this machine?** | Check ALL of these before answering: working tree (`D:\Dev\repos\<name>`), `D:\Dev\repos\_upstream\` (third-party checkouts incl. all xyzcraft + Strata: MIXED wiring, check `git remote -v` per dir - `origin=storytold` is a pure clone (pull-only), `origin=sandraschi` + `upstream=storytold` is a fork (pushable, PRs go upstream). Default read-only either way; never modify without a reason), `D:\Dev\repos\external\` (66 vendored reference clones - migration planned, do NOT move anything, fleet apps link into it), `D:\Dev\external\` (stray root-level dir, known misplaced: `calibre` duplicates `repos\external\calibre`), `D:\Dev\repos\_archives\` (frozen). Declaring "not installed" after checking one location is a defect (observed 2026-10-14: Strata declared absent while `_upstream\Strata` held engine + venv + port-11235 config). |
| **What repos are dirty/uncommitted right now?** | `mcp-central-docs\operations\fleet.lock.json` - **tracked**, the machine-readable source. `operations\fleet-status.md` is the human-readable digest but is **gitignored/untracked**: it exists only on Sandra's machine, so on a fresh clone or CI runner it will be absent. Never cite it as the source; - PRs, issues, uncommitted files per repo, sync drift |
| **What did another agent/session actually DO recently?** | `mcp-central-docs\operations\session-log\` (dated `YYYY-MM-DD.md` + `aiwatcher\` subdir; convention: `operations\session-log\README.md`, 30-day retention) (plain-language work log, written by BOTH human-driven coding agents AND autonomous fleet agents like Fritz/AIWatcher, each entry clearly marked with which - add your own entry at session end / after any heartbeat run that made a real change) |
| Full agent protocols | `mcp-central-docs\standards\AGENT_PROTOCOLS.md` |
| Webapp spec | `mcp-central-docs\standards\WEBAPP_SOTA_STANDARDS.md` |
| FastMCP 3.2 features | `mcp-central-docs\standards\SOTA_REQUIREMENTS.md` |
| Tool design patterns | `mcp-central-docs\standards\TOOL_DESIGN_STANDARDS.md` |
| PowerShell patterns | `mcp-central-docs\standards\POWERSHELL_STANDARDS.md` |
| Backend framework choice | `mcp-central-docs\standards\STARLETTE_NO_PYDANTIC_STANDARD.md` |
| Known bugs | `mcp-central-docs\troubleshooting\BUGS_DEPOT.md` |
| Claude Desktop config | `C:\Users\<user>\AppData\Roaming\Claude\claude_desktop_config.json` |
| MCP server logs | `C:\Users\<user>\AppData\Local\Claude\Logs\mcp-server-{name}.log` (encoding: latin-1; pre-2026-08-21: `AppData\Roaming\Claude\logs`) |
