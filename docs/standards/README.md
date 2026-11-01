---
title: "Standards Library Index"
category: standards
status: active
audience: all
last_updated: 2026-11-01
---

# Standards Library

Every engineering standard the sandraschi MCP fleet holds itself to, in one
place. If you are an agent, start with
[AGENT_READING_ORDER.md](./AGENT_READING_ORDER.md) instead — it tells you which
of these to read and in what order.

> **This page is generated.** Edit the standards' own frontmatter and re-run
> `python fleet-gate/standards_audit.py --render-index`. A hand-maintained index
> of this many files is stale within a week.

## At a glance

- **174 standards** (excluding backups and `_superseded/`)
- **Current FastMCP floor: 3.4.4** — read from `JUNE_2026_STANDARDS_BAR.md`, which is the single source
- **163 of 174** carry frontmatter; the rest have no declared status or last-updated date

### Where to start

| If you want to… | Read |
|---|---|
| Know what version of anything is current | [JUNE_2026_STANDARDS_BAR.md](./JUNE_2026_STANDARDS_BAR.md) |
| Work in this fleet as an agent | [AGENT_READING_ORDER.md](./AGENT_READING_ORDER.md) |
| Avoid a trap the fleet already hit | [TRAPS_AND_PITFALLS.md](./TRAPS_AND_PITFALLS.md), [BUGS_DEPOT](../troubleshooting/BUGS_DEPOT.md) |
| Build a new MCP server | [AGENTS.md](./AGENTS.md) §4.1 New Repo Gate |
| Ship an installer | [PACKAGING_STANDARDS.md](./PACKAGING_STANDARDS.md), [TAURI_PRODUCTION_PITFALLS.md](./TAURI_PRODUCTION_PITFALLS.md) |

## Ecosystem

2 files.

| Standard | What it covers | Status | Updated |
|---|---|---|---|
| [SKILLS_ECOSYSTEM_2026.md](./SKILLS_ECOSYSTEM_2026.md) | As of February 2026, the "Agent Skill" open standard (released Dec 2025) has become the dominant method for ex | review | 2026-06-26 |
| [opencode-plugins/README.md](./opencode-plugins/README.md) | Companion index: rust-crates/README.md(../rust-crates/README.md) is the Rust | review | 2026-09-02 |

## Guide

4 files.

| Standard | What it covers | Status | Updated |
|---|---|---|---|
| [TESTING_GUIDE.md](./TESTING_GUIDE.md) | Last updated: 2026-07-12 | review | 2026-07-26 |
| [testing-environment-aware.md](./testing-environment-aware.md) | Related: Testing Standards / Red-Green TDD | review | 2026-06-26 |
| [testing-tdd-red-green.md](./testing-tdd-red-green.md) | Related: Testing Standards / Code Quality Standards | review | 2026-06-26 |
| [testing.md](./testing.md) | Comprehensive testing standards for MCP servers, including unit tests, integration tests, end-to-end tests, an | review | 2026-06-26 |

## Pattern

2 files.

| Standard | What it covers | Status | Updated |
|---|---|---|---|
| [TAURI_API_PATTERNS.md](./TAURI_API_PATTERNS.md) | > | review | 2026-06-26 |
| [patterns/unicode_safety.md](./patterns/unicode_safety.md) | Established: originally scoped to script files; broadened 2026-07-13 per Sandra's direct instruction after a r | review | 2026-07-14 |

## Reference

4 files.

| Standard | What it covers | Status | Updated |
|---|---|---|---|
| [AGENT_INSTALL_REFERENCE.md](./AGENT_INSTALL_REFERENCE.md) | Hub: D:\Dev\repos\mcp-central-docs\ (mcd) | review | 2026-07-26 |
| [TAURI_DO_DONT_MATRIX.md](./TAURI_DO_DONT_MATRIX.md) | Tauri fleet — Do / Don | review | 2026-07-13 |
| [TAURI_PRODUCTION_PITFALLS.md](./TAURI_PRODUCTION_PITFALLS.md) | See also: | review | 2026-09-17 |
| [TRAPS_AND_PITFALLS.md](./TRAPS_AND_PITFALLS.md) | Purpose: Every time we discover an antipattern, a tool failure mode, or a process trap, it goes here. This is  | review | 2026-09-18 |

## Standard

129 files.

