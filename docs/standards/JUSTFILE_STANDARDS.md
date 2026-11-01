---
title: "SOTA Justfile Standard (Windows/PowerShell)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-18
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# SOTA Justfile Standard (Windows/PowerShell)

## I. Overview

Most MCP fleet repositories use `just` as the primary task orchestration tool. This standard defines the **SOTA Industrial Dashboard** pattern, replacing the default `just --list` which renders unreadable dark-blue text on dark-mode terminals.

## II. The Industrial Dashboard Pattern

Every fleet `justfile` MUST implement a custom help menu that provides:
1. **High Contrast**: Yellow/White/Cyan headlines for dark modes.
2. **Categorization**: Grouping recipes by functional domain (Dev, Security, Test, etc.).
3. **Metadata**: Displaying project name and version in the header.

### Industrial Implementation (Justfile)

**Just 1.50+** does not allow multi-line inline `-Command` blocks in recipes (extra-leading-whitespace parse error). Any recipe requiring complex PowerShell logic (conditionals, loops, multi-line strings) MUST be extracted to a `.ps1` file in `scripts/` and called from `just` as a one-liner.

**Just + `$` on Windows:** `just` interpolates `$name` in recipe bodies before PowerShell sees them — e.g. `$env:MCD_RAG_GPU='1'` becomes `=1`. Never assign PowerShell variables inline; always use `-File scripts/...ps1`. Reference: **`mcp-central-docs/scripts/just/`** (all mega-justfile recipes).

```just
# Pattern: external PowerShell script for complex logic
recipe-name:
    powershell.exe -NoProfile -File "{{justfile_directory()}}/scripts/recipe-name.ps1" -Param1 "value1" -Param2 "{{justfile_directory()}}"
```

Examples:

```just
# Display the SOTA Industrial Dashboard
default:
    @powershell.exe -NoProfile -ExecutionPolicy Bypass -File ../mcp-central-docs/scripts/just-industrial-dashboard.ps1 -Path . -Title my-mcp -Version 1.0.0 -Subtitle "optional hint line"

# Build .mcpb bundle for Claude Desktop
pack mcpb-pack:
    powershell.exe -NoProfile -File "{{justfile_directory()}}/scripts/mcpb-pack.ps1" -RepoRoot "{{justfile_directory()}}"
```

Browser click-to-run UI is **`just-ui`** on port **11030** (not `default`, not **10789**):

```just
just-ui:
    @powershell.exe -NoProfile -ExecutionPolicy Bypass -File ../mcp-central-docs/scripts/just-dashboard.ps1 -Path . -Port 11030
```

## III. Just 1.50+ parameter defaults (mandatory)

**just 1.50** treats unquoted recipe defaults like `mode=dual` as **variable references**, not string literals. Bare numbers like `count=10` fail parsing.

| Wrong | Correct |
| :--- | :--- |
| `serve mode=dual port=PORT:` | `serve mode="dual" port=PORT:` |
| `git-log count=10:` | `git-log count="10":` |
| `export MODE := "dual"` then `serve mode=MODE:` | OK — `MODE` is a defined variable |

**Fleet fix script:** `mcp-central-docs/scripts/fix-justfile-1.50.ps1` (run from repo root after pulling central docs).

**PowerShell recipe lines:** avoid `&&` in `windows-shell` recipes; use separate lines. Use `${p}:` not `$p:` when printing `Port $p` (drive-letter ambiguity).

## IV. Best Practices

- **ANSI Safety**: Stick to named PowerShell colors (`Yellow`, `Cyan`, `Gray`, `White`) for maximum cross-terminal compatibility.
- **Recipe Documentation**: Use the `# Short description` format on the line immediately preceding the recipe.
- **Portmanteau Tasks**: Use categories to group related portmanteau operations (e.g., `audit-deps`, `check-sec` under **Security**).
- **Zombies**: Include a **Housekeeping** category for cleaning build artifacts and port cullings.

## V. Environment Configuration (Windows)

