### 7. justfile MUST use `powershell.exe`, not `pwsh.exe``pwsh.exe` is PowerShell 7+, which is NOT installed on a naked PC.`powershell.exe` is Windows PowerShell 5.1, which ships with every Windows 10/11.```justfile# CORRECTset windows-shell := ["powershell.exe", "-NoProfile", "-Command"]# WRONG -- pwsh is not installed on naked PCsset windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]```Note: use `windows-shell` (not `shell`) so that just falls back to sh onLinux/macOS if anyone runs these recipes cross-platform.---title: "Naked-PC Install Standard"category: standardstatus: activeaudience: mcp-devrelated:  - standards/WEBAPP_STANDARDS.md  - operations/WEBAPP_PORTS.mdlast_updated: 2026-06-16---# Naked-PC Install Standard**Every MCP webapp start.ps1 MUST work on a fresh Windows machine with nothing pre-installed.**This standard exists because non-dev users (e.g. Steve) hit blockers like"vite not found" or "uv not recognised" when cloning a repo and double-clickingstart.bat. These are silent assumptions baked into start.ps1 that break on anymachine that isn't Sandra's Goliath.---## What "naked PC" meansA machine with only a stock Windows install ÔÇö no Python, no Node.js, no npm,no vite, no uv, no pip, no just, no git beyond what Windows ships with.The only assumption is winget (available on Windows 10 1809+ and all Windows 11).## The full dependency chain```winget  ÔåÆ  uv        ÔåÆ  Python 3.11+ (auto-fetched by uv)                     ÔåÆ  .venv with all Python depswinget  ÔåÆ  Node.js   ÔåÆ  npm                     ÔåÆ  node_modules/.bin/vite (and all other local frontend tools)winget  ÔåÆ  just      ÔåÆ  available as `just` in PowerShell after install                        (justfile must declare: set shell := ["powershell.exe", ...])```**Four winget calls covers everything on a naked PC:****Python does NOT need to be installed separately.** uv has managed its ownCPython downloads since v0.2.x. When `uv sync` runs on a machine with no Python,it reads `requires-python` from `pyproject.toml` and downloads the appropriateCPython automatically into its own cache. This means:- `Require-Command "uv"` covers Python implicitly- Every repo MUST declare `requires-python = ">=3.11"` (or appropriate version) in pyproject.toml- Never add a separate `Require-Command "python"` ÔÇö it's redundant and would  install a system Python that uv ignores anyway**vite, ruff, tailwind, typescript** are all local devDependencies ÔÇö installedby `npm install` into `node_modules/`. They must never be required globally.**just is installed by start.bat and IS available on all customer PCs after first run.**`just` has a clean winget entry (`Casey.Just`, updated weekly, currently v1.49.0).Add it to the `Require-Command` chain in every start.ps1 and it becomes availablefleet-wide with no manual action from the user.One Windows-specific issue: `just` defaults to `sh` as its shell, which requiresGit Bash or Cygwin. Since the fleet uses PowerShell, every justfile MUST declare:```justfileset shell := ["powershell.exe", "-NoProfile", "-Command"]```Without this, recipes will fail on machines that don't have Git Bash installed.### 1. Prereq guard via wingetInclude `Require-Command` and call it for `uv` and `node`/`npm`:```powershellfunction Require-Command {    param([string]$Cmd, [string]$WingetId, [string]$Label)    if (Get-Command $Cmd -ErrorAction SilentlyContinue) { return }    Write-Host "  $Label not found - installing via winget ..." -ForegroundColor Yellow    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {        Write-Host "ERROR: winget unavailable. Install $Label manually ($WingetId)." -ForegroundColor Red        exit 1    }    winget install --id $WingetId --silent --accept-source-agreements --accept-package-agreements    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" +                [System.Environment]::GetEnvironmentVariable("PATH","User")    if (-not (Get-Command $Cmd -ErrorAction SilentlyContinue)) {        Write-Host "Installed $Label but '$Cmd' still not in PATH. Reopen PowerShell and retry." -ForegroundColor Yellow        exit 1    }}Require-Command "uv"   "Astral.uv"         "uv (Python package manager)"Require-Command "node" "OpenJS.NodeJS.LTS"  "Node.js LTS"Require-Command "npm"  "OpenJS.NodeJS.LTS"  "npm"Require-Command "just" "Casey.Just"         "just (command runner)"```Winget is available on Windows 10 1809+ and all Windows 11. If a user somehowlacks winget, the error message tells them the winget ID to install manually.### 2. Resolve uv path ÔÇö never call bare `uv````powershell$uvExe = (Get-Command uv).Source& $uvExe sync --project $RepoRoot```Bare `uv` on some machines resolves to a PATH shim that fails in non-interactivePowerShell sessions. Using the resolved path is reliable everywhere.### 3. npm install only if node_modules is absent```powershell$npmExe = (Get-Command npm).Sourceif (-not (Test-Path (Join-Path $WebRoot "node_modules"))) {    Push-Location $WebRoot    & $npmExe install --prefer-offline 2>&1    if ($LASTEXITCODE -ne 0) {        Write-Host "ERROR: npm install failed." -ForegroundColor Red        Pop-Location; exit 1    }    Pop-Location}````--prefer-offline` uses the npm cache on repeat installs (faster for dev).### 4. Explicit vite guard after npm installThis is the exact bug Steve hit. vite is a devDependency ÔÇö it must be local:```powershell$viteLocal = Join-Path $WebRoot "node_modules\.bin\vite"if (-not (Test-Path $viteLocal)) {    Write-Host "ERROR: vite missing from node_modules after npm install." -ForegroundColor Red    Write-Host "Delete '$WebRoot\node_modules' and re-run." -ForegroundColor Yellow    exit 1}```### 5. Import smoke-test before the health-wait loopThe health-wait loop will spin for 90 seconds if the backend crashes on startup.A 2-second import check surfaces the error immediately:```powershell& $uvExe run --project $RepoRoot python -c "import mypackage.api; print('  [ok] Import OK')"if ($LASTEXITCODE -ne 0) {    Write-Host "ERROR: import check failed -- see output above." -ForegroundColor Red    exit 1}```### 6. Helpful error on health timeout```powershellif (-not $ready) {    Write-Host "ERROR: backend health timed out after ${maxWait}s." -ForegroundColor Red    Write-Host "Run this directly to see the error:" -ForegroundColor Yellow    Write-Host "  cd $RepoRoot; $uvExe run python -m mypackage.api" -ForegroundColor Yellow    exit 1}```---## What MUST be local (never assumed global)| Tool | Location | How installed ||---|---|---|| vite | `webapp/node_modules/.bin/vite` | `npm install` (devDependency) || tailwindcss | `webapp/node_modules/.bin/tailwindcss` | `npm install` || typescript / tsc | `webapp/node_modules/.bin/tsc` | `npm install` || ruff | `.venv/Scripts/ruff.exe` | `uv sync` (dev dep) || pytest | `.venv/Scripts/pytest.exe` | `uv sync` (dev dep) |## What CAN be assumed (present on Sandra's Goliath, not on Steve's machine)Nothing. Assume zero. winget handles it.## INSTALL.md requirementEvery repo with a start.bat MUST have an `INSTALL.md` at the root with:1. The two-command quick start (`git clone` + `start.bat`)2. A manual step-by-step for when start.bat itself fails3. A table of what is/isn't required globallySee `D:\Dev\repos\aiwatcher-mcp\INSTALL.md` as the reference implementation.---## Fleet remediation status| Repo | Status ||---|---|| aiwatcher-mcp | Fixed 2026-04-24 || arxiv-mcp | Fixed 2026-04-24 || All others | TODO ÔÇö scan needed |To find all start.ps1 files still using bare `npm install` without node check:```powershell---

