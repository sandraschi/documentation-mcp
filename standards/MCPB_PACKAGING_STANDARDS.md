---
title: "MCPB & Glama Packaging Standards (SOTA v2.0)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-18
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# MCPB & Glama Packaging Standards (SOTA v2.0)

**Version:** 2.2 (June 2026)  
**Status:** Official Fleet Standard  
**Framework**: FastMCP 3+ (floor: 3.2+, current SOTA: 3.4.x)  

---

## 🛠️ 1. Core Tooling: uv + justfile

Modern fleet Python repos MUST use **Astral uv**. Legacy `pip` or `requirements.txt` are deprecated for internal development.

### 1.1. Universal `justfile` Recipes
Every MCP server repository MUST include a root **`justfile`** with these standard recipes:

```justfile
# Bundle for Claude Desktop (MCPB) — MUST wipe+recopy src -> mcpb/src first
mcpb-pack:
    pwsh.exe -NoProfile -ExecutionPolicy Bypass -File scripts/mcpb-pack.ps1
```

Do **not** call bare `mcpb pack .` from a justfile without a fresh-stage script — that is how stale `mcpb/src` ships.
---

## 📦 2. MCPB (Claude Desktop) Architecture

### 2.1. Required Structure
```
mcp-server/
├── manifest.json          # v0.2 Standard
├── assets/
│   ├── icon.png          # 256x256px identifying icon
│   └── prompts/          # SOTA Prompting (3-4-100 Rule)
│       ├── system.md     # 3,000+ words of core capabilities
│       ├── user.md       # 4,000+ words of tutorials
│       └── examples.json # 100+ structured tool call mappings
├── src/                  # Self-contained source code
└── README.md            # Installation & Usage
```

### 2.2. Manifest.json (v0.2)
```json
{
  "manifest_version": "0.2",
  "name": "your-package-name",
  "version": "1.0.0",
  "description": "FastMCP 3+ server description",
  "author": { "name": "Your Name/Team" },
  "server": {
    "type": "python",
    "entry_point": "src/package_name/server.py",
    "mcp_config": {
      "command": "python",
      "args": ["-m", "package_name.server"],
      "env": {
        "PYTHONPATH": "${__dirname}",
        "PYTHONUNBUFFERED": "1"
      }
    }
  },
  "tools": [
    { "name": "tool_name", "description": "High-level summary" }
  ]
}
```

> [!CAUTION]
> **Path variables (HARD, added 2026-10-07).** Claude Desktop expands ONLY the MCPB-spec
> variables in `mcp_config`: `${__dirname}` (the unpacked bundle directory), `${HOME}`,
> `${DESKTOP}`, `${DOCUMENTS}`, `${DOWNLOADS}`, `${pathSeparator}`, `${/}` and
> `${user_config.KEY}`. **`${PWD}` is NOT expanded** -- it reaches the server as the literal
> text `${PWD}`, so the server fails to start on a real install while working in every dev
> check. This section previously prescribed `${PWD}` and ~190 fleet manifests copied it.
> `pack.ps1` now fails the pack on any non-spec `${...}` variable.
>
> Desktop launches **stdio**: `entry_point`/`mcp_config` must start the stdio server
> (`python -m <pkg>`), never an HTTP/PyInstaller sidecar `run_server.py`.

### 2.2b. Release assets and zero-friction install (HARD, added 2026-10-07)

Every fleet MCP repo's GitHub release MUST carry three assets, produced by the fleet pack script (`scripts/fleet-mcpb-pack.ps1`, called through each repo's thin `scripts/mcpb-pack.ps1` shim -- never a vendored copy):

| Asset | Why |
|---|---|
| `<name>-v<ver>.mcpb` | versioned archive |
| `<name>.mcpb` | **stable name**, so `releases/latest/download/<name>.mcpb` never changes |
| `install.ps1` | `scripts/install-mcpb.ps1` with the repo's latest-release URL and bundle SHA256 baked in |

README must open its install section with the Claude Desktop (Windows) one-liner, labelled
as Claude-only, and give the `uvx --from git+...` config for every other client:

```powershell
irm https://github.com/<owner>/<repo>/releases/latest/download/install.ps1 | iex
```

"Install X.mcpb" typed to Claude is served by the `install-mcpb` skill, which runs the same
`scripts/install-mcpb.ps1`. The installer writes Claude Desktop's undocumented extension
store and refuses manifests with non-spec `${...}` variables. Reference: onenote-mcp.

