---
title: "Naked-PC Install Standard"
category: standard
status: review
audience: mcp-dev
related:
  - standards/WEBAPP_STANDARDS.md
  - operations/WEBAPP_PORTS.md
  - standards/ONE_CLICK_INSTALL_UX_STANDARD.md
last_updated: 2026-10-05
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
# 2026-10-05: structure repaired only (duplicate front matter, sections 7/7b
# moved after 1-6, broken code fences, collapsed section 6 snippet). Content
# unchanged except section "full dependency chain" justfile line aligned with
# section 7 (windows-shell). Still needs content verification before active.
---

# Naked-PC Install Standard

**Every MCP webapp start.ps1 MUST work on a fresh Windows machine with nothing pre-installed.** This standard exists because non-dev users (e.g. Steve) hit blockers like "vite not found" or "uv not recognised" when cloning a repo and double-clicking start.bat.

These are silent assumptions baked into start.ps1 that break on any machine that isn't Sandra's Goliath.

The experience layer on top of this plumbing (single entry point, `-Check`, `-Yes`, `docs/AI_SETUP.md`, lifecycle tools, tiers) is specified in [ONE_CLICK_INSTALL_UX_STANDARD.md](./ONE_CLICK_INSTALL_UX_STANDARD.md).

---

## What "naked PC" means

A machine with only a stock Windows install - no Python, no Node.js, no npm, no vite, no uv, no pip, no just, no git beyond what Windows ships with.

The only assumption is winget (available on Windows 10 1809+ and all Windows 11).

## The full dependency chain

```
winget  ->  uv        ->  Python 3.11+ (auto-fetched by uv)                     ->  .venv with all Python deps
winget  ->  Node.js   ->  npm                     ->  node_modules/.bin/vite (and all other local frontend tools)
winget  ->  just      ->  available as `just` in PowerShell after install                        (justfile must declare: set windows-shell := ["powershell.exe", ...])
```

**Four winget calls covers everything on a naked PC:**

**Python does NOT need to be installed separately.** uv has managed its own CPython downloads since v0.2.x. When `uv sync` runs on a machine with no Python, it reads `requires-python` from `pyproject.toml` and downloads the appropriate
CPython automatically into its own cache. This means:

- `Require-Command "uv"` covers Python implicitly

- Every repo MUST declare `requires-python = ">=3.11"` (or appropriate version) in pyproject.toml
- Never add a separate `Require-Command "python"` - it's redundant and would  install a system Python that uv ignores anyway

**vite, ruff, tailwind, typescript** are all local devDependencies - installed
by `npm install` into `node_modules/`. They must never be required globally.

**just is installed by start.bat and IS available on all customer PCs after first run.** `just` has a clean winget entry (`Casey.Just`, updated weekly, currently v1.49.0). Add it to the `Require-Command` chain in every start.ps1 and it becomes available
fleet-wide with no manual action from the user.

One Windows-specific issue: `just` defaults to `sh` as its shell, which requires
Git Bash or Cygwin. Since the fleet uses PowerShell, every justfile MUST declare
(see section 7 for why `windows-shell`, not `shell`):

```justfile
set windows-shell := ["powershell.exe", "-NoProfile", "-Command"]
```

Without this, recipes will fail on machines that don't have Git Bash installed.

### 1. Prereq guard via winget

Include `Require-Command` and call it for `uv` and `node`/`npm`:

