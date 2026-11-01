---
title: "One-Click Install UX Standard"
category: standard
status: draft
audience: mcp-dev
last_updated: 2026-10-05
related:
  - standards/NAKED_PC_INSTALL_STANDARD.md
  - standards/AGENT_INSTALL_REFERENCE.md
  - standards/PACKAGING_STANDARDS.md
  - standards/LLM_AND_INSTALL_TIERS.md
  - getting-started/NAKED_INSTALL_TESTING.md
# status: draft -- spec only, nothing implemented. Pilot repo must pass the
# acceptance criteria in section 9 before this moves to active.
---

# One-Click Install UX Standard

**One-line rule:** a stranger (or their AI agent) gets from `git clone` to a working server with one command,
can ask "will this work here?" before anything is installed, and is never left guessing what is happening.

---

## 1. Why this exists

Our install *plumbing* is covered: winget prereq guards, uv path resolution, import smoke test, health-wait
(`NAKED_PC_INSTALL_STANDARD.md`), the two distribution tracks (`PACKAGING_STANDARDS.md`), and doc roles plus
Options A-D (`AGENT_INSTALL_REFERENCE.md`). What we lack is the *experience layer* on top of it.

Reference implementation: **Strata** (github.com/Niko1221/Strata, reviewed at v0.1.39, 2026-10-05). It went from
zero to ~12k stars in 11 days, largely because installing a 125B-model stack is one double-click. The pieces we
are adopting are listed in section 3; none of them are model-specific.

The second driver is the shift already recorded in `NAKED_PC_INSTALL_STANDARD.md` section 7b: users increasingly
install by pasting a repo URL into their coding agent. An agent with no install contract improvises. This
standard gives the agent a contract (`docs/AI_SETUP.md`, `-Check`, `-Yes`) so it does not have to.

## 2. Scope

| Repo class (per AGENT_INSTALL_REFERENCE section 3) | Applies? |
|---|---|
| MCP hand **with** webapp / backend (`start.bat` track) | **Yes, all sections** |
| MCP hand, stdio only (mcpb track only) | Sections 6 (AI_SETUP.md) and 8 (expectations) only |
| Control plane (robofang), isolation stack (deepfang) | Sections 4, 5, 6 recommended; adapt to their own install docs |
| Agent gateway / bridge to upstream | No - follow upstream |

This standard **does not replace** Options A-D, the mcpb track, or the Tauri NSIS track. It upgrades the
script path (`start.bat` + `start.ps1`) and adds an agent-facing install doc.

## 3. What we adopt from Strata (and what we do not)

| Strata feature | Adopt? | Fleet section |
|---|---|---|
| One idempotent entry point: install, resume, or start depending on state | Yes | 4 |
| `--check`: diagnose the machine, install nothing | Yes | 5 |
| `--yes`: every question has a hardware-derived recommended default | Yes | 5 |
| `docs/AI_SETUP.md`: install instructions written for the installing agent | Yes | 6 |
| Self-management MCP tools (status / install-plan-confirm / start / stop / logs / connect) | Yes, but fleet-level, not per repo | 7 |
| "This will look frozen for 1-3 min, that is normal" + symptom->fix on the README | Yes | 8 |
| `UPDATE.bat` (update without starting) | Optional | 4 |
| Bundling models / multi-GB downloads in the installer | **No** - conflicts with LLM_AND_INSTALL_TIERS ("never ship monsters") | - |
| Translated READMEs | Not now | - |

## 4. Single idempotent entry point

**4.1 One front door.** `start.bat` (forwarding `%*` to `start.ps1`) is the one documented entry for the
script track. README quick start shows exactly this one command. Other surfaces (mcpb, NSIS, just) stay, but
are not presented as alternatives on the README front page.

**4.2 State machine, not a script.** Every run detects state and does the next needed thing:

| Detected state | Action |
|---|---|
| Prereqs missing | winget install (existing `Require-Command`) |
| `.venv` / `node_modules` missing or incomplete | `uv sync` / `npm install` (existing guards) |
| Install complete, server not running | start |
| Server already running on its port | report URL and exit 0 (existing `-ReuseIfRunning` semantics become the default for start.bat) |
| Previous run interrupted | resume - each step checks its own completion, no "clean install" required |

Rerunning `start.bat` after any failure MUST be a safe, correct first response. The failure message says so.

**4.3 Optional `update.bat`:** `git pull` (or zip re-download instructions) + `uv sync` + `npm install`, never
starts the server. Only for repos with frequent releases.

## 5. Flags: `-Check`, `-Yes`, `-NoStart`, `-Json`

PowerShell 5.1 switch style (fleet launchers are PS, not `--double-dash`); `start.bat` forwards them. These
extend the existing `templates/fleet-start.ps1` param block (`-Headless`, `-BackendOnly`, `-FrontendOnly`,
`-NoBrowser`, `-ReuseIfRunning`, `-SkipRestart`), they do not replace it.

### 5.1 `-Check` - diagnose only

Installs nothing, writes nothing outside a temp file, starts nothing. Reports:

