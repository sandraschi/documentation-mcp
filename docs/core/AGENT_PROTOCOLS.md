# AGENT_PROTOCOLS (SOTA v12.1)

> [!IMPORTANT]
> This is a living document. All SOTA MCP development MUST follow these standards to maintain ecosystem stability and peer technical contributor status.

## Technical Standard Modules

The protocol is now modularized for better scannability. Refer to the specific module for your current task:

- **[SOTA Requirements](./SOTA_REQUIREMENTS.md)**: Core Architecture & FastMCP 3.1 features (includes **§2.2 MCP Apps / Prefab**).
- **[MCP Apps & Prefab UI](../fastmcp/mcp-apps-prefab-ui.md)** (FastMCP section): In-chat rich UI with **`prefab-ui`**, **`ToolResult`**, optional **`apps`** extra, fleet checklist (multi-repo).
- **[Prefab use cases & examples](../fastmcp/mcp-apps-prefab-use-cases-and-examples.md)**: When it’s not a gimmick, **Claude Desktop** side/interaction, **example catalog** (stats, fleet, safety, diffs, …).
- **[Webapp Standards](./WEBAPP_STANDARDS.md)**: Blueprint Architecture & Chatbot System.
- **[Tool Design](./TOOL_DESIGN_STANDARDS.md)**: Portmanteaux, docstrings, **agentic checklist** (ToolBench-aligned), **pagination**, `ToolAnnotations`, optional `output_schema`; **§3.3** MCP Apps / **`ToolResult`** + [Prefab UI](../fastmcp/mcp-apps-prefab-ui.md).
- **[Implementation Honesty](./IMPLEMENTATION_HONESTY_STANDARD.md)**: No fake-success paths; explicit `not_implemented`; "Under construction" UX for unavailable features.
- **[ToolBench (Arcade)](../toolbench/README.md)**: External benchmark — what it measures, fleet alignment, [per-server improvements](../toolbench/improvements/README.md).
- **New MCP server scaffolding:** Cursor rule **`.cursor/rules/new-mcp-server-questionnaire.mdc`** — when creating a new `*-mcp` repo, run the **pre-flight questionnaire** (or accept “defaults”) before writing files; ports → [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md).
- **[Verification Standards](./VERIFICATION_STANDARDS.md)**: Visual verification, browser automation, testing coverage.
- **[PowerShell Standards](./POWERSHELL_STANDARDS.md)**: SOTA script error handling, retries, and structure.
- **[Infrastructure Reliability](./INFRASTRUCTURE_RELIABILITY.md)**: Docker recovery, edge hardening, monitoring.
- **[Cursor Rules](./CURSOR_RULES.md)**: Multi-workspace shell context synchronization.
- **[Documentation Standards](./DOCUMENTATION_STANDARDS.md)**: Required files, integration guides, README templates.
- **Capability introspection pattern**: all MCP web backends expose **`GET /api/capabilities`** and webapps consume it for runtime feature gating; see [WEBAPP_STANDARDS.md §1.4](./WEBAPP_STANDARDS.md#14-capability-introspection-endpoint-mandatory).
- **[Packaging Standards](./PACKAGING_STANDARDS.md)**: MCPB (`mcpb pack`), Glama (`glama.json`), **uv** + **justfile** + **`llms.txt`** + **`llms-full.txt`** (required pair), **Gitingest (optional agent aid, not a repo artifact)**, LobeHub, SOTA prompts (3-4-100 rule). **LLM manifest:** [integrations/llms-txt-manifest.md](../integrations/llms-txt-manifest.md).
- **[Code Quality Standards](./CODE_QUALITY_STANDARDS.md)**: Ruff (Python), **pre-commit** hooks, **`ty`** (non-blocking CI during adoption), TypeScript/JavaScript linting/formatting; **§1.5** optional **pip-audit**, **respx**/HTTP test doubles, Vite **`npm run check`**.
- **[Deployment Standards](./DEPLOYMENT_STANDARDS.md)**: Zero-install patterns (uvx, npx) and developer setup.
- **[Gitignore & VCS hygiene](./GITIGNORE_STANDARDS.md)**: **Never commit `node_modules/`, venvs, caches**; recovery if pushed.

## Fleet Operations (Control Plane)

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

`fileops:repo_ops`, `fileops:git_*`, and `winops:git_operations_async` were removed 2026-04-06 as part of the git tool consolidation. They no longer exist on the MCP surface. See `not-mcp-related/git-github/MCP_GIT_TOOL_CONSOLIDATION.md` for the full plan.
