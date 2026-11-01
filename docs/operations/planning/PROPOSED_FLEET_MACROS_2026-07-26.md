# Proposed Fleet Macros / SOPs / Skills

**Date:** 2026-07-26
**Author:** drafted during the NSSM/LocalSystem incident (see `troubleshooting/2026-07-26_nssm-localsystem-ambient-path-resolution.md`)
**Status:** proposals, not yet implemented
**Tags:** [mcp-fleet, macros, sop, standardization, proposal]

Every idea below is grounded in something that actually cost time or caused damage on
2026-07-26, with the evidence stated. Nothing here is speculative tidiness.

Each entry states the **script/LLM split** deliberately. The rule from that session:
a fully specified check should be a script (fast, cheap, reproducible, gate-able); an
unspecified judgment should be an LLM step. Macros that blur the two waste tokens on
mechanical work and apply false rigour to judgment calls.

---

## 1. `twindrift` — stale mcpb/src build artifacts

**Trigger:** `twindrift` (fleet) / `twindrift <repo>`
**Priority: HIGH**, but the fix is simpler than first assumed. See the correction below.

**Evidence (measured 2026-07-26):**

| | count |
|---|---|
| repos with both `src/` and `mcpb/src/` | 110 |
| identical `.py` twins | 668 |
| drifted twins | 315 |
| &nbsp;&nbsp;of which mcpb is **older** than src (stale build output) | **311** |
| &nbsp;&nbsp;of which mcpb is **newer** by mtime | 4 |

Worst: `calibre-mcp` 101, `blender-mcp` 68, `arxiv-mcp` 35, `pywinauto-mcp` 32, `osc-mcp` 29.

### Correction to the first draft of this section

The initial read was "316 forks needing reconciliation, decide which side is canonical".
**That was wrong.** `mcpb/src` is not a parallel source tree; it is a **build artifact**,
produced by copying repo `src/` into `mcpb/src/` as the preliminary step before packaging
with the `mcpb` CLI. Drift therefore means one thing only: *the copy step has not run since
src last changed.*

The 4 mtime-newer cases were investigated and are **not** hand-edited artifacts. AST
comparison of the two `blender-mcp` files showed `src` is a strict superset:

```
blender_mcp/cli.py     only in src: list_available_tools, show_configuration   only in mcpb: (none)
blender_mcp/config.py  only in src: _find_default_blender                      only in mcpb: (none)
```

mcpb contains nothing unique. The newer mtimes are an artifact of a git checkout or a bulk
touch, not authorship. **mtime is not a reliable signal here; content is.** There is no work
to rescue, and no reconciliation is needed.

### The actual root cause

`mcpb/src` is **committed to git** in most repos:

| repo | gitignored | tracked files under mcpb/src |
|---|---|---|
| calibre-mcp | no | 447 |
| blender-mcp | no | 96 |
| arxiv-mcp | no | 52 |
| advanced-memory-mcp | no | 14 |
| fleet-agent-mcp | no | 8 |
| **pywinauto-mcp** | **yes** | **0** |

A derived directory under version control is guaranteed to go stale, because git faithfully
preserves whatever snapshot was last committed and nothing forces a rebuild. `pywinauto-mcp`
already gitignores it and is the correct pattern.

### Recommended standard (removes the category rather than fixing 315 files)

1. **`mcpb/src` is derived. Never edit it.** Fix `src/`, then rebuild.
2. **Gitignore `mcpb/src`** across the fleet, matching `pywinauto-mcp`.
3. **Rebuild the copy as part of packaging**, so the artifact cannot be stale at package
   time by construction.
4. The macro then reduces to two cheap assertions: is `mcpb/src` gitignored, and was it
   regenerated in this build. Both scriptable, both `ship`-gate candidates.

**Script part:** the two assertions, plus the hash comparison for repos not yet migrated.

**LLM part:** nearly none now. This turned out to be a hygiene/standards problem, not a
judgment problem, which is itself the useful lesson: the first framing would have spent a
lot of model attention reconciling files that only needed a `.gitignore` line.

### Caveat on the 1126 "mcpb-only" files

Not all of these are stale leftovers. Some repos flatten the layout during packaging
(`fleet-agent-mcp` has `mcpb/src/config.py` against `src/fleet_agent/config.py`), so
relative paths do not line up and a naive comparison misreports them as mcpb-only. Any
implementation must compare per-repo layout rather than assuming a mirrored tree.

---

## 1b. `mcpbcheck` — does the packaged artifact actually import?

**Trigger:** `mcpbcheck <repo>` / folded into `ship` as a gate
**Priority: HIGHEST.** This is the one that ships broken packages.

Discovered 2026-07-26 while investigating twindrift. The `src/` -> `mcpb/src/` copy step
**flattens the package directory in some repos**, copying the *contents* of
`src/<package>/` into `mcpb/src/` instead of copying `src/<package>/` to
`mcpb/src/<package>/`. The result is a package that cannot import itself.

