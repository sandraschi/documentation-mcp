# AGENT_PROTOCOLS (SOTA v12.2)

> [!IMPORTANT]
> **June 2026 bar:** [JUNE_2026_STANDARDS_BAR.md](./JUNE_2026_STANDARDS_BAR.md) — FastMCP **3.2+**, **MCPB only**, **no DXT**. Saga index: [MCP_SERVER_SAGA_INDEX.md](../operations/MCP_SERVER_SAGA_INDEX.md).

> This is a living document. All SOTA MCP development MUST follow these standards to maintain ecosystem stability and peer technical contributor status.

## Technical Standard Modules

The protocol is now modularized for better scannability. Refer to the specific module for your current task:

- **[June 2026 standards bar](./JUNE_2026_STANDARDS_BAR.md)**: Canonical snapshot — 3.2+, MCPB, retired DXT/2.x minimums.
- **[DXT deprecation](./DXT_DEPRECATION.md)**: DXT packaging retired; MCPB only.
- **[SOTA Requirements](./SOTA_REQUIREMENTS.md)**: Core Architecture & FastMCP 3.2 features (includes **§2.2 MCP Apps / Prefab**).
- **[Agent Client Protocol (ACP)](./AGENT_CLIENT_PROTOCOL.md)**: SOTA architectural standard for connecting IDEs (Xcode 27, Zed) to AI coding agents, and core differences from MCP.
- **[FastMCP 3.2 concurrency](./fastmcp-3.2-concurrency.md)**: Universal safety patterns for concurrent tool calls.
- **[FastMCP 3.2 startup probes](./fastmcp-3.2-startup-probes.md)**: Mandatory shallow connectivity probe in lifespan.
- **[FastMCP 3.x upgrade strategy](./FASTMCP3_UPGRADE_STRATEGY.md)**: Fleet rollout playbook for 2.x → 3.2+.
- **[MCP Apps & Prefab UI](../fastmcp/mcp-apps-prefab-ui.md)** (FastMCP section): In-chat rich UI — **`prefab-ui`** **core** dependency; **mandatory** Prefab surfaces for **list / status / stats** tools; **`ToolResult`** + **`PrefabApp`**; registration toggle env only.
- **[Prefab use cases & examples](../fastmcp/mcp-apps-prefab-use-cases-and-examples.md)**: When it’s not a gimmick, **Claude Desktop** side/interaction, **example catalog** (stats, fleet, safety, diffs, …).
- **[Backend Framework Decision](./STARLETTE_NO_PYDANTIC_STANDARD.md)**: **Starlette 1.0 default, FastAPI when the REST surface earns it** — decision matrix (endpoint count, external exposure, Swagger utility); Starlette 1.0 key patterns; FastAPI patterns with Swagger; AI agent prompt templates for both paths.
- **[Webapp Standards](./WEBAPP_STANDARDS.md)**: Blueprint Architecture & Chatbot System.
- **[Webapp SOTA Standards](./WEBAPP_SOTA_STANDARDS.md)**: Zero-runt React/Tailwind stack — premium UI bar (pairs with Webapp Standards).
- **[Fleet RAG Standard](./ai-rag-2026.md)**: LanceDB + FastEmbed + `bge-small-en-v1.5` — default embedded RAG stack; see `docs_mcp/backend/rag_core.py`.
- **[Webapp Logs Page](./WEBAPP_LOGS_PAGE.md)**: Dedicated `/logs` route — `/api/logs` API, live tail, pagination, export, ring-buffer rotation (extends Logger Panel §6.3).
- **[Playwright E2E](./rules/playwright_e2e_sota.md)**: Mandatory webapp e2e — install, smoke routes, screenshot regen for README Preview.
- **[Tool Design](./TOOL_DESIGN_STANDARDS.md)**: Portmanteaux, docstrings, **agentic checklist** (ToolBench-aligned), **pagination**, `ToolAnnotations`, optional `output_schema`; **§3.3** MCP Apps / **`ToolResult`** + [Prefab UI](../fastmcp/mcp-apps-prefab-ui.md) (**§4** Prefab row — list/status/stats).
- **[Implementation Honesty](./IMPLEMENTATION_HONESTY_STANDARD.md)**: No fake-success paths; explicit `not_implemented`; "Under construction" UX for unavailable features.
- **[ToolBench (Arcade)](../toolbench/README.md)**: External benchmark — what it measures, fleet alignment, [per-server improvements](../toolbench/improvements/README.md).
- **New MCP server scaffolding:** Cursor rule **`.cursor/rules/new-mcp-server-questionnaire.mdc`** — when creating a new `*-mcp` repo, run the **pre-flight questionnaire** (or accept “defaults”) before writing files; ports → [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md).
- **[Git repository safety](./GIT_REPOSITORY_SAFETY.md)**: **MANDATORY** — `git init` + initial commit + GitHub push **before** batch edits on new repos; **checkpoint commit** before recursive/`src/` mass changes; run [`scripts/ensure-mcp-repo-git.ps1`](../scripts/ensure-mcp-repo-git.ps1). Incident: `chip-design-mcp` zero-byte wipe with no rollback.
- **[Verification Standards](./VERIFICATION_STANDARDS.md)**: Visual verification, browser automation, testing coverage.
- **[PowerShell Standards](./POWERSHELL_STANDARDS.md)**: SOTA script error handling, retries, and structure.
- **[Infrastructure Reliability](./INFRASTRUCTURE_RELIABILITY.md)**: Docker recovery, edge hardening, monitoring.
- **[Session Context Injection](./rules/session_context_injection.md)**: Tool-awareness prompt injection at session start — Claude Code hooks, Cursor rules, Windsurf rules, Antigravity skills, Copilot instructions, OpenCode config. Fleet rollout phases. Reference: `advanced-memory-mcp`.
- **[Cursor Rules](./CURSOR_RULES.md)**: Multi-workspace shell context synchronization.
- **[Documentation Standards](./DOCUMENTATION_STANDARDS.md)**: Required files, integration guides, README templates.
- **[Fleet Promotion](./FLEET_PROMOTION.md)**: Discovery without AI spam — registries, wrappee GitHub etiquette, Goodreads (calibre), tone checklist.
- **[README Wrapper MCP](./README_WRAPPER_MCP.md)**: Headless vs GUI + hands-in/out for host-app MCPs.
- **[Open-source ASIC / VLSI CAD](./rules/chip_design_cad_sota.md)**: RTL-to-GDSII pipeline standard; reference repo [`chip-design-mcp`](../projects/chip-design-mcp/README.md) (ports **11022/11023**).
- **[README Webapp Screenshots](./README_WEBAPP_SCREENSHOTS.md)**: Preview images for README self-promotion.
- **Assess & Fix SOP** ([patterns/repo-assess-and-fix.md](../patterns/repo-assess-and-fix.md)): The single highest-leverage workflow in the fleet. `assess and fix <repo>` audits a repo against 19 categories (required files, tool surface, webapp SOTA, CORS, security, Tauri/native, FastMCP, session context injection, error handling, CI/CD, ports, containers, dashboard quality, LLM elicitation) → fixes in severity order → lints → syncs docs → builds packages → pushes. Companion `assfixstat` shows fleet-wide progress via `.assess-fix-timestamp` markers. **Should have been built a year ago.**
- **Capability introspection pattern**: all MCP web backends expose **`GET /api/capabilities`** (standardised response shape per [WEBAPP_STANDARDS.md §1.4](./WEBAPP_STANDARDS.md#14-capability-introspection-endpoint-mandatory)) and webapps consume it for runtime feature gating. Enforced by `assess and fix` (§1B of `repo-assess-and-fix.md`).
- **[Packaging Standards](./PACKAGING_STANDARDS.md)**: MCPB (`mcpb pack`), Glama (`glama.json`), **uv** + **justfile** + **`llms.txt`** + **`llms-full.txt`** (required pair), **Gitingest (optional agent aid, not a repo artifact)**, LobeHub, SOTA prompts (3-4-100 rule). **LLM manifest:** [integrations/llms-txt-manifest.md](../integrations/llms-txt-manifest.md).
- **[MCPB Packaging](./MCPB_PACKAGING_STANDARDS.md)**: Full `.mcpb` layout, manifest fields, staging build, forbidden bundle contents (extends Packaging §5).
- **[Justfile Standards](./JUSTFILE_STANDARDS.md)**: Industrial dashboard `justfile` pattern + **[Justfile Recipes](./JUSTFILE_RECIPES.md)** domain recipe sections.
- **[Fleet Grading](./FLEET_GRADING_STANDARDS.md)**: Repo tiers (★), health metadata in `glama.json`, DONE/marketing gate.
- **[Code Quality Standards](./CODE_QUALITY_STANDARDS.md)**: Ruff (Python), **pre-commit** hooks, **`ty`** (non-blocking CI during adoption), TypeScript/JavaScript linting/formatting; **§1.5** optional **pip-audit**, **respx**/HTTP test doubles, Vite **`npm run check`**.
- **[Bun Adoption Standard](./BUN_STANDARDS.md)**: **Bun replaces npm** as JS package manager + script runner (`bun install` / `bun run`, text `bun.lock`); **Vite stays** the bundler, Node stays as fallback. Two-phase (`--bun` runtime move is optional/per-repo), per-repo migration checklist. `uv`:Python :: `bun`:JS. Reference: [integrations/bun.md](../integrations/bun.md).
- **[Naked-PC Install Standard](./NAKED_PC_INSTALL_STANDARD.md)**: **MANDATORY** for every repo with a `start.bat`. `start.ps1` MUST include `Require-Command` (winget auto-install of uv + Node.js), local vite guard, import smoke-test, helpful health-timeout error message. Every repo MUST have `INSTALL.md`. Reference implementation: `aiwatcher-mcp`. Fixed in: `arxiv-mcp` (2026-04-24). **Run the fleet scan in the standard to find non-compliant repos.**
- **[Start Script Standard](./START_SCRIPT_STANDARD.md)**: Canonical `webapp/start.ps1` + root delegate `start.bat` templates (extends Naked-PC).
- **[Naked Install Testing](./NAKED_INSTALL_TESTING.md)**: Consumer sandbox validation — run published install instructions on a clean Windows box before shipping.
- **[Release Tiers](./RELEASE_TIERS.md)**: T1 (MCPB only), T2 (webapp), T3 (desktop NSIS) — NSIS is the last step, not the first. Per-repo `RELEASE_TIER.md` markers.
- **[Webapp Directory Standard](./WEBAPP_DIRECTORY_STANDARD.md)**: Frontend dir MUST be `webapp/` — not `web_sota/`, not `frontend/`, not `web/`.
- **[Git Workflow](./GIT_WORKFLOW.md)**: Branch naming, PR checklist, worktrees, GitHub protection. For when contributors arrive.
- **[Async Worktree Agent](../patterns/async-worktree-agent.md)**: Run builds/tests in a background worktree agent while developing in the main checkout. Eliminates "waiting for CI."
- **[Unicode Safety](./patterns/unicode_safety.md)**: **MANDATORY, BROADENED 2026-07-13** - **EM DASH (`-`, U+2014) is never allowed** anywhere in the fleet, any filetype, not just scripts (originally scoped to `start.ps1`/`start.bat`/`justfile`; broadened after it silently corrupted a markdown doc write). Enforce with `mcp-central-docs/scripts/check-unicode-safe.ps1` (currently script-only, extension to all filetypes flagged as a follow-up).
- **[Local LLM First Doctrine](./LOCAL_LLM_FIRST_DOCTRINE.md)**: Zero-token-cost development doctrine — local Ollama as default, cloud as opt-in; opencode config with anti-leak; overnight runner economics (100-300x savings); model lineup for RTX 4090; silent paid-API audit checklist. Complements `LOCAL_LLM_STANDARDS.md` (doctrine vs operations).
- **[LLM and Install Tiers](./LLM_AND_INSTALL_TIERS.md)**: **MANDATORY** for repos with LLM features or host-app bridges — user tiers A–D (Ollama/LM Studio, cloud API, vLLM); never bundle Blender/Unity/models; Docker optional only; Tauri installer bundle rules.
- **[Control Plane Install](./CONTROL_PLANE_INSTALL.md)**: RoboFang, DeepFang, OpenClaw/NanoClaw — not Steve-class Option A; Docker required for isolation stacks.
- **[Agent Install Reference](./AGENT_INSTALL_REFERENCE.md)**: **READ BEFORE EDITING INSTALL.md** — fleet install research, Options A–D, anti-patterns, naked testing; for Claude, Cursor, Zed, VS Code, Antigravity.
- **[README Structure](./README_STRUCTURE.md)**: Tiered README / INSTALL / docs/ layout; Options A–D.
- **[Deployment Standards](./DEPLOYMENT_STANDARDS.md)**: Zero-install patterns (uvx, npx) and developer setup.
- **[Gitignore & VCS hygiene](./GITIGNORE_STANDARDS.md)**: **Never commit `node_modules/`, venvs, caches**; recovery if pushed.
- **[Safety Protocols](./SAFETY_PROTOCOLS.md)**: **Atomic Writes** and **Dual-Backups** (Local + Central Archive).
- **[Dialogic Returns](./DIALOGIC_RETURNS.md)**: **SOTA 2026 Feedback Standard** for machine-readable error remediation.
- **[Prompt Injection Hardening](./PROMPT_INJECTION_HARDENING.md)**: **SOTA 2026 Security Standard** (Randomized Spotlighting + Secondary Auditor + RAT UI).
- **[RAT Emergency Protocol](./RAT_EMERGENCY_PROTOCOL.md)**: **Goliath Research Standard** (Quarantine + Task Lock + Silent Block).
- **[RoboFang Control Plane](../operations/FLEET_CONTROL_PLANE.md)**: **Phase 4 Sentinel Roadmap** (Safety Preflight + Hardware Auditor).
- **[Purple Llama Suite](../integrations/purple-llama/README.md)**: **Meta Safety Ecosystem** (Llama Guard, CodeShield, CyberSec Eval).

## Fleet Operations (Control Plane)

- **[Auth-error-surfacing fleet rollout](../operations/AUTH_ERROR_SURFACING_FLEET_ROLLOUT.md)**: Tracks the 401-recovery-hint patch (stale-in-process vs. genuinely-invalid credentials) across the fleet — `tailscale-mcp` done 2026-06-20, 13 candidate repos pending; root cause + hard rule in [TRAPS_AND_PITFALLS.md §6](./TRAPS_AND_PITFALLS.md#6-stale-in-process-api-credentials-surfacing-as-a-flat-invalid-api-key-error).
- **[A2A fleet rollout (pointer)](../operations/A2A_FLEET_ROLLOUT.md)**: Agent2Agent adoption order — **plex-mcp → calibre-mcp → advanced-memory-mcp → supervisor MCPs**; canonical checklists live in plex-mcp `docs/mcp-technical/`; register new HTTP/A2A ports in [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md).
- **[Fleet control plane](../operations/FLEET_CONTROL_PLANE.md)**: RoboFang + MCP fleet — what belongs in `hands/` vs `robofang/tools/`, three-phase model (index → install → operate), optional `iflow-mcp-catalog` integration **without** duplicating server code into RoboFang.
- **[here.now static publishing](../operations/HERE_NOW_STATIC_PUBLISHING.md)**: Optional third-party **instant static URL** for agent-built assets (fleet overview pages, demos); static-only, claim-window caveats — vendor instructions at [here.now](https://here.now).
- **[Cursor Stammtisch demo kit](../research/agentic-ide/CURSOR_STAMMTISCH_DEMO_KIT.md)**: Short, provable demos for meetups (Vienna or elsewhere).

## Domain-Specific Standards

- **[Bugs Depot](../troubleshooting/BUGS_DEPOT.md)**: Central registry for critical bugs and race conditions.
- **[React Hardening Standards](./REACT_HARDENING.md)**: Proactive stability patterns for hooks and effects.
- **[Vibe Operations](../operations/VIBE_OPERATIONS.md)**: Real-time infrastructure status and switching protocols.
- **Desktop vs browser MCP:** Do **not** enable **pywinauto-mcp** in default IDE chains for webapp work — [WEBAPP_STANDARDS.md §7](./WEBAPP_STANDARDS.md#7-mcp-capability-boundaries-web-vs-desktop-ui), [FLEET_COMPUTER_USE_MCP.md](../patterns/FLEET_COMPUTER_USE_MCP.md) (IDE warning), [VERIFICATION_STANDARDS.md §2.4](./VERIFICATION_STANDARDS.md#24-desktop-ui-tools-are-not-a-substitute-for-browser-verification). **Safety / sampling:** [PYWINAUTO_MCP_SAFETY.md](../patterns/PYWINAUTO_MCP_SAFETY.md) (**OpenManus + openmanus-mcp + OpenClaw / Manus-class + pywinauto** = multiplicative risk). **New users:** pywinauto-mcp **`docs/SAFETY.md`** + install **`virtualization-mcp`** for Windows Sandbox/VM isolation (two-server model).

---

**Version History**:
- 1.34 (2026-07-11): **[Release Tiers](./RELEASE_TIERS.md)** T1/T2/T3, **[Webapp Directory Standard](./WEBAPP_DIRECTORY_STANDARD.md)** (`webapp/` not `web_sota/`), **[Git Workflow](./GIT_WORKFLOW.md)** branching + worktrees, **[Async Worktree Agent](../patterns/async-worktree-agent.md)** background build/test pattern.
- 1.33 (2026-06-17): **[June 2026 standards bar](./JUNE_2026_STANDARDS_BAR.md)** — FastMCP 3.2+ fleet minimum; **[DXT deprecation](./DXT_DEPRECATION.md)**; **[MCP server saga index](../operations/MCP_SERVER_SAGA_INDEX.md)**; **[PUBLISH_UPDATE_CHECKLIST.md](../PUBLISH_UPDATE_CHECKLIST.md)** — projects, integrations, AI mandatory IN after update; public prep ([WEED_MANIFEST.md](../WEED_MANIFEST.md), [PUBLIC_INDEX.md](../PUBLIC_INDEX.md)).
- 1.31 (2026-05-31): **[Unicode Safety](./patterns/unicode_safety.md)** - EM DASH never allowed in `start.ps1` / scripts; fleet checker `scripts/check-unicode-safe.ps1`.
- 1.30 (2026-05-31): **Bun Adoption Standard** — [BUN_STANDARDS.md](./BUN_STANDARDS.md) (Bun replaces npm as package manager + runner; Vite kept; two-phase + per-repo migration checklist); reference [integrations/bun.md](../integrations/bun.md); [WEBAPP_SOTA_STANDARDS.md](./WEBAPP_SOTA_STANDARDS.md) §I package-manager line.
- 1.29 (2026-05-28): **[Agent Install Reference](./AGENT_INSTALL_REFERENCE.md)** — mandatory pre-read for agents editing INSTALL/README install docs.
- 1.28 (2026-05-28): **[Control Plane Install](./CONTROL_PLANE_INSTALL.md)** — RoboFang, DeepFang, OpenClaw/NanoClaw vs MCP hands.
- 1.27 (2026-05-28): **[LLM and Install Tiers](./LLM_AND_INSTALL_TIERS.md)** — host-app wrapees, LLM local/cloud parity, Docker scope, native installer bundle rules.
- 1.26 (2026-04-22): **A2A fleet rollout pointer** — [A2A_FLEET_ROLLOUT.md](../operations/A2A_FLEET_ROLLOUT.md); canonical plan in plex-mcp `docs/mcp-technical/A2A_FLEET_ROLLOUT_PLAN.md`.
- 1.25 (2026-04-17): **Prefab fleet mandate** — [SOTA_REQUIREMENTS.md](./SOTA_REQUIREMENTS.md) §2.2 (core **`prefab-ui`**, list/status/stats coverage); [TOOL_DESIGN_STANDARDS.md](./TOOL_DESIGN_STANDARDS.md) §3.3 / §4; [mcp-apps-prefab-ui.md](../fastmcp/mcp-apps-prefab-ui.md) §3 overhaul.
- 1.24 (2026-04-01): **Fleet-Wide Browser Auto-Open Modernization** — [WEBAPP_STANDARDS.md](./WEBAPP_STANDARDS.md) §1.2; [POWERSHELL_STANDARDS.md](./POWERSHELL_STANDARDS.md) §5 (Poll-and-Open pattern).
- 1.23 (2026-03-28): **Prefab use cases & examples** — [fastmcp/mcp-apps-prefab-use-cases-and-examples.md](../fastmcp/mcp-apps-prefab-use-cases-and-examples.md); hub link.
- 1.22 (2026-03-28): **MCP Apps & Prefab UI** — [fastmcp/mcp-apps-prefab-ui.md](../fastmcp/mcp-apps-prefab-ui.md) fleet standard; [SOTA_REQUIREMENTS.md](./SOTA_REQUIREMENTS.md) §2.2; hub links.
- 1.21 (2026-03-26): Added **Capability Introspection Endpoint pattern** — mandatory `GET /api/capabilities` + webapp runtime usage contract in [WEBAPP_STANDARDS.md](./WEBAPP_STANDARDS.md) §1.4.
- 1.20 (2026-03-26): Added **Implementation Honesty Standard** — explicit lifecycle policy for placeholders, truthful failure contracts, UI "Under construction" requirements, CI pattern enforcement.
- 1.19 (2026-03-24): **New MCP server questionnaire** — [.cursor/rules/new-mcp-server-questionnaire.mdc](../.cursor/rules/new-mcp-server-questionnaire.mdc); hub link; use before scaffolding a new `*-mcp` repo unless user says defaults/skip.
- 1.18 (2026-03-24): **ToolBench hub** — [toolbench/README.md](../toolbench/README.md) (analysis, fleet alignment, per-server improvements); hub link under Tool Design.
- 1.17 (2026-03-24): **Agentic tool quality + pagination** — [TOOL_DESIGN_STANDARDS.md](./TOOL_DESIGN_STANDARDS.md) §4–§9 (fleet checklist, pagination patterns, structured errors, output schema, MCP `ToolAnnotations`); hub Tool Design line updated.
- 1.16 (2026-03-24): **here.now static publishing** — [HERE_NOW_STATIC_PUBLISHING.md](../operations/HERE_NOW_STATIC_PUBLISHING.md); hub link under § Fleet operations (optional third-party static URLs for agent outputs).
- 1.15 (2026-03-23): **Fleet control plane + Stammtisch demo kit** — [FLEET_CONTROL_PLANE.md](../operations/FLEET_CONTROL_PLANE.md), [CURSOR_STAMMTISCH_DEMO_KIT.md](../research/agentic-ide/CURSOR_STAMMTISCH_DEMO_KIT.md); hub links under § Fleet operations.
- 1.14 (2026-03-21): **OpenManus / openmanus-mcp / OpenClaw + pywinauto** — [PYWINAUTO_MCP_SAFETY.md](../patterns/PYWINAUTO_MCP_SAFETY.md) new §; [integrations/openmanus.md](../integrations/openmanus.md) Caution; [FLEET_COMPUTER_USE_MCP.md](../patterns/FLEET_COMPUTER_USE_MCP.md) banner; [projects/openmanus-mcp/README.md](../projects/openmanus-mcp/README.md) + [INTEGRATION.md](../projects/openmanus-mcp/INTEGRATION.md).
- 1.13 (2026-03-21): **pywinauto + virtualization two-server** — pywinauto-mcp **`docs/SAFETY.md`**; [DOCUMENTATION_STANDARDS.md](./DOCUMENTATION_STANDARDS.md) §1 high-risk servers; [PYWINAUTO_MCP_SAFETY.md](../patterns/PYWINAUTO_MCP_SAFETY.md) § New users.
- 1.12 (2026-03-21): **pywinauto vs IDE/webapp** — [WEBAPP_STANDARDS.md](./WEBAPP_STANDARDS.md) §7; [FLEET_COMPUTER_USE_MCP.md](../patterns/FLEET_COMPUTER_USE_MCP.md) IDE warning; [VERIFICATION_STANDARDS.md](./VERIFICATION_STANDARDS.md) §2.4.
- 1.11 (2026-03-21): **Adjacent tooling** — [CODE_QUALITY_STANDARDS.md](./CODE_QUALITY_STANDARDS.md) §1.5 (**pip-audit**, **respx**/HTTP tests, Vite check); §4 table extended.
- 1.10 (2026-03-20): **`llms.txt` + `llms-full.txt` (required pair)**, **Ruff pre-commit**, **ty** (non-blocking CI) — [integrations/llms-txt-manifest.md](../integrations/llms-txt-manifest.md), [patterns/LLMS_TXT_FLEET_MANIFEST.md](../patterns/LLMS_TXT_FLEET_MANIFEST.md); [DOCUMENTATION_STANDARDS.md](./DOCUMENTATION_STANDARDS.md) §1; [PACKAGING_STANDARDS.md](./PACKAGING_STANDARDS.md) §5–6; [CODE_QUALITY_STANDARDS.md](./CODE_QUALITY_STANDARDS.md) §1.2–1.4 + §4.
- 1.9 (2026-03-20): **Build bar** — [PACKAGING_STANDARDS.md](./PACKAGING_STANDARDS.md) §5 formalizes **uv**, **justfile**, **llms.txt**, **glama.json**, and **`mcpb pack`** as the Python MCP repo standard; [SOTA_REQUIREMENTS.md](./SOTA_REQUIREMENTS.md) §3 + [DOCUMENTATION_STANDARDS.md](./DOCUMENTATION_STANDARDS.md) **llms.txt** aligned. (**v1.10** adds required **`llms-full.txt`** + integration/pattern docs.)
- 1.8 (2026-03-19): **Stale marking** — [MCP_SERVER_FIRST_TIME_SUCCESS_GUARANTEE.md](./MCP_SERVER_FIRST_TIME_SUCCESS_GUARANTEE.md) flagged **STALE**; canonical hub remains this file + linked modules (README/PRD aligned).
- 1.7 (2026-03-19): **Gitignore standards** — added [GITIGNORE_STANDARDS.md](./GITIGNORE_STANDARDS.md) (node_modules, venv, history rewrite); linked from hub.
- 1.6 (2026-03-18): **Modularization Update.** Split 2000-line protocol into linked files for high-frequency workflows.
- 1.5 (2026-01-01): Comprehensive SOTA v12.0 Update (Sampling, Structural Compositing, MCPB/Glama Standards)
- 1.4 (2025-12-29): Added Code Quality Standards (Ruff linting/formatting)
- 1.3 (2025-12-11): Added Tool Family Modularization, Unity VRM Integration
- 1.0 (2025-10-21): Initial standards based on virtualization-mcp

**Review Schedule:** Quarterly  
**Owner:** Sandra Schi

### Python Execution Rule

**CRITICAL MANDATE**: Never invoke naked 'python' in terminal commands. ALWAYS construct commands using 'uv run python' uniformly across all scripts, analysis, and execution tasks to prevent missing cmdlet or path resolution errors in Windows PowerShell environments.

### Git/GitHub Tool Routing

**ALWAYS use `gitops` (git-github-mcp) for all git and GitHub operations. NEVER use fileops or winops.**

| Task | Tool |
|---|---|
| Any local git operation | `gitops:git_ops` (44 actions) |
| Any GitHub operation | `gitops:github_ops` (58 actions) |
| Natural language multi-step git/GitHub | `gitops:git_agentic_workflow` |
| GitHub repo/org discovery | `gitops:git_github_search_workflow` |
| Check git/gh auth | `gitops:git_github_status` |
| Fleet PR/issue triage (schedule + policy) | See **[patterns/GITHUB_MAINTAINER_HEARTBEAT.md](../patterns/GITHUB_MAINTAINER_HEARTBEAT.md)** — `github_ops(pr_list)` / `issue_list`; supervisor owns cadence; **git-github-mcp** web **`/inbox`**. |

`fileops:repo_ops`, `fileops:git_*`, and `winops:git_operations_async` were removed 2026-04-06 as part of the git tool consolidation. They no longer exist on the MCP surface. See `not-mcp-related/git-github/MCP_GIT_TOOL_CONSOLIDATION.md` for the full plan.
