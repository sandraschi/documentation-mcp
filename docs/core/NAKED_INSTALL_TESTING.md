# Naked Install Testing Standard

**Status**: ACTIVE  
**Tooling**: [virtualization-mcp](https://github.com/sandraschi/virtualization-mcp) (VirtualBox VMs + Windows Sandbox)  
**Purpose**: Validate install instructions work on a clean Windows box with zero dev tools

---

## The Problem

We write install instructions assuming the user has `uv`, `git`, `node`, `npm`,
`just`, `ruff`, `biome` available. They don't. Consumer Windows machines have
none of these. Install instructions that fail silently or with cryptic errors
destroy user trust and generate support load.

**Eat our own dog food**: run the published install instructions from scratch,
exactly as a first-time user would, before shipping.

---

## virtualization-mcp: Two Different Surfaces

virtualization-mcp already ships Win11 isolation and dev bringup. **Do not confuse them.**

| Surface | Use for naked install? | What it provides |
|---------|------------------------|------------------|
| **Windows Sandbox consumer** (`Launch-ConsumerSandbox.ps1`) | **Yes** (today) | Winget bootstrap only; optional Claude MSIX; no dev stack |
| **VirtualBox persistent VM** (`NakedWin11`, snapshot `clean-base`) | **Yes** (when provisioned) | Restorable baseline; faster between-test restore |
| **Windows Sandbox dev bringup** | **No** (wrong baseline) | Disposable VM that **installs dev tools at logon** |

### Consumer bringup — Windows Sandbox (recommended today)

```powershell
.\scripts\Launch-ConsumerSandbox.ps1
.\scripts\Launch-ConsumerSandbox.ps1 -InstallClaudeDesktop
```

Webapp: Sandbox page → **Launch consumer sandbox** (`consumer_setup: true`).

Maps `assets/sandbox` → `C:\Assets`, runs `Setup-ConsumerSandbox.ps1` (shared
`lib/Winget-Bootstrap.ps1`). Writes `Desktop\consumer-install-test-checklist.txt`.

### Naked baseline — VirtualBox VM + snapshots (future / faster iteration)

Build once from ISO/OVA, snapshot immediately after OOBE **without** unattended
`dev_tools`. See `virtualization-mcp/assets/vbox/README.md` and template
`win11-pro` in `config/vm_templates.yaml`.

MCP tools (portmanteau, default server):

```text
snapshot_management(action="create", vm_name="NakedWin11", snapshot_name="clean-base")
snapshot_management(action="restore", vm_name="NakedWin11", snapshot_name="clean-base")
vm_management(action="stop", vm_name="NakedWin11")   # stop before restore if running
```

Webapp equivalent: `POST /api/v1/vms/{name}/restore` (ports 10700/10701).

**Anti-pattern:** `POST /api/v1/vms/{name}/unattended` with `dev_tools` enabled
pre-installs Python, Git, Node, uv, etc. on first logon — that is a dev VM, not
a naked baseline.

### Dev bringup — Windows Sandbox (already implemented)

For contributor smoke tests, risky script isolation, or fleet install scripting —
**not** for validating end-user INSTALL.md from zero.

| Entry | Location |
|-------|----------|
| Host launcher | `virtualization-mcp/scripts/Launch-DevInfraSandbox.ps1` |
| In-sandbox setup | `virtualization-mcp/assets/sandbox/Setup-DevInfraSandbox.ps1` |
| Webapp launch | `POST /api/v1/sandbox/launch` — modes `dev_infra_setup`, `full_dev_setup` |
| Docs | `virtualization-mcp/docs/sandbox.md` |

Dev Infra installs at logon: Git, gh, Node LTS, Python 3.12, ruff, just, biome
(via winget). Full Dev adds VS Code, uv, Windsurf, Cursor, etc.

Use this when you **want** dev tools present (e.g. test Option C/D after manual
clone, run `just test`, validate fleet install scripts). Restore naked baseline
via VirtualBox snapshot when switching back to Option A/B/C user-path testing.

---

## What "Naked" Means

A naked Windows box for this purpose:
- Windows 11 Home, fresh install or clean snapshot
- No Visual Studio, no Python, no Git, no Node
- `winget` available (ships with Windows 11; also on Win 10 1809+)
- Claude Desktop installed (this is a prerequisite we accept)
- Internet access

We are NOT testing:
- The MCP server's actual functionality (that's unit/integration tests)
- Network-restricted environments
- Non-Windows platforms (separate test pass)

---

## Test Procedure

### 0. Setup (one-time)

**Windows Sandbox consumer bringup** (recommended today):

```powershell
D:\Dev\repos\virtualization-mcp\scripts\Launch-ConsumerSandbox.ps1 -InstallClaudeDesktop
```

Or webapp Sandbox page → **Launch consumer sandbox**.