### Measured

Emulating exactly what `run_server.py` does (`sys.path.insert(0, mcpb/src)`) and then
resolving the entry-point import:

| repo | import | resolves from mcpb/src | verdict |
|---|---|---|---|
| arxiv-mcp | `arxiv_mcp` | yes (`mcpb/src/arxiv_mcp/__init__.py`) | OK |
| blender-mcp | `blender_mcp` | yes (`mcpb/src/blender_mcp/`) | OK |
| **fleet-agent-mcp** | `fleet_agent` | **NOT FOUND** | **BROKEN** |
| **advanced-memory-mcp** | `advanced_memory` | **NOT FOUND** | **BROKEN** |

Confirmed from a second angle: `fleet-agent-mcp/mcpb/pyproject.toml` declares
`[tool.hatch.build.targets.wheel] packages = ["src/fleet_agent"]` and its ruff
`per-file-ignores` reference `src/fleet_agent/...`. The packaging config expects the nested
layout that the copy step failed to produce, so hatch cannot find the package either.

These packages only appear to work when the real package happens to be installed in the
environment already, which defeats the entire point of packaging.

### Second, independent fault in the same file

`fleet-agent-mcp/mcpb/run_server.py` calls `uvicorn.run(app, ...)` but never imports
uvicorn. Its imports are `__future__, _strptime, os, pathlib, sys, fleet_agent`. Straight
`NameError` at runtime the moment execution gets past the import line. This has presumably
never been executed successfully.

### Related pollution in the same directories

`mcpb/src` in the affected repos also contains committed `__pycache__` output for **two**
Python versions (`config.cpython-312.pyc` and `config.cpython-313.pyc`) and `.bak` files.
A build artifact directory accumulating compiled bytecode for multiple interpreters and
editor backups is further evidence the copy step is not a clean regeneration.

### Checks the macro must perform

1. Resolve the entry point's top-level import with only `mcpb/src` on `sys.path`. Fail if
   it does not resolve *from that directory*.
2. Assert every module referenced in `mcpb/pyproject.toml`
   (`tool.hatch.build.targets.wheel.packages`) exists at the declared path.
3. AST-check the entry point: every module used at call sites is actually imported.
   (This alone catches the uvicorn `NameError`.)
4. Assert no `.pyc`, `__pycache__`, or `.bak` under `mcpb/`.
5. Ideally, actually launch the packaged entry point in a clean environment and assert it
   serves. A static check cannot prove a package runs.

**Script part:** all five. This is entirely mechanical and belongs in `ship` as a hard gate.

**LLM part:** none for detection. Judgment is only needed for *repair*, deciding whether a
given repo's layout difference is deliberate.

### Fix

The copy step must preserve the package directory:

```
src\<package>\  ->  mcpb\src\<package>\        correct
src\<package>\* ->  mcpb\src\                  flattened, broken
```

Combined with the `mcpb/src` gitignore recommendation above, the artifact then gets
regenerated correctly at package time and cannot silently rot.

**Repos needing repair as of 2026-07-26:** `fleet-agent-mcp`, `advanced-memory-mcp`.
Unknown for the other ~106 repos with an `mcpb/` tree; the macro should sweep them.

---

## 2. `pathaudit` — ambient path resolution scan

**Trigger:** `pathaudit` / `pathaudit <repo>`

**Evidence:** the entire 2026-07-26 incident. Four servers affected
(`advanced-memory-mcp` ~71 notes orphaned 12 days, `fleet-agent-mcp` two live divergent
databases, `arxiv-mcp` two corpus files, `devices-mcp` stale profile dir). Root cause in
every case was a storage path resolved from ambient process state.

**What it scans for:**
- `Path.home()`, `os.path.expanduser("~")`, `%USERPROFILE%`, `%APPDATA%` in server code
- `Path.cwd()` used for storage defaults
- relative `env_file="..."` in pydantic-settings (silently fails to load under a service)
- **empty-valued env vars** in `.env` (`KEY=`), which pydantic coerces to `Path(".")` rather
  than `None`, producing a relative data dir
- class-body-computed path defaults (`db_path: Path = data_dir / "x.db"`), which do not
  follow an overridden `data_dir`
- absence of a startup log line stating the resolved absolute storage path

**Script part:** the grep patterns and the NSSM env-pin check. Already half-built as
`scripts/audit-nssm-env.ps1`; extend it to scan source, not just service config.

**LLM part:** deciding whether a given `Path.home()` is legitimate. Not all are wrong: in
`DEEPLINK_STANDARD.md` it correctly resolves a per-user install location and always runs in
user context. `aiwatcher-mcp` anchors on `Path(__file__).parents[2]` and is clean. A script
would flag both; only judgment separates them.