On Windows systems where `just` is not on the global `PATH` for agentic shells, use the stable **scoop shim** path:

- **Path**: `C:\Users\<user>\scoop\shims\just.exe`
- **Usage**: `& "C:\Users\<user>\scoop\shims\just.exe" <recipe>`

> [!TIP]
> **Agentic Discovery**: Agents attempting tasks in these repositories SHOULD verify the existence of the scoop shim path if the standard shell recognition for `just` fails. This ensures zero-diagnostic execution of tasks like `just weather`.

## VI. Mandatory Recipes

For a repository to be **SOTA Certified**, its `justfile` MUST include the following standardized recipes to enable fleet-wide orchestration:

| Recipe | Description | Command Pattern |
| :--- | :--- | :--- |
| `release` | Triple-play release (mcpb + NSIS + GitHub upload) | `powershell.exe -NoProfile -File scripts/release.ps1` |
| `release-dry` | Dry-run the release pipeline | `powershell.exe -NoProfile -File scripts/release.ps1 -DryRun` |
| `test` | Automated Verification | `uv run pytest tests/` |
| `check` | Linting & Formatting | `uv run ruff format . ; uv run ruff check .` |
| `build` | Dependency Sync | `uv sync` |

### VIa. Fleet Recipe Book Import (MANDATORY)

Every repo justfile MUST import the fleet recipe book at the **top** of the file:

```makefile
import 'scripts/just/fleet.just'
```

**Vendoring (MANDATORY):** `scripts/just/fleet.just` is a **vendored copy** per repo
(copy from `mcp-central-docs/scripts/just/fleet.just`), not an absolute-path import
to the hub - repos must work without mcp-central-docs present. Re-sync the vendored
copy whenever the hub version changes.

**Collision rule (HARD):** this `just` version errors on any recipe name defined
both locally and in the import (`Recipe X first defined on line N is redefined`),
and imported recipes CANNOT be overridden - order does not matter. Therefore a repo
MUST NOT define a recipe that also exists in `fleet.just` (`mcpb-pack`,
`cua-nsis-test`, `cua-webapp-test`, `emojibuster`, `tauri-audit`, `fleet-overview`,
`fleet-stop`, `zombies`, `zombie-clean`, `zombie-clean-ports`, ...). Adopt the
fleet layout the recipes expect (e.g. `mcpb/pack.ps1`, `scripts/just/cua-webapp-test.ps1`)
instead of redefining the recipe. See `TRAPS_AND_PITFALLS.md` "duplicate recipes
colliding with fleet.just imports".

**Payoff:** repos automatically gain `zombies`/`zombie-clean` (port zombie sweep),
`fleet-stop`, `tauri-audit`, `mcpb-pack`, and the CUA recipes without local copies.

## VII. No Bare Venv Tools (HARD RULE)

Every recipe that invokes a **project-venv tool** (`ruff`, `pytest`, `mypy`, `python`,
`pip`, `pyinstaller`, `pre-commit`, `bandit`, `safety`, ...) MUST prefix the call with
`uv run`. The project venv is the only place these tools are guaranteed to exist in
the pinned version the repo expects.

| Wrong | Correct |
| :--- | :--- |
| `ruff check .` | `uv run ruff check .` |
| `pytest tests/ -v` | `uv run pytest tests/ -v` |
| `python -m build` | `uv run python -m build` |
| `pre-commit install` | `uv run pre-commit install` |
| `pip install pyinstaller` | `uv run pip install pyinstaller` |

**Why it is a HARD rule, not style:** a bare call silently resolves against whatever
is on `PATH` — a global ruff of a different version (masking real violations, or
flagging phantom ones), or nothing at all. On a clean shell, CI runner, or naked-PC
checkout the recipe just fails. The failure is **silent until someone runs the
recipe** — every repo with the bug looked fine on the developer's machine.

**Node tooling is exempt:** `npm`, `npx`, `bun` stay bare — node/bun installers add
their shims to PATH by design, and `npx` resolves package-local binaries.