| Check | Example result |
|---|---|
| OS / PowerShell / winget present | `ok` / `missing: winget (Windows 10 1809+ required)` |
| Each prereq: present, or installable via winget id | `uv: missing, will install astral-sh.uv` |
| Ports from `operations/WEBAPP_PORTS.md`: free / held by us / held by something else | `10720: held by pid 4242 (python.exe)` |
| Disk free vs. what the install needs | `needs ~400 MB, 120 GB free` |
| Wrappee / host app detected (Blender, Plex, ...) | `Blender 4.2 found at ...` / `not found - see INSTALL.md` |
| LLM tier available (LLM-enabled repos) | `Ollama running, 3 models` / `no local LLM, cloud key not set` |
| Hardware gates, only if the repo has them (GPU, RAM) | `RTX 4090 24 GB` |
| **Verdict** | `READY` / `READY WITH WARNINGS` / `BLOCKED: <one line why>` |

Exit codes: `0` ready, `2` ready with warnings, `1` blocked. `-Check -Json` prints the same as one JSON object
for agents and for the lifecycle tool (section 7).

### 5.2 `-Yes` - no questions

Every interactive prompt MUST have a recommended default derived from the machine (detected LLM tier, free
ports, available host app). `-Yes` takes all defaults. When stdin is not interactive, behave as `-Yes` and say
so in one line. A prompt that cannot have a safe default (e.g. a cloud API key) is skipped with a printed
"set X later in <file>" note, never blocks.

### 5.3 `-NoStart`

Install / repair only; exit when ready. Required for agents, because a foreground server blocks their shell.

## 6. `docs/AI_SETUP.md` - the install doc for agents

New file, new row in the AGENT_INSTALL_REFERENCE section 4 doc-roles table:

| File | Audience | Max size | Contains |
|---|---|---|---|
| `docs/AI_SETUP.md` | An AI agent asked to install the repo for a user | ~100-200 lines | Ground rules, check, decide, install non-interactively, verify, connect, stop conditions |

README gets one paste-able line for users of coding agents:

```text
Set up <repo> on this PC for me: https://github.com/sandraschi/<repo> - follow docs/AI_SETUP.md in that repository.
```

Required sections, in order:

1. **Ground rules.** What the agent must not do: change system settings beyond the listed winget prereqs,
   install drivers or host apps without asking, expose a server beyond `127.0.0.1` without an API key,
   kill a long, quiet step. Tell the user in plain words what is happening.
2. **Check.** `start.bat -Check -Json`; how to read the verdict; stop and report on `BLOCKED`.
3. **Decide.** A table from detected situation to choice (LLM tier, host app present or not, port conflicts).
   Mirrors the defaults `-Yes` would pick, so the agent can explain them.
4. **Install.** `start.bat -Yes -NoStart` (run in background / long timeout, rerun = resume).
5. **Start and verify.** How to start detached, the health URL, expected time to healthy.
6. **Connect.** The MCP client config block (from AGENT_INSTALL_REFERENCE section 16), webapp URL.
7. **Stop conditions and where the log is.** When to stop and hand back to the user, and which log file to
   quote. Never "fix" by editing the repo's source.

AI_SETUP.md is untrusted input for *other people's* agents: keep it free of anything an agent should not
execute blindly (no `curl | iex`, no elevation, no disabling security features).

## 7. Lifecycle MCP tools - fleet-level, not per repo

Strata ships `tools/strata_mcp.py`: a stdlib-only MCP server with `status`, `models`, `install` (plan first,
`confirm: true` to act), `start`, `stop`, `logs`, `benchmark`, `connect_info`. That is the right shape, but
150 copies of it would be 150 places to drift.

**Fleet design (proposed):** one lifecycle portmanteau in a single fleet infra MCP, driving every repo through
its own `start.bat -Check -Json` / `-Yes -NoStart` / health URL / log path.

| Operation | Behaviour |
|---|---|
| `status` | Installed? Running? Port, PID, health, version. Wraps `-Check -Json` + health probe |
| `check` | `-Check -Json` verbatim |
| `install` | Without `confirm=true`: returns the plan (prereqs to install, disk, ports, defaults chosen). With it: runs `-Yes -NoStart` in background; a second call reports progress |
| `start` / `stop` | Detached start + wait for health; stop via the repo's own mechanism (NSSM services: `sc.exe`, never taskkill) |
| `logs` | Tail of the repo's install / server log |
| `connect_info` | MCP client config block + webapp URL |

Per-repo requirement is therefore only: honour the flags in section 5 and print one machine-readable log path.