**VirtualBox `NakedWin11`** (when provisioned — faster snapshot restore between runs):

1. Import Win11 VM per `virtualization-mcp/assets/vbox/README.md`
2. OOBE only — no dev bringup, no unattended `dev_tools`
3. `snapshot_management(action="create", vm_name="NakedWin11", snapshot_name="clean-base")`

Before each VirtualBox test run:

```text
vm_management(action="stop", vm_name="NakedWin11")
snapshot_management(action="restore", vm_name="NakedWin11", snapshot_name="clean-base")
vm_management(action="start", vm_name="NakedWin11")
```

**Dev Infra sandbox** — wrong baseline for Options A–C; use only for Option D / dev smoke:

```powershell
D:\Dev\repos\virtualization-mcp\scripts\Launch-DevInfraSandbox.ps1
```

### 1. Check Baseline

Verify the VM is truly naked:
```powershell
# Run inside VM:
where.exe uv 2>$null; where.exe git 2>$null; where.exe node 2>$null
python --version 2>$null
# Expected: all empty / "not found"
```

### 2. Test Option A (Drag and Drop — mcpb)

This is the path that should work for 95% of users.

```
1. Open browser → GitHub releases page for the repo
2. Download {repo}-{version}.mcpb
3. Open Claude Desktop
4. Drag .mcpb file onto Claude Desktop window
5. Check: does the server appear in MCP server list?
6. Check: can you run a basic prompt that uses the server?
```

**Pass criteria**: Works with zero terminal interaction.  
**If it fails**: Document the error; fix the .mcpb manifest or the server's
entry point script.

### 3. Test Option B (npx mcpb)

```powershell
# In fresh PowerShell (no PATH modifications):
winget install OpenJS.NodeJS --silent
# Close and reopen terminal (PATH refresh)
npx @anthropic-ai/mcpb install https://github.com/sandraschi/{repo}
```

**Checkpoints**:
- Does winget succeed? (It should — Node is in the winget catalog)
- Does npx find mcpb? (Should work after PATH refresh)
- Does mcpb auto-configure Claude Desktop? (Should write to AppData config)
- Does the server appear after restarting Claude Desktop?

**If npx fails**: Check mcpb version compatibility with the repo's manifest.json.

### 4. Test Option C (Manual Config)

This tests the most failure-prone path.

```powershell
# Step 1: Install uv (Python + uv together)
winget install astral-sh.uv --silent

# Step 2: Clone
winget install Git.Git --silent
# Close and reopen terminal
git clone https://github.com/sandraschi/{repo}
cd {repo}

# Step 3: Install deps
uv sync

# Step 4: Edit claude_desktop_config.json
# (Use notepad or the exact JSON from INSTALL.md)
notepad "$env:APPDATA\Claude\claude_desktop_config.json"

# Step 5: Restart Claude Desktop
```

**Checkpoints**:
- `winget install astral-sh.uv` — does it succeed?
- After uv install, is `uv` in PATH without terminal restart?
- `uv sync` — does it pull all deps cleanly?
- Is the JSON config snippet in INSTALL.md copy-paste correct?
  (Test by copying it verbatim — no editing — and restarting Claude Desktop)

### 5. Record Results

For each option tested, record:

| Step | Expected | Actual | Pass/Fail | Notes |
|------|----------|--------|-----------|-------|
| winget install uv | uv 0.x.x | ... | | |
| uv sync | 0 errors | ... | | |
| Config JSON valid | Server appears | ... | | |
| Basic prompt works | Response received | ... | | |

### 6. Fix and Retest

Any failure → fix the INSTALL.md or the .mcpb manifest → restore clean
snapshot → retest from step 1 of the failing option.

Do not ship until Option A passes. Option B and C failures are lower priority
but should be tracked.

---

## Automation

This is the primary reason virtualization-mcp includes sandbox and VM handling.
The install test facility is a **first-class feature of the webapp** — not a
side procedure. It answers the question "why does this MCP server manage Windows
Sandbox?" with a concrete, useful demo that every repo maintainer in the fleet
can use immediately.

### What's available now

- Host: `scripts/Launch-ConsumerSandbox.ps1` (consumer naked) and `Launch-DevInfraSandbox.ps1` (dev)
- MCP: `snapshot_management`, `vm_management` (VirtualBox when `NakedWin11` exists)
- Webapp: consumer + dev infra launch on Sandbox page

### Planned: Install Test webapp page

A dedicated **Install Test** page in the virtualization-mcp webapp:

```
Pick repo ──► Pick options (A / B / C / all) ──► Run ──► Live log ──► Pass/Fail report
```

Under the hood, per test run:

1. **Bootstrap** — Consumer Sandbox starts; guest script runs:
   - `winget --version` → if absent, fetch `Microsoft.DesktopAppInstaller_*.msixbundle`
     from `microsoft/winget-cli` GitHub releases API → `Add-AppxPackage`
   - `winget upgrade winget --accept-source-agreements --accept-package-agreements`
