# Scanner Ecosystem Assessment (2026-03)

## Executive Take

The AI agent/MCP security scanner space is crowded and increasingly commoditized. Most offerings combine similar ingredients:

- static/signature rules
- behavioral/dataflow checks
- optional LLM semantic judging
- policy/report layers (SARIF, CI gates)

Differentiation is less about detector novelty and more about:

- methodology transparency
- reproducibility and version pinning
- triage/suppression workflow quality
- runtime control integration

Scanners should be treated as **telemetry**, not proof of safety.

## Interface-First Reality (Important)

A lot of scanner value is in protocol/interface quality checks:

- MCP client-to-server compatibility
- discoverability of tools/prompts/resources
- parameter/schema clarity and correctness
- invocation ergonomics and reliability signals

This matters because if clients cannot discover tools or pass correct parameters, even a well-written server becomes operationally useless.

But this also means a core limit:

- interface quality is **not** equivalent to payload safety
- good signatures and metadata do not guarantee safe underlying tool behavior

Operational implication: treat interface quality and payload safety as separate control objectives, and measure both.

## Market Assessment

### What feels mature

- multi-engine scanning is now table stakes
- CI-friendly formats and workflows are common
- better communication of "best-effort" limits is improving

### What remains weak

- inconsistent severity semantics across tools/sites
- unclear benchmark validity in some public leaderboards
- variable transparency about scoring pipelines
- "no findings" still frequently misinterpreted as "secure"

## External Scanner/Assessor Sites (Beyond ToolBench + Glama)

### 1) MCP Scoreboard

- URL: [mcpscoreboard.com](https://mcpscoreboard.com/)
- Positioning: large-scale MCP server quality scoring with methodology page.
- Strengths:
  - broad coverage
  - explicit dimension-style scoring
  - useful for discovery and rough prioritization
- Caveats:
  - score abstraction may hide context-specific risk
  - verify how much is directly tested vs inferred metadata

### 2) MCPScout.ai

- URL: [mcpscout.ai](https://www.mcpscout.ai/)
- Positioning: curated vetted directory with security notes and setup gotchas.
- Strengths:
  - practical install/operational notes
  - readable risk callouts
  - useful shortlist curation
- Caveats:
  - relies on platform claims for vetting depth
  - scoring criteria details should be independently validated before policy use

### 3) Sagentum

- URL: [sagentum.com](https://www.sagentum.com/)
- Positioning: independent MCP assessment registry with multidimensional ratings.
- Strengths:
  - strong emphasis on behavioral consistency and operational reliability
  - explicit "not recommended / caution" style classifications
- Caveats:
  - currently smaller assessed corpus than broad registries
  - should be used as high-signal sample, not exhaustive view

### 4) MCP Atlas

- URL: [mcpatlas.dev](https://mcpatlas.dev/about)
- Positioning: curated registry with weighted quality score model.
- Strengths:
  - transparent weighting model on/about page
  - decent for discovery and maintenance hygiene checks
- Caveats:
  - quality score factors include popularity and recency signals, not only security depth

## Related Resources (Not MCP registries, still useful)

### Prompt-injection/agent-security benchmarks

- InjecAgent: [github.com/uiuc-kang-lab/injecagent](https://github.com/uiuc-kang-lab/injecagent)
- AgentDyn (paper): [arXiv 2602.03117](https://arxiv.org/html/2602.03117v1)
- TensorTrust (game/benchmark dynamics): [tensortrust.ai](https://tensortrust.ai/)

Use these for attack-pattern education and defense evaluation design, not direct MCP fleet scoring.

## Recommended Use Model

- Keep ToolBench + Glama as base ecosystem inputs.
- Add **MCP Scoreboard + Sagentum** as primary external assessment complements.
- Use **MCPScout + MCP Atlas** as secondary discovery/context layers.
- Never gate production security solely on third-party scores.

## Practical Validation Checklist for Any Scanner/Assessor Site

- Is methodology public and versioned?
- Are score dimensions independently reproducible?
- Is there a clear separation between tested evidence and inferred metadata?
- Are false-positive and false-negative limits explicitly documented?
- Can results be exported and compared over time?

If these answers are weak, treat the source as discovery-only.

## Bottom Line

Yes, this is a cottage industry now. The winning strategy is not "find the perfect scanner."
It is to run a consistent internal control loop:

- pinned tools
- repeatable scans
- triage discipline
- runtime least privilege
- measurable remediation outcomes