```powershell
function Require-Command {
    param([string]$Cmd, [string]$WingetId, [string]$Label)
    if (Get-Command $Cmd -ErrorAction SilentlyContinue) { return }
    Write-Host "  $Label not found - installing via winget ..." -ForegroundColor Yellow
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        Write-Host "ERROR: winget unavailable. Install $Label manually ($WingetId)." -ForegroundColor Red
        exit 1
    }
    winget install --id $WingetId --source winget --silent --accept-source-agreements --accept-package-agreements --disable-interactivity
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + `
                [System.Environment]::GetEnvironmentVariable("PATH","User")
    if (-not (Get-Command $Cmd -ErrorAction SilentlyContinue)) {
        Write-Host "Installed $Label but '$Cmd' still not in PATH. Reopen PowerShell and retry." -ForegroundColor Yellow
        exit 1
    }
}
Require-Command "uv"   "astral-sh.uv"      "uv (Python package manager)"
Require-Command "node" "OpenJS.NodeJS.LTS"  "Node.js LTS"
Require-Command "npm"  "OpenJS.NodeJS.LTS"  "npm"
Require-Command "just" "Casey.Just"         "just (command runner)"
```

Winget is available on Windows 10 1809+ and all Windows 11. If a user somehow lacks winget, the error message tells them the winget ID to install manually.

`--source winget` is mandatory, not cosmetic: without it winget also searches
msstore, which fails inside Windows Sandbox with `0x8a15003b` and aborts the
whole search (fleet incident 2026-09-20: naked-matrix `uv` install failed until
pinned). The uv ID is `astral-sh.uv` (`Astral.uv` does not resolve).

### 2. Resolve uv path - never call bare `uv`

```powershell
$uvExe = (Get-Command uv).Source
& $uvExe sync --project $RepoRoot
```

Bare `uv` on some machines resolves to a PATH shim that fails in non-interactive PowerShell sessions. Using the resolved path is reliable everywhere.

### 2b. Hook scripts: resolve every tool absolutely (non-interactive shells have no PATH)

Pre-commit hooks, NSSM services, CI runners, and IDE background tasks all run
**non-interactive**: no login PATH, no npm shims, no `bun`/`npx`/`node` unless
something put them there. A hook entry that works in the dev shell fails there
with `could not determine executable to run` (tvtropes-mcp 2026-10-25: hook script
called bare `npx`; fixed by resolving `node_modules/.bin/biome.cmd` first).
`TRAPS_AND_PITFALLS.md` #18 exempts Node tooling from the absolute-path rule —
that exemption holds for *interactive* shells only.

Resolution chain for vendored hook scripts (first hit wins, else fail loud):

```powershell
$localTool = Join-Path $WebRoot "node_modules/.bin/biome.cmd"
$bunx = Join-Path $env:USERPROFILE ".bun/bin/bunx.exe"
$npx = "C:/Program Files/nodejs/npx.cmd"
if (Test-Path $localTool) { & $localTool ci src/ }
elseif (Test-Path $bunx) { & $bunx --package @biomejs/biome biome ci src/ }
elseif (Test-Path $npx) { & $npx --no-install biome ci src/ }
else { Write-Warning "no biome executable found"; exit 1 }
```

Rules: (1) project-local binary always first (pins the version); (2) absolute
well-known paths only, never bare names; (3) a missing tool is `exit 1` with the
install command printed, never a silent `exit 0`; (4) hooks must be side-effect-free —
no `npm install`/`bun install` inside a hook (it mutates the tree mid-commit;
installing is `just bootstrap`'s job). Reference: `templates/pre-commit-biome.ps1`.

### 3. npm install only if node_modules is absent

```powershell
$npmExe = (Get-Command npm).Source
if (-not (Test-Path (Join-Path $WebRoot "node_modules"))) {
    Push-Location $WebRoot
    & $npmExe install --prefer-offline 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: npm install failed." -ForegroundColor Red
        Pop-Location; exit 1
    }
    Pop-Location
}
```

`--prefer-offline` uses the npm cache on repeat installs (faster for dev).

### 4. Explicit vite guard after npm install

This is the exact bug Steve hit. vite is a devDependency - it must be local:

```powershell
$viteLocal = Join-Path $WebRoot "node_modules\.bin\vite"
if (-not (Test-Path $viteLocal)) {
    Write-Host "ERROR: vite missing from node_modules after npm install." -ForegroundColor Red
    Write-Host "Delete '$WebRoot\node_modules' and re-run." -ForegroundColor Yellow
    exit 1
}
```

### 5. Import smoke-test before the health-wait loop

The health-wait loop will spin for 90 seconds if the backend crashes on startup. A 2-second import check surfaces the error immediately:

```powershell
& $uvExe run --project $RepoRoot python -c "import mypackage.api; print('  [ok] Import OK')"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: import check failed -- see output above." -ForegroundColor Red
    exit 1
}
```

### 6. Helpful error on health timeout

```powershell
if (-not $ready) {
    Write-Host "ERROR: backend health timed out after ${maxWait}s." -ForegroundColor Red
    Write-Host "Run this directly to see the error:" -ForegroundColor Yellow
    Write-Host "  cd $RepoRoot; $uvExe run python -m mypackage.api" -ForegroundColor Yellow
    exit 1
}
```

### 7. justfile MUST use `powershell.exe`, not `pwsh.exe`

`pwsh.exe` is PowerShell 7+, which is NOT installed on a naked PC.
`powershell.exe` is Windows PowerShell 5.1, which ships with every Windows 10/11.

```justfile
# CORRECT
set windows-shell := ["powershell.exe", "-NoProfile", "-Command"]
# WRONG -- pwsh is not installed on naked PCs
set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]
```

Note: use `windows-shell` (not `shell`) so that just falls back to sh on
Linux/macOS if anyone runs these recipes cross-platform.

Enforcement: `POWERSHELL_51_STANDARD.md` is canonical (5.1 everywhere, no
`pwsh` in justfiles, no `#Requires -Version 7` without exemption).
`scripts/Test-Ps51Parse.ps1` gates it in pre-commit + CI + assfix §1J;
genuine 7-needs go in `operations/ps7-exemptions.json`.