---

## 3. `whoruns` — port/service/process/config resolution

**Trigger:** `whoruns <port|service|repo>`

**Evidence:** on 2026-07-26 a large share of diagnosis time went on manually chaining
`netstat -ano` → `Get-CimInstance Win32_Process` → `sc qc` → `reg query ...\Parameters`
to answer "which process actually holds port 10705, under which account, from which
binary, reading which config, writing to which directory". That question was asked at
least six times and answered by hand every time.

**Output, one table:** port → PID → binary → command line → service account → NSSM env →
resolved data dir → process start time → source tree mtime.

**Script part:** all of it. This is pure mechanical joining of five commands.

**LLM part:** essentially none, which is exactly why it should be a script that a skill
merely invokes. Good example of resisting the temptation to LLM everything.

**Note:** owner/command line come back empty for processes in a security context the
current session cannot query. That emptiness is itself a signal (it means SYSTEM/elevated)
and the tool should say so rather than printing blanks.

---

## 4. `staleproc` — is the running process running the current code?

**Trigger:** `staleproc` / included in `whoruns`

**Evidence:** twice on 2026-07-26 a fix was applied and appeared not to work. Both times the
running process predated the edit. `knowledge_router.py` was fixed at 03:17:36 while the
backend serving it had started at 02:58:27. Separately, `advanced-memory-mcp` reported the
same PID (4928) across what was believed to be a restart, because restarting Claude Desktop
does not restart an NSSM service.

**Check:** for each running fleet service, compare process start time against the newest
mtime in its source tree. Flag any process older than its code. Also flag "PID unchanged
across a restart attempt".

**Script part:** all of it.

**LLM part:** none. Another pure-script case.

**Value:** this single check would have saved well over an hour and prevented two wrong
conclusions ("the fix didn't work", "the watcher crashed").

---

## 5. `bootcheck` — startup contract compliance

**Trigger:** `bootcheck <repo>`

**Evidence:** the single highest-value line of code identified in the incident postmortem
was a startup log stating the resolved absolute storage path. No fleet server had one.
Adding it to `advanced-memory-mcp` (`DB location` in `adn_nav status`) turned a class of
multi-hour investigation into a one-call answer.

**Proposed startup contract**, verified by this macro:
1. Log resolved absolute storage path(s) once at INFO on boot
2. Log version, port, and transport
3. Expose the same in a `status`/`health` tool
4. Never return bare `success: true` from a write whose visibility depends on a separate
   index/sync step; report the target or the index status
5. Fail loudly on unresolvable config rather than silently falling back

**Script part:** static checks 2 and 3 (does a health endpoint exist, does it include paths).

**LLM part:** checks 1, 4, 5 need reading the code and judging whether the fallback is
silent. Item 4 in particular is a semantic judgment about API honesty.

---

## 6. `dupefind` — duplicated canonical documents

**Trigger:** `dupefind` (fleet-wide)

**Evidence:** `assfix` existed twice in `mcp-central-docs` (`skills/assfix` and
`.agents/skills/assfix`), created 39 minutes apart, already diverged (11589 vs 11091 bytes,
different hashes). Two copies of a checklist means two truths, and an agent following the
stale one performs the wrong audit with full confidence.

Generalises `twindrift` beyond `src`/`mcpb` to any duplicated SOP, skill, standard, or
config across the fleet.

**Script part:** hash-and-group by filename and by content similarity.

**LLM part:** decide which copy is canonical, and whether to merge, stub, or delete. The
resolution used on 2026-07-26 was to reduce the stale copy to a pointer stub rather than
delete it, preserving history while removing the second truth. That choice is judgment.

---

## Sequencing

These compose with the existing chain rather than replacing it:

```
drift        which repos need attention
  -> pathaudit / twindrift / staleproc   what specifically is wrong (mostly scripted)
  -> fakefind                            is the UI real
  -> qualitycheck                        is the repo worth the effort
  -> assfix                              fix it
  -> bootcheck                           does it meet the startup contract
  -> ship                                release
```

**Gate candidates for `ship`:** `twindrift` (a drifted twin means you are shipping a known
bug back), `pathaudit`, and `audit-nssm-env.ps1`. All three are scriptable and cheap.

---

## Deliberately not proposed

- **A macro that mass-fixes across repos.** `TRAPS_AND_PITFALLS.md` trap 7 already records
  that batch scripts wreck files and the rule is one repo at a time. Any of the above that
  fixes rather than reports should be per-repo and approval-gated, exactly as `fakefind` was
  revised to be read-only on 2026-07-25.
- **`.bak` cleanup as a macro.** Editing tools generate `.bak` files prolifically and the
  fleet has accumulated many. This is real hygiene but is a one-off `Remove-Item` with a
  date filter, not something needing an LLM or a standing macro. Measure before automating.
