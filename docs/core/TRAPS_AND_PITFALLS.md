# Traps & Pitfalls — Agentic Work Standards

**Purpose:** Every time we discover an antipattern, a tool failure mode, or a process trap, it goes here. This is the "lessons learned" document for agentic workflows.

**Status:** Active — append new entries as they are discovered.

---

## Table of Contents

1. [Agent Launch → Wait Violation](#1-agent-launch--wait-violation)
2. [BrightData Out-of-Quota](#2-brightdata-out-of-quota)
3. [Fetch MCP Error -32002](#3-fetch-mcp-error--32002)
4. [Regex Bloopers — No Dry Run, Shell Quoting, Indiscriminate Replace](#4-regex-bloopers--no-dry-run-shell-quoting-indiscriminate-replace)
5. [`# noqa` as a crutch — must fix, not hide](#5-noqa-as-a-crutch--must-fix-not-hide)
6. [JSON Schema Validation in Tool Calls](#6-json-schema-validation-in-tool-calls)

---

## 5. `# noqa` as a crutch — must fix, not hide

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

**Cause:** The BrightData API subscription has run out of quota (monthly credits exhausted). The "token expired" message is misleading — the token is valid, but the account has no remaining balance for the current billing period.

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

## 4. Regex Bloopers — No Dry Run, Shell Quoting, Indiscriminate Replace

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

# Step 2: Verify count and context — only then replace
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
# BROKEN — dots match any char, $1 is a group ref, not literal "$1"
$content -replace "fastmcp.tool.annotations", "..."

# BROKEN — the \b in PowerShell string needs escaping
$content -replace "\breadcrumb", ""

# CORRECT — escape dots, use simple strings for simple replacements
$content -replace "fastmcp\.tool\.annotations", "new.import"

# CORRECT — use [regex]::Escape for literal strings
$pattern = [regex]::Escape("fastmcp.tool.annotations")
$content -replace $pattern, "new.import"
```

### Trap 4c: No backup before batch edit

Modifying 3+ files with a regex or batch script without timestamped backups.

**Consequence:** When the regex hits the wrong files (e.g., matches inside comments, strings, or wrong indentation level), there is no way to revert without git. If git is not available (temp files, generated files), the original content is lost.

**Rule:**
> Any batch operation touching 3+ files MUST create `.bak` timestamped copies first. See `GIT_REPOSITORY_SAFETY.md` for the batch mutation safety rule.

```powershell
# Always backup before batch edit
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
foreach ($file in $filesToEdit) {
    Copy-Item $file "$file.$timestamp.bak"
}
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
- Replace em dashes `—` with `--` or `-` in content strings

---

## 6. Stale In-Process API Credentials Surfacing as a Flat "Invalid API Key" Error

**Discovered:** 2026-06-20 (tailscale-mcp `manage_tailnet_devices` returning 401 despite a valid key on disk)

**Symptom:**
```
Error calling tool 'manage_tailnet_devices': Failed to perform device operation: Failed to list devices: Failed to list devices: Invalid API key or authentication failed
```

The error gives zero signal on what to actually do. The natural reaction — "go generate a new API key" — is often the wrong fix and wastes a key rotation, an admin-console trip, and another server restart that still doesn't help if the real cause is the second one below.

**Cause — two distinct failure modes that both produce HTTP 401, and the wrapper collapses them into one indistinguishable string:**

1. **Genuinely invalid/expired key.** The credential on disk is actually bad (revoked, past expiry, wrong tailnet/account).
2. **Stale in-process credentials (the more common case for long-lived servers).** Most FastMCP servers load credentials once via `load_dotenv()` / `BaseSettings` at *import time* (`config.py`'s module-level `load_dotenv(env_path)`, or inside `__init__` of a manager/client class). If the `.env` file is edited, or credentials are rotated through a webapp settings endpoint, **after** that process already started, the *file* is correct but the *running process* is still holding the old value in memory. Nothing re-reads the file on a per-call basis — that would require either a file-watcher, a TTL-based reload, or an explicit `reload_credentials()` call wired into every settings-mutation path (and even where one exists, like `tailscalemcp.mcp_server.TailscaleMCPServer.reload_credentials()`, it only patches *that* process's instances — a separate stdio-spawned process for the same server, e.g. one Claude Desktop launched independently of a webapp-mounted instance, never sees it).

**Detection — confirm which of the two it is before doing anything:**

```powershell
# Test the key on disk DIRECTLY against the provider's API, bypassing the MCP server entirely.
$key = (Get-Content .env | Where-Object { $_ -match "^TAILSCALE_API_KEY=" }) -replace "^TAILSCALE_API_KEY=", ""
$tailnet = (Get-Content .env | Where-Object { $_ -match "^TAILSCALE_TAILNET=" }) -replace "^TAILSCALE_TAILNET=", ""
Invoke-RestMethod -Uri "https://api.tailscale.com/api/v2/tailnet/$tailnet/devices" -Headers @{Authorization="Bearer $key"}
```
If this succeeds but the MCP tool still 401s: **the file is fine, the running process is stale.** Restart it.
If this also fails: the key itself is bad — rotate it.

Also check process start time vs. last `.env` edit:
```powershell
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match "<server module name>" } | Select ProcessId, Name, CreationDate
(Get-Item .env).LastWriteTime
```
If `CreationDate` predates `LastWriteTime`, that process has stale credentials by definition.

**Fix:**
- Stale-in-process: restart the MCP server process (for stdio-spawned servers, restart the MCP host — Claude Desktop, Cursor, etc.; for a webapp-mounted instance with a `reload_credentials()`-style hook, call that endpoint instead of a full restart).
- Genuinely invalid: rotate the key at the provider, update `.env`, then still restart the process (rotating the file alone does not help a process that already cached the old value).

**Rule (HARD) — error responses MUST distinguish the two causes, not collapse them:**
> Any tool-module exception boundary that can see an HTTP 401 (or equivalent auth failure) from an upstream API MUST NOT re-wrap it into a flat, single-string error. The response must include a structured `recovery_options` (or equivalently named) field listing both candidate causes — stale-in-process vs. genuinely-invalid — each with its own `check` (how to tell which applies) and `fix` (what to actually do). A flat string forces the person to guess, and the wrong guess (key rotation) burns more time than the actual fix (restart).

**Reference implementation:** `tailscale-mcp`'s `src/tailscalemcp/tools/_helpers.py` — `is_auth_error()` walks the exception's `__cause__` chain (with a message-text fallback for call sites that stringify before re-raising, breaking the chain) to detect an `AuthenticationError` anywhere in it, and `build_auth_error_response()` builds the two-cause `recovery_options` payload, including a process-age hint when `server_started_at` is passed (module-import time is a reasonable proxy). Wired into `device_tool.py`'s outer `except Exception` block as the pattern to replicate in every other tool module across the fleet — most fleet servers share the same "load credentials once at import/init time" pattern and are equally susceptible. When patching a given server, check its config-loading layer first (`config.py`, the manager `__init__`, or wherever `load_dotenv()` / equivalent runs) to confirm it's load-once rather than per-call, since that confirms this trap applies before spending time on the fix.

**Anti-pattern to avoid while fixing this:** Don't "fix" it by making credential loading reload from disk on every tool call — that reintroduces a stat()/parse cost on every request for a problem that's actually rare (credentials change maybe a few times a year). The structured error + restart is cheaper and the restart is something the person controls and is aware of, vs. invisible per-call file I/O that nobody asked for.

**Fleet rollout tracking:** See [operations/AUTH_ERROR_SURFACING_FLEET_ROLLOUT.md](../operations/AUTH_ERROR_SURFACING_FLEET_ROLLOUT.md) for the candidate repo list, priority order, and per-repo patch checklist.

---

## 7. Batch Scripts Wreck Files — One Repo at a Time

**Discovered:** 2026-06-21 (Playwright e2e justfile batch — 12 repos, 1 truncated, destroyed 126→13 lines)

**Trap:** Writing a Python/Shell script that iterates over multiple repos and applies the same transformation to each one. The script inevitably hits an edge case — encoding, line endings, file format differences — that corrupts one or more files, and you don't notice until the user screams.

**Rule (HARD):**
> NEVER write a batch script that modifies files across multiple repos. If a task affects more than one repo, do them one at a time using the `edit` tool (or equivalent file-by-file editor). The only exception is read-only audits (grep, lint checks) which cannot destroy content.
>
> If the task genuinely requires the same change in N repos, the correct procedure is:
> 1. Make the change in ONE repo using `edit`
> 2. Test it (lint, build, run — whatever applies)
> 3. Only after it passes, move to the next repo
> 4. Repeat serially

**Why this rule exists:**
- Batch scripts skip per-repo differences (encoding, line endings, file structure)
- A single edge case corrupts one file and the entire batch is suspect
- The time saved by batching is lost tenfold when you have to revert and redo
- Serial editing with `edit` takes ~30 seconds per repo — user waits an extra 5 minutes, but the result is correct
