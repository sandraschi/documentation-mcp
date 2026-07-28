# Fleet Standards Core

**Prerequisites:** `docs/getting-started/`, `docs/fastmcp/`

This directory contains the canonical fleet standards — the rules every MCP server in the 136+ repo fleet must follow. If you're building a server that will be published or maintained long-term, read these first.

## Reading order

| Step | File | Why |
|------|------|-----|
| 1 | `JUNE_2026_STANDARDS_BAR.md` | **Start here.** The current minimum bar: FastMCP 3.2+, MCPB packaging, no DXT. |
| 1b | `../standards/NEW_REPO_BUILD_COMPLETE.md` | Assfix-zero scaffold checklist — first assess should find no CRITICAL/HIGH. |
| 1c | `../standards/ONBOARDING_STANDARD.md` | Wrappee/account onboarding + red CTA / MOCK-until-onboarded. |
| 2 | `SOTA_REQUIREMENTS.md` | Core architecture: FastMCP 3.4+ features, MCP Apps/Prefab UI, native installers. |
| 3 | `TOOL_DESIGN_STANDARDS.md` | The portmanteau pattern, docstrings, pagination, error handling. How to write tools that agents can actually use. |
| 4 | `DEPLOYMENT_STANDARDS.md` | Dual transport (stdio + HTTP), port allocation, start scripts. |
| 5 | `WEBAPP_SOTA_STANDARDS.md` | React/Vite/Tailwind/Zustand stack, mandatory pages, dark theme, local LLM glom-on. |
| 6 | `PACKAGING_STANDARDS.md` + `MCPB_PACKAGING_STANDARDS.md` | Two-track distribution: MCPB bundles for Claude Desktop, NSIS installers for end users. |
| 7 | `GIT_REPOSITORY_SAFETY.md` | Git discipline: checkpoint commits, batch edit gates, `.env` safety. |

## When you need specific guidance

| Topic | File |
|-------|------|
| Webapp dark theme, pages, data-testid | `WEBAPP_SOTA_STANDARDS.md` |
| Tool docstrings (no Args, Annotated+Field) | `TOOL_DESIGN_STANDARDS.md` + `rules/docstrings_sota.md` |
| Tauri NSIS build pipeline | `rules/tauri_nsis_building.md` |
| CORS configuration | `CORS_STANDARD.md` (in `standards/`) |
| CUA-NSIS smoke testing | `rules/cua_nsis_smoke_testing.md` |
| Session context injection (agent awareness) | `rules/session_context_injection.md` |
| Linting (Ruff, Biome) | `RUFF_STANDARDS.md`, `BIOME_STANDARDS.md` |
| Local LLM deployment | `LOCAL_LLM_STANDARDS.md` |
| Error handling patterns | `error-handling.md` |
| Security hardening | `SAFETY_PROTOCOLS.md`, `PROMPT_INJECTION_HARDENING.md` |

## Key directories

| Path | Contents |
|------|----------|
| `rules/` | Granular SOPs (workflow, docstrings, session injection, Tauri) |
| `packaging/` | NSIS and MSI build guides |
| `threats/` | MCP-specific threat models (context bombs, supply chain, botnets) |
