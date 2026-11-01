# BUG-046 — Persistent App Data Resolved Under PyInstaller's Frozen Temp Dir, Wiped Every Exit

- **ID**: `BUG-046`
- **Severity**: `P1` (silent user-data loss — every saved credential/profile/registry
  entry gone on next launch, no error, no warning)
- **Date**: 2026-09-23
- **Repo/Component**: Fleet-wide — 5 repos confirmed and fixed: `google-docs-mcp`
  (OAuth client + token + sync config/manifest), `obs-mcp` (endpoints.json,
  presets.json, programs.json — 3 files), `norirobotics-mcp` (robot_profiles.json,
  robot_profile_active.json), `depot-mcp` (advertised_depots.json), `resonite-mcp`
  (spawn_registry.json)
- **Status**: ✅ Fixed in all 5 confirmed repos; 14 more repos with the same code
  *pattern* (`Path(__file__).resolve().parents[N])`) were individually checked and
  found NOT to have this bug — see "Fleet audit" below for the full breakdown

## Symptom

Surfaced as a user complaint about `google-docs-mcp`'s Settings page: a saved OAuth
client configuration should have persisted but didn't survive reasoning about "how
is this supposed to work with the Tauri app" — prompted a direct check of the
underlying storage path rather than a UI-only fix.

The general symptom, once you know to look for it: any packaged Tauri desktop app
built from one of the affected repos silently forgets everything a user saved
(credentials, named profiles, registries, configuration) every single time it's
closed and reopened. No error is shown — the app just behaves as if it were a fresh
install on every launch.

## Root Cause

A common fleet pattern computes a repo's data directory as:

```python
REPO_ROOT = Path(__file__).resolve().parents[N]
DATA_DIR = REPO_ROOT / "data"
```

In normal dev use (`uv run`) this is correct and stable — `__file__` is the real
file on disk, `parents[N]` walks up to the real repo root. In a **frozen PyInstaller
build** (which is what every Tauri repo's `native/build.ps1` produces as the
embedded backend sidecar), `__file__` resolves to a path **inside the onefile's
`_MEIPASS` extraction directory** — a temp folder PyInstaller creates fresh on
every single launch and deletes on exit. Any file written under that "REPO_ROOT"
in the frozen app is gone the moment the process exits.

