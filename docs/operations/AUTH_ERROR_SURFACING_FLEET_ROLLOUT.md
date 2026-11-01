# Auth-Error-Surfacing Fleet Rollout

**Status:** Tracking — `tailscale-mcp` complete (2026-06-20), fleet rollout not started.
**Origin:** [TRAPS_AND_PITFALLS.md §6](../standards/TRAPS_AND_PITFALLS.md#6-stale-in-process-api-credentials-surfacing-as-a-flat-invalid-api-key-error)
**Reference implementation:** `tailscale-mcp` `src/tailscalemcp/tools/_helpers.py` (`is_auth_error`, `build_auth_error_response`)

---

## The problem, in one line

Any MCP server that loads API credentials once at process startup (`load_dotenv()` at import time, or in a manager's `__init__`) and then re-wraps every downstream exception into a flat string loses the distinction between "the key on disk is bad" and "this long-lived process has a stale key in memory" — and the wrong guess (key rotation) costs more time than the right fix (restart).

Full writeup, detection script, and the hard rule: see the linked Trap 6 entry. This doc only tracks *which repos need the patch* and *who's done*.

## Why this generalizes beyond tailscale-mcp

The same `load_dotenv()`-once-at-import pattern is the standard credential-loading shape used fleet-wide (it's effectively the convention, not an outlier — `config.py`'s `pydantic_settings.BaseSettings` + module-level `load_dotenv(env_path)` shows up nearly verbatim across repos). Any repo in this shape that also talks to an external, credentialed cloud API is exposed to the same trap. Repos that only talk to local desktop apps (Blender, OBS, Reaper, DaVinci Resolve) or local hardware over LAN (most of the `*-mcp` IoT/robotics fleet) generally aren't exposed — there's no remote auth token to go stale.

## Detection method used for this list

```powershell
Get-ChildItem -Path D:\Dev\repos -Directory | ForEach-Object {
    $src = Join-Path $_.FullName "src"
    if (-not (Test-Path $src)) { return }
    Get-ChildItem -Path $src -Filter "*.py" -Recurse -File |
        Where-Object { $_.Name -notmatch "test_" -and $_.FullName -notmatch "\\(tests|__pycache__|\.venv|node_modules)\\" } |
        ForEach-Object {
            $content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
            if ($content -match "load_dotenv" -and $content -match "(API_KEY|api_key|ACCESS_TOKEN|access_token)") {
                "$($_.Directory.Parent.Parent.Name) :: $($_.Name)"
            }
        }
}
```

**This is a text-pattern grep, not a semantic analysis.** It will miss:
- Repos using `BaseSettings` env binding without a literal `load_dotenv()` call
- Non-Python (Node/TS) MCP servers entirely (out of scope for this grep)
- Credential variable names that don't match `*API_KEY*` / `*ACCESS_TOKEN*` (e.g. `*_SECRET`, `*_TOKEN` alone, OAuth client ID/secret pairs)
- Repos where credential loading happens in a file not under `src/`

Treat the list below as a confirmed-candidate floor, not a ceiling. Before patching any repo not on this list, re-run the grep against it specifically or read its `config.py`/equivalent by hand — five minutes either way.

## Candidate repos (last scanned 2026-06-20)

| Repo | File(s) hit | In FLEET_INDEX.md? | Status |
|---|---|---|---|
| `tailscale-mcp` | `config.py`, `mcp_server.py`, `server.py`, `tools/_helpers.py` | Yes | ✅ **Done** — all 16 tool modules patched, see Trap 6 |
| `arr-mcp` | `config.py` | Yes (added 2026-06-20) | Not started |
| `calibre-mcp` | `config.py` | Yes (Gold-adjacent, RAG/media research) | Not started |
| `discord-mcp` | `server.py` | Yes (added 2026-06-20) | Not started |
| `gtfs-mcp` | `config.py` | Yes | Not started |
| `immich-mcp` | `config.py`, `server.py` | Yes | Not started |
| `jellyfin-mcp` | `config.py` | Yes | Not started |
| `nest-protect-mcp` | `auth_tools.py`, `server.py` | Yes — **OAuth-based, likely the most acute case** (Nest tokens expire on their own schedule independent of any rotation Sandra triggers) | Not started |
| `ocr-mcp` | `core/config.py` | Yes | Not started |
| `openrouter-mcp` | `app.py` | Yes (added 2026-06-20; early/v0.1.0, low blast radius) | Not started |
| `qbt-mcp` | `settings.py` | Yes | Not started |
| `speech-mcp` | `server.py` | Yes (added 2026-06-20) — **fleet voice layer, humanoid-scale; high priority given role** | Not started |
| `virtualization-mcp` | `config.py` | Yes — **Gold Standard tier**, worth doing early as the visible reference for fleet quality bar | Not started |
| `worldlabs-mcp` | `api_bridge.py`, `server.py` | Yes | Not started |

13 candidates beyond tailscale-mcp. All now confirmed present in `FLEET_INDEX.md` (last refreshed 2026-06-20; `arr-mcp`, `discord-mcp`, `openrouter-mcp`, `speech-mcp` added during this rollout's research, having been missing from the prior 2026-06-12 snapshot despite being live, maintained repos).

## Suggested priority order

1. **`speech-mcp`** — fleet voice layer for embodied agents/humanoid-scale voice (wake → understand → fleet act → speak); flagged by Sandra as super important. Patch alongside or just after `nest-protect-mcp`.
2. **`nest-protect-mcp`** — OAuth tokens have their own expiry independent of manual rotation, so the stale-vs-invalid ambiguity this fix resolves is *more* likely to occur here than anywhere else on the list, not less.
3. **`virtualization-mcp`** — Gold Standard tier; patching it first makes it a visible example other repos can be checked against, and it already has prompts/skills/Context infrastructure that likely makes wiring in `recovery_options` cleaner.
4. **`arr-mcp`** — substantial, actively used (7 services, 25 tools, 143 tests); each `*arr` service has its own API key, so this is actually a multi-credential variant of the trap worth handling carefully.
5. **`calibre-mcp`, `discord-mcp`, `immich-mcp`, `jellyfin-mcp`, `worldlabs-mcp`** — actively used services with cloud-side auth; moderate blast radius if it bites.
6. **`gtfs-mcp`, `ocr-mcp`, `qbt-mcp`** — lower-stakes, patch opportunistically.
7. **`openrouter-mcp`** — early/v0.1.0, stdio-only, no webapp; low priority until the repo matures past its current minimal scope.

## Per-repo patch checklist (copy this into each repo's own TODO/CHANGELOG when starting it)

1. Read the repo's `config.py` / credential-loading module to confirm the load-once pattern actually applies (don't assume — some repos may already reload per-call, in which case this trap doesn't apply and the repo should be struck from this list with a note why).
2. Identify the repo's actual exception type for auth failures (may not be named `AuthenticationError` — check what's raised on the provider's 401/403 equivalent).
3. Add the two-function pair (`is_auth_error`, `build_auth_error_response`) to that repo's helpers module, adapted to its own exception hierarchy and provider-specific recovery URLs (e.g. Nest's OAuth re-consent flow looks nothing like Tailscale's "generate a new API key" page — don't copy Tailscale's URLs verbatim).
4. Wire it into every tool-module exception boundary that can see that auth failure — grep for the repo's own catch-all exception pattern first (`except Exception as e:` is fleet-standard, per `TRAPS_AND_PITFALLS.md` §4 conventions, but confirm).
5. Compile-check: `uv run python -c "import <package>.<entrypoint_module>"` (matches the verification used for tailscale-mcp).
6. Mark `✅ Done` in the table above with the date.

## Closed / shipped

- **2026-06-20** — `tailscale-mcp`: full rollout across all 16 tool modules (`device_tool.py`, `automation_tool.py`, `backup_tool.py`, `file_tool.py`, `funnel_tool.py`, `integration_tool.py`, `lm_link_tool.py`, `monitor_tool.py`, `network_tool.py`, `new_api_tool.py` [7 boundaries via shared `_raise_auth_aware`], `partner_tailnets_tool.py` [2 boundaries], `performance_tool.py`, `reporting_tool.py`, `sampling_tool.py`, `security_tool.py`, `status_tool.py`) plus the `_helpers.py` `generate_status_info` degraded-fallback path (was masking a 401 as "0 devices found"). `help_tool.py` correctly excluded (static content, no API calls).