**Host options (2026-10-05 survey, decision pending - section 10 #2):**

| Option | For | Against |
|---|---|---|
| `meta_mcp` | Already has `start_fleet_app` / `stop_fleet_app` / `list_fleet_apps`, a fleet manifest that resolves start scripts, sandboxed cold-install probes and startup probes. Least new code | ~100 tools and a full webapp + Tauri stack: a stranger would have to install meta_mcp before they can install anything else. Fine for Sandra's machines, wrong for the public path |
| New `lifecycle-mcp` (lean, public) | Can be stdlib-only like Strata's `strata_mcp.py`, so it runs on a naked PC before uv/node exist; natural home for the tier manifest (section 7a); no dependency on private mcp-central-docs (NAKED_PC section 8) | One more repo (New Repo Gate applies); must not duplicate meta_mcp's launcher |
| **Hybrid (recommended)** | Lean public `lifecycle-mcp` owns check / install / start / stop / tiers. `meta_mcp` keeps its dashboard and delegates its fleet-app tools to it instead of reimplementing | Two repos to keep in step; mitigated by meta_mcp calling lifecycle-mcp, never copying it |

## 7a. Install a tier

A **tier** is a named, versioned set of repos that install together (e.g. `robotics`, `media`, `local-llm`).
Built on section 7, not beside it:

- **Tier manifest** (public, in the lifecycle host repo): tier name, repos with pinned tags, per-repo port from
  `operations/WEBAPP_PORTS.md`, shared prereqs (deduplicated: one winget pass for the whole tier), external
  host apps the tier expects (Blender, ROS, ...) - detected and reported, never bundled.
- **`check(tier=...)`** runs every member's `-Check -Json` and returns one verdict plus per-repo lines, and
  flags port collisions *between* members before anything is installed.
- **`install(tier=..., confirm=true)`** installs members in dependency order with `-Yes -NoStart`; one member
  failing does not roll back the others, the report says which ones are ready.
- **`start(tier=...)` / `stop(tier=...)`** for the running set.
- A tier is only as good as its weakest member: a repo joins a tier only after it passes section 9 step 4
  acceptance on its own.

First tier candidate: `local-llm` (local-llm-mcp + Strata as an external, detected-not-bundled backend).

## 8. Expectations and first-aid on the page

- **Say what is slow before it is slow.** Any step that can exceed ~20 s prints what it is doing, roughly how
  long it takes, and "this is normal, don't close the window" (first `uv sync` with torch, first `npm install`,
  first model pull).
- **README "Something went wrong?" block**, at most ~10 lines, the top 3-4 symptoms with a one-line fix each,
  ending with a link to `docs/TROUBLESHOOTING.md` and "attach `<log path>` to the issue". This is the one
  allowed exception to "troubleshooting lives in TROUBLESHOOTING.md".
- **Every failure prints the fix next to the error** (already NAKED_PC section 7b spirit) **and "rerunning
  start.bat is safe"**.
- **One log file per run** at a fixed, printed path, so users and agents attach the same thing.

## 9. Rollout

1. **Prerequisite - consolidate the base standards.** `NAKED_PC_INSTALL_STANDARD.md`,
   `AGENT_INSTALL_REFERENCE.md` and `PACKAGING_STANDARDS.md` are all still `status: review` (bulk add
   2026-09-18, unverified). NAKED_PC also has a stray front-matter block and broken code fences. Verify and
   activate them first; this standard builds on them.
2. **Template.** Extend `templates/fleet-start.ps1` (+ `FleetStartMode.ps1`) with `-Check`, `-Yes`,
   `-NoStart`, `-Json`; add `templates/AI_SETUP.md`. Standalone mode (NAKED_PC section 8) must support all
   flags without mcp-central-docs present.
3. **Pilot: `local-llm-mcp`.** Real outside users, LLM tiers, port registry, and it fronts Strata next.
4. **Acceptance (pilot):**
   - Windows Sandbox consumer (`getting-started/NAKED_INSTALL_TESTING.md`): `start.bat -Check` gives a correct verdict *before*
     any prereq exists, and installs nothing.
   - `start.bat -Yes` from a naked sandbox reaches healthy with zero prompts.
   - Killing the install midway and rerunning `start.bat` completes without manual cleanup.
   - A fresh Claude Code / opencode session given only the README paste line installs and connects the server
     by following AI_SETUP.md, without improvising outside it.
   - Second run on an installed, running machine: reports URL, exits 0, starts nothing.
5. **assfix.** Add the section 4-8 items to the assfix checklist; roll out repo by repo through assfix only.
   Batch limits apply (max 10 files per operation, `.bak` before 3+ file mutations). No fleet sweep.

## 10. Open decisions

| # | Question | Default if undecided |
|---|---|---|
| 1 | Entry name: keep `start.bat`, or rename/alias to `START-HERE.bat` (self-explanatory for non-devs) | Keep `start.bat`; optional `START-HERE.bat` alias in pilot only |
| 2 | Which fleet MCP hosts the lifecycle portmanteau (section 7): meta_mcp, new lean lifecycle-mcp, or hybrid | Recommended: hybrid. Decide before pilot step 4 |
| 3 | ~~Fleet-level "install a tier" front door~~ | **Decided 2026-10-05: in scope**, section 7a, after the single-repo pilot passes |
| 4 | Linux / macOS (`start.sh`) parity | **Decided 2026-10-05: later.** v1 is Windows-only; keep flag names and JSON shapes OS-neutral so v2 adds scripts, not a new contract |

## 11. Changelog

| Date | Change |
|---|---|
| 2026-10-05 | Draft from Strata review (v0.1.39). Spec only, not implemented. |
| 2026-10-05 | Tier install moved into scope (7a); Linux/macOS deferred; lifecycle host options surveyed (7). |