### 7b. Recipes MUST NOT call bare `python`

On a naked PC there is no system Python and `python` is not on PATH --
and this bites even on dev machines: naked `python` is unresolvable in a
plain PowerShell session (fleet incident 2026-09-09: fresh `on-ai-takeover`
justfile failed on Goliath itself with `Recipe 'default' could not be run
because just could not find the shell`, then with `'python' is not
recognized` after the shell was fixed).

```justfile
# CORRECT -- project repos (have pyproject.toml + .venv via uv sync)
serve:
  @uv run python -m mypackage.api

# CORRECT -- script-only repos (no pyproject, stdlib scripts only)
lore:
  @py -3 tools/lorecheck.py

# WRONG -- bare python resolves nowhere on a naked PC
lore:
  @python tools/lorecheck.py
```

Rule: recipes call `uv run python` when the repo has a Python project,
`py -3` (Windows launcher) for dependency-free script repos. Never bare
`python`, never bare `python3`.

Why this is enforced (2026-09-09): the cost of a broken first run changed.
Last year a failing README meant the user silently deleted the clone and went
elsewhere. This year they tell their agent (Cursor / Claude / Antigravity) to
install anyway - the agent patches around the failure, gets something half
working, and posts an unfriendly issue with logs attached. A loud, early
failure (`just --list` failing on clone) is now cheaper than a slow one: it
fires before the agent starts improvising. Every rule in sections 1-7b is
shaped by that: fail in the first ten seconds, with the fix printed next to
the error.

Fleet audit 2026-09-09: 242 justfiles scanned. 0 others use bare `python`
(fleet already standardised on `uv run python`), but **24 justfiles lack any
`windows-shell` declaration** and will fail the same way on machines without
Git Bash on PATH: agy-mcp, ahk-linter, avatar-pipeline-mcp, benny-the-dog-mcp,
chitchat, comms-mcp, demo-app, edge-bookmark-mcp-server-work,
fritz-pipeline-test, fritz-test, fritz-test-work, huggingface-mcp,
mcp-agent-session-summaries, mcp-test-suite, obscura-mcp, prc-shopping-mcp,
secrets-mcp, security-gym, sfx-mcp, stripe-mcp (+4 more, see audit script
output). Fix: add the section 7 `windows-shell` line per repo with a `just --list`
smoke test. Tracked as follow-up; each repo fix is one line + one test.