**Verification:** `just lint` (or the repo's check recipe) MUST pass from a clean
shell with no global Python tooling on PATH. CI `just ci` exercises this.

**Fleet incident (2026-07-31):** 16 repos shipped justfiles with bare `ruff`
(+ `pytest`/`mypy`/`python`/`pre-commit` in 6 of them). The bare calls happened to
work on the dev machine's global ruff, then failed in the agent shell. All fixed to
`uv run`; see `TRAPS_AND_PITFALLS.md` § 9.

## VIII. Recipe Lines Run in Separate Shell Processes (HARD RULE)

`just` on Windows (`windows-shell := ["powershell.exe", "-NoProfile", "-Command"]`)
spawns a **brand-new `powershell.exe` process for every line** of a recipe body, not
one continuous session for the whole recipe. Nothing set on one line - working
directory, environment variables, anything - survives into the next line. This is
easy to get wrong because it's the opposite of how an ordinary `.ps1` script or an
interactive shell behaves, and the failure is often silent: `Set-Location` "succeeds"
(no error), it's the *next* line that then runs in the wrong place.

**Wrong** (each line below is its own process - `Set-Location` has already been
thrown away by the time `.\build.ps1` runs):
```just
build-native:
    Set-Location '{{justfile_directory()}}\native'
    $env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
    .\build.ps1
```
This fails loudly (`.\build.ps1 : The term '.\build.ps1' is not recognized...`) when
the target is a script. It fails **silently** when the target is a bare command that
implicitly reads the cwd - `npm install`, `uv run ...`, `cargo build` - because those
don't error "not found," they just run against the wrong directory.

**Correct - join into one line** so everything runs in the same process:
```just
build-native:
    $env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"; Set-Location '{{justfile_directory()}}\native'; .\build.ps1
```

**Correct - or better, skip `Set-Location` entirely** when the target is a script and
call it by absolute path. Fleet `build.ps1` templates already resolve their own root
via `$PSScriptRoot`, so `Set-Location` was never actually necessary:
```just
build-native:
    $env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"; & '{{justfile_directory()}}\native\build.ps1'
```

**Detection:** `rg -U -P "Set-Location[^\n;]*\n\s*\S" justfile` - for each hit, check
the matched `Set-Location` line is not that recipe's last line and isn't already
semicolon-joined. A hit targeting a subdirectory is a guaranteed bug; a hit targeting
the bare repo root works by luck when `just` happens to be invoked from repo root,
but is still fragile and should be fixed the same way.

**Fleet incident (2026-09-18):** this exact pattern was baked into
`mcp-central-docs/scripts/scaffold-tauri.ps1`'s `build-native` recipe generator and
mechanically stamped into every repo that ran the Tauri scaffolder. A fleet scan
found **186 broken recipe instances across 81 repos** (`build-native`, webapp/dev
recipes, `e2e` runners, and - worst - `lint`/`fix` recipes that `Set-Location` into
a source subdirectory before running `ruff`, meaning the lint gate may not have been
linting the intended tree). Root cause and full incident: `TRAPS_AND_PITFALLS.md` #37.

## IX. PowerShell 5.1 Only (HARD RULE)

The fleet speaks Windows PowerShell 5.1 — see `POWERSHELL_51_STANDARD.md`
(canonical). Concretely for justfiles:

- `set windows-shell := ["powershell.exe", "-NoProfile", "-Command"]`
  (never `pwsh.exe` — not installed on naked PCs).
- Script invocations use `powershell.exe -NoProfile -File ...`
  (never bare `pwsh` / `pwsh.exe`).
- Every `.ps1` a recipe touches must parse under 5.1 and carry no
  `#Requires -Version 7` (unless listed in
  `operations/ps7-exemptions.json`).
- Enforced by `scripts/Test-Ps51Parse.ps1` (pre-commit + CI + assfix §1J),
  not by convention.

---
*Standard: JUSTFILE-SOTA-2026-04*
*Status: MANDATORY*
