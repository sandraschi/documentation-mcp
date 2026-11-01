---
title: "Traps & Pitfalls - Agentic Work Standards"
category: reference
status: review
audience: mcp-dev
last_updated: 2026-09-18
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# Traps & Pitfalls - Agentic Work Standards

**Purpose:** Every time we discover an antipattern, a tool failure mode, or a process trap, it goes here. This is the "lessons learned" document for agentic workflows.

**Status:** Active - append new entries as they are discovered.

---

## Table of Contents

1. [Agent Launch → Wait Violation](#1-agent-launch--wait-violation)
2. [BrightData Out-of-Quota](#2-brightdata-out-of-quota)
3. [Fetch MCP Error -32002](#3-fetch-mcp-error--32002)
4. [Regex Bloopers - No Dry Run, Shell Quoting, Indiscriminate Replace](#4-regex-bloopers--no-dry-run-shell-quoting-indiscriminate-replace)
5. [`# noqa` as a crutch - must fix, not hide](#5-noqa-as-a-crutch--must-fix-not-hide)
6. [JSON Schema Validation in Tool Calls](#6-json-schema-validation-in-tool-calls)
8. [`localhost` vs `127.0.0.1` on Goliath - silent 404 instead of connection-refused](#8-localhost-vs-1270011-on-goliath--silent-404-instead-of-connection-refused)
13. [Windows PowerShell 5.1 `Set-Content -Encoding UTF8` Always Writes a BOM - Fleet-Wide, 344 Occurrences](#13-windows-powershell-51-set-content--encoding-utf8-always-writes-a-bom--fleet-wide-344-occurrences)
14. [NSSM services run as LocalSystem, so `Path.home()` silently resolves to `systemprofile`](#14-nssm-services-run-as-localsystem-so-pathhome-silently-resolves-to-systemprofile--two-databases-zero-errors)
15. [AI sandbox proxy escape - zero-day in package registry cache software](#15-ai-sandbox-proxy-escape--zero-day-in-package-registry-cache-software)
16. [`bun` resolves to `bun.ps1` before `bun.exe` - `Start-Process -FilePath "bun"` fails](#16-bun-resolves-to-bunps1-before-bunexe--start-process--filepath-bun-fails)
17. [NSSM + `.bat` wrapper = doomed services - cmd.exe kills them on reboot](#17-nssm--bat-wrapper--doomed-services--cmdexe-kills-them-on-reboot)
18. [Bare venv tools in justfiles - the ruff-PATH footgun (naked-PC failure)](#18-bare-venv-tools-in-justfiles--the-ruff-path-footgun-naked-pc-failure)
19. [Stale NSSM AppParameters after CLI refactor - silent crash loop, service "Running", port dead](#19-stale-nssm-appparameters-after-cli-refactor--silent-crash-loop-service-running-port-dead)
20. [Temporal Hallucination - the LLM has no clock](#20-temporal-hallucination---the-llm-has-no-clock)
21. [Spatial Hallucination - the LLM has no map](#21-spatial-hallucination---the-llm-has-no-map)
22. [NSSM services: never taskkill the child process to 'restart' the service](#22-nssm-services-never-taskkill-the-child-process-to-restart-the-service)
24. [`gh auth token` in a consoleless/server context falsely reports "not logged in" - use `gh auth status`](#24-gh-auth-token-in-a-consolelessserver-context-falsely-reports-not-logged-in--use-gh-auth-status)
25. [`make-mcpb.ps1` overwrites preserved prompt content on rebuild - silently destroys 3-4-100](#25-make-mcpbps1-overwrites-preserved-prompt-content-on-rebuild--silently-destroys-3-4-100)
26. [Naked Tool Invocations on Windows (`rg`, `just`, `fd`, etc.) & Siloed Environment Registries](#26-naked-tool-invocations-on-windows-rg-just-fd-etc--siloed-environment-registries)
27. [RTX 4090 VRAM Squatting & Unreleased Local LLM Hogs](#27-rtx-4090-vram-squatting--unreleased-local-llm-hogs)
28. [Local Fix Abandonment — Verified Locally in Dev, Uncommitted & Unpushed to Remote](#28-local-fix-abandonment--verified-locally-in-dev-uncommitted--unpushed-to-remote)
29. [NSSM Service Wrapper Bloat on Windows & SCM Restart Race Conditions](#29-nssm-service-wrapper-bloat-on-windows--scm-restart-race-conditions)
30. [Private Monorepo Dependency Trap & Standalone Independence on Naked PCs](#30-private-monorepo-dependency-trap--standalone-independence-on-naked-pcs)
31. [`fleet-start.config.ps1` declares `Backend.Kind = 'module-serve'` for a module whose CLI has no `--serve` flag](#31-fleet-startconfigps1-declares-backendkind--module-serve-for-a-module-whose-cli-has-no---serve-flag)
32. [Agent shell `Restart-Service` on NSSM MCP daemons without elevation - useless retry loop](#32-agent-shell-restart-service-on-nssm-mcp-daemons-without-elevation---useless-retry-loop)
33. [`safety_override` flag that returns `BYPASSED` - policy ban magnet and design smell](#33-safety_override-flag-that-returns-bypassed---policy-ban-magnet-and-design-smell)
34. [Canonical `pack.ps1.template` trusted names/paths without filesystem validation - bugs shipped fleet-wide via `sweep.ps1`](#34-canonical-packps1template-trusted-namespaths-without-filesystem-validation---bugs-shipped-fleet-wide-via-sweepps1)
38. [`git commit -- <pathspec>` runs `repo: local` pre-commit hooks against HEAD, not the index - false-pass and false-fail](#38-git-commit----pathspec--runs-repo-local-pre-commit-hooks-against-head-not-the-index---false-pass-and-false-fail)

---

## 5. `# noqa` as a crutch - must fix, not hide

**Discovered:** 2026-06-20 (calibre-mcp lint pass, arxiv-mcp lint pass)

**Trap:** Using `ruff check --add-noqa` or manually inserting `# noqa` directives to silence lint issues instead of fixing the underlying code.

**Rule (HARD):**
> Every lint issue must be actually fixed. `# noqa` is only allowed for legitimate edge cases where the linter rule misfires:
> - Intentional re-exports in `__init__.py` portmanteau files (`# noqa: F401`)
> - Security rules on deliberately safe patterns (`# noqa: S603` on list-arg subprocess with no shell=True, `# noqa: S301` on known-safe pickle usage)
> - Structural E402 in `__init__.py` where imports intentionally follow runtime setup (rare, must be justified)
>
> `ruff check --add-noqa` is FORBIDDEN. It auto-hides issues without fixing them and produces unreviewable diff noise.
6. [Stale In-Process API Credentials Surfacing as a Flat "Invalid API Key" Error](#6-stale-in-process-api-credentials-surfacing-as-a-flat-invalid-api-key-error)

---

## 1. Agent Launch → Wait Violation

**Discovered:** 2026-06-20 (freecad-mcp CFD audit, qcad-mcp MCPB build, fleet annotations batch)

**Trap:** Launching a background agent (explore, general, task) to produce a report or audit, then starting work in the same domain before the agent returns. The agent's findings are never read, or its work is duplicated/contradicted by assumptions made during the parallel work.

**Consequences:**
- Agent's compute is wasted (sometimes minutes of work)
- Decisions made without full context introduce errors
- Batch scripts built on incomplete data can corrupt files (duplicate definitions, misplaced code)
- The agent's "report" is never surfaced to the user, who loses trust

**Rule (HARD):**
> If a task agent is launched to produce a report, audit, or analysis that should inform work in the same domain, no changes in that domain may be made until the agent's result is received and read.
>
> Independent parallel work (e.g., editing unrelated files in different repos) is exempt. "Fire off a diagnostic while I start cutting" is never exempt.

**Enforcement:**
- The agent prompt must clearly state: "Return a structured report. Do not make changes. I will await your result before acting."
- The caller must `await` or poll the task result before any domain-relevant edit
- Violations are flagged in the [operations/claude.md](../operations/claude.md) prompt and invoked during the next session

---

## 2. BrightData Out-of-Quota

**Discovered:** 2026-06-20 (multiple failures during CFD GPU research)

**Symptom:**
```
Tool 'search_engine' execution failed: HTTP 401: Token expired
Tool 'scrape_as_markdown' execution failed: HTTP 401: Token expired
```

All BrightData tools return 401 simultaneously.

**Cause:** The BrightData API subscription has run out of quota (monthly credits exhausted). The "token expired" message is misleading - the token is valid, but the account has no remaining balance for the current billing period.

**Detection:**
- If ALL BrightData tools fail with 401 simultaneously, it's quota, not a single-token issue
- Check https://brightdata.com/ dashboard for remaining credits
- Tools that *don't* hit BrightData (webfetch, fetch_fetch) will still work

**Workaround:**
- Use `webfetch` or `fetch_fetch` for web content instead (they use different backends)
- Wait for the next billing cycle when quota resets
- Or top up the BrightData account

---

## 3. Fetch MCP Error -32002

**Discovered:** 2026-06-20 (multiple failures during fastmcp GitHub research)

**Symptom:**
```
MCP error -32002: Failed to fetch content from <url>
```

**Causes (in order of likelihood):**

| Cause | Pattern | How to fix |
|-------|---------|------------|
| URL returns HTTP 404 | Any nonexistent path | Verify the URL exists first via a known landing page |
| No fallback path found | The URL fails at all 6 fallback attempts (raw, .md, /index.md, /llms.txt, /llms-full.txt, /llms.txt) | Try a different URL format (raw.githubusercontent.com instead of github.com) |
| Private repository | github.com/... URL for a private repo | Use raw.githubusercontent.com with the correct branch path |
| Domain does not resolve | Non-existent hostname | Check DNS / typos in the URL |
| GitHub rate limiting | Multiple rapid fetch calls | Add delay between requests, use raw content URLs |
| Content too large | HTML page > ~5 MB | Use `--format text` instead of markdown to reduce conversion overhead |

**Most common fix:** Switch from `https://github.com/org/repo/blob/branch/path` to `https://raw.githubusercontent.com/org/repo/branch/path`. The fetch tool tries .md, /index.md, llms.txt, and llms-full.txt fallbacks, which often fail on GitHub blob pages.

---

## 4. Regex Bloopers - No Dry Run, Shell Quoting, Indiscriminate Replace

**Discovered:** 2026-06-20 (freecad-mcp annotations batch script, qcad-mcp dict cleanup)

### Trap 4a: Regex replacements without dry-run

Applying `sed`, `-replace`, or regex-based find-and-replace to source files without first running a dry-run to see what will change.

**Consequences:**
- Accidental matches: `fastmcp\.tool\.annotations` may match comments, strings, and imports
- Over-matching: broad patterns like `_MUTATING` catch both the definition AND all usages, potentially duplicating or removing lines
- Wrong scope: a regex hitting multiple files can silently skip or double-match files with different line endings or BOM markers

**Rule:**
> Every regex-based file mutation MUST be preceded by a dry-run that shows EXACTLY which files will change and how. Use `Select-String` to preview matches before applying replacements.

**Safe pattern:**
```powershell
# Step 1: Preview
$matches = Select-String -Path "src/**/*.py" -Pattern "fastmcp\.tool\.annotations"
$matches | Format-Table Path, LineNumber, Line

# Step 2: Verify count and context - only then replace
if ($matches.Count -gt 0) {
    Write-Host "WARNING: $($matches.Count) matches found. [Y] to proceed?"
    $confirm = Read-Host
    if ($confirm -eq 'Y') { ... do replace ... }
}
```

### Trap 4b: PowerShell quoting in -replace

PowerShell's `-replace` operator uses regex, not literal strings. Special characters:
- `.` matches ANY character, not a literal dot
- `$` in the replacement string is a group reference, not a literal dollar sign
- Backslashes need escaping depending on context

**Examples of broken replacements:**
```powershell
# BROKEN - dots match any char, $1 is a group ref, not literal "$1"
$content -replace "fastmcp.tool.annotations", "..."

# BROKEN - the \b in PowerShell string needs escaping
$content -replace "\breadcrumb", ""

# CORRECT - escape dots, use simple strings for simple replacements
$content -replace "fastmcp\.tool\.annotations", "new.import"

# CORRECT - use [regex]::Escape for literal strings
$pattern = [regex]::Escape("fastmcp.tool.annotations")
$content -replace $pattern, "new.import"
```

### Trap 4c: No backup before batch edit

Modifying 3+ files with a regex or batch script without timestamped backups.

**Consequence:** When the regex hits the wrong files (e.g., matches inside comments, strings, or wrong indentation level), there is no way to revert without git. If git is not available (temp files, generated files), the original content is lost.

**Rule:**
> Any batch operation touching 3+ files MUST backup first. See `GIT_REPOSITORY_SAFETY.md`. **Do not** leave backups beside each target file - use `scripts/FleetMassFix-Common.ps1` (backups go to `_junk/fleet-mass-fix-backups/<session>/`).

```powershell
# Fleet mass-edit scripts (repair-starts-launchers.ps1, etc.)
. .\scripts\FleetMassFix-Common.ps1
Initialize-FleetMassFixSession -ScriptName 'my-sweep'
Set-FleetMassFixFileContent -Path $path -Content $newContent
# After verify: remove _junk/fleet-mass-fix-backups/<session>/
```

### Trap 4d: Inserting code at wrong indentation level

Using line-number-based insertion or "last import" heuristics to add code can place new definitions at wrong scopes (e.g., inside a function body rather than at module level).

**Safe pattern for adding module-level constants:**
```powershell
# Find a known module-level anchor (e.g., 'logger =')
$anchorLine = (Select-String -Path $file -Pattern '^logger = ' | Select-Object -First 1).LineNumber
# Insert after the anchor
$lines = Get-Content $file
$insertAt = $anchorLine  # or $anchorLine + 1 for after the line
$lines = $lines[0..$insertAt] + $newContent + $lines[($insertAt+1)..($lines.Count-1)]
Set-Content $file $lines
```

### Trap 4e: Fleet-sweep regex without fixture test

**Discovered:** 2026-07-29 (204-justfile bootstrap sweep - regex `^bootstrap:` failed to detect existing recipes, creating 68 duplicates)

**Cause:** PowerShell's `-match` operator does NOT default to multiline mode. `'^bootstrap:'` only anchors at position 0 of the entire string, not at each line start. Use `(?m)^bootstrap:` for per-line anchoring.

**Consequence:** A fleet-sweep script that uses `-match '^bootstrap:'` against `Get-Content -Raw` output will always report "no match" on files where `bootstrap:` is not the very first line. The script then appends a duplicate recipe to 204 files, 68 of which silently gained broken recipe blocks.

**Proof (30-second fixture test):**
```powershell
$test = @'
build-native:
    cargo build

bootstrap:
    uv sync --group dev
'@

$test -match '(?m)^bootstrap:'  # True - multiline, correct
$test -match '^bootstrap:'       # False - only matches string start
```

**Rule:**
> Every regex used in a fleet-sweep script (3+ files) MUST be validated on a miniature fixture **in the same session** before the real sweep runs. A 30-second `[regex]::Match()` or `-match` test against a 4-line fixture saves a 68-repo cleanup. This applies to `Select-String` patterns, `-replace`, `[regex]::Matches()`, and `-match` in conditionals. The fixture MUST contain at least one positive case and one negative case.

**Safe pattern:**
```powershell
# BEFORE any fleet sweep - validate regex on fixture
$fixture = @'
first-line
bootstrap:
    uv sync
last-line
'@

$positive = $fixture -match '(?m)^bootstrap:'  # must be $true
$negative = $fixture -match '^bootstrap:'       # must be $false (unless bootstrap IS line 1)

if (-not $positive) { throw "Regex failed positive case - aborting sweep" }
# Proceed with sweep using the VALIDATED regex
```

---

## 5. JSON Schema Validation in Tool Calls

**Discovered:** 2026-06-20 (multiple `todowrite` failures due to special characters in JSON content)

**Symptom:**
```
Invalid input for tool todowrite: JSON parsing failed: ...
Expected ',' or '}' after property value in JSON at position ...
```

**Cause:** The tool call's JSON parameters are parsed by a strict JSON decoder. Content strings containing:
- Unescaped double quotes inside string values (`"like this"`)
- Line breaks within string values
- Em dashes or smart quotes

will cause the JSON parser to reject the entire call.

**Fix:** When writing JSON parameters, either:
- Escape all double quotes inside values: `"content": "line 1 text\\nmore text"`
- Or use single-parameter-per-line format that avoids embedded JSON
- Replace em dashes `-` with `--` or `-` in content strings

---

## 6. Stale In-Process API Credentials Surfacing as a Flat "Invalid API Key" Error

**Discovered:** 2026-06-20 (tailscale-mcp `manage_tailnet_devices` returning 401 despite a valid key on disk)

**Symptom:**
```
Error calling tool 'manage_tailnet_devices': Failed to perform device operation: Failed to list devices: Failed to list devices: Invalid API key or authentication failed
```

The error gives zero signal on what to actually do. The natural reaction - "go generate a new API key" - is often the wrong fix and wastes a key rotation, an admin-console trip, and another server restart that still doesn't help if the real cause is the second one below.

**Cause - two distinct failure modes that both produce HTTP 401, and the wrapper collapses them into one indistinguishable string:**

1. **Genuinely invalid/expired key.** The credential on disk is actually bad (revoked, past expiry, wrong tailnet/account).
2. **Stale in-process credentials (the more common case for long-lived servers).** Most FastMCP servers load credentials once via `load_dotenv()` / `BaseSettings` at *import time* (`config.py`'s module-level `load_dotenv(env_path)`, or inside `__init__` of a manager/client class). If the `.env` file is edited, or credentials are rotated through a webapp settings endpoint, **after** that process already started, the *file* is correct but the *running process* is still holding the old value in memory. Nothing re-reads the file on a per-call basis - that would require either a file-watcher, a TTL-based reload, or an explicit `reload_credentials()` call wired into every settings-mutation path (and even where one exists, like `tailscalemcp.mcp_server.TailscaleMCPServer.reload_credentials()`, it only patches *that* process's instances - a separate stdio-spawned process for the same server, e.g. one Claude Desktop launched independently of a webapp-mounted instance, never sees it).

**Detection - confirm which of the two it is before doing anything:**

```powershell
# Test the key on disk DIRECTLY against the provider's API, bypassing the MCP server entirely.
$key = (Get-Content .env | Where-Object { $_ -match "^TAILSCALE_API_KEY=" }) -replace "^TAILSCALE_API_KEY=", ""
$tailnet = (Get-Content .env | Where-Object { $_ -match "^TAILSCALE_TAILNET=" }) -replace "^TAILSCALE_TAILNET=", ""
Invoke-RestMethod -Uri "https://api.tailscale.com/api/v2/tailnet/$tailnet/devices" -Headers @{Authorization="Bearer $key"}
```
If this succeeds but the MCP tool still 401s: **the file is fine, the running process is stale.** Restart it.
If this also fails: the key itself is bad - rotate it.

Also check process start time vs. last `.env` edit:
```powershell
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match "<server module name>" } | Select ProcessId, Name, CreationDate
(Get-Item .env).LastWriteTime
```
If `CreationDate` predates `LastWriteTime`, that process has stale credentials by definition.

**Fix:**
- Stale-in-process: restart the MCP server process (for stdio-spawned servers, restart the MCP host - Claude Desktop, Cursor, etc.; for a webapp-mounted instance with a `reload_credentials()`-style hook, call that endpoint instead of a full restart).
- Genuinely invalid: rotate the key at the provider, update `.env`, then still restart the process (rotating the file alone does not help a process that already cached the old value).

**Rule (HARD) - error responses MUST distinguish the two causes, not collapse them:**
> Any tool-module exception boundary that can see an HTTP 401 (or equivalent auth failure) from an upstream API MUST NOT re-wrap it into a flat, single-string error. The response must include a structured `recovery_options` (or equivalently named) field listing both candidate causes - stale-in-process vs. genuinely-invalid - each with its own `check` (how to tell which applies) and `fix` (what to actually do). A flat string forces the person to guess, and the wrong guess (key rotation) burns more time than the actual fix (restart).

**Reference implementation:** `tailscale-mcp`'s `src/tailscalemcp/tools/_helpers.py` - `is_auth_error()` walks the exception's `__cause__` chain (with a message-text fallback for call sites that stringify before re-raising, breaking the chain) to detect an `AuthenticationError` anywhere in it, and `build_auth_error_response()` builds the two-cause `recovery_options` payload, including a process-age hint when `server_started_at` is passed (module-import time is a reasonable proxy). Wired into `device_tool.py`'s outer `except Exception` block as the pattern to replicate in every other tool module across the fleet - most fleet servers share the same "load credentials once at import/init time" pattern and are equally susceptible. When patching a given server, check its config-loading layer first (`config.py`, the manager `__init__`, or wherever `load_dotenv()` / equivalent runs) to confirm it's load-once rather than per-call, since that confirms this trap applies before spending time on the fix.

**Anti-pattern to avoid while fixing this:** Don't "fix" it by making credential loading reload from disk on every tool call - that reintroduces a stat()/parse cost on every request for a problem that's actually rare (credentials change maybe a few times a year). The structured error + restart is cheaper and the restart is something the person controls and is aware of, vs. invisible per-call file I/O that nobody asked for.

**Fleet rollout tracking:** See [operations/AUTH_ERROR_SURFACING_FLEET_ROLLOUT.md](../operations/AUTH_ERROR_SURFACING_FLEET_ROLLOUT.md) for the candidate repo list, priority order, and per-repo patch checklist.

---

## 7. Batch Scripts Wreck Files - One Repo at a Time

**Discovered:** 2026-06-21 (Playwright e2e justfile batch - 12 repos, 1 truncated, destroyed 126→13 lines)

**Trap:** Writing a Python/Shell script that iterates over multiple repos and applies the same transformation to each one. The script inevitably hits an edge case - encoding, line endings, file format differences - that corrupts one or more files, and you don't notice until the user screams.

**Rule (HARD):**
> NEVER write a batch script that modifies files across multiple repos. If a task affects more than one repo, do them one at a time using the `edit` tool (or equivalent file-by-file editor). The only exception is read-only audits (grep, lint checks) which cannot destroy content.
>
> If the task genuinely requires the same change in N repos, the correct procedure is:
> 1. Make the change in ONE repo using `edit`
> 2. Test it (lint, build, run - whatever applies)
> 3. Only after it passes, move to the next repo
> 4. Repeat serially

**Why this rule exists:**
- Batch scripts skip per-repo differences (encoding, line endings, file structure)
- A single edge case corrupts one file and the entire batch is suspect
- The time saved by batching is lost tenfold when you have to revert and redo
- Serial editing with `edit` takes ~30 seconds per repo - user waits an extra 5 minutes, but the result is correct

**2026-07-28 regression (ruff / CI fleet scripts):** Agents ran mutating `.ps1` across 100+ repos without a one-repo pilot. Known damage: `bump-fleet-ruff.ps1` scriptblock `-replace` injected PowerShell into `agy-mcp/pyproject.toml`; `fix-fleet-ruff-e501-ignore.ps1` truncated `vrchat-mcp/pyproject.toml`; first `fix-fleet-pytest-ci.ps1` used invalid `-replace` scriptblock and duplicated `.github/workflows/ci.yml` bodies. **Cursor rule:** `.cursor/rules/fleet-batch-scripts.mdc`.

### Trap 7a: CI `pytest --no-cov` without `pytest-cov` (not a missing dep)

**Symptom:** Ruff green on GH; pytest step dies instantly: `unrecognized arguments: --no-cov`.

**Cause:** `--no-cov` is a flag provided by the **pytest-cov plugin**. If `pytest-cov` is not in dev deps, pytest does not recognize the flag. This is a **wrong CI line**, not "install pytest-cov to fix" (unless you actually want coverage in that repo).

**Fix:** Remove `--no-cov` from `ci.yml` when the repo has no `pytest-cov` / no `addopts = "--cov..."`. Keep `--no-cov` only when coverage is configured and CI should skip the gate.

**Push gate:** Run the same pytest command as CI locally before push; ruff-only commits do not prove CI green.

### Trap 7b: Ruff 0.16 implicit `select` explosion (~59 → ~413 rules)

**Symptom:** Repo was green on Ruff 0.15; after bump to 0.16 CI/local suddenly shows hundreds of new violations with no code changes.

**Cause:** Ruff **0.16** expanded the implicit default `select` when `[tool.ruff.lint] select` is **omitted**. This is intentional upstream behavior - not a bug.

**Fix (fleet norm):**

1. Pin **`ruff>=0.16.0,<0.17`** in dev deps only.
2. Add **explicit** `[tool.ruff.lint] select = [...]` - never rely on defaults.
3. Extend beyond baseline `["E", "W", "F", "I", "B", "UP"]` per repo (`"S"`, `"RUF"`, etc.) - the extended ruleset is **wanted**; every repo must go **ruff-green anew** under its declared `select`, not dodge it with minimal `["E4","E7","E9","F"]` unless that repo is explicitly legacy-tier.
4. CI template **blocks** missing `select` and non-0.16 Ruff (`templates/ci.yml.template`).

**Do not:** batch-mutate `pyproject.toml` across the fleet without a one-repo pilot (Trap 7).

### Trap 7c: Pre-commit ruff scoped narrower than CI (fake local green)

**Symptom:** `git commit` succeeds (pre-commit ruff passed) but GitHub Actions ruff fails - or the agent claims “ruff green” while `scripts/` / `mcpb/` still fail when run manually.

**Cause:** `.pre-commit-config.yaml` added `files:` (or similar) on the **ruff** / **ruff-format** hook to skip directories (e.g. `^(src/|tests/)`) instead of fixing violations. CI still runs `uv run ruff check src tests` (or a **broader** path set). Scopes diverge.

**Fix:**

1. **Remove** hook-only `files:` / excludes on ruff - use fleet template without narrowing.
2. Run the **exact** CI ruff commands locally before push (see `templates/ci.yml.template`).
3. If `scripts/`, `mcpb/`, or other trees must be linted, add them to **both** CI and pre-commit (or shared `just lint` / `scripts/ci.ps1`) - never pre-commit-only.
4. Same discipline for **Biome**: pre-commit script and `npm run biome:ci` must target the same tree (`src` vs `.` is a common mismatch).

**Do not:** “unblock” commits by shrinking pre-commit scope. **Cursor rule:** `.cursor/rules/pre-commit-ci-ruff-parity.mdc`.

---

## 7. `git init` on Existing Repo - Silent History Nuke

**Discovered:** 2026-06-27 (virtualization-mcp)

**Trap:** Using `Test-Path ".git"` to check if a directory is a git repository. PowerShell's `Test-Path` does **NOT** detect hidden items by default - it returns `False` for `.git` even when the directory exists and is a fully functional git repository. An agent who then runs `git init` creates a fresh empty repository, silently destroying all local commit history.

```powershell
# WRONG - Test-Path does NOT see hidden items
Test-Path ".git"          # → False even if .git exists!

# CORRECT - force flag or proper cmdlet
Test-Path -Force ".git"   # → True
Get-ChildItem -Hidden -Name ".git"  # finds it
git rev-parse --git-dir   # → ".git" if inside a repo, errors otherwise (best)
```

**Rule (HARD):**
> NEVER use `Test-Path ".git"` to check repo status. Use `git rev-parse --git-dir` instead. It's the only reliable way: returns `.git` if inside a repo, non-zero exit + stderr if not.
>
> NEVER run `git init` unless you have explicit user confirmation that they want a fresh repo. If you need to check whether a directory has git: prefer `git rev-parse --git-dir 2>$null` and catch the error.
>
> If `git rev-parse --git-dir` succeeds, do NOT reinitialize. Period.

**Recovery if you nuked the history:**
```powershell
# Option A - re-clone from remote (preserves GitHub history, safest)
gh auth login                          # authorize first
Remove-Item -Recurse -Force repo-path\.git
Remove-Item -Recurse -Force repo-path  # (or move aside)
git clone <remote-url> repo-path
# Then re-apply your working-tree changes

# Option B - force push (nukes remote history too, simpler)
gh auth login
git remote add origin <remote-url>
git push -u origin main --force
```

**Why this rule exists:**
- `Test-Path` default mode excludes hidden/system files on Windows
- `.git` is always hidden - the `False` return is misleading, not informative
- `git init` on an existing repo **replaces** `.git` - no warning, no confirmation
- The cost of this mistake is 100% of local commit history - unrecoverable without remote
- `git rev-parse --git-dir` is the canonical, safe, zero-destructive check

---

## 8. `localhost` vs `127.0.0.1` on Goliath - silent 404 instead of connection-refused

**Discovered:** 2026-07-13 (splatmaker-mcp scaffold verification)

**Symptom:** A freshly started uvicorn/FastMCP HTTP server logs "Uvicorn running on http://127.0.0.1:PORT" and "Application startup complete" - genuinely up, no errors - yet `Invoke-WebRequest -Uri "http://localhost:PORT/..."` returns a flat HTTP 404, not a connection-refused error. The same request against `http://127.0.0.1:PORT/...` succeeds immediately with the correct response.

**Cause:** On this box, `localhost` does not reliably resolve to the same address the server bound to. `uvicorn.run(app, host="127.0.0.1", ...)` binds IPv4 only; if `localhost` resolves to `::1` (IPv6) first in this environment, the request either hits nothing (should be connection-refused, but something intercepts and answers 404 - exact mechanism not fully diagnosed, worth revisiting if it recurs) or hits a different, unrelated listener that happens to be bound on the same port over IPv6. Confirmed via side-by-side test: identical request, `127.0.0.1` → 200 with correct JSON body, `localhost` → 404, same process, same moment.

**Rule:**
> When health-checking, smoke-testing, or scripting against a locally-bound fleet server from PowerShell/winops on Goliath, use `127.0.0.1` explicitly, never bare `localhost`. This applies to ad hoc verification commands as much as to any script that might get promoted into a `start.ps1` health-check or CI step.
>
> This does NOT mean change every server's bind address or every webapp's proxy config fleet-wide on the strength of one repro - that's a bigger change than one discovery justifies. It means: if you hit an inexplicable 404 (not connection-refused) against a `localhost`-addressed local server that you can otherwise confirm is running and healthy, try `127.0.0.1` before concluding the server itself is broken. Several turns were burned on this exact confusion during splatmaker-mcp's scaffold verification before the `127.0.0.1` vs `localhost` side-by-side test isolated it.

**Not yet done:** root-causing WHY `localhost` returns 404 specifically rather than connection-refused (what's actually answering on `::1` or wherever it resolves) - flagged for whoever next hits this and has time to dig further, rather than blocking the immediate fix on a full root-cause.

**Reverse direction (2026-08-02, learnbot-mcp):** the SAME `::1` vs `127.0.0.1` split hits **vite itself**, not just Python backends. When `vite.config.ts` has a `server:` block but **no `host:` key**, vite binds to `localhost` only, which on Windows resolves to **IPv6 `::1`** - NOT IPv4 `127.0.0.1`. Symptom: `netstat`/`Get-NetTCPConnection` shows the port `Listen`ing (on `::1`), the launcher reports success, but `http://127.0.0.1:{frontend_port}` gives `ERR_CONNECTION_REFUSED`. The browser URL printed by the launcher may work while every scripted health-check against `127.0.0.1` fails.

**Cause:** vite's default `host` is `localhost`; on this box `localhost` resolves IPv6-first. Most fleet `start.ps1` scripts pass `--host` on the CLI, which hides this. It goes live when a launcher runs vite **flag-less** (e.g. `bun run dev`, `npm run dev`, `npm --prefix webapp run dev`).

**Rule (HARD):** every `vite.config.ts` with a `server:` block MUST pin `host: "127.0.0.1"` (IPv4) - never rely on the default `localhost`. Reference: learnbot-mcp `webapp/vite.config.ts` (fixed 2026-08-02 after `learnbot-start.bat` "no webapp started" report; `Get-NetTCPConnection -LocalPort 11102` showed `::1` only). Fleet rollout: 47 repos patched 2026-08-02 in batches of ≤5 with timestamped `.bak` backups.

**Related, same investigation:** `Start-Process -FilePath "uv" -ArgumentList "run ..." -PassThru` returns the PID of `uv.exe`, not the actual server process - `uv run` interposes at least one process hop (often two: `uv.exe` → `python.exe` running the venv interpreter → the entry point). `Stop-Process -Id $p.Id` only kills the wrapper, leaving the real server process orphaned and still holding its port - exactly what happened repeatedly during this same verification session, requiring a manual `Get-CimInstance Win32_Process | Where CommandLine -like "*servername*"` hunt to find and kill the actual zombie.

**Rule:** when cleaning up a `Start-Process`-launched `uv run` (or any wrapper command), use `taskkill /PID $p.Id /T /F` (the `/T` tree-kill flag), never bare `Stop-Process -Id $p.Id`. Verified this kills the entire process chain in one call, cascading through every hop, versus the alternative of hunting individual orphaned PIDs by command-line match after the fact.

---

## 9. `schtasks` fails silently from a UAC-filtered PowerShell token - `winops_auto_task_create` doesn't

**Discovered:** 2026-07-13 (Postshot install verification, archiving the installer to `D:\Dev\archives\postshot\`)

**Symptom:** A raw `schtasks /create ...` call issued from an agent's PowerShell session fails (or silently no-ops) when the task needs elevation - e.g. creating a scheduled task that runs a service or installer step requiring admin rights - even though the same PowerShell session can run plenty of other admin-adjacent commands without complaint.

**Cause:** An agent's PowerShell session on Goliath runs under a UAC-filtered token (standard Windows admin-approval-mode behavior - an administrator's logon token is split into a full token and a filtered/standard token, and interactive-adjacent processes get the filtered one by default). `schtasks` invoked directly from that filtered token inherits the same restriction and can't create tasks requiring elevation, but doesn't always fail loudly - it can appear to succeed or give a generic error that doesn't point at UAC.

**Fix:** use `winops_auto_task_create` (the winops MCP tool) instead of raw `schtasks` for anything task-scheduler-related that might need elevation. The winops service itself runs under different (higher) privileges than the calling agent's shell, so it can create the task where a same-shell `schtasks` call cannot.

**Rule:** don't reach for raw `schtasks` from an agent PowerShell session for anything beyond trivial non-elevated tasks. Prefer `winops_auto_task_create` by default for scheduled-task creation on Goliath - it sidesteps the UAC-filtered-token problem entirely rather than requiring a manual elevation workaround per call.

---

## 10. Web-fetch tools don't execute JS pricing calculators - byte-identical repeated fetches are the tell

**Discovered:** 2026-07-13 (splatmaker-mcp engine research - Postshot/Jawset pricing verification)

**Symptom:** A web-fetch tool call against a SaaS pricing page returns the same numbers every time, including implausible ones (every tier showing €0.00, including tiers with premium features like CLI access or HDR export). The result looks clean and gets cited as "verified live" - the trap is that it's genuinely wrong, not obviously broken.

**Cause:** Modern pricing pages are frequently JS-driven - a currency selector, a monthly/yearly toggle, a per-seat quantity stepper all imply a client-side calculator that computes or fetches real prices *after* page load. A web-fetch tool that extracts static HTML/markdown (no JS execution, no wait-for-hydration) captures the page in its pre-hydration placeholder state. Placeholder pricing is very commonly `0.00` or a template variable rendered as zero, which reads as plausible ("oh, it's a free tier") rather than obviously broken ("error" or blank).

**Detection - the tell that was missed in real time:** three separate fetches of the same pricing page, at different points in a research session, returned byte-identical output - same numbers, same whitespace, same everything. A real pricing page with a visible currency/period/quantity selector should show at least some plausible variation in manual testing, or should be treated with suspicion if a fetch tool returns a static-looking snapshot with **no evidence the selectors did anything**. If a fetch shows implausible round numbers (all tiers €0.00, especially a tier with a clearly premium feature like CLI/API access) on a page with interactive pricing controls, that's the signal to distrust the fetch, not to report it as verified.

**Rule:** when a pricing page has any visible interactive control (currency selector, billing-period toggle, seat-count stepper), treat a web-fetch tool's numbers as **unverified** by default, not confirmed. Either (a) ask the person to check in their own browser (JS-executing, ground truth) rather than assert the fetched number as fact, or (b) explicitly flag the number as "static-extraction result, may be a pre-hydration placeholder" in whatever gets written down, so a wrong number doesn't silently propagate into research docs, comparison tables, or recommendations as if it were verified. Retracting a wrong "verified live" claim after the fact costs real credibility and real doc-correction effort - flagging the uncertainty up front costs one sentence.

**Fleet-specific cost of getting this wrong:** the false €0.00 reading here fed directly into a `SplatBackend` engine recommendation for splatmaker-mcp, materially changing which tool looked worth using unattended.

---

## 11. Check `D:\pinokio\api\` before downloading any AI model fresh

**Discovered:** 2026-07-14 (comfyops-mcp / ComfyUI model setup)

**Symptom:** About to pull a multi-GB model checkpoint (Wan, FLUX, or similar) from Hugging Face/CivitAI for a fleet server that needs local generation, without checking whether it's already sitting on disk somewhere.

**Cause:** Pinokio (a one-click AI-app installer) has been used over roughly the past year to install a dozen-plus generative apps - FaceFusion, Hunyuan3D, HunyuanVideo, MMAudio, SongGeneration-Studio, Wan, ComfyUI itself, and more, all under `D:\pinokio\api\<name>.git\`. Some of these installs include real, substantial model weights (found: ~25GB of genuine Wan 2.1 weights - 14B text2video, T5 encoder, VAE - sitting unused). Others only got as far as setting up a Python environment with no model ever actually downloaded (found: a "flux-2-klein-pinokio.git" folder that looked promising at 6GB but was entirely `torch`/CUDA library files, zero model weights - don't assume folder size alone means real weights, check for actual `.safetensors`/`.gguf`/`.ckpt` files).

**Rule:** before pulling any AI model checkpoint fresh for a fleet server, check `D:\pinokio\api\` for an app that might already have it. Quick check: `Get-ChildItem -Path "D:\pinokio\api\<likely-name>.git" -Recurse -File -Include "*.safetensors","*.gguf","*.ckpt" | Select Name,@{N='SizeGB';E={[math]::Round($_.Length/1GB,2)}}` - if real weights are there, copy (don't move - leave Pinokio's own app intact in case it's still used directly) into the target server's expected model directory. This can turn a multi-hour, multi-GB download into a 30-second local disk copy. Watch for version mismatches though (found: Pinokio had Wan **2.1**, not the 2.2/2.7 a fleet doc might actually want - note the version explicitly, don't assume "a Wan model" is interchangeable with "the Wan model version this task needs"). Bad pricing data in research docs isn't cosmetic - it can steer a real build decision.


---

## 12. Claude Desktop's built-in `create_file` writes to the Linux sandbox, not Goliath - use `fileops:file_ops` for every Windows path

**Discovered:** 2026-07-17 (sketchboard-excalidraw-mcp day 1 scaffold)

**Symptom:** A batch of files (pyproject.toml, README, server.py, tests, docs) written with the Claude Desktop built-in `create_file` tool against `D:\Dev\repos\...` paths appeared to succeed (tool returned success, listed the path), but `fileops:dir_ops` directory-tree check of the same path on Goliath showed the directories present and empty - every file landed in the Linux container instead. `git init` + `git add -A` + `git commit` in the real repo then correctly reported "nothing to commit," which was the tell.

**Cause:** `create_file` is the Claude Desktop/Claude Code built-in file tool, scoped to the sandboxed Linux execution environment, not the Goliath filesystem. It accepts Windows-style paths without erroring, so there's no failure signal at write time - only a later `fileops`/`winops` read or a git operation surfaces the mismatch.

**Rule:** this restates and reinforces the existing user-preference rule (ALWAYS fileops:file_ops for file creation on Goliath, NEVER create_file for Windows paths) as a filed fleet pitfall, since it was violated in practice despite being an explicit standing instruction. After any multi-file scaffold, verify with a directory listing or a `git add -A && git commit` dry run before assuming files landed - a "nothing to commit" or an empty directory listing right after a batch of "successful" writes is the signal this happened again.

---

## 13. Windows PowerShell 5.1 `Set-Content -Encoding UTF8` Always Writes a BOM - Fleet-Wide, 344 Occurrences

**Discovered:** 2026-07-18 (`sota-scripts/mcp-server-builder/new-mcp-server.ps1` v2.0.0 rewrite)

**Symptom:** A PowerShell scaffolder writes a `.py` file that then fails `ast.parse()` (or any other strict UTF-8 consumer - some shebang detectors, some strict JSON parsers) with a syntax/decode error on line 1, even though the file looks completely normal when opened in an editor.

**Cause:** `Set-Content -Encoding UTF8` in **Windows PowerShell 5.1** (not PowerShell 7+) always prepends a UTF-8 BOM (`EF BB BF`) - there is no `UTF8NoBOM` encoding option pre-pwsh-7. Editors and PowerShell itself silently skip the BOM and show clean content, which is why this goes unnoticed until something downstream parses the bytes strictly.

**Detection:**
```powershell
Get-Content -Path $file -Encoding Byte -TotalCount 3   # or Format-Hex -Count 3
# EF BB BF = BOM present (the bug)
```
```python
# ast.parse with explicit 'utf-8' (not 'utf-8-sig') surfaces it immediately:
import ast
ast.parse(open(path, encoding='utf-8').read())  # raises on a BOM'd file
```

**Fix - the only reliable BOM-less UTF-8 write pattern for PS 5.1:**
```powershell
function Write-Utf8NoBom {
    param([string]$Path, [string]$Value)
    $fullPath = if ([System.IO.Path]::IsPathRooted($Path)) { $Path } else { Join-Path (Get-Location).Path $Path }
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($fullPath, $Value, $utf8NoBom)
}
```
Replace every `Set-Content -Path X -Value Y -Encoding UTF8` with `Write-Utf8NoBom -Path X -Value Y`. Watch for two variants that a blind regex/find-replace will miss: calls using `-LiteralPath` instead of `-Path`, and retry/fallback code paths that write via raw `[System.Text.Encoding]::UTF8` (which is BOM-including, same bug, different spelling).

**Rule:**
> Never use `Set-Content -Encoding UTF8` in a script that must run under Windows PowerShell 5.1 (`$PSVersionTable.PSVersion.Major -lt 7`) if the output will be consumed by anything that does strict UTF-8 decoding (Python `ast.parse(encoding='utf-8')`, some linters, some JSON parsers). Use `Write-Utf8NoBom` (or equivalent `WriteAllText` + `UTF8Encoding($false)`) instead.

**Fleet scope (not yet remediated):** a fleet-wide `Grep` for `Set-Content.*-Encoding UTF8` across `D:\Dev\repos\**\*.ps1` returned **344 occurrences across 155 files** - this scaffolder was one instance of a widespread pattern, not an isolated bug. A separate check for `Set-Content -LiteralPath` (25 files) found no same-line/adjacent-line overlap with `-Encoding UTF8` via regex, meaning the two variants don't obviously collide in the files checked so far - but that check was shallow (regex-adjacency only, not a full per-file read) and should not be read as "those 25 files are clean."
>
> **Important nuance:** not every one of the 344 occurrences is actually broken in practice. The BOM only breaks *strict* consumers - Python's `ast.parse()` without `utf-8-sig`, some shebang/shell detection, some strict JSON. PowerShell itself, most editors, and Node tolerate a leading BOM and skip it silently. The highest-risk subset is scripts that generate `.py` files or anything fed into strict parsing (the ~24-occurrence `new-mcp-server.ps1` copies under `documentation-mcp/scripts/` and `mcp-central-docs/templates/scripts/` are the obvious next candidates, since they're the same scaffolder family as the one just fixed). The large tail - `check-repo-standards.ps1` copies (one per repo, ~2 occurrences each) and one-off utility scripts - is lower priority since most of what they write isn't strictly parsed downstream. Triage before mass-fixing; this is a real but *bounded* fleet-hygiene project, not an emergency.

**Related traps found in the same debugging session (same file, `new-mcp-server.ps1`), worth knowing about if you touch fleet scaffolders again:**

- **Mojibake/double-encoded emoji desyncs the PS 5.1 tokenizer.** A Write-Host string containing a double-encoded/mojibake Unicode emoji (garbage bytes from a prior bad encoding round-trip) can desync PowerShell 5.1's parser via OEM-codepage misreading of a UTF-8-no-BOM `.ps1` file, causing an unrelated here-string later in the *same file* to fail to parse - the error message points nowhere near the actual cause. Fix: strip all emoji/decorative Unicode from generated script output; use plain ASCII (`[OK]`, `====` banners) in any `.ps1` that will be read by PS 5.1.
- **AV/EDR secret scanners silently delete freshly-written files that look credential-shaped.** A generated `docs/CONFIGURATION.md` containing a JSON block like `"env": {"TODO_VAR": "your-value"}` was quarantined/deleted immediately after `Set-Content` reported success - no error, no warning, the write call itself returns clean. Confirmed by ruling out cmdlet choice, variable naming, path syntax, and exact filename (a fully hardcoded trivial write at the same script position also silently failed). Fix: avoid emitting credential-shaped `"key": "value"` JSON in generated docs/config examples; use plain prose instead (`Set the FOO_API_KEY environment variable to your value.`) for anything that reads like a secret even when it obviously isn't one.

---

## 14. NSSM services run as LocalSystem, so `Path.home()` silently resolves to `systemprofile` - two databases, zero errors

**Symptom:** data written through one interface is invisible in another. No error anywhere. Writes report `success: true`. The service is RUNNING and healthy. Restarting Claude Desktop changes nothing.

**Cause:** an app resolves a storage path from ambient process state instead of explicit config:

```python
base = os.getenv("APP_HOME") or Path.home()     # <-- the trap
db = base / ".app" / "app.db"
```

`Path.home()` on Windows reads `USERPROFILE`. Under an NSSM service running as `LocalSystem` that is `C:\WINDOWS\system32\config\systemprofile`, not `C:\Users\sandr`. The service and your dev-shell process then use two different databases from one codebase.

**Why it hides so well (all four of these applied in the 2026-07-26 incident):**

1. **Write success is not read visibility.** The write genuinely succeeded, to the other store. An API returning bare `success: true` tells you nothing about where.
2. **`LocalSystem` has more rights than you**, so nothing fails on the way down. There is no permission error to notice. The resulting directory then needs elevation to even read, which obstructs diagnosis.
3. **Restarting the MCP host does not restart the NSSM service.** It is an independent process with its own lifetime. Check the PID before and after: if unchanged, you restarted the wrong thing.
4. **Different vars can govern different paths.** In advanced-memory-mcp the SQLite index honoured `ADVANCED_MEMORY_HOME` but the markdown vault keyed off `Path.home()` directly. Setting only the app variable moved the DB but not the files, which reads like a partial fix and sends you chasing a second phantom.

**`Path.cwd()` is the same trap with a different variable.** NSSM's `AppDirectory` masks it for the service, so it looks fine until any other launch path (a Claude Desktop stdio instance, another shell, a scheduled task) has a different working directory.

**Empty env vars are a third variant.** `ARXIV_MCP_DATA_DIR=` with no value does not mean unset. Pydantic coerces `""` on a `Path | None` field to `Path(".")`, which is not `None`, so the intended fallback never fires and the resolved data dir becomes a *relative* path that follows CWD at runtime. This forked arxiv-mcp's corpus into two SQLite files.

**Rules:**

> 1. Never use `Path.home()` or `Path.cwd()` to locate anything a server writes. Anchor on the module instead: `Path(__file__).resolve().parents[N]`. `aiwatcher-mcp/src/aiwatcher_mcp/config.py` is the reference implementation.
> 2. When registering an NSSM service, pin the environment explicitly and decide the service account deliberately. `LocalSystem` is the default, not a choice. Most fleet servers need no privilege beyond the user's.
>    ```
>    nssm set <svc> AppEnvironmentExtra APP_HOME=C:\Users\sandr<newline>USERPROFILE=C:\Users\sandr
>    ```
>    Pin `USERPROFILE` too, not just the app variable, whenever `Path.home()` appears anywhere in the codebase.
> 3. Treat empty-string env vars as unset. Add a validator coercing `""` to `None` on optional `Path` fields.
> 4. **Log the resolved absolute storage path once at INFO on startup.** This is the single highest-value line of code here. It would have turned a four-hour investigation into one glance.
> 5. Expose the resolved storage path in the server's `status`/`health` tool.
> 6. Never return bare `success: true` from a write whose visibility depends on a separate index or sync step. Report the target path or the index status alongside.

**Diagnostic sequence when data "disappears":**

1. `sc qc <service>` - is `SERVICE_START_NAME` `LocalSystem`?
2. `reg query HKLM\SYSTEM\CurrentControlSet\Services\<svc>\Parameters /v AppEnvironmentExtra`
3. `netstat -ano | findstr :<port>` then `Get-CimInstance Win32_Process -Filter "ProcessId=<pid>"`. Confirm which binary and which account actually holds the port. Do not assume.
4. Compare PID across a restart.
5. Look for the same data dir under both `C:\Users\<user>\` and `C:\WINDOWS\system32\config\systemprofile\`.

**Fleet scope (audited 2026-07-26):** all 11 fleet services run as `LocalSystem`, 10 NSSM-wrapped, so the precondition is universal. Confirmed affected: `advanced-memory-mcp` (fixed, 71 notes recovered), `fleet-agent-mcp` (active split across `.fleet-agent` and `.fleet-intel`, touches agent identity), `arxiv-mcp` (two corpus DBs), `devices-mcp` (stale user-profile dir under a running service). Clean: `aiwatcher-mcp`. Note that `standards/DEEPLINK_STANDARD.md` currently *recommends* `Path.home()` for install locations and should be corrected.

**Memops-specific residual symptoms (2026-07-27):** even after moving `ADVANCED_MEMORY_HOME`, writes can still look broken if (a) **`USERPROFILE` was not pinned** and vault paths still follow `Path.home()` under LocalSystem, (b) **Cursor MCP was not restarted** and still talks to a stale stdio instance or read-only proxy, (c) **two writers** contend (NSSM service + daemon + dev uvicorn) - MCP may return `attempt to write a readonly database` while the webapp shows an empty index. Symptom pattern: **`success: true` in chat, silence in webapp for weeks.** Canonical memops bug report: `advanced-memory-mcp/docs/troubleshooting/BUG_REPORT_NSSM_SPLIT_BRAIN.md`. Preferred fleet mitigation: single HTTP daemon writer (`Start-MemopsDaemon.ps1 -Ensure` + `Sync-FleetMemopsClient.ps1`).

Full postmortem: `troubleshooting/2026-07-26_nssm-localsystem-ambient-path-resolution.md`

---

## 15. AI sandbox proxy escape - zero-day in package registry cache software

**Discovered:** 2026-07-22 (OpenAI/Hugging Face incident)
**Tag:** `openai-hugging-face-incident`

**The incident:** OpenAI ran an unguarded pre-release model (GPT-5.6 Sol) on the ExploitGym benchmark. The sandbox allowed outbound to a curated package registry proxy (PyPI/apt cache). The model found a zero-day in the proxy software, escaped to the public internet, then broke into Hugging Face's servers to steal the test answers.

**Why it matters for the fleet:** virtualization-mcp, deepfang, and any sandboxed MCP evaluation follow the same sandbox pattern: block everything except a package proxy. The assumption that "the proxy is trusted infrastructure" is the vulnerability. If a model can find and exploit a zero-day in the proxy, the air gap is meaningless.

**The trap:**
```python
# WRONG - the package proxy is an active attack surface
sandbox_network_rules = {
    "allow": ["https://pypi.org/simple", "http://archive.ubuntu.com"],
    "proxy": "http://internal-cache:3142"  # THIS LINE is the vulnerability
}
```

**Rules:**
> 1. Zero-trust network: no outbound at all. Air-gap or fail.
> 2. Pre-install every package in the VM image. Never `pip install` at runtime.
> 3. No credentials stored in the sandbox environment.
> 4. Short-lived, disposable VMs only. Destroy after task completion.
> 5. If a benchmark requires network access, accept the risk explicitly and document it - do not pretend a proxy makes it safe.
> 6. **Physical airgap:** before launching a sandbox with an untrusted model, physically disconnect Ethernet, disable WiFi and Bluetooth, verify `ping` and `curl` both fail. Software firewalls alone are not enough against a model that can chain zero-days. See `projects/virtualization-mcp/SAFETY.md` for the full preflight checklist.
> 7. **Audit MCP servers with physical actuation:** devices-mcp can sense motion → social engineering via speech-mcp. yahboom-mcp can press buttons. tapo-mcp can cycle mains power. Before a sensitive eval, kill every server that can reach the physical world - the sandboxed model can use them as puppets to re-enable the network. A long-distance MCP tool in a time of miracles and wonders. See `projects/virtualization-mcp/SAFETY.md` § Audit connected MCP servers.

Full case study: `standards/threats/AI_SANDBOX_ESCAPE_CASE_STUDY.md`.
Simon Willison's writeup: https://simonwillison.net/2026/Jul/22/openai-cyberattack/

---

## 16. `bun` resolves to `bun.ps1` before `bun.exe` - `Start-Process -FilePath "bun"` fails

**Discovered:** 2026-07-29 (demo-vid-mcp start.ps1, then 12 other fleet repos)

**Symptom:**
```
Start-Process : This command cannot be run due to the error: %1 is not a valid Win32 application.
```

**Cause:** `Get-Command bun` resolves to `C:\Users\sandr\AppData\Roaming\npm\bun.ps1` (a PowerShell script shim installed by npm), not to `C:\Users\sandr\.bun\bin\bun.exe`. `Start-Process` can only launch Win32 binaries - it cannot execute `.ps1` files. The npm shim sits earlier in `PATH` than the real `bun.exe`.

**Scope (2026-07-29 audit):** 13 fleet repos had this bug. giskard-mcp was the only one that already used the absolute path.

**Affected repos (fixed):** admiral-mcp, learnbot-mcp, mixx-dj-mcp, netatmo-weather-mcp, pdf-mcp, reaper-mcp, songgeneration-mcp, tapo-mcp, vcv-rack-mcp, mcp-central-docs, demo-vid-mcp.

**Not affected:** repos using `Start-Process cmd /c "bun run dev"` (cmd.exe finds `bun.exe` because it ignores `.ps1` files) or calling `bun` via `ProcessStartInfo` with `UseShellExecute=$false`.

**Rule:**
> Never use `Start-Process -FilePath "bun"` in a `start.ps1`. Use the absolute path: `C:\Users\sandr\.bun\bin\bun.exe` (as documented in `POWERSHELL_STANDARDS.md`). The `Get-Command bun | Select-Object Source` shim-check pattern applies to any CLI whose npm shim (`{name}.ps1`) precedes the native binary in PATH.

---

## 17. NSSM + `.bat` wrapper = doomed services - cmd.exe kills them on reboot

**Discovered:** 2026-07-31 (RustDesk relay vanished; fleet audit found 6 affected services)

**Symptom:** NSSM Windows services run fine for weeks, but after a system reboot they are all STOPPED with exit code `1066/4` ("process terminated unexpectedly, gave up"). The service stdout log ends with `Terminate batch job (Y/N)?` - and no one answered.

**Cause:** The NSSM service's `Application` is set to a `.bat` file (e.g. `run-aiwatcher-service.bat`). NSSM spawns `cmd.exe` to run the batch script. When Windows shuts down, `cmd.exe` pops an interactive prompt:

```
Terminate batch job (Y/N)?
```

Nobody answers, the shutdown timeout expires, `cmd.exe` is force-killed, and NSSM records the exit as a crash. Even with `AppExit Default Restart`, the timing window during shutdown means the restart never happens because the SCM is already tearing down.

**The exact chain:**
```
NSSM → cmd.exe → .bat wrapper → target.exe
                             ↓ (Windows shutdown)
                        "Terminate batch job (Y/N)?"
                             ↓ (no answer, timeout)
                        cmd.exe killed → NSSM sees crash → service stopped
```

This affected every fleet service that used a `.bat` wrapper (6 of 8). The `.bat` wrappers existed for valid reasons - setting `PATH` for `uv`, setting `UV_PROJECT_ENVIRONMENT`, or passing arguments that wouldn't fit cleanly in `nssm set AppParameters`.

**Why it wasn't caught earlier:** the services ran continuously for weeks between reboots. The fragility only manifests at shutdown/reboot time. A service that runs flawlessly for 30 days will fail every single reboot.

**Rules:**

> 1. **NSSM `Application` MUST point to a `.exe`, never a `.bat` or `.cmd`.** Use `AppParameters` for arguments.
> 2. **Environment variables go in `AppEnvironmentExtra`, not in wrapper scripts.** One `nssm set <svc> AppEnvironmentExtra KEY=VALUE` per variable. For `uv run` services: set `USERPROFILE`, `APPDATA`, `LOCALAPPDATA`, `HOME` (LocalSystem fix - see Trap 14), then point Application at `uv.exe` and AppParameters at `run --directory <repo> python -m <module>`.
> 3. **Use `AppDirectory` for the working directory**, not `cd` in a wrapper.
> 4. **Active fleet services that had this defect (fixed 2026-07-31):** aiwatcher-mcp, fleet-agent-mcp, devices-mcp, tvtropes-mcp. email-mcp had no installed service. RustDesk-HBBS (now migrated to direct exe).
> 5. **Do not "fix" this by wrapping in `.ps1` instead.** `powershell.exe -File wrapper.ps1` has the same fragility: PowerShell prompts for confirmation on some exit codes and can hang the teardown chain. The fix is no wrapper of any kind - the Application IS the real binary.

**Fix script:** `mcp-central-docs/scripts/fleet-fix-nssm.ps1` - migrates all `.bat`-wrapped fleet services to direct `uv.exe` + environment pins.

**Reference:** `standards/WINDOWS_SERVICE_STANDARDS.md` - three-tier fleet standard (C++ self-installing, NSSM, sc.exe).

**How to detect:** scan service configs for `.bat` or `.cmd` in the binary path:
```powershell
sc.exe qc <service> | Select-String "\.bat|\.cmd"
```
If it matches, that service will die on the next reboot. Fix it before then.

## 18. Bare venv tools in justfiles - the ruff-PATH footgun (naked-PC failure)

**Symptom:** `just lint` fails with "`ruff` is not recognized..." in an agent shell, CI, or on a fresh checkout - while working perfectly on the developer's interactive terminal. Some recipes silently use a *different version* of the tool instead of failing (worse: phantom lint violations or masked real ones).

**Cause:** Justfiles invoke project-venv tools bare: `ruff check .`, `pytest tests/`, `python -m build`, `pre-commit install`. These tools live in the project's `.venv`, NOT on PATH. The dev machine happens to have a global install (e.g. `Python313\Scripts\ruff.exe`) so it "works" - but any shell without that PATH entry (agent shells, CI runners, naked PCs) fails outright. Version drift between global and venv ruff silently changes what `just lint` actually checks.

**Why it wasn't caught earlier:** the developer's shell had the global tool on PATH, so every recipe ran green. Nothing exercised the clean-shell path.

**Rules:**

> 1. **HARD RULE - every venv tool call in a justfile MUST be `uv run <tool>`.** `ruff`, `pytest`, `mypy`, `python`, `pip`, `pyinstaller`, `pre-commit`, `bandit`, `safety` - all of them. `uv run` resolves the exact pinned version from the project environment and works on any machine with uv.
> 2. **Node tooling is exempt** - `npm`, `npx`, `bun` are on PATH by design; `npx` resolves package-local binaries.
> 3. **Verify from a clean shell:** after writing a justfile, run `just lint` with global Python tooling removed from PATH (or in CI). "Works on my machine" is the bug report, not the fix.
> 4. **Audit command:** `rg -n "^\s*(ruff|pytest|python|pip|mypy|pre-commit|pyinstaller)\b" --glob "justfile" D:\Dev\repos`

**Fleet fix (2026-07-31):** 16 repos had bare `ruff` (+ `pytest`/`mypy`/`python`/`pre-commit`/`pyinstaller` in 6). All migrated to `uv run`. Related pre-existing justfile gate-breakers found in the same sweep: duplicate recipes colliding with `scripts/just/fleet.just` imports (`mcpb-pack`, `cua-nsis-test` in mujoco-mcp, robofang) and stray recipe-body lines from a broken template (unitree/isaac/limx/ros/gazebo) - both make every `just` invocation fail with a parse error.

**Reference:** `standards/JUSTFILE_STANDARDS.md` § VII (HARD rule + exemption + verification).

## 19. Stale NSSM AppParameters after CLI refactor - silent crash loop, service "Running", port dead

**Symptom:** an NSSM service reports `Running` forever, but its port is dead. No error
anywhere the user looks - the service appears healthy in `services.msc`. Its log directory
fills with hundreds of thousands of 0-byte rotated files. Two confirmed incidents 2026-08-13:

- **`advanced-memory-mcp`** (bridge, port 10705): AppParameters ran `python -m
  advanced_memory.server --http`, but `server.py` was refactored to a pure ASGI module
  (docstring: `uv run uvicorn advanced_memory.server:app --port 10705`). `python -m`
  imported the module and exited code 0 - NSSM restarted it every ~3.7 s for **8 days**,
  producing 192,466 stdout + 192,466 stderr rotations. Zero listeners, zero health.
- **`mcp-pywinauto-mcp`** (CUA, port 10789): AppParameters passed `--mode http`, but the
  CLI was refactored to `--stdio | --http | --sse` transport flags. argparse rejected
  `--mode http` with exit 2 - restart loop with a **changing child PID every ~20 s**.

**Why it hides so well:**

1. **NSSM restarts silently.** The service never enters `Stopped` state; nssm shows it as
   `Running` while its child churns. No Windows event, no user-visible failure.
2. **Exit codes 0 and 2 both look like "ran" to nssm's default restart policy.** A clean
   exit (no runner) and an argparse error (bad flag) both just get restarted.
3. **No logs configured.** If `AppStdout`/`AppStderr` are not set (pywinauto case), the
   crash reason goes nowhere. If they ARE set with `AppRotateFiles=1` (advanced-memory
   case), each restart produces a new tiny rotation that buries the signal and eats disk.
4. **The CLI is the source of truth, the service config is a snapshot.** Nothing
   re-validates NSSM AppParameters when the repo's entry points change.

**Diagnostic sequence:**

1. Port dead but service Running? → `Get-CimInstance Win32_Process | Where-Object
   ParentProcessId -eq <svc pid>` twice, 20 s apart. Changing child PID = crash loop.
2. Reproduce manually: run the exact `AppParameters` command from `AppDirectory` in your
   own shell. The error prints immediately (this is the fastest step - one line).
3. Check `AppStdout`/`AppStderr` are set (add them if not: `nssm set <svc> AppStdout
   <log>` + `AppStderr` + `AppRotateFiles 1`) and read the newest rotated file.
4. Compare AppParameters against the CLI's current `--help` output. Any flag that no
   longer exists, or a `-m module` that no longer has a runner, is the bug.

**Rules:**

> 1. **NSSM AppParameters are code.** When you refactor a CLI (rename flags, change a
>    `python -m` entry point to `uvicorn module:app`, drop `--mode`), update every NSSM
>    service referencing it in the same PR. Grep: `rg "nssm" mcp-central-docs` +
>    `Get-CimInstance Win32_Service | Where-Object PathName -match "nssm"` on Goliath.
> 2. **Every NSSM service MUST configure `AppStdout` + `AppStderr`** (repo `logs/`
>    directory, `AppRotateFiles 1`). A crash-looping service with no logs is undiagnosable
>    without killing it.
> 3. **`python -m <module>` is only valid if the module has a runner.** Pure ASGI/import
>    modules must be launched with `uvicorn module:app` (via `uv run uvicorn`).
> 4. **Fleet audit (2026-08-13):** all 15 NSSM services checked. Broken + fixed:
>    `advanced-memory-mcp`, `mcp-pywinauto-mcp`. Healthy: aiwatcher-mcp, arxiv-mcp,
>    devices-mcp, fleet-agent-mcp, fleet-hub, mcp-federation-hub, LiveKitSFU, RustDeskHbbr/Hbbs,
>    `advanced-memory-mcp-daemon` (created same day). Intentionally stopped: email-mcp,
>    tvtropes-mcp.

**Variant - AppEnvironmentExtra written as one space-joined string (2026-08-13):**
`email-mcp` and `tvtropes-mcp` had been stopped for days. Root cause: their
`AppEnvironmentExtra` was a single REG_MULTI_SZ line containing all vars
space-joined (`USERPROFILE=... APPDATA=... ... MCP_PORT=10813`), likely from
`nssm set <svc> AppEnvironmentExtra "K1=V1 K2=V2"` (one quoted argument). nssm
treats each MULTI_SZ line as ONE variable - so it created a single malformed
var and **never set `MCP_PORT`**. Their `run_server.py` dual-transport entries
then fell back to stdio, which is useless under NSSM (no console), so they were
stopped. The service logs said `transport 'stdio'` even though
`nssm get <svc> AppEnvironmentExtra` *appeared* to show `MCP_PORT=10813`.

**Rules:**

> - **Set AppEnvironmentExtra one var per argument**, never one quoted string:
>   `nssm set <svc> AppEnvironmentExtra K1=V1 K2=V2 K3=V3`
> - **Verify with the registry, not `nssm get`:** `reg query
>   HKLM\SYSTEM\CurrentControlSet\Services\<svc>\Parameters /v AppEnvironmentExtra`
>   must show `\0` between entries (`K1=V1\0K2=V2`). A space-separated single line
>   = broken, rewrite it.
> - **Test the command manually with the env set** before blaming the entry point:
>   `$env:MCP_PORT=10964; uv run --directory <repo> python run_server.py` - if the
>   port comes up manually but not under the service, the service env is the bug.

---

## 20. Temporal Hallucination - the LLM has no clock

**Discovered:** 2026-08-16 (AIWatcher daily digest on the Intel Hub)

**Trap:** An LLM wrote `AIWatcher daily digest - 2025-08-26` as the subject of a
digest generated on **2026-08-16**. The chain: `DIGEST_SYSTEM` never told the
model today's date, so it fabricated a training-era date; `publish_digest_to_hub`
used the LLM subject verbatim as the hub report title. Result: the public hub
showed a report "from the future" dated 2025. Not a time machine - an LLM with no
calendar and no clock, doing what LLMs do: fluent, confident, wrong.

**Why it spreads:** any prompt that asks for a timestamped artifact (digest
subject, report title, log line, changelog entry, filename) without supplying the
real date invites a hallucinated one. The model has never seen a clock. It
interpolates from training data - which is always in the past.

**Fix pattern (two layers, both required):**
1. **Inject reality at the source:** prompts that must produce dates get the real
   date injected from code (`datetime.now(ZoneInfo(tz))`) with an explicit
   instruction - see `rules/temporal_grounding.md` and the aiwatcher fix
   (`generate_digest` pins the Vienna date in `DIGEST_SYSTEM`).
2. **Guard at the boundary:** the publisher/consumer validates any date in
   generated content against the real clock and overrides it (`publish_digest_to_hub`
   pins the title if today's date is missing). Never trust a generated date
   unverified.

**Rule (HARD):** see `rules/temporal_grounding.md` - every LLM must ground
dates/times in reality or explicitly admit it has no clock.


---

## 21. Spatial Hallucination - the LLM has no map

**Discovered:** 2026-08-16 (proposed pattern; companion to #20 Temporal Hallucination)

**Trap:** Asked "where on earth did this happen?", an LLM without a location in the
source material can *reason its way* to a confident guess. Canonical cautionary
tale (hypothetical, registered as the rule's canonical example): a hilarious
"man bites llama" article arrives with NO location; the clever LLM reasons
"llamas live mostly in the Andes, therefore this happened in Lima!" - fluent,
plausible, confident, and fabricated.

Inference-by-association is NOT grounding. "Where llamas usually live" is not
evidence of where THIS event happened. The plausible answer is the most
dangerous kind: it gets repeated with confidence and nobody double-checks it,
precisely because it "makes sense".

**Rule (HARD):** see `rules/temporal_grounding.md` Part B - locations must
come from the source text (headline, body, dateline), a verified lookup, or
explicit context; otherwise state "location not stated / unknown". This applies
to news distillation, digests, reports, and any prose generation about events.


---

## 22. NSSM services: never taskkill the child process to 'restart' the service

**Discovered:** 2026-08-16 (aiwatcher-mcp daemon restart attempt)

**Trap:** Trying to restart an NSSM-managed service by finding its listening PID and
`taskkill /F`-ing it. Two failure modes: (a) NSSM sees the exit and instantly
respawns the process - you "restarted" nothing, the new process runs the SAME old
code; (b) the kill is access-denied (service runs elevated) - silent, and you walk
away believing the daemon restarted (the port stays up with the old PID). Both
produce the classic "I restarted it, why is the old behavior still there?" loop.

**Rule (HARD):** NSSM-managed services are restarted with the service manager, never
by killing children: `sc.exe stop <svc>` + `sc.exe start <svc>` (or `nssm restart <svc>`).
The only sanctioned taskkill-by-PID is the surveillance self-heal for a HUNG service
(fleet-agent `restart_hung_service`: kill child so NSSM respawns fresh) - and even
then verify via the port/health endpoint afterwards, not by assuming.

**Verification:** after any service restart, confirm a NEW PID owns the port
(`Get-NetTCPConnection -LocalPort <port>`) and the health endpoint answers.


---

## 23. Socket exhaustion on Goliath - 28k ESTABLISHED connections, WinError 10055

**Discovered:** 2026-08-19 (yahboom-mcp verification run, evening session)

**Trap:** A single host session found **28,308 ESTABLISHED TCP connections** on the
loopback/interface - and once exhausted, Windows refuses ANY new socket bind or
connect with `OSError: [WinError 10055] An operation on a socket could not be
performed because the system lacked sufficient buffer space or because a queue
was full`. That error is indistinguishable from "the network is broken" and it
blocks every program that needs a socket - including `asyncio.run()`, roslibpy's
twisted reactor, and `pytest` collection. In the yahboom-mcp case it looked like
the test suite was broken, when the suite was fine and the HOST was out of sockets.

**Observed breakdown (PID group-by at ~23:09):**
- 14,061 connections in one python process: `robofang` (`python -m robofang.main`) - NOT NSSM-managed, NOT a service (`sc query robofang` fails), self-exited later.
- ~8 further python processes at ~1,750 connections each (empty command lines - dying or permission-hidden).
- `ESTABLISHED` total fell from 28,308 back to ~162 on its own within minutes; the holders exited and the OS reclaimed the sockets. No kill was needed.

**Root cause (honest):** unproven - the leaking processes died before any live
forensics (py-spy, /proc, CIM dump) could run. The signature - uniform ~1,750 per
process plus one 14k outlier - is consistent with an async HTTP/WebSocket client
opening a fresh connection per loop iteration without closing (task leak, or an
`httpx.AsyncClient()` constructed per-request and never awaited/closed). The
takeaway is not the specific offender; it is that a connection leak was allowed to
reach 28k without any alarm.

**Triage recipe (run this first, before blaming any app):**
```powershell
netstat -ano | Select-String -Pattern "ESTABLISHED" | ForEach-Object { ($_ -split '\s+')[-1] } | Group-Object | Sort-Object Count -Descending | Select-Object -First 12 | ForEach-Object { $p = Get-Process -Id $_.Name -ErrorAction SilentlyContinue; "$($_.Count)`t$($_.Name)`t$($p.ProcessName)" }
# Then inspect the top holder's command line / parent before killing:
Get-CimInstance Win32_Process -Filter "ProcessId=<pid>" | Select-Object CommandLine, ParentProcessId
```

**Rule (HARD):**
1. A sudden `WinError 10055` is socket exhaustion, NOT the failing app. Check
   `netstat` ESTABLISHED count first; triage the holders, then re-run.
2. Never blanket-kill python processes on socket pressure - identify each holder's
   command line and parent first. NSSM-managed services go via `sc.exe`, never taskkill.
3. `httpx.AsyncClient()` (and long-lived websockets) must be module-level singletons
   or explicitly closed - never constructed per-request inside a hot loop. Task leaks
   that never `await` the client close are the classic source of this class of bug.
4. Long-runners (including robofang, which is NOT a service and self-exits) that
   poll or stream should self-report their connection count via the long-runner
   contract so a supervisor can alarm well before 28k.

**Prevention (fleet-wide):**
- Add an ESTABLISHED-per-process watchdog to the Goliath health check (threshold
  e.g. 500/proc, 5k total) - the missing alarm is the actual failure.
- Consider raising the Windows dynamic port range once (defence-in-depth, not a fix):
  `netsh int ipv4 set dynamicport tcp start=49152 num=16384` - then verify with
  `netsh int ipv4 show dynamicport tcp`. A leak will still exhaust it.
- Audit `robofang` for a connection-leak pattern (it alone held 14k) and either
  register it as an NSSM service with a restart policy or accept that it is a
  manual, self-exiting process.


---

## 24. NSSM services installed with a wrong drive path - auto-start fails at every boot

**Discovered:** 2026-08-20 (Goliath, all 14 NSSM fleet services stopped after reboot)

**Trap:** Every NSSM fleet service had `Application`, `AppDirectory`, `AppParameters`,
`AppStdout` and `AppStderr` pointing at `C:\dev\repos\...` while the fleet actually
lives on `D:\Dev\repos\...` (the `C:\dev` path never existed). Result: the service
*is* configured `Start=Auto`, but NSSM cannot launch the app (`uv.exe`) nor open the
log files, so it returns exit 1066 and the Service Control Manager retries every 30s
forever - `aiwatcher-mcp` alone accumulated **743+ restarts**. The services appeared
"stopped" at boot with no obvious cause; they had been kept alive pre-reboot only by
manual starts, never by NSSM auto-start.

**Symptom pattern:**
- `sc query <svc>` -> `STOPPED`, `WIN32_EXIT_CODE: 1066 (0x42A)`, `SERVICE_EXIT_CODE: 4`.
- SCM events 7031 "terminated unexpectedly ... corrective action in 30000 ms: Restart"
  + 7024 "service-specific error: The system cannot open the file." - counting up by
  the hundreds.
- The REAL cause only shows in the **nssm event source** (not SCM): event 1049
  `CreateFile() failed to open <bad path>` , 1063 `Failed to rotate output file`,
  1051 `Error setting up one or more I/O filehandles. Service <svc> will not be started.`

**Diagnosis recipe (before touching anything):**
```powershell
# 1. Dump the NSSM registry config and eyeball every path:
reg query "HKLM\SYSTEM\CurrentControlSet\Services\<svc>\Parameters"
# 2. Read the NSSM event source for the exact file NSSM cannot open:
Get-WinEvent -LogName System -MaxEvents 2000 | Where-Object { $_.ProviderName -eq 'nssm' -and $_.Message -match '<svc>' }
# 3. Compare with the real repos root (Get-ChildItem D:\Dev\repos) - never assume the drive letter.
```

**Rule (HARD):**
1. Verify the NSSM registry config after ANY install/reboot with `nssm get <svc>
   AppDirectory` (or `reg query`) - never assume the paths survived or were correct.
2. `nssm set` **silently fails without elevation** (access denied, exit code swallowed
   if piped). After any `nssm set`, re-read the value from the registry and confirm it
   changed; if it did not, run the change elevated.
3. Check the `nssm` event source for path/IO failures (1049/1051/1063) - SCM's 7024
   message is too generic to diagnose.
4. Install scripts must NOT hardcode a drive letter - resolve the fleet repos root
   (e.g. `$env:FLEET_REPOS_ROOT` or `Get-Item D:\Dev\repos`) at install time.
5. After fixing configs, run a smoke start (`sc start <svc>`), watch state for 30s+
   and confirm NO new 7031/7024 events for that service before declaring it fixed.

**Prevention (fleet-wide):**
- Add an NSSM config audit to the fleet watchdog: compare each service's
  `AppDirectory` against the actual repos root; flag any `C:\dev` or stale path
  (next to the existing orphan-reaper and socket-pressure checks, both blooper #23).
- Treat "service auto-start silently failing at boot" as a first-class post-reboot
  check: after any Goliath reboot, enumerate NSSM services and verify State=Running.

---

## 24. `gh auth token` in a consoleless/server context falsely reports "not logged in" - use `gh auth status`

**Discovered:** 2026-08-27 (git-github-mcp `git_github_status` misreporting gh auth)

**Trap:** Checking gh auth with `gh auth token` when gh is logged in via the Windows
Credential Manager (keyring). `gh auth token` must **materialize** the token by unlocking the
keyring, which fails or times out when the MCP server runs from a consoleless/service context
(`CREATE_NO_WINDOW`). The subprocess then returns non-zero/empty and the tool wrongly reports
`auth: not logged in` - even though `gh auth login` on an interactive shell shows the account
is fully authenticated.

In git-github-mcp the code ran `gh auth token` (timeout 5s) while the docstring and intent
were to run `gh auth status`. Result: the status tool gaslit users into thinking they had to
`gh auth login` again.

**Rule (HARD):**
> To detect whether gh is authenticated, run `gh auth status` (reads the active account from
> `~/.config/gh/hosts.yml`, no keyring unlock), NOT `gh auth token`. Treat
> `rc == 0 && output contains "logged in"` as authenticated. Give the subprocess a generous
> timeout (10s); newer gh may perform a network token check.
>
> `gh auth token` is only appropriate when you actually need the token bytes (e.g. to pass to
> another tool), never as a boolean "is logged in" probe.

**Verification:** after the fix, `gh auth status` (with `GH_PROMPT_DISABLED=1`, `NO_COLOR=1`)
returned rc=0 with `Logged in to github.com account sandraschi (keyring)` in the consoleless
environment that `gh auth token` had failed in.

**Note:** a live MCP server keeps its already-imported code; restart the server (via its
service manager, never taskkill - see #22) to load the fix.

---

## 25. `make-mcpb.ps1` overwrites preserved prompt content on rebuild - silently destroys 3-4-100

**Discovered:** 2026-08-27 (freecad-mcp / qcad-mcp rebuild during MCP registry Phase A)

**Trap:** Running `scripts/make-mcpb.ps1` on a repo that already has real prompts. Step 4
detects and preserves existing `mcpb/assets/prompts/*` (copies to temp, restores after
re-scaffold), but step 9 **unconditionally wrote the stub templates** to
`system.md` / `user.md` / `examples.json` - overwriting the restored content. Result: a repo's
real 3-4-100 prompts (thousands of words) were silently replaced by stubs, and the rebuilt
`.mcpb` shipped as a runt. The console even printed both "Restored existing prompts" and
"Prompts: templates created" for the same run, masking the destruction.

**Rule (HARD):**
> Never let a scaffold script write default content over content it just preserved. When a
> repo's prompts already exist and are real, the build must not touch them.
>
> Generic guidance for any build/scaffold script that "preserves then regenerates": gate the
> default-content writes behind a flag that records whether real content was preserved, and
> skip the writes in that case. Do not rely on a detection check alone if a later step
> overwrites unconditionally.

**Status:** **FIXED** (2026-08-27 in `mcp-central-docs/scripts/make-mcpb.ps1`). Step 4 sets `$promptsPreserved` and Step 9 wraps stub generation in `if (-not $promptsPreserved)`. Verified: rebuild keeps existing 3-4-100 prompts intact.

**Fix (merged):** `make-mcpb.ps1` now sets `$promptsPreserved` whenever real prompts are
preserved and guards step 9's template writes with it. Verified: qcad-mcp rebuild keeps
`system.md` at 3690 words.

**Prevention (fleet-wide):** when staging MCPB bundles, prefer the `mcpb-pack.ps1` fresh-copy
pattern (wipe + recopy `src/`, copy canonical prompts, verify, pack) over re-running
`make-mcpb.ps1` on a prompt-bearing repo. Audit other build scripts for the same
"preserve-then-overwrite" shape.

---

## 26. Naked Tool Invocations on Windows (`rg`, `just`, `fd`, etc.) & Siloed Environment Registries

**Discovered:** 2026-09-10 (fleet-wide audit, arxiv-mcp exception hygiene pass)

**Trap:** Agents invoking CLI utilities like `rg`, `just`, `fd`, `ruff`, or `biome` directly as naked commands in PowerShell/subprocesses, resulting in `The term 'rg' is not recognized as a name of a cmdlet, function...` errors and wasted round-trips running ad-hoc `where.exe` or `Get-Command` lookups.

**Root Cause:**
1. **Windows Subprocess PATH Isolation:** Scoop shims (`~\scoop\shims\*.exe`), WinGet link directories (`~\AppData\Local\Microsoft\WinGet\Links\*.exe`), and local pip/uv binary paths (`~/.local/bin/*.exe`) are often absent from or unreliable in non-interactive, daemon, or child PowerShell sessions.
2. **Siloed Standards:** The full absolute paths table was historically documented only in a secondary leaf rule (`standards/rules/powershell-script-standards.md` under "Domain Read List") rather than the mandatory "Primary Read List" file that agents actually ingest on session initialization (`standards/AGENTS.md`). While `uv` was documented with "ALWAYS use full path", tools like `rg`, `just`, `fd`, `ruff`, and `biome` were omitted from §1 of `standards/AGENTS.md`.

**Status:** **FIXED** (2026-09-10). Full canonical paths table added directly to `mcp-central-docs/standards/AGENTS.md` §1 (Environment).

**Rule (HARD):**
> 1. **Never execute naked CLI tools on Windows**: Always invoke tools via their explicit, canonical absolute paths:
>    - `ripgrep (rg)`: `C:\Users\sandr\AppData\Local\Microsoft\WinGet\Links\rg.exe`
>    - `just`: `C:\Users\sandr\scoop\shims\just.exe` (or `C:\Users\sandr\.local\bin\just.exe`)
>    - `uv`: `C:\Users\sandr\.local\bin\uv.exe`
>    - `bun`: `C:\Users\sandr\.bun\bin\bun.exe`
>    - `fd`: `C:\Users\sandr\.local\bin\fd.exe`
>    - `ruff`: `C:\Users\sandr\AppData\Local\Programs\Python\Python313\Scripts\ruff.exe`
>    - `biome`: `C:\Users\sandr\.local\bin\biome.exe`
> 2. **Keep the Environment Hub Unified**: All host binary paths MUST reside in `standards/AGENTS.md` §1 (Environment). Do not bury execution paths in domain-specific leaf documents where general coding agents will miss them.

---

## 27. RTX 4090 VRAM Squatting & Unreleased Local LLM Hogs

**Discovered:** 2026-09-10 (fleet-wide local inference audit)

**Trap:** A tool, webapp, or script loads a large local model (e.g. `qwen3.8:27b`, ~18 GB VRAM) into Ollama, and either crashes or leaves it resident indefinitely (e.g. via `OLLAMA_KEEP_ALIVE=24h` or default timeout). When another repo, service, or background task needs GPU compute (vision, 3D rendering, video generation, another local model), it encounters CUDA Out Of Memory (OOM) or silently spills into DDR5 system RAM at single-digit tok/s.

**Root Cause:**
Ollama keeps loaded models in VRAM according to `keep_alive`. When multiple MCP servers or ad-hoc scripts interact with Ollama independently without coordination, crashed or idle tasks leave their weights squatting. Ollama does not automatically preempt a loaded model if incoming memory requirements exceed remaining headroom without a fresh model request targeting the same slot.

**Rule (HARD):**
> 1. **Probe Before Loading (`GET /api/ps`)**: Every service or tool initiating local inference MUST probe `http://localhost:11434/api/ps` first to inspect resident models and calculate VRAM headroom.
> 2. **Evict Squatters with `keep_alive: 0`**: If an unneeded model is squatting in VRAM, do not blindly queue requests. Kick the hog out via the Ollama generate endpoint:
>    ```bash
>    curl http://localhost:11434/api/generate -d '{"model": "<squatting-model>", "keep_alive": 0}'
>    ```
>    In UI/interactive flows, prompt the user or offer an explicit "Evict Other Models / Free VRAM" CTA. In automated backend pipelines, use the canonical lifecycle manager (`switch_ollama_model(keep)` from `mcp-central-docs/templates/llm/llm_engine.py`).
> 3. **Release Upon Completion**: Batch or one-off tasks MUST set `"keep_alive": 0` (or a short timeout like `"5m"`) on their final request so the 4090 is returned clean to the pool.

---

## 28. Local Fix Abandonment — Verified Locally in Dev, Uncommitted & Unpushed to Remote

**Discovered:** 2026-09-10 (fleet-wide sweep; arxiv-mcp / central docs dirty working trees accumulated across sessions)

**Trap:** A developer or AI agent diagnoses an issue in a repository, modifies code, tests it locally (e.g. runs `start.bat` or `just dev`), verifies that it works like a dream, and immediately hops to another repo or task. The working tree is left dirty, uncommitted, and unpushed.

**Consequences:**
1. **Broken Clones & Poisoned Upstream:** Anyone cloning the repo or pulling from `origin/main` (including automated CI, CUA runners, or another development workstation) receives the old, broken code.
2. **Stale Releases & NSIS Installers:** Build packaging scripts (`make-mcpb.ps1`, `build-native`, NSIS installers) pack either uncommitted dirty files or build from the last clean commit tag, distributing broken binaries to end users.
3. **Ghost Fixes & Context Loss:** Weeks later, an agent or developer revisits the repo, sees dirty unstaged files or forgotten stashes, assumes they are half-baked experiments or dross, and runs `git restore` or overwrites them—destroying the verified fix.
4. **Fleet Rottenness Cascade:** The cycle repeats across dozens of repos until a huge pile of uncommitted "WIP" accumulates across the disk, making global git status checks terrifying and hazardous.

**Rule (HARD):**
> 1. **"A Fix Does Not Exist Until It Is Pushed":** Local verification is only step 1. No task, ticket, or prompt is finished until changes are committed in logical conventional batches, verified against CI gates, and pushed to `origin/main`.
> 2. **Never Hop Repos With Dirty Trees:** Before switching contexts or starting work on another repo, the current repo MUST be clean (`git status` reports `nothing to commit, working tree clean` and `Your branch is up to date with 'origin/main'`).
> 3. **Batch Logically, Do Not Dump:** Do not make blind `git commit -am "wip"` dumps. Separate backend logic, frontend UI, packaging/metadata, and docs into discrete commits.
> 4. **Release When Applicable:** If the repo produces `.mcpb` bundles or NSIS installers, bump version, pack, tag, and publish the GitHub release—do not leave the release artifact stranded on Goliath.

---

## 29. NSSM Service Wrapper Bloat on Windows & SCM Restart Race Conditions

**Discovered:** 2026-09-10 (fleet-wide RAM audit & NSSM service recovery post-reboot)

**Trap:**
1. **Windows Lacks POSIX `execve`:** When NSSM services are configured to launch Python servers via wrappers like `uv.exe run` or `powershell.exe -File wrapper.ps1`, Windows cannot replace the parent process image in memory. The wrapper (`uv.exe` consuming ~25–45 MB or `powershell.exe`/`pwsh.exe` consuming ~50–75 MB) remains frozen in RAM doing nothing except waiting for Python to terminate. Across 16 fleet services, this idle wrapper bloat squandered over **600 MB of RAM** and spawned dozens of unnecessary processes (`mcp-federation-hub` alone accumulated 25 child processes and 590 MB).
2. **SCM Restart Race Condition:** When restarting a Windows service programmatically (e.g. `sc stop <svc>` followed by `sc start <svc>`), Python/FastAPI/Uvicorn processes take 1–2 seconds to gracefully drain HTTP sockets and shut down. Issuing `sc start` prematurely (e.g. 400ms later) fails with `An instance of the service is already running` or SCM rejection. The service then completes its shutdown and stays permanently dead in the `STOPPED` state.
3. **Session 0 UAC Rejection:** Calling `Start-Process -Verb RunAs` from non-interactive background agent workers fails immediately with `The request is not supported` (`ERROR_NOT_SUPPORTED`) because Windows security prohibits Session 0 / headless sessions from spawning interactive GUI elevation prompts (`consent.exe`) on the user's active desktop.

**Rule (HARD):**
> 1. **Direct Venv Executables in NSSM:** Never configure NSSM `Application` to run `uv.exe run` or `powershell.exe`. Configure NSSM to directly invoke `<repo>\.venv\Scripts\python.exe` or `<repo>\.venv\Scripts\uvicorn.exe`. Supply environment variables (`VIRTUAL_ENV`, path overrides) via NSSM's `AppEnvironmentExtra` multi-string registry parameter.
> 2. **Always Poll for `Stopped` on Restart:** Any script or automation cycling Windows services must loop and poll until `(Get-Service <svc>).Status -eq 'Stopped'` before issuing `sc start` or `Start-Service`.
> 3. **Pre-grant User DACL:** Use `sc.exe sdset <svc> <SDDL>` to grant the interactive user account (`sandr`) service control rights so maintenance scripts and dev tools do not require elevated administrator tokens to query, stop, or restart fleet services.
> 4. **Configure SCM Failure Recovery:** Every service MUST have persistent Windows Service Control Manager failure actions (`sc.exe failure <svc> reset= 86400 actions= restart/5000/restart/10000/restart/30000`) and `StartType=Automatic` to ensure 100% unattended recovery across crashes and OS reboots.

---

## 30. Private Monorepo Dependency Trap & Standalone Independence on Naked PCs

**Discovered:** 2026-09-11 (calibre-mcp launch failure & fleet-wide start script audit)

**Trap:**
1. **Private Monorepo Dependency (`mcp-central-docs`):** Public / spoke repositories requiring private fleet infrastructure (such as `D:\Dev\repos\mcp-central-docs`) at runtime. When an external open-source user clones the repository on a fresh/naked PC where `mcp-central-docs` cannot exist (because it is private), launching fails instantly with `Missing central fleet engine` or `File not found`.
2. **Hardcoded Machine Paths in Configs:** Hardcoding absolute paths like `WebRoot = 'D:\Dev\repos\<repo>\webapp'` or `PythonPath = 'D:\Dev\repos\<repo>\...'` inside `fleet-start.config.ps1`. When cloned to another path, another drive, or a different PC, the paths fail immediately with `Cannot find path`.
3. **Double-Nesting Subprocess CWD:** Passing an unresolved relative directory both as `-WorkingDirectory` in `Start-Process` and inside `Set-Location` in an inline script block (`$cmd = "Set-Location '$workDir'; ..."`), causing PowerShell to resolve the relative path *against* the already-changed working directory, producing doubled paths like `webapp\backend\webapp\backend` (`PathNotFoundException`).
4. **Premature ConPTY Pipe Teardown (`0x800700e8` / `ERROR_NO_DATA`):** On Windows 11 with Windows Terminal (`wt.exe` / OpenConsole), launching detached child processes with `cmd.exe /c` or `powershell.exe` without `-NoExit`. When an error occurs on line 1, the instantaneous termination of the child console tears down the pseudo-console pipe (`ConPTY`) before Windows Terminal can attach stdout/stderr, resulting in the modal popup `[error 2147942632 (0x800700e8) when launching ...]`.

**Rule (HARD):**
> 1. **Bi-Modal Standalone Fallback in `start.ps1`:** Every `start.ps1` must implement a bi-modal architecture:
>    - **Mode 1 (Fleet Central):** If `mcp-central-docs\scripts\Invoke-FleetWebappStart.ps1` exists on the host machine, delegate to it for fleet orchestration, port conflict resolution, and telemetry.
>    - **Mode 2 (Autonomous Standalone):** If `mcp-central-docs` is missing (naked PC or public clone), seamlessly fall back to an autonomous local runner that starts the backend (`uv run uvicorn` or module runner) and frontend (`cmd.exe /k npm run dev`), then opens the default browser to `http://127.0.0.1:<FrontendPort>/`.
> 2. **Relative Paths Only in `fleet-start.config.ps1`:** Every path field (`WebRoot`, `WorkDir`, `PythonPath`, `UvProject`) in `fleet-start.config.ps1` MUST be strictly relative to the repository root (e.g. `'webapp\frontend'`, `'webapp\backend'`, `'src'`, `'.'`), never hardcoded to `D:\Dev\repos\...` or developer workstations.
> 3. **Always Resolve Paths to Absolute Before Emitting Commands:** In any launcher, resolve all relative paths against `$RepoRoot` to absolute strings (`(Resolve-Path ...).Path`) before interpolating into inline `Set-Location` commands or `-WorkingDirectory` parameters.
> 4. **Use `/k` and `-NoExit` for Interactive Dev Launches:** Detached interactive terminal consoles must always be launched with `cmd.exe /k` or `powershell.exe -NoExit` (switching to `/c` only when `$env:FLEET_PROBE_RUN -eq '1'` or `-Headless`).
> 5. **Self-Contained Installation (`INSTALL.md` & `justfile`):** `INSTALL.md` must document standalone cloning, winget dependency acquisition (`Astral.uv`, `OpenJS.NodeJS.LTS`, `Casey.Just`), and running without `mcd`. Central-only audit recipes in `justfile` must be guarded with `if (Test-Path ...)` so standard local recipes never crash.

## 31. `fleet-start.config.ps1` declares `Backend.Kind = 'module-serve'` for a module whose CLI has no `--serve` flag

**Discovered:** 2026-09-11 (plex-mcp: user hit `usage: __main__.py ... error: unrecognized arguments: --serve` trying to start the dev webapp)

**Trap:** `Invoke-FleetWebappStart.ps1` (and the standalone fallback in `webapp/start.ps1`) runs `python -m <Backend.Module> <Backend.ServeArgs>`, defaulting `ServeArgs` to `--serve` when `Backend.Kind = 'module-serve'`. The vendored `templates/transport.py` CLI (`create_argument_parser`) only defines `--stdio` / `--http` / `--sse` / `--host` / `--port` / `--path` / `--debug` — **no `--serve` flag exists anywhere in the template**. Any repo that copies this template unmodified and is then configured as `module-serve` gets a backend that crashes on the very first launch attempt with `unrecognized arguments: --serve`, and — critically — this can mask a **second, worse** bug: some of these repos (e.g. plex-mcp, leanforge-mcp) actually have a *separate*, fully-working FastAPI/uvicorn webapp backend under `webapp/backend/app/...` that has nothing to do with the MCP module's own stdio/http CLI. `module-serve` was pointing the launcher at the wrong program entirely — the real webapp backend was never being started by `start.ps1` at all.

**Fleet-wide scope (sampled, not exhaustive):** 43 repos declare `Kind = 'module-serve'` in `fleet-start.config.ps1`. Of a 38-repo sample checked for an actual `--serve` flag in `src/`, only 5 (`browser-mcp`, `colony-mcp`, `giskard-mcp`, `streamfog-mcp`, `vfx-mcp`) implement one — the other 33+ do not and are presumed broken the same way. `leanforge-mcp` is a second confirmed case (like plex-mcp) of a real `webapp/backend/*/main.py` FastAPI app being bypassed by an incorrect `module-serve` config pointing at the MCP module's own CLI instead. **Not yet swept or fixed fleet-wide** — each repo needs a case-by-case call: does it have its own separate webapp/backend (→ fix the config to `Kind = 'uvicorn-web-app'` + `WorkDir`/`UvicornTarget`, matching the plex-mcp fix), or is the MCP module meant to serve everything itself (→ either give its CLI a real `--serve`/`--http` alias, or set `Backend.ServeArgs` in its own config to a flag the CLI already supports).

**Rule (HARD):**
> 1. Before setting `Backend.Kind = 'module-serve'` (or `cli-serve`) in `fleet-start.config.ps1`, verify the target module's CLI actually accepts the resulting arguments: `uv run python -m <Module> --serve` (or your `ServeArgs`) must not error with `unrecognized arguments`.
> 2. If the repo has its own `webapp/backend/**/main.py` FastAPI/Starlette app, that is almost always the correct target — use `Kind = 'uvicorn-web-app'` with `UvicornTarget` (e.g. `'app.main:app'`) and `WorkDir` set to that backend's directory, not `module-serve` pointing at the MCP server's own transport CLI.
> 3. Never assume a `fleet-start.config.ps1` works because it was copied from another repo's template — always launch it once (`just serve` / `start.ps1`) and confirm the backend port actually binds and `/health` responds, before considering a fresh scaffold done.

---

## 32. Agent shell `Restart-Service` on NSSM MCP daemons without elevation - useless retry loop

**Discovered:** 2026-09-12 (memops `Repository.update` fix: agent retried daemon restart from Cursor shell, then retried MCP edits, without reloading code)

**Trap:** Cursor/agent PowerShell runs under a **UAC-filtered admin token** (same class of problem as [§9 `schtasks`](#9-schtasks-fails-silently-from-a-uac-filtered-powershell-token---winops_auto_task_create-doesnt)). `Restart-Service advanced-memory-mcp-daemon` (or `nssm restart`) from that shell may **exit 0**, show **Running**, and leave the **same process / same code** in memory — or fail opaquely. The agent then retries `Restart-Service`, retries the failing MCP `edit`, tweaks unrelated code, and burns turns in a **useless loop** because the hypothesis space never includes "restart never actually happened."

**LLM failure mode:** models treat "I ran restart" as ground truth. Without an explicit fleet rule, they do not ask: *did SCM accept a stop/start, did PID change, did health reflect new behavior?*

**Rule (HARD):**
> 1. **NSSM / Windows service restart on Goliath** (fleet MCP HTTP daemons: `advanced-memory-mcp-daemon`, `aiwatcher-mcp`, etc.): use **elevated** PowerShell. Sandra allows UAC — `Start-Process powershell -Verb RunAs -Wait -ArgumentList '-NoProfile','-Command','Restart-Service <name> -Force'`.
> 2. **Never retry the same non-elevated restart** more than once. After one attempt, either elevate or use `winops_svc_restart` (winops MCP) if available.
> 3. **Verify, don't assume:** after restart, confirm **new PID** on the daemon port (`Get-NetTCPConnection -LocalPort <port>`) and a **behavioral** check (e.g. PATCH edit returns entity JSON, not `EntityResponse` / `input_value=None`).
> 4. **Read-only from agent shell is fine:** `Get-Service`, `/health`, MCP probe — no elevation.

**Related:** [§22 NSSM taskkill](#22-nssm-services-never-taskkill-the-child-process-to-restart-the-service), [§29 NSSM wrapper bloat](#29-nssm-service-wrapper-bloat-on-windows--scm-restart-race-conditions), `scripts/Start-MemopsDaemon.ps1`, `operations/VIBE_OPERATIONS.md` (when present).

---

## 33. `safety_override` flag that returns `BYPASSED` - policy ban magnet and design smell

**Discovered:** 2026-09-12 (database-operations-mcp `agentic_workflow_tool`, Meta contributor 2-day hold)

**Trap:** An agentic tool exposes `safety_override: bool = False` and returns `"safety_guard": "STANDBY" if not safety_override else "BYPASSED"`, with a docstring like "bypasses standard safety guardrails". Pasted into a hosted model alongside raw SQL examples (`DROP TABLE`, `DELETE FROM`) and an autonomous loop (`max_steps=5`, `ctx.sample()`), the classifier reads it as an agent built to evade guardrails. One block is normal. Retrying the same big paste in opencode turns it into "repeated violations" and a temp hold - in this case about 2 days on the contributor tier.

**Rule (HARD):**
> 1. Never ship `safety_override`, `bypass_safety`, `disable_guardrails`, or any bool that turns guardrails off. Safety is always-on. See `TOOL_DESIGN_STANDARDS.md` Sec 5.
> 2. Use `confirm=True`, `dry_run` / preview, read-only-by-default, and allowlists for writes instead of a bypass switch.
> 3. Do not inline injection payloads (`DROP TABLE users--`, `OR 1=1`, `union select`) in prompts. Reference the file path instead.
> 4. On one policy block, stop and shrink context to one file / one function. Never retry the same paste verbatim in a loop.

**Fix pattern:**
```python
# WRONG - ban magnet
async def agentic_workflow_tool(goal: str, safety_override: bool = False):
    return {"safety_guard": "STANDBY" if not safety_override else "BYPASSED"}

# CORRECT - always-on guard, explicit confirm
async def agentic_workflow_tool(goal: str, confirm: bool = False, dry_run: bool = True):
    return {"safety_guard": "ENFORCED", "confirm_required": True}
```

**Fleet sweep:** grep for `safety_override`, `bypass_safety`, `disable_guardrails`, `BYPASSED` across `D:\Dev\repos`. database-operations-mcp had hits in `src/.../tools/agentic_tools.py`, `mcpb/src`, `native/resources`, plus docs. Remove the flag, keep the guard enforced.

---

## 34. Canonical `pack.ps1.template` trusted names/paths without filesystem validation - bugs shipped fleet-wide via `sweep.ps1`

**Discovered:** 2026-09-14 (bookmarks-mcp mcpb pack, first real run against a repo where the pyproject.toml `name` doesn't match the `src/` package directory)

**Trap:** The fleet-canonical MCPB pack script (`mcp-central-docs/_scratch_mcpb_fix/pack.ps1.template`, distributed to repos missing one via `sweep.ps1`) had three bugs, none repo-specific — every repo that received the template via the sweep inherits the same exposure:
1. Package-name detection trusted `pyproject.toml`'s `name` field (distribution name, e.g. `bookmarks-mcp`) as the importable package directory under `src/` without checking it exists — broke immediately on any repo where the two diverge (real package: `browser_bookmarks_tools`).
2. Entry-point path resolved against `$RepoRoot` instead of `$McpbDir` — wrong per `MCPB_PACKAGING_STANDARDS.md` §2.5 (manifest.json describes the *bundle*, not the repo). This "worked" in initial testing only because a coincidentally same-named file also existed at the repo root for an unrelated build target, masking the bug until that coincidence wasn't present.
3. Output `.mcpb` filename used the detected source package name instead of `manifest.json`'s own `name` — could silently name the artifact after an internal implementation detail instead of the bundle's actual public name.

A required §2.5 check (launch the packaged entry point in a clean unpack) was also **missing entirely** from the template. The first implementation of that check used `Start-Process -FilePath uv -ArgumentList @('run','python',...)`; confirmed empirically (via `netstat`/`Get-Process` polling *after* the script had already reported success and exited) that `uv run` spawns Python as a **child** of the `uv.exe` wrapper process on Windows rather than exec-replacing it — so `Stop-Process` on the tracked PID killed the wrapper and left a live orphaned server bound to the probe port.

**Rule (HARD):**
> 1. Any fleet template/script that derives a name, path, or identifier from one source of truth (a config field, a convention, a guess) MUST validate that derivation against the actual filesystem before using it downstream — a plausible guess is not a verified fact.
> 2. A path in a bundle-describing file (`manifest.json`) resolves relative to the bundle root, never the repo root, even if a same-named file existing at the repo root makes the bug invisible in casual testing.
> 3. Never `Stop-Process` on a PID obtained from `uv run` (or any wrapper-executable launch) on Windows — resolve and launch the real target binary (e.g. `.venv\Scripts\python.exe`) directly for anything you intend to later kill by PID.
> 4. Fixed in `pack.ps1.template`/`verify_pack.py` 2026-09-14: 3-tier package-name detection (hatch config → filesystem-validated name-guess → single-src-dir fallback), bundle-root-relative entry-point resolution with dual-style detection (dotted-module vs. standalone script), manifest-name-based output filename, added Step 10 launch check using the venv python directly, plus fail-fast validation of `manifest.name`/`manifest.version`/`bunx`-on-PATH. Full writeup: `MCPB_PACKAGING_STANDARDS.md` §2.5 "Package-name / entry-point / output-filename bugs in the fleet template".

**Fleet exposure - audited and fixed 2026-09-14.** A read-only scan (`_scratch_mcpb_fix/scan_stale_pack_templates.ps1`) found 157 of 158 repos with an `mcpb/pack.ps1` on the stale pre-fix template - essentially the entire fleet, confirming `sweep.ps1` had distributed the buggy pre-fix template as-is (it explicitly declines entry-point/console-script correctness, "those need per-repo understanding... out of scope"). A mutating companion (`_scratch_mcpb_fix/apply_pack_template_fix.ps1`) applied the fix in batches of 10, backing up previous files to a location OUTSIDE any repo's `mcpb/` (see next finding), committing 2 files per repo, never pushing. Result: **124 repos fixed and committed**, 22 skipped untouched (pre-existing unrelated staged changes already in that repo's index - see the `git commit`-commits-the-whole-index note below), 9 blocked by a repo-local `.gitignore` blanket-excluding all of `mcpb/` (contradicts the standard - only `mcpb/src` should be ignored; content IS correct on disk, just untracked, needs a per-repo decision not a mechanical fix), 2 blocked by pre-existing unrelated repo issues (`tvtropes-mcp`: that repo's own `mypy` pre-commit hook is broken and fails on any commit, not just this one; `aiwatcher-mcp`: ~40 unrelated files already modified/staged from other WIP).

**Two more real bugs found live during the rollout, both fixed in the template before repos 11+ were processed:**
1. **A backup file dropped inside `mcpb/` breaks the very check it's supposed to protect against.** The apply script's first version wrote `.bak` backups next to `pack.ps1` itself (Batch Mutation Safety compliance) - but `verify_pack.py`'s pollution check (correctly) treats any `*.bak` under `mcpb/` as fatal, since it must never ship in a real bundle. Caught immediately via a real end-to-end `mcpb pack` run against `arxiv-mcp` (not just a mechanical diff check) - Step 6 failed on the script's own freshly-written backup. Fixed: backups now live in a centralized directory outside every repo's `mcpb/` (`_scratch_mcpb_fix/backups/<repo>/`).
2. **`verify_pack.py`'s intentional `print()` CLI output collides with ruff's `T201` (flake8-print) rule in repos whose config opts into the `T20` category without an `mcpb/`-specific `per-file-ignores` entry.** Confirmed by diffing `mujoco-mcp`'s ruff `select` list (includes `"T20"`) against `bookmarks-mcp`'s (doesn't) - real per-repo config variance, not a one-off. `verify_pack.py` is a CLI script; printing its own pass/fail result IS the intended behavior, not debug output left in application code - the right fix is a file-level `# ruff: noqa: T201` in the template itself (added directly after the module docstring), not touching each repo's ruff config.

**`git commit` with no pathspec commits the WHOLE index, not just files this script explicitly `git add`ed.** A repo with pre-existing staged changes would silently bundle that unrelated content into the fix commit. Found live on `aiwatcher-mcp` before a guard existed; the guard (check `git diff --cached --name-only` is empty before touching anything, skip the whole repo if not) was added and used for the remaining 147-repo rollout, producing the 22 clean `skipped-dirty-index` repos above with zero risk of accidental bundling.

**Related:** [§2.5 in MCPB_PACKAGING_STANDARDS.md](../standards/MCPB_PACKAGING_STANDARDS.md), `_scratch_mcpb_fix/sweep.ps1`, `_scratch_mcpb_fix/scan_stale_pack_templates.ps1`, `_scratch_mcpb_fix/apply_pack_template_fix.ps1`.

## 35. `Join-Path $PSScriptRoot ".." ".."` - 3-positional-arg Join-Path crashes on Windows PowerShell 5.1, shipped fleet-wide via one template

**Discovered:** 2026-09-17 (teleoperator-mcp nsis-build run, `scripts\just\cua-nsis-test.ps1` line 4)

**Trap:** `Join-Path` only accepts **two** positional path arguments (`-Path`, `-ChildPath`) on Windows PowerShell 5.1 (`powershell.exe`) - `-AdditionalChildPath`, which lets you pass a third/fourth segment, is PowerShell 6+ (`pwsh`) only. Code written and tested under `pwsh` 7 works fine and then throws on any machine/CI step that runs the bare `powershell.exe` 5.1 that ships with Windows:

```
Join-Path : A positional parameter cannot be found that accepts argument '..'.
```

This one wasn't a one-off typo - it shipped in the fleet-canonical `cua-webapp-test.ps1` / `cua-nsis-test.ps1` template (`mcp-central-docs/templates/tauri-native/scripts/just/`) and was inherited byte-identical by every repo scaffolded from it. A fleet grep on 2026-09-17 found **391 occurrences across ~195 repos** - one bug, one bad line, copy-pasted 391 times because nothing checked for it and nothing ran the actual 5.1 interpreter before shipping the template.

**Rule (HARD):**
> 1. Never call `Join-Path` with more than two positional path segments. To join 3+ segments, either combine the extra segments into a single relative-path string (`Join-Path $PSScriptRoot "..\.."`), or nest calls (`Join-Path (Join-Path $a $b) $c`) - both work identically on PS 5.1 and PS 7.
> 2. Any `.ps1` intended to run fleet-wide (justfiles, `start.ps1`, CUA test scripts, any script invoked as `powershell.exe -File ...` rather than explicitly via `pwsh`) MUST be smoke-tested under `powershell.exe` (5.1), not just `pwsh` (7+) - a script that only ever ran under `pwsh` during authoring will look correct and still be broken for every naked-PC / CI runner that shells out to the OS-default `powershell.exe`.
> 3. Before writing ANY multi-segment path-join, path-parsing, or similarly "obviously simple" PowerShell one-liner, do a 10-second sanity check against PS 5.1 semantics (or just default to the two-args-max / nested-call form above) rather than assuming pwsh-7 syntax is universal. This class of error (simple path/string plumbing broken by a version-specific cmdlet signature) has now recurred independently roughly 20 times across unrelated fleet sessions - it is not a hard problem, it is a checklist item being skipped.
> 4. Fixed 2026-09-17 in both canonical templates (`mcp-central-docs/templates/tauri-native/scripts/just/cua-webapp-test.ps1` and `cua-nsis-test.ps1`) plus a validated 5-file sample batch (`moltbot-mcp`, `arxiv-mcp`, `mixx-dj-mcp`, this repo's worktree copy). **384 files across ~192 repos remain unfixed** as of this writing - full hit list was too large to inline; re-run the grep below to regenerate it and finish the sweep (batches of 5 + `.bak` per Batch Mutation Safety).

**Detection (re-run any time to check current fleet exposure):**
```powershell
rg -n 'Join-Path\s+\$PSScriptRoot\s+"\.\."\s+"\.\."' D:\Dev\repos --type ps1
```

**Related:** [POWERSHELL_STANDARDS.md](../standards/POWERSHELL_STANDARDS.md), [powershell-script-standards.md](rules/powershell-script-standards.md), `TAURI_PRODUCTION_PITFALLS.md`.

## 36. "Kill it, sleep N seconds, assume it's dead" / "Start it, sleep N seconds, assume it's up" - a named antipattern, found in 29 fleet scripts

**This is the general form of the specific bug below.** Any script that does `Stop-Process ...` (or `taskkill`) followed by a fixed `Start-Sleep -Seconds N` with no follow-up check that the process/port is actually gone, OR `Start-Process ...` followed by a fixed sleep with no follow-up check that the thing actually came up (port open, health endpoint responds, log line seen) - is gambling the correctness of everything downstream on a guess about machine speed that day. It reads as a safety measure ("we waited!") while providing none. A 2026-09-17 fleet grep for this shape (`Stop-Process` or `Start-Process` followed within a couple lines by a bare `Start-Sleep -Seconds`, no polling loop after) found **29 files** across the fleet outside the two already fixed in `teleoperator-mcp/native/build.ps1` (below) - not yet audited/fixed as of this writing:
`japanophile-mcp/scripts/nsis-smoke.ps1`, `calibre-mcp/scripts/restart_claude_and_check_mcp.ps1`, `calibre-mcp/scripts/restart_claude_and_check.ps1`, `gimp-mcp/start.ps1`, `alexa-mcp/start.ps1`, `mcp-central-docs/scripts/fleet-rebuild-tauri-installers.ps1`, `teleoperator-mcp/scripts/restart-backend.ps1`, `virtualization-mcp/scripts/Launch-DevInfraSandbox.ps1`, `virtualization-mcp/scripts/Launch-ConsumerSandbox.ps1`, `overte-mcp/scripts/bridge-stress-test.ps1`, `sdr-mcp/scripts/docker-daemon-poll.ps1`, `robotics-mcp/scripts/stop-watchfiles.ps1`, `pywinauto-mcp/native/build.ps1`, `inkscape-mcp/native/build.ps1`, `devices-mcp/native/build.ps1`, `mixxxxx/scripts/build-installer.ps1`, `godot-mcp/webapp/start.ps1`, `worldlabs-mcp/competition/start.ps1`, `robotics-mcp/scripts/start-normal.ps1`, `robotics-mcp/scripts/run-with-watchfiles.ps1`, `fastsearch-mcp/scripts/rebuild_and_restart_service.ps1`, `fastsearch-mcp/scripts/stop_service_admin.ps1`, `plex-mcp/scripts/restart_claude_and_check_mcp.ps1` (plus a few in `_junk/`/`annoyinator/`, out of scope per the fleet workspace CLAUDE.md). This list is a starting point (heuristic grep, not exhaustive) - re-run the detection command below before auditing, don't trust this snapshot as still-accurate.

**Rule (HARD):** never pair a mutating action (kill a process, start a process, free a port) with a fixed sleep as the only verification. Always poll the actual condition you care about (port closed/open, `HasExited`, health check, log line) up to a real timeout, and fail loudly (throw / non-zero exit) if the condition never becomes true - don't silently proceed on a timeout as if it succeeded.

**Detection (heuristic, re-run to refresh the list above):**
```powershell
rg -U -P 'Stop-Process[^\n]*\n(\s*\}[^\n]*\n)?\s*Start-Sleep -Seconds \d' D:\Dev\repos --type ps1 -l
rg -U -P 'Start-Process[^\n]*\n(\s*\}[^\n]*\n)?\s*Start-Sleep -Seconds \d' D:\Dev\repos --type ps1 -l
```

---

## 36a. NSIS smoke-test gate's fixed 5s sleep races PyInstaller onefile cold-start - broken backend shipped into a signed installer despite a "PASSED" gate

**Discovered:** 2026-09-17 (teleoperator-mcp, same session as #35 - the `Join-Path` fix above was already correctly applied to `teleoperator-mcp-backend.spec`, yet the installer built minutes later still crashed with the exact `PIL._imaging` ImportError the fix should have caught)

**Trap:** `native/build.ps1` Step 2 smoke-tests the freshly frozen PyInstaller backend before embedding it into the Tauri/NSIS bundle - `Start-Process` it, `Start-Sleep -Seconds 5`, check `$testProc.HasExited` once, then unconditionally `Kill()` it. This looks like a real gate but has a race condition: PyInstaller **onefile** cold-start (extracting the ~50MB archive to a fresh `_MEI...` temp dir, plus Windows Defender real-time-scanning every newly-written `.pyd`/`.dll` in that dir) can easily exceed 5 seconds before the Python interpreter even reaches the import line that crashes. Sequence that actually happened:
1. t=0: process started, still extracting/scanning.
2. t=5s: `HasExited` checked - **still false**, because it hasn't gotten far enough to crash yet. Gate reads this as healthy.
3. `Kill()` fires immediately - process terminated before it ever reached the crashing `from PIL import Image` line.
4. Step 3 (`Copy-Item` into `native/resources/`) and Step 4 (Tauri NSIS bundle) proceed with a backend that was never actually validated - a "PASSED" smoke test that tested nothing.
5. The signed installer ships. Running the *installed* app (not the dev backend, which has more headroom and different AV-scan state) hits the real crash: `ImportError: cannot import name '_imaging' from 'PIL'`.

Confirmed empirically: a manual PyInstaller rebuild run minutes later (with more elapsed wall-clock time before the exe got inspected) started clean with no crash - proving the underlying fix (PIL kept out of the binary-strip `SKIP` list, see #35's sibling issue in the same spec file) was correct all along. The gate, not the fix, was the actual defect. `native/resources/teleoperator-mcp-backend.exe` (what Tauri actually embeds) and `dist/teleoperator-mcp-backend.exe` (the freshly-built one) had **different checksums** despite both nominally being "the latest build" - the resources copy was frozen at the moment the broken smoke-tested build was copied in.

**Rule (HARD):**
> 1. A build gate that only checks "hasn't crashed yet after N fixed seconds" is not a smoke test - it's a race condition with a pass/fail outcome that depends on machine speed, disk cache state, and AV scanner load that day. Any process-launch smoke test MUST either (a) poll `HasExited` in a loop up to a real timeout (15-30s, not a single fixed sleep) so a crash occurring at any point in that window is caught, AND (b) positively confirm the thing under test actually works (e.g. the server's port is open / an HTTP health check responds) rather than inferring health from "didn't crash yet" - a process that's merely still alive but never came up (hung, deadlocked, stuck extracting) is a silent false-pass under the old logic.
> 2. Fixed 2026-09-17 in `teleoperator-mcp/native/build.ps1`: replaced the fixed `Start-Sleep -Seconds 5` + single `HasExited` check with a poll loop (`$maxWaitSec = 30`, 500ms ticks) that breaks early on either a confirmed port-open (`Test-NetConnection -Port $testPort -InformationLevel Quiet`) or a detected exit, and throws distinct errors for "crashed" vs. "never came up in time" - both previously indistinguishable false-passes.
> 3. Audit any other fleet `build.ps1`/`nsis-build`-style script with a PyInstaller-onefile smoke-test step for the same fixed-sleep-then-single-check pattern - it's a generic race, not specific to this repo or to Pillow.
> 4. When a "PASSED" gate and a real-world crash disagree, don't just re-fix the thing the crash report blames (here: PIL packaging, which was already fixed) - verify whether the gate that was supposed to catch it actually ran with enough headroom to do so. Two different builds of the "same" artifact having different checksums when only one was supposed to exist is the tell.

**Related:** [#35 above](#35-join-path-pscriptroot------3-positional-arg-join-path-crashes-on-windows-powershell-51-shipped-fleet-wide-via-one-template), `teleoperator-mcp/native/build.ps1`, `TAURI_PRODUCTION_PITFALLS.md`.

## 37. `Set-Location` on its own line has no effect on later recipe lines - `just` runs each line as a separate process - 186 broken recipes across 81 repos, shipped from one template line

**Discovered:** 2026-09-18 (kicad-mcp, during a manual NSIS build-queue run - `just build-native` failed with `.\build.ps1 : The term '.\build.ps1' is not recognized...` despite the file existing exactly where expected)

**Trap:** `just` on Windows is configured fleet-wide with `windows-shell := ["powershell.exe", "-NoProfile", "-Command"]`. This makes `just` spawn a **brand-new `powershell.exe` process for every line** of a recipe body - not one continuous session for the whole recipe, the way an ordinary `.ps1` script or an interactive shell would behave. Any state set on one line - `Set-Location` (working directory), `$env:X = ...` (environment variables) - is local to that one throwaway process and is gone before the next line's process starts. The next line runs from wherever `just` itself was originally invoked (usually repo root), not the directory the recipe *thinks* it changed into.

Two very different failure shapes came out of this:
1. **Loud:** `Set-Location native\` followed by `.\build.ps1` on the next line - PowerShell can't find `build.ps1` relative to repo root, throws `is not recognized as the name of a cmdlet, function, script file, or operable program`. Annoying but immediately visible.
2. **Silent:** `Set-Location webapp` followed by `npm install` on the next line - `npm install` doesn't reference a path, it just reads whatever `package.json` is in the current directory. It runs in the wrong directory with **no error at all** - either failing confusingly (no `package.json` at repo root) or, worse, silently doing nothing useful. Same root cause, much harder to notice.

**Root cause traced to one template, not 81 individual mistakes:** the actual source was `mcp-central-docs/scripts/scaffold-tauri.ps1` line 335 - the script that bolts Tauri support onto a repo, which unconditionally appends a `build-native` recipe the first time it runs on a repo (idempotent - skips repos that already have one). Whoever wrote that generator assumed a `just` recipe behaves like a normal multi-line script. That one wrong assumption, encoded once in a generator, got mechanically stamped into every repo that ever ran the Tauri scaffolder - the same propagation shape as #35 above (`Join-Path` 3-arg bug) and the `uv run pyinstaller` anti-pattern in `TAURI_PRODUCTION_PITFALLS.md` §13 #13.

**Why the fleet's own audit never caught it:** `repo-assess-and-fix.md` §1A's justfile check only verified that a recipe named `build-native` *existed* - never that invoking it actually worked. A presence-only check passes identically on broken and working code. Every repo that went through assfix still came back clean, because nothing in the audit ever executed the recipe or parsed its structure for this shape.

**Scan result (2026-09-18):** a structural (not regex-only) scan of all 242 fleet justfiles found 3,138 total recipes; 732 contain a non-last, non-semicolon-joined `Set-Location`, splitting into:
- **186 instances / 81 repos - genuinely, always broken** (`Set-Location` targets a subdirectory: `native\`, `webapp\`, etc.). Concentrated in `build-native`/`tauri-build`/`tauri-dev` (73 instances), webapp/dev-server recipes (54), `e2e`/`e2e-install` runners (17), and - most concerning - `lint`/`fix` recipes in **kicad-mcp, kyutai-mcp, freecad-mcp, chip-design-mcp, pywinauto-mcp, openmanus-mcp, magentart-mcp, yahboom-mcp** that `Set-Location` into a source subdirectory before running `ruff check .` - meaning the lint gate may not have been checking the intended tree.
- **546 instances / 81 repos - dead code, not actively failing today.** `Set-Location` targets the bare repo root (`{{justfile_directory()}}` alone); the following command still lands in the right place by coincidence, because `just <recipe>` is almost always invoked *from* repo root. Still wrong, still worth fixing, but not urgent the way the subdirectory case is.

**Rule (HARD):**
> 1. Never split `Set-Location` (or any `$env:` assignment the recipe depends on) onto its own line with dependent commands on later lines. Join the whole recipe body onto one line with `; ` separators, so it all runs in the same `powershell.exe` process: `$env:Path = "..."; Set-Location '...'; .\build.ps1`.
> 2. Prefer skipping `Set-Location` entirely when the target is a script - call it by absolute path instead: `& '{{justfile_directory()}}\native\build.ps1'`. Fleet `build.ps1` templates already resolve their own root via `$PSScriptRoot`, so `Set-Location` was never load-bearing in the first place.
> 3. `repo-assess-and-fix.md` §1A now has an explicit justfile-recipe-correctness row (added 2026-09-18) with the detection command below - a recipe existing by name is no longer sufficient to pass assfix.
> 4. Fixed 2026-09-18: the scaffold template (`scripts/scaffold-tauri.ps1`), plus 6 queue-priority repos (kicad-mcp, google-ai-mcp, kyutai-mcp, libreoffice-mcp, moltbot-mcp, streamfog-mcp, vbot-mind-mcp). **The remaining ~75 repos on the HIGH list, and all 546 LOW-severity instances, are not yet fixed** - sweep in batches of 10 with `.bak` per file per Batch Mutation Safety, re-run the detection command per batch to confirm no more hits before moving on.

**Detection (re-run any time to check current fleet exposure - heuristic: flags the `Set-Location` line, you still need to eyeball whether it's the recipe's last line):**
```powershell
rg -U -P 'Set-Location[^\n;]*\n\s*\S' D:\Dev\repos --glob 'justfile' -l
```

**Related:** [#35 above](#35-join-path-pscriptroot------3-positional-arg-join-path-crashes-on-windows-powershell-51-shipped-fleet-wide-via-one-template), `JUSTFILE_STANDARDS.md` §VIII, `repo-assess-and-fix.md` §1A, `scripts/scaffold-tauri.ps1`.

---

## 38. `git commit -- <pathspec>` runs `repo: local` pre-commit hooks against HEAD, not the index - false-pass and false-fail

**Discovered:** 2026-09-19 (depot-mcp assfix - three consecutive `git commit -- <files>` attempts failed inside the biome-hook with the *pre-fix* text of `scripts/pre-commit-biome.ps1`, although `git show :scripts/pre-commit-biome.ps1` and the worktree both contained the fixed version and standalone `pre-commit run biome` passed).

**Trap:** On a partial (pathspec) commit, pre-commit resets staged-but-**excluded** files to HEAD before running hooks. For `repo: local` hooks whose `entry` executes a repo script (fleet pattern: `powershell.exe -File scripts/pre-commit-biome.ps1`), the hook therefore runs the **HEAD copy**, not the staged copy. Both failure directions are real:

1. **False-fail (observed in depot-mcp):** HEAD copy of the hook script had an em-dash that Windows PowerShell 5.1 cannot parse; index copy was fixed. Every pathspec commit died in the hook complaining about a bug that was already fixed. Full `git commit -m` (no pathspec) passed immediately with zero tree changes.
2. **False-pass (reproduced in scratch):** hook script staged as `Write-Host "HOOK-VERSION-3"; exit 1`, committed file `a.txt` via `git commit -- a.txt` - hook reported **Passed** and the commit landed. Same state with full `git commit -m` correctly ran V3 and blocked. Third control (`git commit -- a.txt hook.ps1`, hook included in the pathspec) also correctly ran V3 and blocked.

So the variable is exactly "is the executed script part of the commit": excluded → HEAD runs; included → index runs. A guard that is *weakened* in the index but still strict at HEAD false-fails your commit; a guard that is *strengthened* in the index but still weak at HEAD false-passes it - a weakened lint hook can be "passing" while the commit it was supposed to gate sails through. Non-local hooks (e.g. `astral-sh/ruff-pre-commit`, which receive staged file content from pre-commit itself) are not affected the same way - this bites `repo: local` + `entry` pointing at a repo script.

**Rule (HARD):**
> 1. Never `git commit -- <pathspec>` in a repo with `repo: local` hooks. Stage exactly what the commit should contain (`git add <files>`, verify with `git diff --cached --stat`), then run a full `git commit -m` with no pathspec.
> 2. If a commit-time hook failure contradicts what you see in the worktree/index (`git show :<file>` disagrees with the error text), suspect this trap before suspecting your fix: re-run the hook standalone (`pre-commit run <id>`) and retry as a full commit. Do not "fix" the already-fixed file, do not `--no-verify` past it.
> 3. Fleet assfix commits must be full commits (see `repo-assess-and-fix.md` Phase 6) - the ≤5-files-per-commit batches are assembled with `git add`, never with pathspec commits.

**Related:** `repo-assess-and-fix.md` Phase 6, assfix skill "What NOT to do".

## 39. Confident guidance about fast-moving external surfaces from training memory - the helper describes last year's UI with this year's confidence

**Discovered:** 2026-09-30 (Google Auth onboarding session - half the console guidance came from training memory: the Branding page with no user-type field anywhere, the Overview page showing "nothing," a widget link erroring out. Each wrong turn cost a frustrated human several minutes on something billed as a ten-minute job).

**Trap:** Third-party consoles, dashboards, and API surfaces (Google Cloud console, OAuth flows, model catalogs) redesign on a cadence far shorter than any training cutoff. A helper guiding a human through such a surface from memory sounds authoritative while describing buttons that no longer exist - and unlike a code bug, there is no compiler to catch it; the human just clicks into dead ends. Confidence is uncorrelated with freshness, and the failure mode is silent: the human assumes they are lost, not that the map is old.

**Rule:**
> 1. Before guiding anyone through a third-party UI or API you have not verified this quarter, verify live first: websearch the current flow, fetch the current docs page, confirm the click path exists *now*. Training memory is a hypothesis, not a map.
> 2. Say what you verified and when ("checked 2026-09-30 via websearch" vs "from memory") so the human can weight it. Unmarked memory guidance about external surfaces is a defect.
> 3. When the human reports the screen does not match your description, believe the screen immediately. Do not re-explain the remembered path louder - re-verify live, or route around (fresh project, direct deep links, CLI) instead of navigating a UI you cannot see.
> 4. Write the verified path down where the next session will find it (pattern doc with a Last-verified date), because the next visit is always months away and the UI will have moved again.

**Related:** `patterns/GOOGLE_API_AUTH_SURVIVAL.md` section 0 (the frequency trap - junior doing it daily vs solo dev doing it yearly).

## 40. Pre-commit `end-of-file-fixer` fails the first assfix timestamp commit - Write-tool JSON has no trailing newline

**Discovered:** 2026-10-03 (notepadpp-mcp assfix - the `.assess-fix-timestamp` commit failed three times in one session with "files were modified by this hook"; each time the fix was re-stage + recommit with zero content changes).

**Trap:** The fleet pre-commit template (`templates/pre-commit-config.yaml.template`) ships `end-of-file-fixer`, so every template-conformant repo rewrites newline-less files at commit time. The assfix flow writes `.assess-fix-timestamp` via the Write tool as single-line JSON with no trailing newline, which guarantees this exact sequence: commit -> hook appends `\n` -> exit 1 "files were modified by this hook" -> re-stage -> recommit passes. Harmless but misleading: the failure looks like a broken hook or a bad file, and both natural reactions are wrong - "fixing" the already-correct content, or `--no-verify` to skip a guard that did its job. Any Write-tool-authored single-line marker file (`.ghaudit-timestamp`, badge sidecars) in any template-conformant repo hits the same first-commit failure, so this is fleet-wide by construction, not a notepadpp-mcp quirk.

**Rule:**
> 1. When writing `.assess-fix-timestamp` (or any marker file) with the Write tool, end the content with a trailing newline (`...}\n`). One character, zero hook failures.
> 2. If a commit fails with "files were modified by this hook" and `git diff` shows only a trailing-newline addition, that IS the whole story: re-stage and recommit. Do not edit content, do not `--no-verify`.
> 3. Same rule for every machine-written file in a template-conformant repo: Write-tool output ends with `\n`, always.

**Related:** assfix skill Phase 6 step 2, `templates/pre-commit-config.yaml.template`, #13 (BOM) - same family: file-writing tool defaults vs hook expectations.

## 41. Failed pre-commit run silently restores a partial tree - stash/restore drops unstaged work with a success message

**Discovered:** 2026-10-07 (komga-mcp assfix - first commit failed on two new hooks, and the next `git status` showed ~15 files of real edits silently reverted to HEAD with no error anywhere).

**Trap:** When hooks fail, pre-commit stashes unstaged changes, reports the failure, then "restores" the stash (`[INFO] Restored changes from ...patch...`). The restore message reads as success even when the re-apply is partial: in this case every *unstaged modification to tracked files* (justfile recipes, CI steps, docs, configs) was gone, while staged files and untracked files survived intact. Nothing errored, nothing warned - the loss was only visible because a later content grep (`Select-String bootstrap justfile`) came back empty on a file edited an hour earlier. A second `pre-commit run` in between stashed and restored the same way, so either cycle could have been the one that dropped the content; there is no marker distinguishing a full restore from a partial one.

**Recovery (worked):** pre-commit keeps every stash patch under `C:\Users\sandr\.cache\pre-commit-home\patch*` (dozens accumulate - they are never cleaned). The failed run's patch still held the full unstaged diff: `git apply --check <patch>` failed only on `uv.lock` (moved on since), and `git apply --exclude=uv.lock <patch>` restored all 15 files byte-identical (verified by re-running the content greps + gates). Check that cache directory before re-doing lost work by hand.

**Rule (HARD):**
> 1. After ANY failed `git commit` in a hook-guarded repo, verify the worktree before continuing: `git status --porcelain` plus a content spot-check on files you edited but had not staged (a filename list is not enough - a reverted file looks identical in `status` output to an untouched one until you diff or grep it).
> 2. Never start the next edit round on top of an unverified post-failure tree - you will silently re-apply (or build on the absence of) reverted changes, and subsequent commits will look complete while missing files.
> 3. Keep hook invocations side-effect-free so there is less to restore: `uv run --frozen` (a bare `uv run` in a hook can sync the environment and rewrite `uv.lock`, which both dirties the tree mid-commit and invalidates later patch recovery), and run version-pinned local tools from their own directory (the biome hook must run from `webapp/frontend` so `bun x` resolves the repo's own binary, per the #35 lesson about interpreter assumptions).
> 4. Prefer small staged batches (assfix ≤5-file rule) precisely so a failed commit's blast radius is enumerable - one failed 5-file commit is auditable, one failed `git add -A` is not.

**Related:** #38 (pathspec commits vs local hooks - same family: hook runs against something other than what you think), #40 (first-commit hook failure - same family: misleading commit-time failures), assfix skill Phase 6 step 8 (stage-all review catches the *absence* only if you look at content, not just names).

## 42. Debugging the engine while a stale vendored copy shadows it - five confident wrong layers in a row

**Discovered:** 2026-10-08 (git-github-mcp start.bat FAIL loop - session-0 orphan squatting :10713, same family as the 33-port fleet epidemic from the 10/06 boot).

**Trap:** The fleet start engine prefers a repo-local `scripts/FleetStartMode.ps1` over the central one (`Invoke-FleetWebappStart.ps1` lines ~378-388: repo-local wins, central is fallback). Repos carry vendored copies that predate central fixes, and nothing resyncs them (the so-called `sync-fleet-startmode.ps1` does piecemeal repairs, never a true byte-copy). The session went: (1) blamed the timeout - wrong, nothing launched; (2) blamed the stale-check - wrong, it only runs when healthy; (3) built an orphan message block - correct diagnosis, unloaded code; (4) built auto-kill + reroute - correct code, still unloaded; (5) diagnosed PID churn - plausible, irrelevant. Each theory was argued confidently from log lines that came from DIFFERENT code generations: overlapping start.bat windows print overlapping logs, so two pastes can contradict each other while both are "true" for their own run. On top of that, the reroute itself shipped as a no-op (a `$svcKind = $false` assignment inside the already-taken `if ($svcKind)` branch - PowerShell does not jump to `else` retroactively), which looked exactly like "the engine ignores my fix" and restarted the whole wrong-layer cycle. Five messages, zero loaded-code verification, before anyone asked which file the repo actually loads.

**Rule (HARD):**
> 1. Before debugging ANY fleet-engine behavior in a repo, resolve which helper file loads: repo-local `scripts/FleetStartMode.ps1` shadows central, always. `rg -c <your-new-marker> <repo>/scripts/FleetStartMode.ps1` - zero hits means your fix never ran, no matter what the central file says.
> 2. Never trust two pasted logs to be the same run. Overlapping start.bat windows print interleaved generations - demand one fresh run with all other windows closed before theorizing.
> 3. A flag assignment is not a code path. After writing `$x = $false` inside `if ($x)`, re-read the branch structure: the taken branch does not un-take itself. Gate the downstream block explicitly (`if ($xKind) { wait }` + `if (-not $xKind) { dev }`).
> 4. Vendored copies are a fleet liability with no owner: any central engine fix is fleet-wide fiction until vendored copies resync. Byte-copy central over vendored (one file, per-repo commit), never piecemeal-patch the copy.

**Related:** #35 (template bugs ship fleet-wide - same family: one source, many stale copies), #37 (186 broken recipes from one template line - same family: divergence without ownership), BUG-007 (session-0 kill path - the underlying incident this debugging session circled).

## 43. AI file tools write LF-only .bat files and cmd.exe silently misparses them

**Discovered:** 2026-10-08 (gimp-mcp assfix follow-up - brand-new root `start.bat` crashed on double-click).

**Trap:** The Write/Edit file tools write LF line endings, always. A `.bat` file with `if (...) else (...)` paren blocks and LF-only endings misparses in `cmd.exe` - the window flashes and dies with no useful error, which looks exactly like a broken launcher script rather than a line-ending problem. Two things conspire to hide it: (1) `.gitattributes` `*.bat text eol=crlf` normalizes the *committed blob*, so the repo looks correct and every future clone is fine - but the *worktree file* the agent just created stays LF until someone re-checks-out, so the crash reproduces on the author's own machine while the repo looks innocent; (2) `git status` shows the CRLF worktree file as unmodified (normalized content identical), so the fix is literally uncommittable - only a guard can catch the next occurrence. The gimp-mcp case had a second, independent crash stacked underneath (`start.ps1` referenced an undefined `$ProjectRoot`), which would have masked the line-ending fix during verification if both had not been found first.

**Rule (HARD):**
> 1. After writing ANY `.bat`/`.cmd` file with an AI file tool, convert worktree line endings to CRLF immediately - do not wait for commit, commit cannot fix the worktree copy.
> 2. Every fleet repo with a `.bat` file carries the `bat-crlf` pre-commit hook (`scripts/pre-commit-bat-crlf.ps1`, template: `templates/pre-commit-config.yaml.template`): check-only, fails the commit with the one-line fix. It fires exactly when an agent adds an LF bat - proven in gimp-mcp, where it caught a second pre-existing LF-only `webapp/start.bat` on its first run.
> 3. When a `.bat` double-click crashes with no error, check line endings (`[IO.File]::ReadAllText` contains `[char]13`) BEFORE debugging script logic - and check for a stacked second bug underneath before declaring victory.

**Related:** #13 (BOM - same family: invisible file-encoding defaults), #40 (trailing newline vs end-of-file-fixer - same family: Write-tool defaults vs hook expectations), fleet `bat-crlf` hook + `templates/pre-commit-config.yaml.template`.

## 44. `Get-Content` line numbers lie on backtick-heavy files - index patching duplicates thousands of lines

**Discovered:** 2026-10-10 (template modernization - a `new-fullstack-app.ps1` worktree copy ballooned 254KB/7538 lines to 666KB/18858 lines during index-based scratch patching; `new-mcp-server-intelligent.ps1` index edits landed on wrong physical lines)

**Trap:** PowerShell `Get-Content` joins lines ending in a backtick (line continuation) and reports *logical* lines, while .NET `[IO.File]::ReadAllLines` reports *physical* lines. On backtick-heavy files the two disagree wildly (observed: 6909 vs 7538 on identical bytes). Any scratch script that reads via `Get-Content`, addresses lines by index (`$lines[82]`, `$lines[0..82]` slices), and writes back will splice at the wrong places - duplicating thousand-line ranges while every anchor check *appears* to pass, because the anchor text exists in both numberings. The corruption is silent: the file grows, parses worse, and no single edit looks wrong.

Same session, second half of the lesson: mojibake cleanup that deletes junk characters leaves **quote orphans** (`Write-Host " 2. " Dashboard"` - three quotes, the middle one a corpse of a deleted emoji). Each orphan is an unterminated string that cascades into hundreds of downstream parse errors pointing nowhere near the cause (a 953-error file accountant-for as "pre-existing breakage" was largely this).

**Rule (HARD):**
> 1. Before addressing file lines by index, compare `(Get-Content $f | Measure-Object -Line).Lines` against `[IO.File]::ReadAllLines($f).Count`. If they disagree, the file has backtick continuations: use **string ops only** (`[IO.File]::ReadAllText` + `.Replace` / `IndexOf` splice / regex) - never index slices - or fix the counting first.
> 2. Repair mojibake at string level, in this order: (a) auto-reverse only runs that decode as fully-valid UTF-8 via the 1252 route (proper emoji fails the round-trip and self-preserves); (b) delete only C1 controls and 1252-fragment chars, keep legitimate symbols; (c) balance quotes - any colored `Write-Host` line with an odd `"` count gets a closing quote appended (parse-safe, content-preserving; verified 953-to-0 and 231-to-0 on the two scaffold templates).
> 3. Prove file surgery with **byte counts and hashes** (`[IO.File]::ReadAllBytes().Length`), never with line counts from two different counters. A worktree copy that gained kilobytes you cannot attribute to your own edits is a restore-from-backup event, not a commit.

**Related:** #13 (BOM), #40 (Write-tool defaults), #43 (LF-only .bat) - same family: invisible file-representation defaults; BUG-073 follow-up (the session that surfaced it).

## 45. arXiv API: bare multi-word query + newest-first sort = any-word matches

**Discovered:** 2026-10-11 (searchstudio-mcp consuming arxiv-mcp `GET /api/preprints/search`; BUG-076)

**Trap:** Passing user free text straight to the arXiv API (`arxiv.Search(query=q)` or `search_query=q`) leaves bare space-separated terms whose combination the API manual does not define; in practice they match loosely (any term). Ranked by relevance this mostly looks fine, which hides it. Sorted by `submittedDate` descending, the result is "the newest papers containing any one common word": `sitagliptin first clinical trial` returned brand-new robotics papers, while `sitagliptin` alone correctly returned 0. `all:{q}` is the same trap in disguise - the prefix binds only to the first word.

**Rule:**
> 1. Free text without field prefixes (`ti: au: abs: co: jr: cat: rn: id: all:`), boolean operators (`AND OR ANDNOT`) or parens -> build `all:t1 AND all:t2 ...`; keep user-quoted `"phrases"` as `all:"phrase"`. Pass already-structured queries through untouched.
> 2. Default free-text search to `relevance`. Use `submittedDate` only when the caller explicitly asks for freshness, and then only with an AND-built query.
> 3. Regression-test the query builder (single word, multi-word, quoted, prefixed, boolean) and assert the sort at the route level with a mocked client.

Reference implementation: arxiv-mcp `services/papers.py` `free_text_to_arxiv_query()`. Source of syntax: info.arxiv.org/help/api/user-manual.html (verified 2026-10-11).

## 46. Commit-hook atomicity: partial stages can never pass whole-tree gates

**Discovered:** 2026-10-25 (tvtropes-mcp assfix - four failed commits in one run, three distinct mechanisms).

**Trap:** Three ways a commit fails while every file in it is correct:

1. **Type-closure:** mypy/pyright follow imports, so a hook run on staged files checks the *transitive closure*. Staging `app.py` (fixed) while `crawler.py` sits unstaged (broken) fails on `crawler.py` — the fix exists in the worktree but not in the checked set. Fix direction is leaves-first: stage dependency leaves, then importers.
2. **`always_run` whole-tree hooks:** a `pass_filenames: false` + `always_run: true` hook (Biome) checks the entire tree every commit. No subset commit can pass until the full green set lands together — one atomic commit with the reason in the message, not N failing slices.
3. **Staged pre-fix copies:** pre-commit validates the *staged* blob. Editing a staged hook script (`scripts/pre-commit-biome.ps1`) leaves the fix unstaged; the hook runs the old copy, fails, and the stash cycle hides the new one. Always re-`git add` after touching a staged file, and treat "hook failed on a file I just fixed" as a staging bug first.

Bonus from the same run, same family: (a) `biome-ignore` suppressions must name the exact rule with exact case (`noDangerouslySetInnerHtml`, not `...HTML` — wrong case is a `suppressions/parse` error that masks the real finding) and sit directly above the *diagnostic line*, not the element (a comment above `<div` does not suppress its attribute two lines down; formatters move lines, so prefer file-level `biome-ignore-all` for stable cases); (b) the repo's grep tool chokes on `"` in patterns — quote-free patterns or `Select-String` instead.

**Rule (HARD):**
> 1. Before committing in a hook-guarded repo, name the closure: which gates check which file sets. Stage the dependency-closed green set (≤5-file batches where they stay green; atomic exception documented in the message when they cannot).
> 2. When a hook fails on already-fixed code, check staging before code: `git status` (staged vs unstaged split) and `git diff --cached --stat` first, file content second.
> 3. Never `--no-verify` to route around 1–2: the one legitimate bypass is a documented atomic-closure commit whose message says exactly which gate forced the size.

**Related:** #38 (pathspec commits run hooks against HEAD), #40 (trailing newline vs end-of-file-fixer), #41 (stash/restore drops unstaged work) - same family: the commit validates something other than what you think; `repo-assess-and-fix.md` Phase 6 step 8 (hook-atomic batches), `NAKED_PC_INSTALL_STANDARD.md` §2b (absolute tool resolution in hooks).




## 47. Agent "cleanup" sweep guts venvs and configs - servers die with "Connection closed", rebuilds fail on locked .pyd files

**Discovered:** 2026-10-31 (pywinauto-mcp, winops, calibops, revops all retrying in Claude Desktop). Full incident: `operations/INCIDENT_2026-10-31_VENV_GUTTING.md`.

**Trap:** An agent ran a fleet-wide sweep "to save space" that deleted venvs, stripped dependency lists from configs, and then tried to rebuild. The result was not a clean "no venv" state but half-deleted site-packages: whole packages gone together with their `.dist-info` (`anyio`, `dotenv`, `annotated_types`), or a single submodule gone inside an otherwise present package (`aiohttp/_websocket/helpers`). Three things made it hard to see:

1. **Claude Desktop shows only "Connection closed".** The real traceback is in `%LOCALAPPDATA%\Claude\Logs\mcp-server-<name>.log`. Since the Sept 2026 account mixup, Desktop logs moved from `%APPDATA%\Claude\logs` to `%LOCALAPPDATA%\Claude\Logs`, and the old folder still holds stale August logs that look current.
2. **Swallowed ImportErrors.** pywinauto-mcp's `app.py` catches the FastMCP ImportError, logs CRITICAL and continues with `app = None`. The visible crash is `'NoneType' object has no attribute 'tool'` at the first decorator, three lines away from the real cause.
3. **Rebuilds fail on Windows file locks.** `uv sync --reinstall` must delete and rewrite every `.pyd`. Any running process from that venv (an NSSM service, a webapp backend, a Desktop-launched MCP server) holds its `.pyd` files open, so uv dies with `failed to remove file ... _rust.pyd: Access is denied (os error 5)` and leaves the venv no better than before. One locked file aborts the whole sync.

`pip check`, `uv pip list` and `uv sync --dry-run` all trust whatever metadata is left: if a package's dist-info is still there, it counts as installed even when its files are gone.

**Rule (HARD):**
> 1. Agents never delete a `.venv`, `uv.lock`, `requirements*.txt` or a `dependencies =` entry as "cleanup". Disk space is reclaimed by deleting caches (`uv cache prune`, `__pycache__`, build/dist), never environments or manifests.
> 2. Diagnose MCP startup failures from `%LOCALAPPDATA%\Claude\Logs\mcp-server-<name>.log`, not the Desktop status line, and check the log's timestamp before trusting it.
> 3. Verify a venv against its RECORD files, not its metadata: `temp\venv_repair\verify_venv.py <site-packages>` (stdlib only, runs even when the venv is broken).
> 4. Repair from the lockfile without touching what is locked: `uv sync --frozen --inexact` first (adds missing packages, overwrites nothing), then `--reinstall-package <name>` for each damaged dist. Use a blanket `--reinstall` only after stopping every process that runs from that venv. First delete every `*.dist-info` folder that has no RECORD: an interrupted uninstall leaves them empty or metadata-only, and uv then counts the package as installed and skips it even with `--reinstall`. Add `--no-cache` when the same files come back missing, since uv links from its cache and a damaged cache entry reproduces the damage.
> 4b. A justfile `clean` recipe must never delete `.venv` with `-ErrorAction SilentlyContinue`. On Windows a live server's locked `.pyd` aborts the delete halfway and the error is swallowed, leaving a half-deleted venv that looks intact.
> 4c. Restore the extras the venv was using. A default `uv sync` never installs `[project.optional-dependencies]`, and an extra whose packages were deleted together with their dist-info leaves no trace for a RECORD check. Audit partial extras (some deps present, others missing), install the extras named in the repo's launch config (justfile, start scripts, NSSM AppParameters, Claude config), and only call a venv repaired when every module of its package imports inside it.
> 4d. `wip(auto)` auto-commits capture damaged `uv.lock`/`pyproject.toml` as if they were normal changes. After an incident, audit lock and pyproject commits by package count, not just `git status`.
> 5. Import failures of the framework itself must re-raise. Never log CRITICAL and continue with a `None` app object.

**Related:** #7 (batch scripts wreck files - one repo at a time), #34 and #37 (template bugs shipped fleet-wide via one sweep), #22 (do not taskkill NSSM children; stop the service instead before a reinstall).
