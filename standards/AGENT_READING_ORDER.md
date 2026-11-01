---
title: "Agent Reading Order"
category: standards
status: active
audience: all-agents
last_updated: 2026-09-18
---

# Agent Reading Order

**Every agentic IDE working in this fleet reads this file.** Claude Code, OpenCode,
Antigravity (agy), Cursor, Cline, Windsurf and Zed all get here through their own rules
file; the per-tool files are thin pointers, this is the content.

## Why this file exists

The mandatory reading list used to live only in a personal, machine-local
`~/.claude/CLAUDE.md`. That file is read by exactly one tool, is not version
controlled, and is invisible to every other IDE -- so six of the seven agents working
this fleet had no idea a standards library existed. There are **124 files** under
`standards/`; without an ordering they are unusable, and an agent that cannot find them
reinvents decisions the fleet already made.

Anything an agent must know belongs here, in git, reachable from every tool.

---

## 1. The AGENTS.md chain (read in this order)

`AGENTS.md` is a **locational** convention: an agent loads the nearest one and walks up.
That means a file named `AGENTS.md` deep inside a content directory is *not* delivered
by the convention, whatever its name implies.

| Order | File | Contains |
|---|---|---|
| 1 | `<repo>/AGENTS.md` | This repo: identity, key files, ports, transports |
| 2 | `D:\Dev\repos\AGENTS.md` | Fleet navigation map **and the hard rules that must not wait for a pointer** |
| 3 | `mcp-central-docs/AGENTS.md` | Documentation hub entry |
| 4 | `mcp-central-docs/standards/AGENTS.md` §9 | **Critical Don'ts** -- the full list |
| 5 | `mcp-central-docs/standards/AGENT_PROTOCOLS.md` | Tool routing, module index |

Item 4 is a reference document, not an auto-loaded one. Read it deliberately.

## 2. Before any coding task -- the Primary Read List

Thirteen files. Not from memory, not extrapolated from another repo.