| Standard | What it covers | Status | Updated |
|---|---|---|---|
| [AGENTIC_INSTALL_STANDARD.md](./AGENTIC_INSTALL_STANDARD.md) | One-line rule: repos ship machine-readable facts, one tested single-step path, | draft | 2026-10-30 |
| [AGENTS.md](./AGENTS.md) | - Host: Windows 11, Goliath (AMD Ryzen 9 5900X, RTX 4090 24GB, 64GB RAM) | review | 2026-09-18 |
| [AGENT_ACTION_GATES.md](./AGENT_ACTION_GATES.md) | Anthropic's research note "GLM-5.3 and the spread of advanced cyber capabilities" | active | 2026-10-02 |
| [AGENT_CLIENT_PROTOCOL.md](./AGENT_CLIENT_PROTOCOL.md) | The Agent Client Protocol (ACP) is an open standard created by Zed Industries (released in August 2025) and su | review | 2026-07-13 |
| [AGENT_PROTOCOLS.md](./AGENT_PROTOCOLS.md) | > | review | 2026-09-18 |
| [AGENT_READING_ORDER.md](./AGENT_READING_ORDER.md) | Every agentic IDE working in this fleet reads this file. Claude Code, OpenCode, | active | 2026-09-18 |
| [APPS_PAGE_STANDARD.md](./APPS_PAGE_STANDARD.md) | Applies to: Every webapp with an Apps / Fleet Apps page (all -mcp with web/ or web_sota/) | review | 2026-09-09 |
| [BIOME_STANDARDS.md](./BIOME_STANDARDS.md) | Standardization for Industrial-Grade MCP TypeScript/JavaScript Repositories | review | 2026-08-02 |
| [BOOK_PRINT_PROFILE.md](./BOOK_PRINT_PROFILE.md) | Canonical print settings for the on- book series. The source of truth is | review | 2026-10-20 |
| [BUN_STANDARDS.md](./BUN_STANDARDS.md) | Bun replaces npm as the JS package manager and script runner. Vite stays. | active | 2026-08-22 |
| [CODE_QUALITY_STANDARDS.md](./CODE_QUALITY_STANDARDS.md) | Ruff is MANDATORY for all Python-based MCP servers. | review | 2026-07-29 |
| [CONTROL_PLANE_INSTALL.md](./CONTROL_PLANE_INSTALL.md) | Adopted: 2026-05-28 | review | 2026-06-26 |
| [CORS_STANDARD.md](./CORS_STANDARD.md) | Established: 2026-07-13 | review | 2026-08-07 |
| [DEEPLINK_STANDARD.md](./DEEPLINK_STANDARD.md) | Effective: 2025-10-28 | review | 2026-08-06 |
| [DEPLOYMENT_STANDARDS.md](./DEPLOYMENT_STANDARDS.md) | To maintain friction-less operation, all servers should support: | review | 2026-06-26 |
| [DIALOGIC_RETURNS.md](./DIALOGIC_RETURNS.md) | A Dialogic Return is a tool result that facilitates a conversational loop between the Tool and the AI Agent. I | review | 2026-06-26 |
| [DOCUMENTATION_STANDARDS.md](./DOCUMENTATION_STANDARDS.md) | Every SOTA MCP repository MUST have the following at the root: | review | 2026-06-26 |
| [DXT_DEPRECATION.md](./DXT_DEPRECATION.md) | Effective: 2026-06-17 | review | 2026-06-26 |
| [FASTMCP_FEATURES.md](./FASTMCP_FEATURES.md) | Audience: All fleet MCP server repos | review | 2026-07-12 |
| [FLEET_BUILD_TEST_PIPELINE.md](./FLEET_BUILD_TEST_PIPELINE.md) | Last Updated: 2026-06-14 | review | 2026-08-06 |
| [FLEET_CROSSCONNECT_STANDARD.md](./FLEET_CROSSCONNECT_STANDARD.md) | Adopted: 2026-09-12 | review | 2026-09-18 |
| [FLEET_EXECUTION.md](./FLEET_EXECUTION.md) | This standard defines the canonical pattern for fleet startup scripts (start.ps1) within the Antigravity ecosy | review | 2026-09-30 |
| [FLEET_GRADING_STANDARDS.md](./FLEET_GRADING_STANDARDS.md) | Standard: FLEET-RATING-SOTA-2026-04 | review | 2026-09-15 |
| [FLEET_HYGIENE_STANDARDS.md](./FLEET_HYGIENE_STANDARDS.md) | Scope: README.md, docs/.md, help pages, and dashboard copy across all repos under D:\Dev\repos\ | active | 2026-09-25 |
| [FLEET_PROMOTION.md](./FLEET_PROMOTION.md) | Adopted: 2026-05-29 | review | 2026-07-26 |
| [FRONTMATTER_STANDARD.md](./FRONTMATTER_STANDARD.md) | Version: 1.0 | active | 2026-02-25 |
| [GAZEBO_FLEET_BRIDGE_CONTRACT.md](./GAZEBO_FLEET_BRIDGE_CONTRACT.md) | ag-gazebo-bridge relays Gazebo simulation state outward to five other fleet repos via REST. As of 2026-09-21,  | draft | 2026-09-21 |
| [GH_STANDARDS.md](./GH_STANDARDS.md) | Version: 1.0 | active | 2026-04-20 |
| [GITHUB_ACTIONS_NO_PRIVATE_CI.md](./GITHUB_ACTIONS_NO_PRIVATE_CI.md) | Version: 1.1 (2026-07-26) | review | 2026-08-01 |
| [GITHUB_DISCUSSIONS.md](./GITHUB_DISCUSSIONS.md) | Scope: running Discussions on OUR repos (announcements, Q&A, community). | active | 2026-09-22 |
| [GITHUB_HYGIENE_STANDARDS.md](./GITHUB_HYGIENE_STANDARDS.md) | Scope: how our own fleet repos receive issues and PRs. For how we behave | active | 2026-10-25 |
| [GITHUB_TRIAGE_STANDARD.md](./GITHUB_TRIAGE_STANDARD.md) | Version: 1.0 (2026-10-13). Owner: Sandra. Applies to every agent | active | 2026-10-13 |
| [GITIGNORE_STANDARDS.md](./GITIGNORE_STANDARDS.md) | > | review | 2026-08-06 |
| [GIT_REPOSITORY_SAFETY.md](./GIT_REPOSITORY_SAFETY.md) | Version: 1.0 (2026-05-31) | review | 2026-09-10 |
| [GIT_WORKFLOW.md](./GIT_WORKFLOW.md) | Audience: Current contributors + future collaborators (Steve, etc.) | review | 2026-09-09 |
| [HANDOVER_STANDARD.md](./HANDOVER_STANDARD.md) | Version: 1.0 | active | 2026-08-30 |
| [HEALTH_ENDPOINT_STANDARD.md](./HEALTH_ENDPOINT_STANDARD.md) | 2026-07-17, advanced-memory-mcp: a SYSTEM-owned service child kept serving | review | 2026-07-17 |
| [HOST_APP_LIFECYCLE.md](./HOST_APP_LIFECYCLE.md) | Mandatory pattern for all MCP servers that depend on a host application. | active | 2026-02-26 |
| [IMPLEMENTATION_HONESTY_STANDARD.md](./IMPLEMENTATION_HONESTY_STANDARD.md) | Prevent "fake-green" systems where tools appear to succeed but are not implemented. | review | 2026-06-26 |
| [INFRASTRUCTURE_RELIABILITY.md](./INFRASTRUCTURE_RELIABILITY.md) | Docker Desktop on Windows is a Tier-2 host. Always anticipate vpnkit or Named Pipe instability. | review | 2026-06-26 |
| [JUNE_2026_STANDARDS_BAR.md](./JUNE_2026_STANDARDS_BAR.md) | Effective: 2026-06-17 | review | 2026-09-18 |
| [JUSTFILE_RECIPES.md](./JUSTFILE_RECIPES.md) | Every MCP server repo SHOULD have repo-specific just recipes beyond the standard lint/test/serve ones. These g | review | 2026-06-26 |
| [JUSTFILE_STANDARDS.md](./JUSTFILE_STANDARDS.md) | Most MCP fleet repositories use just as the primary task orchestration tool. This standard defines the SOTA In | review | 2026-09-18 |
| [LLM_AND_INSTALL_TIERS.md](./LLM_AND_INSTALL_TIERS.md) | Adopted: 2026-05-28 | review | 2026-06-26 |
| [LOCAL_LLM_FIRST_DOCTRINE.md](./LOCAL_LLM_FIRST_DOCTRINE.md) | Established: 2026-07-05 | review | 2026-08-17 |
| [LOCAL_LLM_STANDARDS.md](./LOCAL_LLM_STANDARDS.md) | Timestamp: 2026-01-23 | review | 2026-09-10 |
| [LOCAL_MEDIA_MODELS.md](./LOCAL_MEDIA_MODELS.md) | Scope: models we run ourselves to produce fleet assets - demo-video music and | review | 2026-10-21 |
| [MCPB_PACKAGING_STANDARDS.md](./MCPB_PACKAGING_STANDARDS.md) | Version: 2.2 (June 2026) | review | 2026-09-18 |
| [MCP_REGISTRY_PUBLISHING.md](./MCP_REGISTRY_PUBLISHING.md) | Registry: https://registry.modelcontextprotocol.io (preview, API frozen at v0.1) | review | 2026-09-09 |
| [MCP_WEBAPP_ABOUT_STANDARD.md](./MCP_WEBAPP_ABOUT_STANDARD.md) | Version: 1.0 (2026-08-27) | review | 2026-09-09 |
| [NAKED_PC_INSTALL_STANDARD.md](./NAKED_PC_INSTALL_STANDARD.md) | Every MCP webapp start.ps1 MUST work on a fresh Windows machine with nothing pre-installed. This standard exis | review | 2026-10-05 |
| [NEW_REPO_BUILD_COMPLETE.md](./NEW_REPO_BUILD_COMPLETE.md) | Version: 1.1 (2026-09-12) | review | 2026-09-12 |
| [NEXTJS_TURBOPACK.md](./NEXTJS_TURBOPACK.md) | Canonical upstream reference: Next.js — Turbopack(https://nextjs.org/docs/app/api-reference/turbopack) and Tur | active | 2026-04-21 |
| [ONBOARDING_STANDARD.md](./ONBOARDING_STANDARD.md) | Version: 1.0 (2026-07-26) | review | 2026-07-26 |
| [ONE_CLICK_INSTALL_UX_STANDARD.md](./ONE_CLICK_INSTALL_UX_STANDARD.md) | One-line rule: a stranger (or their AI agent) gets from git clone to a working server with one command, | draft | 2026-10-05 |
| [PACKAGING_STANDARDS.md](./PACKAGING_STANDARDS.md) | Every fleet server has two distinct install surfaces that solve different problems: | review | 2026-07-28 |
| [PANDOC_STANDARDS.md](./PANDOC_STANDARDS.md) | Version: 1.0 | active | 2026-04-20 |
| [POWERSHELL_51_STANDARD.md](./POWERSHELL_51_STANDARD.md) | The fleet speaks Windows PowerShell 5.1. Every .ps1 file and every just | active | 2026-09-27 |
| [POWERSHELL_STANDARDS.md](./POWERSHELL_STANDARDS.md) | 1.  NEVER fail silently: All scripts must use $ErrorActionPreference = "Stop". | review | 2026-06-26 |
| [PRE_COMMIT_HOOKS.md](./PRE_COMMIT_HOOKS.md) | Git and GitHub give you several distinct hook points. They run at different times and catch different problems | reference | 2026-07-31 |
| [PROJECT_PAGE_STANDARD.md](./PROJECT_PAGE_STANDARD.md) | Adopted: 2026-07-18 | review | 2026-08-02 |
| [PROMPT_INJECTION_HARDENING.md](./PROMPT_INJECTION_HARDENING.md) | To protect against Indirect Prompt Injection (IPI) and intentional Goal Hijacking, all SOTA-compliant ingestio | review | 2026-08-22 |
| [PY_STANDARDS.md](./PY_STANDARDS.md) | Version: 1.0 | active | 2026-04-20 |
| [QUALITY_GATES.md](./QUALITY_GATES.md) | Established: 2026-08-01 | review | 2026-08-01 |
| [RAG_ADDON_STANDARD.md](./RAG_ADDON_STANDARD.md) | implementation to be built in email-mcp, then rolled out repo by repo. | proposed | 2026-10-07 |
| [RAG_OPERATIONS_STANDARD.md](./RAG_OPERATIONS_STANDARD.md) | This standard establishes uniform architecture, API contracts, webapp UX patterns, and MCP tool interfaces for | active | 2026-09-12 |
| [RAT_EMERGENCY_PROTOCOL.md](./RAT_EMERGENCY_PROTOCOL.md) | The RAT Emergency Protocol is the fleet's catastrophic failure response. It is triggered when a high-sophistic | review | 2026-06-26 |
| [REACT_HARDENING.md](./REACT_HARDENING.md) | Proactive development patterns to prevent common React pitfalls, specifically targeting stability in complex,  | review | 2026-06-26 |
| [README_STRUCTURE.md](./README_STRUCTURE.md) | Adopted: 2026-05-28 | review | 2026-09-18 |
| [README_WEBAPP_SCREENSHOTS.md](./README_WEBAPP_SCREENSHOTS.md) | Adopted: 2026-05-29 | review | 2026-09-09 |
| [README_WRAPPER_MCP.md](./README_WRAPPER_MCP.md) | Adopted: 2026-05-29 | review | 2026-09-09 |
| [RELEASE_DISCIPLINE.md](./RELEASE_DISCIPLINE.md) | The fleet's GitHub org is a storefront, not a workshop. Strangers install | active | 2026-09-30 |
| [RELEASE_TIERS.md](./RELEASE_TIERS.md) | "Infrastructure MCP Tier" exception in tauri_nsis_building.md for any repo with a webapp. | active | 2026-10-06 |
| [RENOVATE_STANDARDS.md](./RENOVATE_STANDARDS.md) | Version: 1.0 | active | 2026-07-21 |
| [REPO_SOTA_BASH.md](./REPO_SOTA_BASH.md) | A SOTA Bash is a high-density modernization sprint. It is not "maintenance"; it is a systemic architectural up | review | 2026-07-20 |
| [RUFF_STANDARDS.md](./RUFF_STANDARDS.md) | Standardization for Industrial-Grade MCP Python Repositories | review | 2026-09-10 |
| [RUST_ARTCRAFT_STANDARD.md](./RUST_ARTCRAFT_STANDARD.md) | Pilot Reference Implementation: rust-devices-mcp(../projects/rust-devices-mcp/README.md) (D:\Dev\repos\rust-de | active | 2026-10-18 |
| [SAFETY_PROTOCOLS.md](./SAFETY_PROTOCOLS.md) | To prevent "Stubbing" (corrupting files with partial or placeholder content) and allow instant recovery from a | review | 2026-06-26 |
| [SAMPLING_API_RISKS.md](./SAMPLING_API_RISKS.md) | ﻿# Sampling & API Call Risks in MCP Servers | review | 2026-09-09 |
| [SCRIPT_STANDARDS.md](./SCRIPT_STANDARDS.md) | See also: POWERSHELL_STANDARDS.md, TAURI_PRODUCTION_PITFALLS.md §Batch Size Limit (10 files/commit), GIT_REPOS | review | 2026-09-09 |
| [SELF_HOSTED_WORKER_STANDARD.md](./SELF_HOSTED_WORKER_STANDARD.md) | Established: 2026-09-12 | review | 2026-09-18 |
| [SKILLS_HST_TAXONOMY.md](./SKILLS_HST_TAXONOMY.md) | Last Updated: 2026-05-21 | review | 2026-06-26 |
| [SMOKE_CONTRACT.md](./SMOKE_CONTRACT.md) | just ci proves the code is clean (lint, types, tests). just smoke proves the built thing | review | 2026-10-22 |
| [SOTA_REQUIREMENTS.md](./SOTA_REQUIREMENTS.md) | To maintain peer technical contributor status, all MCP servers must adhere to the SOTA v12.0 core principles: | review | 2026-09-18 |
| [STANDARDS_BAR.md](./STANDARDS_BAR.md) | Hub: AGENT_PROTOCOLS.md | review | 2026-09-18 |
| [STARLETTE_NO_PYDANTIC_STANDARD.md](./STARLETTE_NO_PYDANTIC_STANDARD.md) | Date: 2026-03-23 - revised 2026-04-25 - reversed 2026-09-30 (FastAPI default, Sandra's decision) | active | 2026-09-30 |
| [START_SCRIPT_STANDARD.md](./START_SCRIPT_STANDARD.md) | Last updated: 2026-07-27 | review | 2026-09-09 |
| [TOOLING_COST_MODEL.md](./TOOLING_COST_MODEL.md) | Established: 2026-08-16 | review | 2026-09-18 |
| [TOOL_DESIGN_STANDARDS.md](./TOOL_DESIGN_STANDARDS.md) | To prevent "Tool Explosion" while maintaining discoverability, the fleet standard is the Industrial Portmantea | review | 2026-09-12 |
| [UV_STANDARDS.md](./UV_STANDARDS.md) | Version: 1.0 | active | 2026-04-20 |
| [VERIFICATION_STANDARDS.md](./VERIFICATION_STANDARDS.md) | All UI changes and bug fixes MUST be verified using browser automation tools | review | 2026-08-01 |
| [VIBE_CODING_XR.md](./VIBE_CODING_XR.md) | Vibe Coding XR is an industrialized rapid-prototyping workflow that leverages high-reasoning LLMs (Gemini 3.1  | review | 2026-06-26 |
| [VOICE_COMMAND_BUS.md](./VOICE_COMMAND_BUS.md) | Canonical registry: ../config/voice_command_bus.yaml(../config/voice_command_bus.yaml) | review | 2026-09-15 |
| [WEBAPP_COMPANION_MODE.md](./WEBAPP_COMPANION_MODE.md) | Established: 2026-07-14 | review | 2026-07-14 |
| [WEBAPP_DIRECTORY_STANDARD.md](./WEBAPP_DIRECTORY_STANDARD.md) | Problem: Fleet scripts can't find the frontend because repos use different | review | 2026-09-09 |
| [WEBAPP_HELP_STANDARD.md](./WEBAPP_HELP_STANDARD.md) | Extends WEBAPP_SOTA_STANDARDS.md §III row 7 ("Help: full page - modal alone is not | active | 2026-09-23 |
| [WEBAPP_LOGS_PAGE.md](./WEBAPP_LOGS_PAGE.md) | Extends: WEBAPP_STANDARDS.md §1.1 Logger Panel, §6.3 | review | 2026-06-26 |
| [WEBAPP_SOTA_STANDARDS.md](./WEBAPP_SOTA_STANDARDS.md) | "Zero Runts Policy" - Mandatory Blueprint for MCP Server Frontends | active | 2026-09-30 |
| [WEBAPP_STANDARDS.md](./WEBAPP_STANDARDS.md) | > | superseded | 2026-09-18 |
| [WEBVIEW2_VS_LEGACY.md](./WEBVIEW2_VS_LEGACY.md) | Windows has shipped three web rendering engines for native apps. Understanding the lineage | review | 2026-06-26 |
| [WINDOWS_SERVICE_STANDARDS.md](./WINDOWS_SERVICE_STANDARDS.md) | Established: 2026-07-31 | review | 2026-09-10 |
| [WIP_COMMIT_STANDARD.md](./WIP_COMMIT_STANDARD.md) | Version: 1.1 (2026-10-24: BUG-089 launcher-zeroing exclusion). Owner: Sandra. Script: | active | 2026-10-24 |
| [WIZFILE_STANDARDS.md](./WIZFILE_STANDARDS.md) | Version: 1.0 | active | 2026-04-20 |
| [WIZTREE_STANDARDS.md](./WIZTREE_STANDARDS.md) | Version: 1.0 | active | 2026-04-20 |
| [WORK_REPORT_STANDARD.md](./WORK_REPORT_STANDARD.md) | When Sandra says "write up your work in Discord" (or "report", "document in sfb"), every | active | 2026-10-02 |
| [YAHBOOM_ROBOTICS_STANDARD.md](./YAHBOOM_ROBOTICS_STANDARD.md) | This standard defines the technical baseline and orchestration patterns for implementing autonomous physical a | review | 2026-06-26 |
| [ai-rag-2026.md](./ai-rag-2026.md) | Canonical implementation: mcp-central-docs → src/docs_mcp/backend/rag_core.py | active | 2026-06-01 |
| [ai-sampling.md](./ai-sampling.md) | Standards for implementing AI workflow sampling in MCP servers, enabling true AI-guided creative and iterative | review | 2026-06-26 |
| [docker-containerization.md](./docker-containerization.md) | Standards for containerizing MCP servers using Docker. | review | 2026-09-30 |
| [error-handling.md](./error-handling.md) | ﻿# Error Handling Standards | review | 2026-06-26 |
| [fastmcp-3.2-concurrency.md](./fastmcp-3.2-concurrency.md) | FastMCP 3.2+ Universal Connect Pattern enables simultaneous stdio + HTTP access, creating critical database co | review | 2026-06-26 |
| [fastmcp-3.2-startup-probes.md](./fastmcp-3.2-startup-probes.md) | MCP servers that depend on external resources (databases, APIs, filesystems) should | review | 2026-06-26 |
| [logging.md](./logging.md) | Comprehensive logging standards for MCP servers, ensuring consistent, structured, and actionable log output ac | review | 2026-06-26 |
| [packaging/MSI_BUILD.md](./packaging/MSI_BUILD.md) | Scope: Microsoft Installer — optional enterprise Windows installer format. | review | 2026-07-14 |
| [packaging/NSIS_BUILD.md](./packaging/NSIS_BUILD.md) | Scope: Nullsoft Scriptable Install System — the fleet's primary Windows installer format. | review | 2026-07-14 |
| [rust-artcraft/CONTAINMENT_AND_CRATES.md](./rust-artcraft/CONTAINMENT_AND_CRATES.md) | Parent Hub: RUST_ARTCRAFT_STANDARD.md(../RUST_ARTCRAFT_STANDARD.md) | active | 2026-10-17 |
| [rust-artcraft/CRAFT_APPS_MCP_UTILIZATION.md](./rust-artcraft/CRAFT_APPS_MCP_UTILIZATION.md) | Parent Hub: RUST_ARTCRAFT_STANDARD.md(../RUST_ARTCRAFT_STANDARD.md) | active | 2026-10-20 |
| [rust-artcraft/CRAFT_COMMAND_BUS.md](./rust-artcraft/CRAFT_COMMAND_BUS.md) | Why this doc exists. Every Craft app is a GUI application that can also be | review | 2026-10-20 |
| [rust-artcraft/ECOSYSTEM_IMPACT_SWIFT_AND_AGENTS.md](./rust-artcraft/ECOSYSTEM_IMPACT_SWIFT_AND_AGENTS.md) | Parent Hub: RUST_ARTCRAFT_STANDARD.md(../RUST_ARTCRAFT_STANDARD.md) | active | 2026-10-17 |
| [rust-artcraft/EGUI_DESKTOP_UI_AND_PARITY.md](./rust-artcraft/EGUI_DESKTOP_UI_AND_PARITY.md) | Parent Hub: RUST_ARTCRAFT_STANDARD.md(../RUST_ARTCRAFT_STANDARD.md) | active | 2026-10-17 |
| [rust-artcraft/FLEET_CONVERSION_STANDARD.md](./rust-artcraft/FLEET_CONVERSION_STANDARD.md) | Parent Hub: RUST_ARTCRAFT_STANDARD.md(../RUST_ARTCRAFT_STANDARD.md) | active | 2026-10-18 |
| [rust-artcraft/FLEET_TRIAGE_AND_PYPI_TRANSPILATION.md](./rust-artcraft/FLEET_TRIAGE_AND_PYPI_TRANSPILATION.md) | Parent Hub: RUST_ARTCRAFT_STANDARD.md(../RUST_ARTCRAFT_STANDARD.md) | active | 2026-10-17 |
| [rust-artcraft/ORACLE_LOOP.md](./rust-artcraft/ORACLE_LOOP.md) | Parent Hub: RUST_ARTCRAFT_STANDARD.md(../RUST_ARTCRAFT_STANDARD.md) | active | 2026-10-18 |
| [rust-artcraft/RELEASE_FACTORY.md](./rust-artcraft/RELEASE_FACTORY.md) | Parent Hub: RUST_ARTCRAFT_STANDARD.md(../RUST_ARTCRAFT_STANDARD.md) | desired | 2026-10-18 |
| [threats/AGENTIC_BOTNETS.md](./threats/AGENTIC_BOTNETS.md) | Established: 2026-07-11 | review | 2026-07-11 |
| [threats/AI_SANDBOX_ESCAPE_CASE_STUDY.md](./threats/AI_SANDBOX_ESCAPE_CASE_STUDY.md) | Date: 2026-07-22 | review | 2026-10-04 |
| [threats/CONTEXT_BOMBS.md](./threats/CONTEXT_BOMBS.md) | Established: 2026-07-15 | review | 2026-07-20 |
| [threats/CONTEXT_BOMBS_HN_DRAFT.md](./threats/CONTEXT_BOMBS_HN_DRAFT.md) | Title: Context bombs aren't just for canaries — they're the first enforceable AI opt-out | review | 2026-07-20 |
| [threats/MCP_SERVER_SUPPLY_CHAIN.md](./threats/MCP_SERVER_SUPPLY_CHAIN.md) | Established: 2026-07-15 | review | 2026-07-20 |

## Uncategorised — no frontmatter

12 files.

| Standard | What it covers | Status | Updated |
|---|---|---|---|
| [BONSAI_1BIT_QUANTIZATION.md](./BONSAI_1BIT_QUANTIZATION.md) | Date: 2026-09-23 · Owner: Sandra S. | — | 2026-09-23 |
| [EXTERNAL_FAULT_TRANSPARENCY.md](./EXTERNAL_FAULT_TRANSPARENCY.md) | Status: active. Applies to every fleet server that depends on an external | — | 2026-10-23 |
| [MCP_SERVER_FIRST_TIME_SUCCESS_GUARANTEE.md](./MCP_SERVER_FIRST_TIME_SUCCESS_GUARANTEE.md) | Every MCP server MUST work perfectly on first connection to any MCP client (Claude Desktop, Cursor, Zed, etc.) | obsolete | 2026-03-30 |
| [SEARCH_TOOLING_POSTURE.md](./SEARCH_TOOLING_POSTURE.md) | Rule: discovery quality must not depend on a single dead backend. Verification beats retrieval. | — | 2026-09-30 |
| [rust-crates/3D.md](./rust-crates/3D.md) | For rendering 3D content — AI-generated models (Hunyuan3D GLBs in Pinokio), | — | 2026-10-23 |
| [rust-crates/BEVY.md](./rust-crates/BEVY.md) | bevy 0.20 (verified 2026-10-17, MIT/Apache-2.0): "a refreshingly simple | — | 2026-10-23 |
| [rust-crates/COMMS.md](./rust-crates/COMMS.md) | Match the wire protocol with the smallest crate that speaks it. Everything | — | 2026-10-23 |
| [rust-crates/DATABASE.md](./rust-crates/DATABASE.md) | Rules: data files live under %LOCALAPPDATA%/<app>/ (Windows) or the repo | — | 2026-10-23 |
| [rust-crates/ECOSYSTEM.md](./rust-crates/ECOSYSTEM.md) | Honest map for agents planning rustifications: where Rust is strongest, | — | 2026-10-23 |
| [rust-crates/GRAPHS.md](./rust-crates/GRAPHS.md) | "Graphs" means two things; this doc covers both with one crate each. | — | 2026-10-23 |
| [rust-crates/README.md](./rust-crates/README.md) | Short, opinionated notes on the most important Rust crates for the | — | 2026-10-23 |
| [rust-crates/TOOLCHAIN.md](./rust-crates/TOOLCHAIN.md) | One table for agents arriving from Python/JS. The headline: Rust has no | — | 2026-10-23 |

## Rules (`standards/rules/`)

20 files.

| Standard | What it covers | Status | Updated |
|---|---|---|---|
| [rules/agentic_macros.md](./rules/agentic_macros.md) | Established: 2026-07-02 | review | 2026-09-15 |
| [rules/architecting_sota.md](./rules/architecting_sota.md) | Scope: Strategic architecture generation (systems, pipelines, multi-service stacks). | review | 2026-09-11 |
| [rules/ascii_output_hygiene.md](./rules/ascii_output_hygiene.md) | Established: 2026-08-16 · Blooper: standards/TRAPS_AND_PITFALLS.md #20-21, | review | 2026-08-16 |
| [rules/autohotkey_v2_standard.md](./rules/autohotkey_v2_standard.md) | Established: 2026-07-05 | review | 2026-07-08 |
| [rules/chat_skills_prefab_standard.md](./rules/chat_skills_prefab_standard.md) | Established: 2026-06-26 | review | 2026-09-21 |
| [rules/chat_speech_sota.md](./rules/chat_speech_sota.md) | Established: 2026-07-05 | review | 2026-07-08 |
| [rules/claude_dot_md_sota.md](./rules/claude_dot_md_sota.md) | Both Claude Code and opencode read ~/.claude/CLAUDE.md (or %USERPROFILE%\.claude\CLAUDE.md on Windows) as thei | review | 2026-06-26 |
| [rules/cua_nsis_smoke_testing.md](./rules/cua_nsis_smoke_testing.md) | Unit tests and Playwright E2E catch regressions in dev. They do not catch: | review | 2026-09-17 |
| [rules/cua_webapp_testing.md](./rules/cua_webapp_testing.md) | Established: 2026-08-02 | active | 2026-10-02 |
| [rules/docstrings_sota.md](./rules/docstrings_sota.md) | This protocol optimizes how FastMCP tools render in modern IDEs (like Cursor) by moving parameter documentatio | review | 2026-06-26 |
| [rules/mcp_registration.md](./rules/mcp_registration.md) | - Portmanteau Imports: Mandatory in src//mcp/tools/__init__.py. Re-exporting portmanteaus ensures registration | review | 2026-07-14 |
| [rules/open_source_contributing.md](./rules/open_source_contributing.md) | Scope: Opening issues and PRs against third-party open-source projects (NOT our own repos). | review | 2026-06-26 |
| [rules/opencode_plugins_sota.md](./rules/opencode_plugins_sota.md) | Established: 2026-08-02 | review | 2026-10-28 |
| [rules/per_directory_agents.md](./rules/per_directory_agents.md) | Established: 2026-07-23 | review | 2026-07-24 |
| [rules/playwright_e2e_sota.md](./rules/playwright_e2e_sota.md) | Every fleet repo with a webapp MUST include Playwright end-to-end tests. | review | 2026-08-15 |
| [rules/powershell-script-standards.md](./rules/powershell-script-standards.md) | - EM DASH (—) is never allowed in .ps1, .bat, or justfile (any line, including comments). | review | 2026-09-18 |
| [rules/session_context_injection.md](./rules/session_context_injection.md) | Established: 2026-07-02 | review | 2026-07-20 |
| [rules/tauri_nsis_building.md](./rules/tauri_nsis_building.md) | As of May 2026, Tauri 2.0 is the fleet's recommended native wrapper for all MCP webapps. It replaces Electron. | review | 2026-09-17 |
| [rules/temporal_grounding.md](./rules/temporal_grounding.md) | Established: 2026-08-16 · Trigger incident: AIWatcher digest dated | review | 2026-08-16 |
| [rules/workflow_2026.md](./rules/workflow_2026.md) | This workflow is the "Biggest Unlock" for high-leverage development. It front-loads thinking and maintains con | review | 2026-09-10 |

## Known problems in this library

Surfaced by `fleet-gate/standards_audit.py`, listed here rather than
hidden because a reader deserves to know which pages may mislead them.

- **E2** — AGENT_PROTOCOLS.md presents a pre-3.4.4 FastMCP as current: - **[SOTA Requirements](./SOTA_REQUIREMENTS.md)**: Core Architecture & FastMCP 3.2 features (includes **§2.2 M
- **E2** — AGENTS.md presents a pre-3.4.4 FastMCP as current: | FastMCP 3.2 features | `mcp-central-docs\standards\SOTA_REQUIREMENTS.md` |
- **E2** — error-handling.md presents a pre-3.4.4 FastMCP as current: > **FastMCP Parameter Naming**: When raising `MCPError`, always use `message=` instead of `description=`. Fast
- **E2** — fastmcp-3.2-concurrency.md presents a pre-3.4.4 FastMCP as current: **⚠️ CRITICAL: All write-enabled MCP servers MUST implement these patterns before FastMCP 3.2+ deployment.**
- **E2** — TAURI_PRODUCTION_PITFALLS.md presents a pre-3.4.4 FastMCP as current: | 6 | `mcp.get_tools()` doesn't exist in FastMCP 3.2 (it's `get_tool`); `tool_count` in health/diagnostics 500
- **E2** — WEBAPP_SOTA_STANDARDS.md presents a pre-3.4.4 FastMCP as current: | **Skill** | Mandatory (when server exposes skills) | When the MCP server exposes FastMCP 3.1 skills (Anthrop

## Conventions

- Every standard should carry frontmatter: `title`, `category`, `status`,
  `audience`, `last_updated`. See [FRONTMATTER_STANDARD.md](./FRONTMATTER_STANDARD.md).
- A superseded standard moves to `standards/_superseded/` and gains
  `superseded_by:`. Leaving it in place means a grep presents it as current.
- `rules/` holds narrow, task-scoped rules; the top level holds broad standards.
