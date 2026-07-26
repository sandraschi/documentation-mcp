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
