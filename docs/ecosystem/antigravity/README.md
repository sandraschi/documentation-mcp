# Antigravity IDE Integration (SOTA)

> [!CAUTION]
> **DATA SAFETY RISK (Feb 2026 Registry)**: Antigravity is a powerful AI-first IDE, but it is subject to documented "drive-nuking" incidents where recursive deletions occurred during complex orchestration. 
> - **Requirement**: Cold storage backups are mandatory for all production repositories.

## Overview
Antigravity is Google's flagship Agentic IDE, built by the former Windsurf/Codeium team. It is optimized for the Gemini 3.0 ecosystem and provides deep orchestration for multiple parallel agents.

**Pricing (Jun 2026):** No longer a generous freebie — see [Antigravity 2.0 (May 2026)](#antigravity-20-may-2026) and [IDE_LOCAL_INFERENCE.md](../IDE_LOCAL_INFERENCE.md).

## MCP Integration
Antigravity features a hidden custom MCP server integration.
- **Access**: Navigate to `...` → `Manage MCP Servers` → `View raw config`.
- **Config Path**: Section 2.3 of [STANDARDS.md](../../../STANDARDS.md) details the primary `%APPDATA%\Antigravity` config and log roots.

## Specialized Features
- **Unicode-Free Code**: Unlike competitors, Antigravity is tuned to avoid superfluous emojis in scripts/programs, solving a major "BuzzKillCoding" pain point.
- **Agent Orchestration**: Native support for 10-minute high-speed runs with uninterrupted execution flow.

## Antigravity 2.0 (May 2026)

### Pricing & providers (fleet stance, Jun 2026)

| Topic | Verdict |
|-------|---------|
| **Free tier** | Effectively dead for real use (~20 req/day class); Gemini CLI individual free ends **2026-06-18** |
| **Paid** | Bundled: **$20 Pro**, **$100 Ultra (5×)**, **$200 Ultra top (20×)** — [plan changes blog](https://antigravity.google/blog/changes-to-antigravity-plans) |
| **Ollama / LM Studio** | **No** first-class provider (same class of problem as Cursor) |
| **DeepSeek** | **Not built-in**; OpenAI-compat BYOK often fails — prefer Zed/OpenCode for DS |
| **Appeal** | Low unless Google AI sub already justified; needs stable quotas + features to compete |

Full matrix: [IDE_LOCAL_INFERENCE.md](../IDE_LOCAL_INFERENCE.md).

## Antigravity 2.0 — SDK & CLI (May 2026)

As of May 2026, Google has open-sourced the **Antigravity SDK** (`google-antigravity` on PyPI, Apache 2.0) — a Python library for building AI coding agents with Gemini. A **CLI** (terminal TUI) shares the same core agent engine.

See **[ANTIGRAVITY_2.0_SDK_CLI.md](ANTIGRAVITY_2.0_SDK_CLI.md)** for the full architecture analysis, feature depth assessment, and fleet utility verdict.

**Planned fleet project:** **[antigravity-cli-mcp](../../projects/antigravity-cli-mcp.md)** — alternative approaches for a Cursor ↔ CLI MCP bridge (design only; SDK deprioritized due to token cost).

> [!WARNING]
> The SDK's agentic loop runs in a **closed-source Go binary** (`localharness`) bundled in the wheel. The Python code is pure orchestration. This violates fleet SOTA principle "self-own the critical path." Document and monitor — do not integrate into fleet workflows.

## Third-Party Ecosystem
Despite having no public GitHub repo, a surprisingly active third-party ecosystem has grown around Antigravity — account managers, mobile companions, MCP servers, and cross-IDE config tools.

See **[THIRD_PARTY_ECOSYSTEM.md](THIRD_PARTY_ECOSYSTEM.md)** for the full directory (10+ projects, including cockpit-tools at 7.9k stars).

## Fleet integration (resolved 2026-08-29)

The "Antigravity fleet" concept referenced elsewhere in fleet tooling (e.g. memops `adn_system`) is **not** a separate mystery integration — it's **[agy-fleet-mcp](../../projects/agy-fleet-mcp/README.md)** (v0.1.0, Beta, port 10825): a config-bridge MCP that syncs the Cursor MCP fleet into Antigravity CLI's Gemini config paths (`~/.gemini/config/mcp_config.json`, `~/.gemini/antigravity-cli/`, `~/.gemini/antigravity/`), diffs configs, validates commands, and enforces Antigravity's ~50-tool budget. Direction matters: **agy-fleet-mcp** pushes fleet config *into* Antigravity; the separate **agy-mcp** (PyPI, unbuilt stub at `projects/agy-mcp`) would go the other direction — wrapping the `agy` CLI itself as MCP tools. Don't confuse the two when grepping.

## Aug 2026 update (not yet reflected above)

Since this doc's pricing table was last touched (Jun 2026), two further Antigravity announcements landed:
- **Custom Agents** — Aug 12, 2026
- **IDE Extensions** + Gemini Enterprise integration — Aug 20, 2026
- **Gemini 3.6 Flash** (Jul 21) then **3.7 Flash** (Aug 13) as the underlying model — check current version before benchmarking, Google is iterating roughly monthly.

Not yet assessed for fleet relevance — flagging so the pricing/appeal verdict above isn't read as current without a re-check.

## Technical Deep Dive
For comprehensive hardware integration and Google AI universe details, refer to the specialized documentation:
- **[Google Ecosystem: Antigravity](../../google-ecosystem/antigravity/README.md)**