## Workstation baseline (install on every machine)

These are not start.ps1 dependencies — they're personal workstation tools that should be installed on any new PC in the fleet:

```powershell
# Terminal / navigation
winget install Notepad++.Notepad++
winget install Tailscale.Tailscale
winget install AntibodySoftware.WizTree
winget install AntibodySoftware.WizFile
winget install ajeetdsouza.zoxide       # smarter cd — z proj jumps to project
winget install Clement.bottom            # graphical system monitor (terminal)
winget install sharkdp.hyperfine         # command benchmarking
winget install chmln.sd                  # sed replacement with readable regex
winget install ya-z.yazi                 # terminal file manager with previews
winget install muesli.duf                # df replacement with colored output

# Archive / backup
winget install 7zip.7zip
winget install Hasleo.BackupSuiteFree
winget install Syncthing.Syncthing        # P2P folder sync — keeps D:\dev\repos warm across machines (see integrations/syncthing.md)

# Media / documents
winget install calibre.calibre           # ebook manager + PDF store
winget install Plex.PlexMediaServer      # media server

# AI development tools
winget install SST.OpenCodeDesktop         # opencode WinApp — Windows desktop UI
winget install Anysphere.Cursor            # Cursor IDE (AI editor)
winget install ZedIndustries.Zed            # Zed editor (Rust, fast, GPUI)

# opencode CLI + TUI — install after WinApp or standalone:
#   CLI:  opencode command (auto-bundled with WinApp, or via `npm install -g @opencode/cli`)
#   TUI:  opencode-tui (terminal UI, separate binary from GitHub releases)
# See https://github.com/anomalyco/opencode for all variants

# Claude Desktop — not on winget, download from https://claude.ai/download
# Antigravity — not on winget, download from https://antigravity.antigravity.ai

# Virtualization (if compatible — see caveats below)
winget install Oracle.VirtualBox
```

**Tailscale:** Auth via `tailscale up` after install. Required for fleet cross-machine access (ssh, webapp testing, MCP server connections between Goliath and MiniPC).

**Notepad++:** Lightweight editor for quick file peeks. No config needed.

**VirtualBox compatibility:**

| Machine | Compatible | Notes |
|---------|-----------|-------|
| Goliath | ✅ Yes | Full hardware virt support (AMD Ryzen with SVM) |
| MiniPC | ✅ Yes | 4-core CPU supports VT-x/AMD-V. UHD 600 iGPU handles 2D acceleration fine. 16GB RAM limits concurrent VMs — one at a time with ≤4GB assigned |

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
| **MiniPC** (UHD 600, 16GB CPU-only) | Install both but stick to 1B-3B models (Phi-3, Gemma-2-2B, Gemma-4-2B, Qwen2.5-3B). CPU inference at ~15-25 tok/s for 2B models. GPU (Intel UHD 600) cannot accelerate inference — no tensor cores, too few EUs |

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

Get-ChildItem D:\Dev\repos -Recurse -Filter "start.ps1" |    Select-String "npm install" |    Where-Object { $_.Line -notmatch "Require-Command" } |    Select-Object -ExpandProperty Path |    Sort-Object -Unique```