---

## What MUST be local (never assumed global)

| Tool | Location | How installed |
|---|---|---|
| vite | `webapp/node_modules/.bin/vite` | `npm install` (devDependency) |
| tailwindcss | `webapp/node_modules/.bin/tailwindcss` | `npm install` |
| typescript / tsc | `webapp/node_modules/.bin/tsc` | `npm install` |
| ruff | `.venv/Scripts/ruff.exe` | `uv sync` (dev dep) |
| pytest | `.venv/Scripts/pytest.exe` | `uv sync` (dev dep) |

## What CAN be assumed (present on Sandra's Goliath, not on Steve's machine)

Nothing. Assume zero. winget handles it.

## INSTALL.md requirement

Every repo with a start.bat MUST have an `INSTALL.md` at the root with:

1. The two-command quick start (`git clone` + `start.bat`)
2. A manual step-by-step for when start.bat itself fails
3. A table of what is/isn't required globally
4. Troubleshooting section for ConPTY pipe teardown (`0x800700e8`) and port collision handling

See `D:\Dev\repos\calibre-mcp\INSTALL.md` and `D:\Dev\repos\aiwatcher-mcp\INSTALL.md` as reference implementations.

---

## 8. Zero Dependency on Private Central Infrastructure (`mcp-central-docs`)

**CRITICAL ARCHITECTURAL REQUIREMENT**:
`mcp-central-docs` is a private, internal repository. External users, open-source contributors, and agents installing on clean machines CANNOT clone it.

1. **Bi-Modal Launchers**: Every repo's `start.ps1` must be bi-modal:
   - **Mode 1 (Fleet Central)**: If `Invoke-FleetWebappStart.ps1` is present, use it for fleet-wide features.
   - **Mode 2 (Autonomous Standalone)**: If missing, launch standalone using `uv run` and local `npm run dev` directly from the repo's own `fleet-start.config.ps1`.
2. **Strictly Relative Config Paths**: All paths in `fleet-start.config.ps1` (`WebRoot`, `WorkDir`, `PythonPath`, `UvProject`) must be relative to the repo root (`webapp\frontend`, `webapp\backend`, `src`), NEVER hardcoded to `D:\Dev\repos\...` or developer workstations.
3. **No Private Imports/Tools in CI or Justfiles**: Never allow a `justfile` recipe or CI step to depend unconditionally on private internal scripts. Guard internal checks with `if (Test-Path ...)` or keep them in central fleet scripts.

## Fleet remediation status

| Repo | Status |
|---|---|
| aiwatcher-mcp | Fixed 2026-04-24 |
| arxiv-mcp | Fixed 2026-04-24 |
| All others | TODO - scan needed |

To find all start.ps1 files still using bare `npm install` without node check:

```powershell
Get-ChildItem D:\Dev\repos -Recurse -Filter "start.ps1" |
    Select-String "npm install" |
    Where-Object { $_.Line -notmatch "Require-Command" } |
    Select-Object -ExpandProperty Path |
    Sort-Object -Unique
```

---

## Workstation baseline (install on every machine)

These are not start.ps1 dependencies - they're personal workstation tools that should be installed on any new PC in the fleet:

