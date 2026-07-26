# ToolBench — fleet alignment

[ToolBench](https://toolbench.arcade.dev/) (Arcade) scores published MCP tools on **definition quality**, **protocol readiness**, and **supportability** (GitHub signals). Grades are informative, not authoritative — but they surface gaps (missing enums, weak docstrings, no recovery hints) that match our own [TOOL_DESIGN_STANDARDS.md](../standards/TOOL_DESIGN_STANDARDS.md) §4+.

## Contents

| Doc | Purpose |
|-----|---------|
| [ARCADE_TOOLBENCH_ASSESSMENT.md](ARCADE_TOOLBENCH_ASSESSMENT.md) | **Thorough assessment:** Arcade affiliation, business model, what “scraping” means, heuristics, stdio cap, stars/supportability, how grades move |
| [TOOLBENCH_ANALYSIS.md](TOOLBENCH_ANALYSIS.md) | Short operational summary (dimensions, limitations) |
| [FLEET_ALIGNMENT.md](FLEET_ALIGNMENT.md) | Fleet checklist, rescan workflow, portmanteau vs benchmark |
| [TOOLBENCH_ECOSYSTEM.md](TOOLBENCH_ECOSYSTEM.md) | Glama vs ToolBench, **rescoring** after fixes, Arcade’s MCP product vs ToolBench, optional **`toolbench-mcp`** local repo |
| [PROACTIVE_HARDENING.md](PROACTIVE_HARDENING.md) | User-friendly anti-"F" workflow: what to capture, weekly loop, scope guardrails |
| [improvements/](improvements/README.md) | One note per server after we ship ToolBench-oriented fixes |
| [GLAMA_SCORING.md](GLAMA_SCORING.md) | **Glama-specific** scoring: TDQS 6 dimensions, grade thresholds, F→C fix, C-target docstring template, portmanteau tips, rescan workflow |
| [scripts/](scripts/README.md) | Optional **Playwright** scraper: discover assessment URLs + rate-limited fetch (no API) |

## Hub links

- Standards: [AGENT_PROTOCOLS.md](../standards/AGENT_PROTOCOLS.md) → Tool Design (ToolBench-aligned checklist).
- Naming: verb-led `snake_case` tools; optional domain token when disambiguation is needed ([TOOL_DESIGN_STANDARDS.md](../standards/TOOL_DESIGN_STANDARDS.md) naming row).

## Good idea?

Yes: a **single place** for “what ToolBench measures,” **how to interpret** it, and **what we changed per repo** avoids repeating the same explanation in every server README and gives reviewers a paper trail when scores move.
