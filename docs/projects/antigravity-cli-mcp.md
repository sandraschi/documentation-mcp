---
project: antigravity-cli-mcp
status: planned
priority: medium
tags: [antigravity, agy, mcp-bridge, cursor, gemini, cli, orchestration, fleet]
created: 2026-06-01
updated: 2026-06-01
repo: (not scaffolded)
related:
  - ../ecosystem/antigravity/ANTIGRAVITY_2.0_SDK_CLI.md
  - ../ecosystem/antigravity/THIRD_PARTY_ECOSYSTEM.md
  - ../ecosystem/antigravity/README.md
  - ./fleet-agent-mcp.md
---

# antigravity-cli-mcp — Cursor ↔ Antigravity CLI bridge (planning)

**Status:** Design only — **no repo scaffolded yet.**

Expose Google Antigravity CLI (`agy`) capabilities to MCP clients (primarily **Cursor**) beyond what third-party wrappers offer today. The fleet already runs a large MCP surface inside Antigravity IDE via shared config at `~/.gemini/config/mcp_config.json`; this project is about the **reverse direction**: other agents calling Antigravity’s harness.

**Context:** [Google Antigravity @ I/O 2026](https://antigravity.google/blog/google-io-2026) — unified harness across Antigravity 2.0, CLI, SDK, and Gemini API; MCP Atlas benchmark; subagents, `/goal`, `/schedule`, shared MCP config.

---

## Problem

| What exists | Gap |
|---|---|
| [nadimtuhin/antigravity-cli-mcp](https://github.com/nadimtuhin/antigravity-cli-mcp) (npm) | Only **4 tools**: `ping`, `ask-agy`, `search-web`, `write-file` |
| Antigravity CLI in terminal | Rich slash commands (`/goal`, `/agents`, `/export`, `/schedule`, …) not exposed to Cursor |
| Fleet MCP in `mcp_config.json` | Antigravity **consumes** fleet servers; Cursor does not get Gemini harness without a bridge |
| [null-g-mcp](https://github.com/cristianoaredes/null-g-mcp) | Different axis: controls **IDE** language server (~85 tools), not CLI headless flows |

A greenfield repo is **not** justified to re-implement `ping` + generic prompt. It **is** justified if the deliverable is **fleet orchestration** (goal modes, MCP/skills introspection, plugin mgmt, Windows-native paths) without paying SDK token burn on every orchestration hop.

---

## Alternative approaches

### A — Use nadimtuhin as-is (lowest effort)

Install `antigravity-cli-mcp` via npx; point `AGY_PATH` at `agy.exe`; add entry to Cursor `mcp.json`.

| Pros | Cons |
|---|---|
| Zero maintenance | Meagre tool surface |
| Works today if `agy` installed | Bun/npx path quirks on Windows |
| Good smoke test | No `/goal`, subagents, export, fleet conventions |

**Cost:** Antigravity / Google AI subscription (same as running CLI directly). No extra API layer.

**Verdict:** OK for “try Gemini from Cursor once.” Not a fleet product.

---

### B — Fork / extend nadimtuhin (CLI subprocess MCP) ⭐ preferred if we build

Keep **stdio MCP → spawn `agy`** architecture; add tools the upstream package skips.

**Candidate v1 tools (no TUI automation):**

| Tool | Mechanism |
|---|---|
| `agy_ping` | `agy --version`, binary path, workspace root |
| `agy_goal` | Non-interactive prompt prefixed with `/goal` semantics + `--dangerously-skip-permissions` where appropriate |
| `agy_grill` | `/grill-me` mode — clarifying questions before work |
| `agy_search` | Web search via agy (upstream has this) |
| `agy_plugin_list` / `agy_plugin_install` | Shell wrapper: `agy plugin …` |
| `list_mcp_servers` / `mcp_server_health` | Read `~/.gemini/config/mcp_config.json`; optional lightweight stdio ping |
| `list_skills` / `invoke_skill` | Filesystem: `~/.gemini/skills`, `~/.gemini/antigravity-cli/skills`, `.agents/skills/` |
| `read_cli_log` | Tail `~/.gemini/antigravity-cli/log/cli-*.log` for failures |

**Deferred (brittle — need TUI or undocumented flags):**

- `agy_agents_status` (`/agents`)
- `agy_export` (`/export` to Antigravity 2.0)
- `agy_schedule` (`/schedule` cron)

| Pros | Cons |
|---|---|
| Matches fleet stack (FastMCP or thin Node like upstream) | Many CLI features are **in-session slash only** |
| Windows-first: `D:/Dev/repos`, `uv.exe`, absolute paths | Subprocess + log parsing fragile |
| Inherits shared MCP config automatically | Still a hop: Cursor → MCP → agy → MCP → fleet |
| No per-call Gemini API billing beyond CLI quota | Depends on Google not breaking non-interactive flags |

**Cost:** Same as CLI — subscription/quota bound, not metered API tokens per MCP tool call (unless `ask-agy` runs long autonomous `/goal` jobs).

**Verdict:** Best ROI for a **fleet-specific** repo. Fork upstream or reimplement in **Python + FastMCP 3.2** to match fleet conventions.

---

### C — null-g-mcp (IDE bridge, not CLI)

MCP server → Antigravity IDE ConnectRPC language server (~85 tools across 12 modules). Auto-discovers running IDE instances.

| Pros | Cons |
|---|---|
| Richest surface when IDE is open | **Requires Antigravity IDE running** |
| Real editor state, MCP server states in IDE | Not headless / SSH / CI |
| Complements CLI bridge | Different product; npm `antigravity-mcp` binary |

**Cost:** IDE session quota; no separate SDK install.

**Verdict:** Use alongside **B**, not instead of it. Cursor controls GUI Antigravity when desktop is up; **B** for terminal/headless.

---

### D — Skip MCP bridge; use `agy` + shared config directly

Install Antigravity CLI; rely on `~/.gemini/config/mcp_config.json` (already synced with IDE). Use `/export` to hand off to Antigravity 2.0.

| Pros | Cons |
|---|---|
| No extra repo | Cursor cannot invoke agy without human in terminal |
| Simplest mental model | No orchestration from Composer |
| Same MCP fleet everywhere | |

**Cost:** CLI/subscription only.

**Verdict:** Correct default for **human-in-terminal** work. Does not solve “Cursor delegates to Gemini.”

---

### E — google-antigravity SDK as MCP backend ⚠️ expensive

`pip install google-antigravity` — programmatic agent with built-in tools, MCP client support, subagents, hooks, policies. Agent loop runs in **closed-source Go binary** (`localharness`).

| Pros | Cons |
|---|---|
| Richest programmatic API | **Token cost** scales with turns, tool calls, subagents |
| Native MCP server attachment in agent config | Closed harness — fleet SOTA violation |
| Subagents, hooks, structured output first-class | `GEMINI_API_KEY` / cloud billing |
| Same harness as CLI/2.0 in theory | Redundant with opencode for open multi-provider agents |

**Cost model (why we deprioritize):**

| Factor | Impact |
|---|---|
| Every agent turn | Gemini API tokens (Flash cheaper; long `/goal`-style runs add up) |
| Subagents | **Multiplicative** — each subagent is its own loop |
| MCP tool results | Large context → compaction → more tokens |
| Scheduled / cron agents | 24/7 burn without careful budgets |
| vs CLI subscription | CLI often quota-based; SDK is **metered API** |

Google AI Ultra (~$100/mo at I/O 2026) raises capacity but does not remove per-token economics for SDK/API paths.

**Verdict:** Document and monitor ([ANTIGRAVITY_2.0_SDK_CLI.md](../ecosystem/antigravity/ANTIGRAVITY_2.0_SDK_CLI.md)). **Do not** build fleet MCP on SDK unless there is a explicit budget and a task that requires embedded Python agents outside `agy`. For Cursor integration, **B beats E** on cost and simplicity.

---

### F — Wait for Google official MCP / Gemini API agent endpoint

I/O 2026: “Antigravity agent via Gemini API” for programmatic querying; MCP Atlas benchmark suggests Google cares about MCP-native agents.

| Pros | Cons |
|---|---|
| No maintenance | Timeline unknown |
| Likely better TUI/API parity | May still be quota/token priced |

**Verdict:** Revisit quarterly. Do not block **B** on this.

---

## Decision matrix

| Approach | Effort | Tool richness | Headless | Fleet fit | Ongoing cost |
|---|---|---|---|---|---|
| A — nadimtuhin as-is | Low | ★ | Partial | Low | CLI quota |
| **B — fork/extend CLI MCP** | **Medium** | **★★★** | **Yes** | **High** | **CLI quota** |
| C — null-g-mcp (IDE) | Low (consume) | ★★★★ | No | Medium | IDE quota |
| D — agy direct | None | ★★ (manual) | Yes | High | CLI quota |
| E — SDK MCP | High | ★★★★★ | Yes | Low | **$$$ API tokens** |
| F — wait for Google | None | ? | ? | ? | TBD |

**Recommended path if we proceed:** **B** (fleet CLI MCP, Python/FastMCP) + optional **C** for IDE sessions. **Not E** unless budgeted.

---

## Proposed scope (v1 — when scaffolded)

**In scope**

- FastMCP 3.2 stdio server (fleet pattern) **or** maintained fork of nadimtuhin with Windows fixes
- Tools listed under approach **B** (config introspection + goal/grill + plugin shell)
- Progress streaming for long `agy` runs (MCP `notifications/progress`)
- Env: `AGY_PATH`, `AGY_WORKSPACE_ROOT`, `GEMINI_CONFIG_DIR` → `~/.gemini`
- Docs + `install-mcp.ps1 antigravity` parity for Cursor only (do not duplicate full fleet into Antigravity config)

**Out of scope v1**

- TUI driving (`/agents`, `/export`, `/schedule`)
- SDK wrapper
- Replacing fleet MCP servers inside Antigravity
- Scaffold / PyPI / CI until design sign-off

**Non-goals**

- Another thin `ping` + `ask` clone
- Owning Google’s closed Go harness

---

## Fleet integration notes

- **Shared MCP config:** `C:\Users\sandr\.gemini\config\mcp_config.json` — agy already sees arxiv, fileops, jellyfin, etc.
- **Cursor config:** `C:\Users\sandr\.cursor\mcp.json` — add bridge here only
- **Tool budget:** Antigravity recommends ≤50 enabled tools for performance; fleet has many servers — use `disabled` / `disabledTools` aggressively ([Antigravity MCP docs](https://antigravity.google/docs/mcp))
- **Cross-validation pattern:** Cursor (Composer) plans; `agy_goal` executes with Gemini 3.5 Flash — documented in [ANTIGRAVITY_2.0_SDK_CLI.md](../ecosystem/antigravity/ANTIGRAVITY_2.0_SDK_CLI.md) as optional, not fleet-critical

---

## Open questions

1. Fork nadimtuhin (MIT) vs greenfield FastMCP — preference for fleet consistency?
2. Is `agy` non-interactive `/goal` stable enough for production MCP calls?
3. Do we need `null-g-mcp` in Cursor at the same time (tool count explosion)?
4. Rate limits: cockpit-tools ecosystem suggests Antigravity quotas are tight — cap concurrent `agy` processes (`AGY_MAX_CONCURRENT=2`)?

---

## Related

- [Antigravity 2.0 SDK & CLI analysis](../ecosystem/antigravity/ANTIGRAVITY_2.0_SDK_CLI.md)
- [Third-party Antigravity ecosystem](../ecosystem/antigravity/THIRD_PARTY_ECOSYSTEM.md)
- [Antigravity IDE overview](../ecosystem/antigravity/README.md)
- [Google I/O 2026 — Antigravity](https://antigravity.google/blog/google-io-2026)
- [nadimtuhin/antigravity-cli-mcp](https://github.com/nadimtuhin/antigravity-cli-mcp)
- [null-g-mcp](https://github.com/cristianoaredes/null-g-mcp)

---

## Changelog

| Date | Change |
|---|---|
| 2026-06-01 | Initial planning page — alternative approaches, SDK cost warning, no scaffold |