**Runtime prerequisites are installed by the installer, never by the user (HARD, 2026-10-07).**
A normal user must not need to know what `uv` is. `scripts/install-mcpb.ps1` detects
`mcp_config.command` of `uv`/`uvx`, and if `uv` is missing installs it (winget
`astral-sh.uv`, else the official astral installer) before registering the bundle. Because
`install.ps1` is generated from that script at pack time, **every repo that packs through
`fleet-mcpb-pack.ps1` gets this automatically**; a repo whose latest release has no
`install.ps1` built from the current script does NOT have it and is a retrofit target.
README/INSTALL for end users must not tell them to install `uv` by hand (only the
non-Claude `uvx` config section may mention it). New runtime prerequisites (any other
command a manifest launches) must be added to the installer the same way, in the same change.

### 2.3. Package Inclusions & Exclusions

To ensure Claude Desktop can successfully interpret and run the bundle, follow these strict rules:

| Category | **IN (Mandatory)** | **OUT (Forbidden)** |
|----------|-------------------|----------------------|
| **Metadata** | `manifest.json` | `glama.json`, `pyproject.toml`, `uv.lock` |
| **Logic** | `src/` (Self-contained) | `.venv/`, `node_modules/`, `__pycache__/` |
| **Assets** | `assets/icon.png`, **`assets/prompts/*` (3-4-100 — see §2.3b)** | `.git/`, `.github/`, `.vscode/` |
| **Docs** | `README.md`, `CHANGELOG.md` | `llms.txt`, `llms-full.txt` |

> [!CAUTION]
> Including a `.venv` or `node_modules` inside the `.mcpb` will significantly increase package size and may cause Claude Desktop to reject the bundle due to platform-specific binary conflicts.

### 2.3b. SOTA Prompting — 3-4-100 Rule (HARD — not a runt)

A `.mcpb` without extensive prompts is a **runt package**. Minimal stub `system.md` / `user.md` / three toy examples **fail the new-repo gate**.

| Artifact | Path | Minimum | What it is |
|----------|------|---------|------------|
| **system.md** | `assets/prompts/system.md` | **≥ 3,000 words** | Core capabilities, tool surface, safety, architecture — Claude Desktop system prompt material |
| **user.md** | `assets/prompts/user.md` | **≥ 4,000 words** | Natural-language tutorials, workflows, troubleshooting, example dialogues |
| **examples.json** | `assets/prompts/examples.json` | **≥ 100 entries** | Structured tool-call mappings (valid JSON array of objects) |

**Word count:** whitespace-split English tokens (PowerShell / Python `str.split()`). Headings and lists count; do not pad with repeated filler sentences — content must be domain-useful.

**examples.json shape (each element):**

```json
{
  "name": "outbox-approve-happy",
  "description": "Approve a pending fleet draft",
  "prompt": "Approve outbox item 42",
  "tool": "mastodon_social_tool",
  "arguments": { "operation": "outbox_approve", "outbox_id": 42 }
}
```

Cover the full portmanteau / tool surface — not 100 clones of one happy path.

**Verification (mandatory before `mcpb pack` / ship):**

```powershell
function Word-Count([string]$Path) {
  (@(Get-Content -Raw $Path) -split '\s+' | Where-Object { $_ }).Count
}
$sys = Word-Count assets/prompts/system.md
$user = Word-Count assets/prompts/user.md
$ex = (Get-Content assets/prompts/examples.json -Raw | ConvertFrom-Json).Count
if ($sys -lt 3000 -or $user -lt 4000 -or $ex -lt 100) {
  throw "3-4-100 FAIL: system=$sys user=$user examples=$ex (need 3000 / 4000 / 100)"
}
```

**Forbidden runt patterns:** empty files, “TODO prompts”, under-minimum word counts, `examples.json` with fewer than 100 entries, prompts only under `mcpb/assets/` without live `assets/prompts/` (staging may copy; source of truth is repo `assets/prompts/`).

Also documented in [PACKAGING_STANDARDS.md](./PACKAGING_STANDARDS.md) §2. New-repo gate: AGENTS.md ship checklist item **11**.

### 2.4. Exclusion Mechanism (.mcpbignore)

The `mcpb` CLI uses a **`.mcpbignore`** file (syntax identical to `.gitignore`) to filter files during the packing process. Every SOTA repository MUST include this file to prevent environmental leakage.

