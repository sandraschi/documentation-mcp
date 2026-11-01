# Incident 2026-10-31: fleet-wide venv gutting by an agent "cleanup" sweep

**Status:** mostly repaired, residual lock-held venvs pending a stop-then-repair (see Remaining work).
**Severity:** high. Four Claude Desktop servers down (pywinauto-mcp, winops, calibops, revops); fleet-wide breakage of venvs, most of it silent until a server is next started.
**Pitfall:** [#47 in standards/TRAPS_AND_PITFALLS.md](../standards/TRAPS_AND_PITFALLS.md) ("Agent cleanup sweep guts venvs and configs").
**Repair tooling and raw reports:** `D:\Dev\repos\temp\venv_repair\` (scripts, `report.csv`, `report2.csv`, `config_audit.csv`, `pass3.txt`, per-repo logs).

## What happened

An agent ran a fleet-wide sweep, in Sandra's words, that "swept the configs and borked them": it deleted requirements from configs, deleted venvs to save space, and its venv rebuilds then failed. The exact date of the sweep is not established; Desktop logs show pywinauto-mcp failing on every start on 2026-10-31 from at least 10:56 local.

## Symptoms

- Claude Desktop: four servers stuck on retry with only `Connection closed`.
- Real errors, from `%LOCALAPPDATA%\Claude\Logs\mcp-server-<name>.log`:
  - pywinauto-mcp: `No module named 'annotated_types'`, then `'NoneType' object has no attribute 'tool'` (app.py swallowed the ImportError, see Code fixes)
  - winops: `No module named 'anyio'`
  - revops: `No module named 'dotenv'`
  - calibops: `No module named 'aiohttp._websocket.helpers'`
  - virtualization-mcp: started, but its plugins failed on the same aiohttp damage (warning only)
- The first diagnosis looked at `%APPDATA%\Claude\logs`, which stopped on 2026-08-21. Desktop moved its user data to `%LOCALAPPDATA%\Claude` during the September 2026 account mixup; the old folder holds stale logs that look current.

## Evidence

- Venv base interpreters were intact (all on uv CPython 3.12.9, same as the working fileops), and entry-point modules existed. The damage was inside site-packages.
- Damage came in three shapes, all of which keep the `.venv` folder itself:
  1. **Emptied:** site-packages stripped to zero installed dists (25 venvs, e.g. admiral-mcp, depot-mcp, teleconference-mcp, travelprep-mcp).
  2. **Partly gutted:** whole packages removed together with their `.dist-info` (anyio, dotenv, annotated_types, and roughly half of pywinauto-mcp's site-packages: everything sorting before "c"), so `pip`/`uv` metadata no longer knows they existed.
  3. **Hollowed:** dist-info present but files missing (`aiohttp/_websocket/helpers`, cryptography submodules, pandas with 1390 of its files gone, easyocr data).
- **Deleted outright:** 122 Python repos had no `.venv` at all; rebuilt in pass 2 (119 from their lockfiles; 3 have no `uv.lock`).
- **Configs:** the git-tracked state does not show stripped dependency lists. `config_audit.csv` found:
  - `bakemono-runter`: `dependencies = []`, but it is a v0.0.1 stub that plausibly never had any.
  - `documentation-mcp`: `uv.lock` modified and uncommitted. The committed lock was itself corrupt (it contained other projects' packages and markdown text); the working copy is a regenerated, sane lock. Review and commit it.
  - `this-is-intentionally-broken-for-testing`: modified by design.
  - **Caveat:** many repos carry `wip(auto)` auto-commits. If the sweep removed individual dependencies and an auto-commit captured that, a git-state audit cannot see it, and neither can an empty-list check. Every lockfile tested so far still installs the full dependency set (e.g. admiral-mcp restored 87 packages), but only an import smoke test per server proves a manifest complete (Remaining work 3).
- **Why the rebuilds failed:** Windows file locks. `uv sync --reinstall` must delete and rewrite every `.pyd`; any process running from that venv holds them open, and uv aborts with `failed to remove file ... Access is denied (os error 5)`. One locked file aborts the whole sync. The failed reinstalls also left dist-info folders without a RECORD (interrupted uninstalls).
- **The uv cache is suspect too:** pandas, easyocr and standard-aifc came back incomplete even after a successful reinstall, including in a freshly created venv (giskard-mcp). uv links installed files from its cache, so damaged cache entries reproduce the damage. `uv cache clean` blocks while any `uv run` server holds the cache lock; reinstalling with `--no-cache` bypasses it.

## Repair

Tooling in `D:\Dev\repos\temp\venv_repair\`:

| Step | Script | What it does |
|---|---|---|
| Detect | `verify_venv.py` | Stdlib only. Checks every dist's RECORD against the files on disk, which catches damage that `pip check` and `uv sync --dry-run` miss because they trust leftover metadata. |
| Pass 1 | `fleet_venv_repair.ps1` | 124 repos with a venv. `uv sync --frozen --inexact --reinstall` from `uv.lock`: exact pinned versions, hand-installed extras (dlib) kept. |
| Pass 2 | `fleet_pass2.ps1` | All 246 repos with a `pyproject.toml`. Config audit; rebuilds deleted venvs with `uv sync --frozen`; repairs lock failures by adding missing dists first (`--inexact`, no overwrite), then `--reinstall-package` per damaged dist, so one locked `.pyd` only blocks its own package. |
| Pass 3 | `pass3_cache.ps1` | `--no-cache` reinstall of the cache-suspect packages, a full re-verify, and a holder scan covering every process (not just python.exe) per damaged venv. |

The scripts were launched by double-clicking them in File Explorer (computer use), because no surviving MCP server could run commands at the time. Once winops came back after pass 1, it was used directly.

## Numbers

| | Count |
|---|---|
| Python repos (pyproject.toml) | 246 |
| Venvs present at start | 124 |
| Clean at start | 63 |
| Emptied (0 dists), rebuilt in pass 1 | 25 |
| Partly damaged, fixed in pass 1 | 8 (fleet-agent, meta_mcp, plex, ring, searchstudio, videogen, windows-operations, ocr partially) |
| Partly damaged, pass 1 failed on locks | 28 |
| Of those, clean after pass 2 | 3 (butterchurn, docker, system-admin) |
| Venvs deleted outright, recreated in pass 2 | 119 |
| Deleted, no uv.lock, not recreated | 3 (dj-media-hub, fleet-tool-bridge, rust-test-c) |

### Pass 3 (14:30)

- `--no-cache` reinstalls fixed the cache-corruption cases: pandas (giskard-mcp, local-llm-mcp) and standard-aifc (speech-mcp). easyocr in ocr-mcp reinstalled with exit 0 but still lacks 83 data files listed in its RECORD; this needs separate investigation (wheel contents vs RECORD, or Defender quarantining the dict files).
- Every other failure is a lock: `os error 32, being used by another process` on a `.pyd`. Holders include Claude Desktop (claude.exe), Cursor, OpenCode, an IDE language server, and running NSSM services: advanced-memory-mcp, advanced-memory-mcp-daemon, aiwatcher-mcp, arxiv-mcp, discord-mcp, email-mcp, fastsearch-mcp, fleet-agent-mcp, fleet-hub, mcp-federation-hub, mcp-pywinauto-mcp. One orphaned python.exe (parent exited) holds iptv-org-mcp. Several holders run elevated or as SYSTEM, so a non-elevated shell cannot see their loaded modules.
- Still damaged when pass 3 was read (verify incomplete past ocr-mcp, list therefore partial): advanced-memory-mcp, agy-fleet-mcp, aiwatcher-mcp, arxiv-mcp, calibre-mcp, devices-mcp (5 jupyter config json files only, harmless), discord-mcp, email-mcp, fastsearch-mcp, filesystem-mcp, git-github-mcp, google-docs-mcp, iptv-org-mcp, local-llm-mcp, ocr-mcp; pass 2 also left pywinauto-mcp, reversing-mcp, robofang, rustdesk-mcp, speech-mcp, virtualization-mcp, yahboom-mcp. Most entries are dist-info folders without a RECORD (interrupted uninstalls), which import fine only if the package files survived; treat them as broken until reinstalled.

### Final step: `FINISH_REPAIR.cmd`

`D:\Dev\repos\temp\venv_repair\FINISH_REPAIR.cmd` (calls `FINISH_REPAIR.ps1`, self-elevates). Run it with Claude Desktop, Cursor and OpenCode closed. It rescans every venv, stops the NSSM services pointing into damaged repos, kills leftover processes that still load files from those venvs, does a full `--no-cache --reinstall` from `uv.lock`, re-verifies, restarts the services it stopped, and writes `finish_report.txt`.

## Code fixes

- `pywinauto-mcp/src/windows_computer_use_mcp/app.py`: both `app = None` fallbacks (ImportError and generic Exception) now re-raise, so the real missing module is the last line of the log instead of a NoneType crash at the first decorator. Not yet committed.

## Remaining work

1. **Stop-then-repair:** close Claude Desktop, Cursor and OpenCode, run `FINISH_REPAIR.cmd`, approve the UAC prompt, then check `finish_report.txt`.
2. Start Claude Desktop again, and confirm in `%LOCALAPPDATA%\Claude\Logs` that all servers initialize.
2a. ocr-mcp easyocr: 83 data files missing even after a clean reinstall; investigate separately.
3. Import smoke test per server (`python -c "import <pkg>"` from each venv) to catch manifests missing dependencies that an auto-commit may have captured.
4. Manual venvs for dj-media-hub, fleet-tool-bridge and rust-test-c (no lockfile).
5. Review and commit documentation-mcp's regenerated `uv.lock`.
6. Find the agent and the session that ran the sweep, and add the HARD rule from pitfall #47 to its instructions (`AGENT_PROTOCOLS.md`).
7. `C:\Users\<user>\Desktop\RUN_VENV_REPAIR.cmd` is a leftover helper; it was not needed and can be deleted.

## Round 2 (15:36)

FINISH_REPAIR.cmd did not run (no `finish_report.txt`). After Sandra restarted Claude Desktop, fileops, gitops and virtualization-mcp failed on `No module named 'pywintypes'` (pywin32), and memops and calibops on `cannot import name 'getcurrent' from 'greenlet'`. Both packages had lost their RECORD in the earlier interrupted uninstalls. With the Desktop servers dead, their locks were gone, and winops (still up) was used to repair:

- Killed the remaining holders: git-github-mcp's webapp backend (a standalone `uv run` started from a PowerShell window) and calibre-mcp copies hosted by Cursor and Antigravity (the IDEs restart them).
- Stopped the advanced-memory-mcp and advanced-memory-mcp-daemon NSSM services. A non-elevated `Stop-Service` worked; both were restarted afterwards.
- `uv sync --frozen --inexact --no-cache --reinstall` for filesystem-mcp, git-github-mcp, advanced-memory-mcp, virtualization-mcp and calibre-mcp. All five verify clean and pass an import test.
- **New finding: hollow dist-info folders.** An interrupted uninstall can leave `<pkg>-<ver>.dist-info` empty or holding only METADATA, with no RECORD. uv then treats the package as installed and `--reinstall` skips it ("Audited N packages"). calibre-mcp's bcrypt and orjson only came back after those folders were deleted. Delete every dist-info without a RECORD before reinstalling.

Then `fix_all.ps1` ran the same procedure (stop NSSM services pointing at the repo, kill python/uv processes running from it, delete hollow dist-info, `--no-cache --reinstall`, restart services) over all 16 venvs still failing the fleet scan. It excluded windows-operations-mcp, which was the shell doing the work.

### State at 16:13

- Fleet scan before fix_all: 227 clean, 16 damaged.
- Fixed by fix_all: agy-fleet-mcp, aiwatcher-mcp, arxiv-mcp, discord-mcp, email-mcp, fastsearch-mcp, google-docs-mcp, pywinauto-mcp.
- Services stopped and restarted (all Running): aiwatcher-mcp, arxiv-mcp, devices-mcp, discord-mcp, email-mcp, fastsearch-mcp, advanced-memory-mcp, advanced-memory-mcp-daemon. mcp-pywinauto-mcp is Running.
- All 20 Claude Desktop MCP servers announced, including fileops, gitops, memops, calibops, virtualization-mcp, winops, pywinauto-mcp and revops.
- Still damaged, held by processes that a non-elevated shell can neither see nor kill (os error 5 on a `.pyd`/`.dll`):
  - iptv-org-mcp: watchfiles (orphaned python.exe whose parent exited)
  - local-llm-mcp: watchfiles; opencv-python-headless missing 82 files
  - rustdesk-mcp: psutil, pywin32
  - speech-mcp: pywin32 (`pythoncom313.dll`), standard-aifc
  - yahboom-mcp: pywin32 (`pywintypes313.dll`)
- Not lock-related:
  - ocr-mcp: easyocr is missing 83 data files even after a clean `--no-cache` install. Suspect Defender quarantine or a wheel/RECORD mismatch; not yet investigated.
  - devices-mcp: 5 missing jupyter config json files under `etc\jupyter`. Harmless.
  - robofang: stale `openfang-0.3.0.dist-info` (editable install under a former package name). Remove it by hand.

The remaining five need an elevated run: stop the holder or reboot, then `uv sync --directory D:\Dev\repos\<repo> --frozen --inexact --no-cache --reinstall` after deleting hollow dist-info folders. `FINISH_REPAIR.cmd` does exactly this, self-elevating.

### Culprit search

No saved script that deletes venvs across repos has been found yet. Searched: every .ps1/.py/.bat/.cmd changed since 2026-09-01 under D:\Dev\repos, scripts, Desktop and Downloads; PSReadLine history (only old single-repo deletions); session logs of Claude Code, OpenCode, Cursor, Antigravity, Codex and Windsurf (only single stray-venv removals). Strongest lead: the fleet justfile `clean` recipe written by `mcp-central-docs\scripts\harmonize_p2_repos.py` (`Remove-Item -Recurse -Force .venv ... -ErrorAction SilentlyContinue`), still present in 19 justfiles. An agent running `just clean` (or the same inline delete) across repos would produce exactly this damage with no error and no script file. Unconfirmed; needs the date and tool of the sweep.

## Round 3 (16:17, elevated)

`FINISH_REPAIR.ps1` was launched elevated (UAC, explicitly allowed by Sandra). Two additions before the run: kill python/uv processes by command line as well as by loaded module, and delete hollow dist-info folders before reinstalling. Run elevated, it saw and killed the hidden holders: 2 python processes each for local-llm-mcp, yahboom-mcp, rustdesk-mcp and speech-mcp, plus the orphaned python on iptv-org-mcp. No services needed stopping.

Result (16:28): iptv-org-mcp, local-llm-mcp (full CUDA torch/cupy/ray re-download), rustdesk-mcp and yahboom-mcp verify clean.

### False positive: easyocr

ocr-mcp's "83 missing files" (`easyocr/dict/*`) are not damage. The official `easyocr-1.7.2-py3-none-any.whl` on PyPI contains zero `easyocr/dict/` entries while its own RECORD lists 83. A fresh install into a throwaway venv reproduces it; Defender shows no detections. Upstream packaging bug, ignore.

### Gap found: optional extras deleted entirely

speech-mcp still lacked `aifc` after its reinstall. It runs Python 3.13, where aifc left the stdlib, so standard-aifc comes in via librosa/audioread. Investigation showed the venv had the sherpa, qwen-tts and kokoro extras intact, but **the funasr extra (FunASR, the main STT engine) had lost funasr, modelscope and torchcodec**, and audioread was gone too.

Root cause of the gap: every repair pass ran `uv sync` with the default dependency set. Packages that belonged only to an optional extra and were deleted together with their dist-info leave no trace, so `verify_venv.py` (RECORD-based) cannot see them and the default sync does not reinstall them.

Fix: `extras_audit.py` (stdlib only) reads each repo's `[project.optional-dependencies]` and flags an extra for restore when some of its direct deps are installed and others are missing; partial presence means the extra was in use. `extras_fix.ps1` then runs `uv sync --frozen --inexact --no-cache --extra <x>` for the flagged extras, across all repos with a venv and a lockfile. Report: `temp\venv_repair\extras_report.txt`.

Limits:
- An extra whose packages were all deleted cannot be told apart from one that was never installed; those stay missing until a server fails on import.
- Shared deps (numpy, torch, soundfile) can make an unused extra look partial, so a few extras may get installed that were not there before. Additive and reversible.

### Round 3 results (16:55)

- RECORD scan (`final_scan2.txt`): 240 clean, 3 flagged, all known non-damage (devices-mcp jupyter config json, ocr-mcp easyocr upstream wheel bug, robofang stale `openfang-0.3.0.dist-info`).
- Partial-extras pass (`extras_report.txt`, done 16:49) restored functional extras: speech-mcp funasr (funasr 1.4.2, modelscope, torchcodec; with audioread and standard-aifc, aifc imports again), advanced-memory-mcp voice (43 packages incl. faster-whisper, kokoro), arxiv-mcp rag (pylance), audio-studio-mcp cuda, local-llm-mcp full, health-mcp webapp, leanforge-mcp web, openclaw-molt-mcp webapp-api, moltbot-mcp web. The rest were dev/test tool extras (pytest, ruff, mypy, pre-commit), restored where partially present.
- Declared-extras pass (`extras_declared.txt`, running) installs the extras each repo's justfile, start scripts, NSSM AppParameters, Claude config, manifest or README names. 50 repos with extras declare none anywhere. For those, the import smoke is the only check left.
- Repos with functional extras that neither pass installed, so the import smoke decides: ocr-mcp (ml, webapp, scanner), devices-mcp (labels, climate, voice), database-operations-mcp (ai), email-mcp (anthropic), gimp-mcp (http), blender-mcp (monitoring), function-generator-mcp and multimeter-mcp (serial), loona-mcp (adb, gpio).

### Lockfiles

- Deleted: none. No repo with a git-tracked `uv.lock` lost it. dj-media-hub, fleet-tool-bridge and rust-test-c never had one committed (rust-test-c is a throwaway per Sandra).
- Commits since 2026-10-10 that dropped 3+ lock packages or 2+ pyproject deps:
  - google-ai-mcp, 2026-10-29 `wip(auto)`: google-cloud-aiplatform dropped, google-genai bumped to >=2.6. Looks like a deliberate migration, but committed under an auto message; review.
  - publictransport-mcp, 2026-10-18: "cut Postgres", deliberate.
  - bakemono-runter, 2026-10-13 `wip(auto)`: lock lost 76 packages. Not sweep damage: `pyproject.toml` was created 2026-10-02 with `dependencies = []` although `server.py` imports fastmcp and pydantic; the auto-commit relocked from the empty list. Needs fastmcp and pydantic declared and a relock.
- Risk: `wip(auto)` auto-commits commit whatever state they find, so damage from a future incident lands in history looking like a normal change, and a git-state audit then reports it clean.

## Round 4: extras and import smoke (16:43 to 18:00)

### Declared-extras pass

`extras_declared.ps1` installed the extras each repo names in its justfile, start scripts, NSSM AppParameters, Claude config, manifest or README (`--all-extras` where a launcher uses it). 50 repos with optional extras declare none anywhere; for those the import smoke decides. One failure: stems-mcp declares `cpu` and `gpu` as conflicting extras and the pass requested both; installed `gpu` (plus `dev`) by hand, including onnxruntime-gpu.

### Import smoke

`import_smoke.py` imports every module of every package a repo ships, inside that repo's own venv, and records `ModuleNotFoundError` names. Harness bug found and fixed on the way: MCP stdio servers close or replace stdout on import (protecting the protocol channel) and some call `sys.exit`/`os._exit`, so the result line never appeared ("SMOKE FAILED TO RUN"). Results are now written to `smoke_json\<repo>.json` after every module, and exit calls are neutralised during imports.

Result (17:50): 243 repos with a venv, 225 import completely. Fixed during this round:
- mcp-studio: passlib, then pandas, numpy, tzdata, tomli via `uv pip install -r requirements.txt` (its declared requirements file). Now 40/40 modules.
- devices-mcp: structlog (declared in `requirements-watchfiles.txt`).

Remaining 17, none of them declared in `pyproject.toml`, `uv.lock` or an extra, so nothing was installed for them (decision for Sandra):

| Repo | Missing | Classification |
|---|---|---|
| avatar-mcp | cv2, pyttsx3, pyvrm, aiohttp | undeclared third-party |
| avatar-pipeline-mcp | fastapi | undeclared third-party |
| calibre-mcp | spacy; calibre_plugins | spacy undeclared; calibre_plugins exists only inside Calibre |
| devices-mcp | torch; toml, aiocache; ring_mcp | torch only via the `voice` extra (openai-whisper); toml/aiocache undeclared; ring_mcp is a stale internal import |
| ednaficator | aiofiles, aiohttp | undeclared third-party |
| local-llm-mcp | docker | undeclared (vllm_v1 docker_manager) |
| multi-backup-mcp | psutil | undeclared |
| vrchat-mcp | psutil | undeclared (system plugin) |
| bakemono-runter | fastmcp | undeclared; its package is identical to `this-is-intentionally-broken-for-testing`, so it looks like a copy of the broken test fixture |
| documentation-mcp | fastmcp_version | broken internal import |
| publictransport-mcp | data_loader | broken internal import |
| teleconference-mcp | contacts_substrate, conferencing_mcp | broken internal imports (monorepo packages not on path) |
| freecad-mcp | FreeCAD | exists only inside FreeCAD, expected |
| this-is-intentionally-broken-for-testing | fastmcp | broken by design |
| vroidstudio-mcp-backup-20260607-231839 | fastapi | old backup copy |
| mcp-server-template, demo-app | aiohttp / fastapi | templates |

Most of these venvs probably had the packages pip-installed by hand before the sweep; the sweep removed them and nothing declared can bring them back. The durable fix is declaring each dependency in `pyproject.toml` and relocking.

### Auto-commit source

The `wip(auto)` and "fleet: hourly sync" commits come from `mcp-central-docs\scripts\Invoke-FleetWipSweep.ps1` (Task Scheduler `\Fleet\WipSweep`, daily 04:00): it commits and pushes every dirty file in every repo. It does not delete venvs (`git rm --cached` only untracks), so it is not the culprit, but it is how a damaged lockfile reaches origin looking like normal work. It already parks zeroed launcher configs for human review (BUG-089); an equivalent guard for `uv.lock`/`pyproject.toml` losing dependencies is proposed, not yet implemented.