This is a documented, known pitfall
(`TAURI_PRODUCTION_PITFALLS.md` §13 item 15: "Installed app loses OAuth tokens /
rules") but had only actually been implemented as a fix in the one repo the
postmortem was originally written against — every other repo using the same
`REPO_ROOT / "data"` pattern for real persistent app data inherited the
vulnerability without anyone having gone back to check.

## Fix

Per repo, added a small `data_dir()` helper (co-located as `config.py` in
google-docs-mcp since it already had a live-property `Settings` class to extend;
a standalone `data_dir.py` module in the other four, since their config lives in a
`pydantic_settings.BaseSettings` class that a resolved directory doesn't map onto
naturally):

```python
def data_dir() -> Path:
    override = os.getenv("{REPO}_DATA_DIR")
    if override:
        return Path(override)
    if getattr(sys, "frozen", False):
        local_app_data = os.getenv("LOCALAPPDATA")
        if local_app_data:
            return Path(local_app_data) / "{tauri identifier}" / "data"
    return Path(__file__).resolve().parents[N] / "data"
```

Dev mode (`uv run`, unfrozen) is byte-for-byte unchanged. The frozen build detects
itself via `sys.frozen` (set automatically by PyInstaller, no extra env var
plumbing needed) and switches to `%LOCALAPPDATA%\{tauri identifier}\data` —
matching where each repo's own Rust `backend.rs` already writes `backend-spawn.log`
(`app.path().app_log_dir()`), so this isn't a new convention, just extending an
existing one to the Python side. Each repo's `{tauri identifier}` was read directly
from its own `native/tauri.conf.json`, not guessed.

## Fleet audit (full breakdown, not a sample)

Grepped every repo with a real `native/` Tauri directory for
`Path(__file__).resolve().parents[N]`, found 23 repos using the pattern somewhere,
then individually read each hit's actual usage (not just counted the grep match):

**Confirmed same bug, fixed:** google-docs-mcp, obs-mcp (×3 files), norirobotics-mcp,
depot-mcp, resonite-mcp.

**Same code pattern, NOT the same bug (verified individually, not assumed safe):**
- `discord-mcp`, `overte-mcp`, `resonite-mcp/http_server.py` — cosmetic git-SHA
  version string lookup; harmless if it fails in the frozen build (returns
  `"unknown"`, no data ever written)
- `grandorgue-mcp` — its actual settings storage already correctly uses
  `Path.home() / "AppData" / "Roaming" / ...`; the flagged `parents[N]` hit was an
  unrelated bundled-asset (`midi_depot`) lookup
- `home-assistant-mcp`, `norirobotics-mcp/tool_vr.py`, `vroidstudio-mcp` — bundled
  **read-only** assets shipped inside the package (skills directory, 3D mesh/URDF
  files, config templates) — correct to resolve via `__file__` even when frozen,
  since that's where PyInstaller's `datas=[...]` actually puts them; this is the
  same pattern `google-docs-mcp`'s own `_SKILLS_DIR` correctly uses
- `meta_mcp` — its real persistent user data already uses `Path.home()`; the
  flagged hit locates bundled fleet-probe scripts, not user data
- `openmanus-mcp`, `lewm-mcp` — dev-only / fleet-tooling sibling-repo path lookups,
  not user data persisted by the packaged app
- `arxiv-mcp` — already has a deliberate, documented fallback (walks up to `.git`,
  explicitly falls back to env-var configuration for packaged copies with no `.git`)
- `sakana-mcp` — the flagged function's return value isn't actually used for
  persisted user output in the current code path
- `aiwatcher-mcp/config.py`'s `resolved_interests_path()` (the `parents[N]` grep hit
  that started this line of investigation) is genuinely **read-only** (checks
  `.exists()`, never writes) — a missing `interests.json` in the frozen build just
  skips an optional sync step. But `interests.json` is a **static seed file, not
  where the app's real mutable interest data lives** — the webapp's actual "New
  Interest Bundle" flow (`BundlesPage.tsx` → `POST /api/bundles/create` →
  `add_bundle()` in `database.py`) writes to a **SQLite database**
  (`aiosqlite.connect(cfg.db_path)`, default `"data/aiwatcher.db"`) that never
  showed up in the `parents[N]` grep at all, because it's resolved as a **bare
  relative path against the process's current working directory** — a different
  mechanism than every other repo in this audit. Initially mis-assessed as "no data
  ever destroyed" on the strength of the read-only `interests.json` check alone,
  without tracing the actual webapp write path — corrected after a live test:
  1. Built the PyInstaller sidecar (`aiwatcher-mcp-backend.spec`), ran it from a
     scratch directory with an explicit `cwd`, matching what `backend.rs` does
     (`.current_dir(app.path().executable_dir())`).
  2. First attempt hit the **already-running production NSSM service** on the
     default port instead of the scratch instance (the scratch exe failed to bind
     with `WinError 10013` and exited immediately, but the port-conflict was missed
     before issuing API calls) — created a real test bundle in the live database.
     **Caught and reverted immediately**: deleted the exact row by id+name match,
     verified via the live API that the bundle count and contents were back to the
     original 11.
  3. Retried on a genuinely free port (confirmed via `netstat` first) — the fresh
     scratch instance showed `items_total: 0` and only 3 auto-seeded default
     bundles, confirming real isolation from production this time.
  4. Inserted a uniquely-named row directly into the scratch SQLite file, killed the
     process, relaunched it from the same directory, confirmed the row was still
     there via the live API.
  - **Conclusion: not the same bug, verified for real this time.** `backend.rs`
    explicitly sets `current_dir` to the stable, user-writable installed-app
    directory (`installMode: "currentUser"` → `%LOCALAPPDATA%\com.sandraschi.
    aiwatcher-mcp\`), not PyInstaller's wiped `_MEIPASS` temp dir — so the relative
    `"data/aiwatcher.db"` path happens to resolve safely and persist across
    restarts. This works, but by a fragile coincidence (it depends on `backend.rs`
    continuing to set `current_dir` correctly, not on the Python side defending
    itself the way `data_dir()` does elsewhere) — worth hardening to the same
    explicit pattern as the other 5 repos rather than leaving it as an accident of
    two files agreeing implicitly, but not an active data-loss bug today.

## Lineage note

`norirobotics-mcp/robot_profiles.py`'s own docstring states it copied
`obs-mcp/endpoints.py`'s pattern earlier in the same session that pattern was
written — direct evidence of how this propagated fleet-wide via copy-paste rather
than each repo independently reinventing the same mistake.

## Related

- `TAURI_PRODUCTION_PITFALLS.md` §13 item 15 (the original, narrower documentation
  of this pitfall — this bug entry is the fleet-wide propagation audit)
- [BUG-045](./BUG-045_Naked_Bun_Bunx_Stale_PATH.md) — different bug, same repo/session
  (PATH resolution for `bun`/`bunx`, not data persistence), do not conflate the two