#### Standard `.mcpbignore` Template:
```text
# Logic/Dev Bloat
.venv/
node_modules/
__pycache__/
.ruff_cache/
.pytest_cache/
tests/

# Discovery & Fleet Metadata
glama.json
llms.txt
llms-full.txt
.git/
.github/
.vscode/

# Build Artifacts
dist/
build/
*.mcpb

# Editor / tooling backups (added 2026-07-26)
# Sneak-in specialists leave timestamped backups; both patterns required.
# Backup files accumulate in mcpb/src because editing tools write them next to
# the file they touch. They were found committed inside mcpb/src in the fleet.
*.bak
*.bak.*
*.orig
*.rej
```

### 2.5. Source Layout Verification (added 2026-07-26 — NON-NEGOTIABLE)

> [!CAUTION]
> **`mcpb/src` is a BUILD ARTIFACT, not a source tree.** It is produced by copying the
> repo `src/` tree (exact package layout) into `mcpb/src/` as the preliminary step before
> `mcpb pack`. Never edit it. Fix `src/`, then re-copy / rebuild. **MUST be gitignored** —
> never commit `mcpb/src/` (stale twins are the #1 MCPB drift failure mode).

The copy step **must preserve the package directory**:

```
src\<package>\      ->  mcpb\src\<package>\     CORRECT
src\<package>\*     ->  mcpb\src\               FLATTENED - PACKAGE IS BROKEN
```

Flattening produces a bundle that cannot import itself. `run_server.py` does
`sys.path.insert(0, <bundle>/src)` and then `from <package>.server import ...`; with the
package directory missing, that import cannot resolve. The bundle then only appears to work
on a machine where the package is already installed by other means, which defeats the entire
purpose of packaging and hides the fault until a clean install.

It also contradicts §2.2, which specifies `"entry_point": "src/package_name/server.py"`,
and breaks hatch, whose `[tool.hatch.build.targets.wheel] packages = ["src/<package>"]`
points at a directory that no longer exists.

#### Why this section exists

§2.3 already said "src/ (Self-contained)" and §2.4 already excluded `__pycache__/`. Both
rules were correct and both were violated fleet-wide, because **"verify src/ is
self-contained" was prose with no mechanism**, so it degraded into a box that gets ticked.

#### Fleet audit, 2026-07-26 (`scripts/audit-mcpb-bundles.ps1`)

| result | repos |
|---|---|
| **BROKEN** (flattened and/or hatch path missing) | **83** |
| warned (pollution and/or git-tracked only) | 25 |
| clean | **4** |

| finding | count |
|---|---|
| flattened `mcpb/src` (no package dir) | 84 |
| hatch `packages = [...]` points at a nonexistent path | 49 |
| `mcpb/src` committed to git | 56 |
| `.pyc` / `.bak` pollution under `mcpb/` | 98 |

Flattening is the **norm**, not the exception. The MCPB staging directories are broken
across most of the fleet: a flattened bundle only runs where the package is already
installed by other means, so the fault is invisible on the developer's own machine and
appears only on a clean install.

#### Blast radius: what was actually shipped (checked 2026-07-26)

**No broken bundle has been published.** The audit above covers the `mcpb/` **staging
directory**, which is not the same thing as a released artifact. Measured across 45 git
repos:

| | count |
|---|---|
| repos with a published `.mcpb`/`.dxt` release asset | **2** |
| repos with releases but no bundle attached | 8 |
| repos with no releases at all | 35 |

Both published artifacts were downloaded and inspected. Both are **correct**:

| artifact | entry_point | present in archive | package dir | verdict |
|---|---|---|---|---|
| `cursor-mcp-v0.2.0.mcpb` | `src/cursor_mcp/__main__.py` | yes | `cursor_mcp` | OK |
| `devices-mcp.mcpb` | `src/devices_mcp/server.py` | yes | `devices_mcp` | OK |

Note `devices-mcp`: its staging directory is flagged BROKEN, yet its published artifact is
correct. The good artifact predates the staging rot. This is the pattern across the fleet:
of 203 packed artifacts found on disk, roughly half are correct, and several repos hold
both a correct and a broken bundle side by side, distinguishable by manifest:

```
advanced-memory-mcp   126 KB  entry=run_server.py                       flattened  BROKEN
advanced-memory-mcp  1680 KB  entry=src/advanced_memory/mcp/server.py   pkg dir    OK
```

`entry_point: run_server.py` is the broken generation; `entry_point: src/<pkg>/server.py`
is the correct one. **This is the tell to grep for.**

So the exposure is a latent release hazard, not a live incident: the next `mcpb pack` from a
rotted staging directory would ship a broken bundle. Nothing needs recalling. Fix the copy
step and the checks below before the next release, and verify any artifact before attaching
it to a release.

Confidence note: 49 of the 83 are confirmed by **two independent signals** (flattened layout
*and* a hatch declaration pointing at a path that does not exist). The remainder are flagged
on layout alone, and a small number of those may be legitimately flat single-module servers.
Triage before mass-fixing; the check is deliberately conservative.

Verified examples of the two states:

| repo | entry-point import resolves from `mcpb/src` | verdict |
|---|---|---|
| arxiv-mcp | yes | OK |
| blender-mcp | yes | OK |
| fleet-agent-mcp | **no** | **BROKEN** |
| advanced-memory-mcp | **no** | **BROKEN** |

Separately, `fleet-agent-mcp/mcpb/run_server.py` calls `uvicorn.run(...)` and never imports
uvicorn, a guaranteed `NameError`. No structural check would catch that, which is why check
3 below is an AST check rather than a file-existence check.

#### Fresh copy before pack (HARD — avoids stale mcpb/src shipping old crap)

Incident class: a leftover `mcpb/src/` twin was older than repo `src/`; `mcpb pack`
shipped the stale tree. Gitignore alone does **not** fix a dirty local disk.

**Mandatory pack pipeline (every `just mcpb-pack` / `scripts/mcpb-pack.ps1`):**

1. **Delete** `mcpb/src` entirely (if present).
2. **Copy** repo `src/<package>/` → `mcpb/src/<package>/` (preserve package dir — never flatten).
3. Copy/update `mcpb/manifest.json` (and other mcpb metadata) from the live repo as required by the pack script.
4. Run the mechanical checks below (§ Required checks).
5. **Only then** run `mcpb pack` (from `mcpb/` or repo root per script — but content must be the just-copied tree).
6. Optionally delete `mcpb/src` again after pack so the next run cannot accidentally reuse it.

**Forbidden:**

- `mcpb pack` against an existing `mcpb/src` without a wipe+recopy in the same script invocation
- Editing files under `mcpb/src` by hand
- Committing `mcpb/src` (see Version control)

Reference script pattern: `calibre-mcp/scripts/build-mcpb-package.ps1` (sync then pack).

```powershell
# Minimal fresh-stage fragment (PowerShell)
$pkg = "my_package"   # under src/
$stage = Join-Path $RepoRoot "mcpb\src\$pkg"
if (Test-Path (Join-Path $RepoRoot "mcpb\src")) {
    Remove-Item -Recurse -Force (Join-Path $RepoRoot "mcpb\src")
}
New-Item -ItemType Directory -Force -Path (Split-Path $stage) | Out-Null
Copy-Item -Recurse -Force (Join-Path $RepoRoot "src\$pkg") $stage
# ... then mcpb pack
```

#### Required checks before `mcpb pack` (all mechanical, all gate `ship`)

0. **Fresh stage proved** — script wiped and recopied `src/` → `mcpb/src/` in this run (log a line; fail if copy source missing).
1. Resolve the entry point's top-level import with **only** `mcpb/src` on `sys.path`, and
   assert the resolved origin is *inside that directory*. A successful import from
   site-packages is a false pass.
2. Assert every path in `mcpb/pyproject.toml` `[tool.hatch.build.targets.wheel] packages`
   exists.
3. AST-check the entry point: every module referenced at a call site is actually imported.
4. Assert no `__pycache__`, `*.pyc`, `*.bak`, `*.bak.*` anywhere under `mcpb/`.
5. Launch the packaged entry point in a clean environment and assert it serves. Static
   checks cannot prove a bundle runs.

#### Pack-root `.mcpbignore` gotcha (added 2026-08-27)

`mcpb pack <dir> <out>` reads `.mcpbignore` from the **pack root** (`mcpb/`), not the repo
root. If `.mcpbignore` exists only at the repo root, pack reports `ignored files: 0` and
ships whatever the fresh copy dragged in (`.pyc`, `__pycache__`, sneak-in `.bak` twins).
Measured on resonite-mcp: a bundle ballooned from 59 clean files to 196 / 1.1MB entirely
because `.mcpbignore` was repo-root-only and the freshly copied `src/` carried bytecode and
`.bak` files.

Mandatory in every pack script: **ensure `.mcpbignore` is present at `mcpb/.mcpbignore`**
before packing (copy from repo root if missing). Verify the pack summary's
`ignored files: N` is non-zero as a smoke check, and expand/verify the archive rather than
trusting the summary alone.

#### Import-verification bytecode gotcha (added 2026-08-27)

A §2.5 required check is "launch/import the entry point to prove self-containment." Running
that import **generates `__pycache__/*.pyc` inside `mcpb/src`** — and if the pollution check
ran *before* the import, the bytecode ships in the bundle. Fixes (both, not either):
1. Set `PYTHONDONTWRITEBYTECODE=1` around the import-verification subprocess.
2. Run the pollution check (check 4) **after** the import-verification step, so anything the
   import left behind is still caught.

Also strip `__pycache__` / `*.pyc` / `*.bak` / `*.bak.*` from the fresh stage right after the
copy, so the pollution check is a safety net, not the only cleaner. Sneak-in `.bak` twins
inside `src/` are the top recurring source of this; clean them from `src/` itself, not just
from the stage.

#### Package-name / entry-point / output-filename bugs in the fleet template (found + fixed 2026-09-14)

Found while packing `bookmarks-mcp` from the fleet-canonical `pack.ps1.template`
(`mcp-central-docs/_scratch_mcpb_fix/`), which `sweep.ps1` had already distributed to
however many repos were missing a pack script at the time it last ran. All three bugs were
in the template itself, not repo-specific — every repo that received it via the sweep
carries the same exposure until it repacks with the fixed template.

1. **Package-name detection trusted the pyproject.toml `name` field without checking the
   derived directory exists.** `name = "bookmarks-mcp"` → guessed `src/bookmarks_mcp/`,
   but the real package is `src/browser_bookmarks_tools/` (PyPI/distribution name and the
   importable package directory are not required to match, and often don't after a rename).
   First run failed at the copy step with "Copy source missing". Fixed with 3-tier detection,
   each tier validated against the filesystem: (1) hatch's own
   `[tool.hatch.build.targets.wheel] packages = ["src/<pkg>"]` — most authoritative, since
   hatch/`uv build` already depends on it being correct; (2) the name-derived guess, only
   trusted if `src/<guess>/` actually exists; (3) last resort, exactly one directory under
   `src/`.
2. **Entry point resolved against the repo root instead of the bundle root.** `manifest.json`
   describes the *bundle* (`mcpb/` is what gets packed), so `entry_point` must resolve
   relative to `mcpb/`, not `$RepoRoot`. The old template did
   `Join-Path $RepoRoot $entryPointRel`. This silently "worked" during testing only because a
   byte-identical same-named `run_server.py` happened to also exist at the repo root for an
   unrelated build — it surfaced only once that coincidence produced a malformed dotted
   module string and `importlib.import_module` raised `TypeError: the 'package' argument is
   required to perform a relative import`. Fixed: resolve against `$McpbDir`, and detect
   which of the two real fleet entry-point styles (see §2.5 above) is in play by checking
   whether the resolved path lands under `mcpb/src` at all (`GetRelativePath` starting with
   `..` means it's a standalone wrapper script, not a staged module).
3. **Output filename used the detected source package name instead of `manifest.json`'s own
   `name`.** They can differ (`bookmarks-mcp` vs. `browser_bookmarks_tools`) — the packed
   file should be named after what `mcpb pack` itself calls the bundle (shown in its own
   "Archive Contents" summary), not an internal implementation detail. Fixed: build the
   output filename from `$manifest.name`/`$manifest.version`.
4. **`verify_pack.py`'s import check only supported dotted-module imports** (`importlib.
   import_module`), so it could not verify a standalone bootstrap-script entry point (the
   `run_server.py` style, at least as common fleet-wide as the dotted-module style — see the
   two entry-point styles under §2.5). Fixed: `check_import` now takes a 3rd arg
   (`package_name`) and branches — a `.py` file path runs via
   `runpy.run_path(path, run_name="__mcpb_verify__")` (avoids triggering
   `if __name__ == "__main__":`) then asserts `sys.modules[package_name]` resolved under the
   staged dir; a dotted string still goes through `importlib.import_module` as before.
5. **The §2.5 "launch the packaged entry point" check (item 5) was entirely missing from the
   template** — added as Step 10. First implementation used
   `Start-Process -FilePath uv -ArgumentList @('run','python',...)`; confirmed empirically
   (via `netstat`/`Get-Process` polling *after* the script reported success and exited) that
   `uv run` spawns Python as a **child** of the `uv.exe` wrapper on Windows rather than
   exec-replacing it, so `Stop-Process -Id $proc.Id` killed the wrapper and orphaned a live
   server bound to the probe port. Fixed: launch `.venv\Scripts\python.exe` directly,
   bypassing `uv run` for this one check, with try/finally cleanup and a save/restore of any
   pre-existing `$env:MCP_PORT`. Hardened further: "still alive after 4s" alone can't
   distinguish a genuinely serving process from one blocked on `stdin.readline()` (a
   stdio-transport server with no client attached looks identical) or one whose startup
   failed in a background thread without killing the main process — the check now also scans
   stderr for a Python traceback even when the process is still running.

Also hardened while fixing (not bugs per se, but silent-failure modes the template should
not ship with): `manifest.json` missing/empty `name` or `version` now fails fast with an
explicit message instead of silently producing a malformed output filename like `-v.mcpb`;
missing `bunx` on `PATH` now fails with an actionable "install Bun" message instead of
whatever cryptic error the shell gives for a not-found command.

**Fleet exposure — not yet audited.** `sweep.ps1`'s own docstring states it does not touch
entry-point/console-script correctness ("those need per-repo understanding... explicitly out
of scope here"), meaning it distributed the *buggy* pre-fix template as-is to every repo it
touched. The drift-scan JSON it reads from (`$env:TEMP\mcpb_drift_scan.json`) is ephemeral
and may no longer reflect current fleet state. A repo count and a decision on whether to
re-sweep with the fixed template is a separate, larger-blast-radius action than fixing the
template itself — flag to the user before doing it, per the Batch Size Limit and Batch
Mutation Safety rules (this is potentially 100+ repos, far past the 10-file-per-operation
ceiling even done in small batches).

#### Version control

`mcpb/src` **MUST** be gitignored (new-repo gate item 9). It is an exact staging copy of
`src/` for packing — derived, regenerable, guaranteed to go stale if committed.
Measured 2026-07-26: 315 drifted twins across 110 repos, 311 of them simply stale copies.
`pywinauto-mcp` already gitignores `mcpb/src` and is the reference pattern; most other repos
tracked it historically (calibre-mcp: 447 files) — do not repeat that.

Pack scripts **MUST** still wipe+recopy even when gitignored: local untracked `mcpb/src`
is how the stale-pack incident happened.

---

## 🌐 3. Discovery & Registry (glama.json)

The `glama.json` manifest is for **external indexing** (glama.ai) and MUST be excluded from the `.mcpb` bundle.

```json
{
  "mcpServers": {
    "server-id": {
      "command": "python",
      "args": ["-m", "src.package.server"],
      "env": { "PYTHONPATH": "${workspaceFolder}" },
      "capabilities": {
        "tools": { "enabled": true },
        "prompts": { "enabled": true }
      },
      "metadata": {
        "version": "1.0.0",
        "tags": ["category", "tool-type"],
        "homepage": "https://github.com/..."
      }
    }
  }
}
```

---

## 🚀 4. CI/CD (GitHub Actions 2026)

Always use `@v4` or `@v5` for core actions.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v1
      - name: Build MCPB
        run: |
          bunx @anthropic-ai/mcpb pack . dist/package.mcpb
      - uses: actions/upload-artifact@v4
        with:
          name: release-bundle
          path: dist/
```

---

## 🔧 5. CLI Installation & Usage

The Anthropic `mcpb` CLI is a Node.js-based tool used to bundle and validate your MCP server.

### 5.1. Installation
```powershell
# Use bunx (no global install needed)
bunx @anthropic-ai/mcpb --version

# Or global install if preferred
bun add -g @anthropic-ai/mcpb
mcpb --version
```

### 5.2. Core Commands
| Command | Purpose |
|---------|---------|
| `mcpb pack <dir> <output.mcpb>` | Create a bundle from a SOTA layout. |
| `mcpb validate <file>` | Check a `manifest.json` or `.mcpb` for errors. |
| `mcpb info <file.mcpb>` | List the contents and manifest of a bundle. |
| `mcpb unpack <file.mcpb> [output]` | Unpack a bundle -- use for the launch-in-clean-copy required check (§2.5 check 5). |

> Verified against `@anthropic-ai/mcpb` v2.1.2, 2026-09-10 — `inspect` does not exist on this CLI (`error: unknown command 'inspect'`); the real command is `info`. This table was previously wrong and nothing had exercised it against the actual tool.

> [!WARNING]
> **FORBIDDEN**: Never use `mcpb init` or `mcpb create`. These commands generate legacy/broken manifests that do not comply with v2.0 SOTA standards. Always author your layout manually according to Section 2.

---

*Last Updated: June 16, 2026*  
*Standard maintained by the Antigravity SOTA Fleet.*