2. **Option A** — download latest `.mcpb` from repo releases API, simulate drag-and-drop
   install (Claude Desktop CLI or registry write), verify MCP server entry exists
3. **Option B** — `winget install OpenJS.NodeJS` → `npx @anthropic-ai/mcpb install …`
   → verify server entry
4. **Option C** — `winget install astral-sh.uv` + `Git.Git` → clone → `uv sync --all-extras`
   → write `claude_desktop_config.json` → verify server entry
5. **Record** — structured pass/fail table per step; surface in webapp; persist to SQLite
6. **Report** — green/red badge per option; link from repo's GitHub Actions summary (future)

For dev-path regression (Options C/D, `just test`), launch Dev Infra Sandbox
instead of the consumer baseline.

### MCP tool surface (planned)

```text
sandbox_install_test(repo="blender-mcp", options=["A","B","C"])
  → { option_a: pass, option_b: pass, option_c: fail, logs: [...] }
```

---

## Pilot Repos

**Primary pilot (host app + LLM tiers + Options A–D):**

1. **blender-mcp** — Blender prerequisite, Ollama/LM Studio/cloud LLM paths, bridge add-on; reference for [LLM_AND_INSTALL_TIERS.md](./LLM_AND_INSTALL_TIERS.md). Run consumer sandbox tests here first.

**Additional pilots (install path patterns):**

2. **git-github-mcp** — INSTALL.md with all three MCP options; good CLI-heavy test bed  
3. **filesystem-mcp** — Different entry point pattern; good second test  

**Not consumer-sandbox pilots** (see [CONTROL_PLANE_INSTALL.md](./CONTROL_PLANE_INSTALL.md)): robofang, deepfang, openclaw-molt-mcp — operator/agent prerequisites differ.

---

## Dev Tools: What to Install, How

This table should be in every repo's `docs/DEVELOPMENT.md` — copy-paste ready:

| Tool | Windows | macOS | Version Check |
|------|---------|-------|---------------|
| uv (Python) | `winget install astral-sh.uv` | `brew install uv` | `uv --version` |
| Git | `winget install Git.Git` | `brew install git` | `git --version` |
| Node.js | `winget install OpenJS.NodeJS` | `brew install node` | `node --version` |
| Just | `winget install Casey.Just` | `brew install just` | `just --version` |
| Ruff (via uv) | `uv tool install ruff` | `uv tool install ruff` | `ruff --version` |
| Biome | `npm install -g @biomejs/biome` | `npm install -g @biomejs/biome` | `biome --version` |

Ruff and Biome are **dev-only** — never required for end users.  
Just is **dev-only** — never required for end users.  
uv and Node are required only for Options B/C/D installs.

---

## Scheduled Cadence

- **On every release**: Run Option A test (mcpb drag-and-drop) before tagging
- **Monthly**: Full three-option test for top-5 repos by usage
- **On INSTALL.md change**: Re-run affected option immediately

---

## Known Winget Gotchas

- **winget may be absent entirely** — Sandbox images and some LTSC/minimal Win11 builds
  ship without App Installer. The bootstrap script handles this automatically:
  check `winget --version`; if absent, download `Microsoft.DesktopAppInstaller_*.msixbundle`
  from the `microsoft/winget-cli` GitHub releases API and install via `Add-AppxPackage`.
  **This must be scripted, not manual** — the install test is fully automated.
- `winget install` requires accepting the MSVC license on first run — this
  blocks automation; use `--accept-source-agreements --accept-package-agreements`
- PATH changes from winget don't apply to the current terminal session —
  close and reopen terminal, or run `$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")`
- winget itself may need updating on stale images: `winget upgrade winget` — run
  this immediately after the winget-absent check, before any package installs
- Some winget packages require Restart — document this in INSTALL.md if applicable
- Dev Infra Sandbox bootstrap (`Setup-DevInfraSandbox.ps1`) uses the same winget
  flags; do not set global `$ErrorActionPreference = 'Stop'` during winget loops
  (partial install success is normal)

## References

- `virtualization-mcp/docs/sandbox.md` — Windows Sandbox dev bringup
- `virtualization-mcp/assets/vbox/README.md` — Win11 OVA workflow
- `virtualization-mcp/docs/usage-cases.md` — unattended VM + dev tools (dev VM only)
- `standards/README_STRUCTURE.md` — INSTALL.md Options A–D
- `standards/LLM_AND_INSTALL_TIERS.md` — host apps, LLM tiers A–D, bundling rules, Docker scope
- `standards/CONTROL_PLANE_INSTALL.md` — RoboFang, DeepFang, OpenClaw (advanced)
- `audits/INSTALL_AUDIT.md` — fleet install bug history