| # | File | Why |
|---|------|-----|
| 0 | `standards/RUST_ARTCRAFT_STANDARD.md` | **2026-10-17 Red-Letter Regime Change:** Pure-Rust ArtCraft 3-tier architecture (`L1 core` -> `L2 CLI+MCP` / `L3 in-process Tauri`). **Supersedes Python/FastMCP/Starlette/port-claiming standards (#4, #5, #6, #11) for all Rust repos (`Cargo.toml` at root)** |
| 1 | `standards/STANDARDS_BAR.md` | Version floor, retired tools, Dual-Track bar (Pure-Rust ArtCraft track vs Legacy Python/FastMCP track) |
| 2 | `standards/AGENTS.md` | Environment, tool routing, naming, critical don'ts |
| 3 | `standards/GIT_REPOSITORY_SAFETY.md` | git-first rule, checkpoint commits, batch edit gates |
| 4 | `standards/TOOL_DESIGN_STANDARDS.md` | Portmanteau pattern, docstrings, Prefab UI, pagination *(Legacy Python track; Rust repos use ArtCraft Command Bus)* |
| 5 | `standards/STARLETTE_NO_PYDANTIC_STANDARD.md` | Backend framework decision matrix *(Legacy Python track; INVALIDATED for Rust repos which call L1 in-process)* |
| 6 | `standards/NAKED_PC_INSTALL_STANDARD.md` | start.ps1 / Require-Command / Steve-class install *(Legacy Python track; Rust repos ship zero-dep native `.exe`)* |
| 7 | `standards/MCPB_PACKAGING_STANDARDS.md` | Two-track distribution: mcpb + NSIS |
| 8 | `standards/MCPB_PACKAGING_STANDARDS.md` | Full .mcpb layout, manifest, forbidden commands |
| 9 | `standards/TAURI_PRODUCTION_PITFALLS.md` | NSIS pitfalls Phase 1 checklist A-J |
| 10 | `standards/rules/tauri_nsis_building.md` | NSIS build pipeline, embedded backend, cert |
| 11 | `standards/WEBAPP_SOTA_STANDARDS.md` | React/Vite/Bun/Tailwind/Zustand stack |
| 12 | `standards/VERIFICATION_STANDARDS.md` | Browser verification, test coverage, anti-loop guards |
| 13 | `troubleshooting/BUGS_DEPOT.md` | Known bugs, symptom lookup, fleet-wide issues |

## 3. Pitfalls -- read before you trip

| File | Covers |
|---|---|
| `standards/TRAPS_AND_PITFALLS.md` | Cross-cutting traps (temporal grounding #20, spatial #21, NSSM restarts #22) |
| `standards/TAURI_PRODUCTION_PITFALLS.md` | NSIS/Tauri Phase 1 checklist A-J |
| `troubleshooting/BUGS_DEPOT.md` | Symptom lookup for every bug the fleet has already paid for |
| `troubleshooting/details/BUG-*.md` | Full write-up per bug, with detection commands |

**Search the depot by symptom before debugging anything.** A bug the fleet has already
hit is a lookup, not an investigation.

## 4. Domain Read List -- read when the task involves

| Task domain | Read |
|-------------|------|
| **Pure-Rust MCP / ArtCraft port (`rust-*-mcp` or `Cargo.toml` root)** | **`standards/RUST_ARTCRAFT_STANDARD.md` (FIRST -- supersedes Python/FastMCP/sidecar rules)** + `<repo>/AGENTS.md` |
| **Repo conversion / Rustification (`repconv <repo>` / `rustify`)** | **`patterns/REPCONV_SOP.md` + `standards/rust-artcraft/FLEET_CONVERSION_STANDARD.md` + `standards/rust-artcraft/FLEET_TRIAGE_AND_PYPI_TRANSPILATION.md`** |
| New MCP server scaffold | **New Repo Gate** -- `standards/RUST_ARTCRAFT_STANDARD.md` (Bucket A/B default) or `standards/AGENTS.md` §4.1 (Bucket C/D Python) |
| PowerShell scripts | `standards/POWERSHELL_STANDARDS.md` + `standards/rules/powershell-script-standards.md` |
| AutoHotkey scripts | `standards/rules/autohotkey_v2_standard.md` |
| Workflow / planning | `standards/rules/workflow_2026.md` + `standards/rules/architecting_sota.md` |
| Python docstrings | `standards/rules/docstrings_sota.md` |
| FastMCP concurrency / SQLite | `standards/fastmcp-3.2-concurrency.md` |
| Sampling -- **`ctx.sample()`** | ⚠️ Deprecated by the MCP 2026-07-28 spec; MRTR replaces it. Read `fastmcp/2026-07-28-spec-migration.md` **first**, then `standards/SOTA_REQUIREMENTS.md` §2.1. `ai-sampling.md` is *not* about this. |
| Sampling -- creative/iterative workflows | `standards/ai-sampling.md` (design/3D/audio variation loops in wrapper MCPs -- a different thing entirely) |
| RAG / embeddings | `standards/ai-rag-2026.md` |
| Local audio / image generation (music beds, SFX, posters) | `standards/LOCAL_MEDIA_MODELS.md` (measured numbers, licence thresholds, FreeSound key, what to use for what) |
| Webapp frontend | `webapp/frontend-sota.md` or `standards/BUN_STANDARDS.md` + `standards/REACT_HARDENING.md` |
| CUA / pywinauto smoke test | `standards/rules/cua_nsis_smoke_testing.md` |
| Repo smoke test ("did it run?") | `standards/SMOKE_CONTRACT.md` (`just smoke`: versions, one real call, one artifact check) |
| CUA webapp test (pre-Tauri) | `standards/rules/cua_webapp_testing.md` |
| Publishing / promotion / Glama | `standards/FLEET_PROMOTION.md` + `standards/MCPB_PACKAGING_STANDARDS.md` §3 |
| End of session: "write up / report / document in discord" | `standards/WORK_REPORT_STANDARD.md` (report file + digest in `#sfb-work`, all agents) |
| Destructive / exec / actuator / outbound-message tools | `standards/AGENT_ACTION_GATES.md` (gates the model cannot open) |
| Docker / containerisation | `standards/docker-containerization.md` |
| GitHub Actions / CI | `standards/GITHUB_ACTIONS_NO_PRIVATE_CI.md` |
| README / INSTALL editing | `standards/AGENT_INSTALL_REFERENCE.md` + `standards/README_STRUCTURE.md` |
| Arazzo API workflows | `patterns/arazzo/` |
| Robot / Yahboom | `standards/YAHBOOM_ROBOTICS_STANDARD.md` |
| Chip / VLSI design | `standards/rules/chip_design_cad_sota.md` |
| Open source PRs | `standards/rules/open_source_contributing.md` |
| Fleet grading / health | `standards/FLEET_GRADING_STANDARDS.md` |
| Unicode / EM dash issues | `patterns/unicode_safety.md` |
| Agentic macros | `standards/rules/agentic_macros.md` |
| OpenCode plugins | `standards/rules/opencode_plugins_sota.md` |
| Release tiers / NSIS build | `standards/RELEASE_TIERS.md` + `patterns/async-worktree-agent.md` |

## 5. Rules that fail silently

These are repeated in every tool's rules file rather than linked, because a rule whose
violation produces **no error** cannot depend on anyone following a link.

- **Never author multi-line file content with a Bash heredoc** (`cat > file <<'EOF'`).
  Intermittently fails on this Windows/Git-Bash setup and writes nothing. Use the Write
  tool. → `BUG-031`
- **Never patch files with inline Python** (`python - <<'PY'`, `python -c`). Python's
  string parser silently converts backslash escapes: `"D:\Dev\repos\x"` becomes `D:` +
  `\D` + `ev` + CR + `epos` + CR + `x`. Observed: a `# noqa` insertion deleted dict
  entries -- valid Python, ruff clean, wrong behaviour, no error anywhere. Use Edit and
  Write. → `BUG-039`
- **Never hardcode a port.** Claim one with `fleet-gate/claim_ports.py`, which checks
  both `operations/WEBAPP_PORTS.md` **and** every `fleet-start.config.ps1`. Checking one
  source is how ten repos ended up squatting on each other's ports.
- **Max 10 files per commit and per script invocation** (no per-session cap). Bigger batches have broken this
  fleet twice (100+ `build.ps1`, 63 spec files).
- **3+ file edits require a timestamped `.bak` per file** written before the edit.
- **Never restart an NSSM service by killing its child process.** Use
  `sc.exe stop/start`, then verify a NEW PID owns the port. → `TRAPS_AND_PITFALLS.md` #22
- **Never invent a date or a location.** Read the clock; if unreachable write
  `UNKNOWN-DATE`. → `TRAPS_AND_PITFALLS.md` #20, #21
- **Generated prose must be ASCII.** No em dashes, smart quotes or emoji in digests,
  titles, filenames, log lines or commit messages.

## 6. Verify, do not assume

A tool that reports success while having examined nothing is the fleet's most common
failure -- five separate instances were found in a single day (2026-09-17), including a
probe that skipped every running service and still printed `SMOKE GATE PASSED`.

- Prove a change by running the thing, not by reading the diff.
- A scan that finds zero must distinguish "looked and found nothing" from "never
  looked". `fleet-gate/coverage.py` enforces this for the nightly gates.
- Report what actually happened, including the parts that failed.

---

## Maintaining this file

It is the single source for agent reading order. The per-tool rules files
(`CLAUDE.md`, `.cursorrules`, `.clinerules`, `.windsurfrules`, `.rules`, `AGENTS.md`)
carry a short generated block pointing here, refreshed by:

```bash
python mcp-central-docs/fleet-gate/agent_context.py --check    # coverage report
python mcp-central-docs/fleet-gate/agent_context.py --repo X --apply
```

Do not hand-edit the generated blocks; edit this file and regenerate.