```powershell
# Terminal / navigation
winget install Notepad++.Notepad++
winget install Tailscale.Tailscale
winget install AntibodySoftware.WizTree
winget install AntibodySoftware.WizFile
winget install ajeetdsouza.zoxide       # smarter cd - z proj jumps to project
winget install Clement.bottom            # graphical system monitor (terminal)
winget install sharkdp.hyperfine         # command benchmarking
winget install chmln.sd                  # sed replacement with readable regex
winget install ya-z.yazi                 # terminal file manager with previews
winget install muesli.duf                # df replacement with colored output

# Archive / backup
winget install 7zip.7zip
winget install Hasleo.BackupSuiteFree
winget install Syncthing.Syncthing        # P2P folder sync - keeps D:\dev\repos warm across machines (see integrations/syncthing.md)

# Media / documents
winget install calibre.calibre           # ebook manager + PDF store
winget install Plex.PlexMediaServer      # media server

# AI development tools
winget install SST.OpenCodeDesktop         # opencode WinApp - Windows desktop UI
winget install Anysphere.Cursor            # Cursor IDE (AI editor)
winget install ZedIndustries.Zed            # Zed editor (Rust, fast, GPUI)

# opencode CLI + TUI - install after WinApp or standalone:
#   CLI:  opencode command (auto-bundled with WinApp, or via `npm install -g @opencode/cli`)
#   TUI:  opencode-tui (terminal UI, separate binary from GitHub releases)
# See https://github.com/anomalyco/opencode for all variants

# Claude Desktop - not on winget, download from https://claude.ai/download
# Antigravity - not on winget, download from https://antigravity.antigravity.ai

# Virtualization (if compatible - see caveats below)
winget install Oracle.VirtualBox
```

**Tailscale:** Auth via `tailscale up` after install. Required for fleet cross-machine access (ssh, webapp testing, MCP server connections between Goliath and MiniPC).

**Notepad++:** Lightweight editor for quick file peeks. No config needed.

**VirtualBox compatibility:**

| Machine | Compatible | Notes |
|---------|-----------|-------|
| Goliath | ✅ Yes | Full hardware virt support (AMD Ryzen with SVM) |
| MiniPC | ✅ Yes | 4-core CPU supports VT-x/AMD-V. UHD 600 iGPU handles 2D acceleration fine. 16GB RAM limits concurrent VMs - one at a time with ≤4GB assigned |

VirtualBox 7+ is required for the fleet (VBoxManage CLI, unattended installs). The winget install pulls the latest stable. If winget fails (region-restricted), download manually from [virtualbox.org](https://www.virtualbox.org/wiki/Downloads).

## Optional workstation tools (fleet dev needs)

These are per-workstation decisions, not start.ps1 dependencies. Documented here because the MiniPC (16GB, 4-core, Intel UHD 600, 240GB SSD) has different constraints than Goliath (64GB, 12-core, RTX 4090).

### Container runtime (Docker Desktop vs Podman)

| Condition | Decision |
|-----------|----------|
| **Goliath** (64GB RAM, powerful) | Docker Desktop is fine if stable. If Dockerd crashes silently (known issue), switch to Podman |
| **MiniPC** (16GB RAM, small SSD) | Skip Docker Desktop. It idles at ~2GB RAM and ~8-10GB disk. Podman is lighter (~800MB, ~4-6GB) but still consumes scarce resources. For fleet sandbox testing, a lightweight Ubuntu VM in VirtualBox is more resource-efficient |

Install Podman on MiniPC if needed:

```powershell
winget install RedHat.Podman
podman machine init --cpus 2 --memory 2048 --disk-size 10
```

### Local LLM inference (Ollama / LM Studio)

| Condition | Decision |
|-----------|----------|
| **Goliath** (RTX 4090 24GB) | Install both. Ollama for CLI/API, LM Studio for browsing. Can run 7B-13B models at usable speed on GPU |
| **MiniPC** (UHD 600, 16GB CPU-only) | Install both but stick to 1B-3B models (Phi-3, Gemma-2-2B, Gemma-4-2B, Qwen2.5-3B). CPU inference at ~15-25 tok/s for 2B models. GPU (Intel UHD 600) cannot accelerate inference - no tensor cores, too few EUs |

```powershell
# Ollama (CLI + API server)
winget install Ollama.Ollama
ollama pull gemma4:2b

# LM Studio (GUI)
winget install ElementLabs.LMStudio
```

### Docker Desktop (Goliath only, optional)

Install only on Goliath for integration testing:

```powershell
winget install Docker.DockerDesktop
```

Expect ~2GB RAM idle and ~8-12GB disk. If the daemon hangs (triple-kill scenario), replace with Podman (see `integrations/virtualization/podman.md`).
