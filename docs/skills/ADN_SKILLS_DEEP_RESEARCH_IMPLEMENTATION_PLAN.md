# ADN Skills Deep Research Implementation Plan

**Date:** 2026-02-10  
**Status:** Plan (pre-implementation)  
**Target:** Advanced Memory MCP skill tools

---

## Executive Summary

Enhance Advanced Memory's skill tools with **research chaining**, **LLM-guided looping**, **reference scaffolding**, and **research-first creator mode** to produce deeply researched, spec-compliant skills from multi-source synthesis.

---

## Current State

| Component | Capability | Gap |
|-----------|------------|-----|
| `adn_research` | web_search, arxiv, github, rag_query, document_ingest, research_orchestrate | No LLM-guided loop; orchestrate is single-pass |
| `make_skill_advanced` | research_driven_skill, iterative_improvement, create_complete_skill | research_driven uses web only; no arxiv/github/rag chaining |
| `adn_skills` creator | One-shot prompt to generate skill | No research phase before generation |
| `adn_skills_creator` | scaffold, validate, package, upgrade | validate = structure only; no agentskills.io spec validation |
| Reference scaffolding | None | No automatic references/ population from research |

---

## Goals

1. **Research chaining** â€“ arxiv -> github -> rag -> document_ingest -> web in configurable pipelines
2. **LLM analysis along the path** â€“ After each research step, LLM analyzes findings, decides next sources, identifies gaps
3. **Looped refinement** â€“ Repeat research->analyze until coverage threshold or max iterations
4. **Reference scaffolding** â€“ Auto-populate `references/` (REFERENCE.md, etc.) from synthesized research
5. **Spec validation** â€“ agentskills.io compliance (name, description constraints, progressive disclosure)
6. **Research-first creator** â€“ New workflow: research phase -> draft -> LLM review -> final skill

---

## Architecture

### Phase 1: Research Chain Service

**New module:** `advanced_memory/services/skill_research_chain.py`

```
ResearchChainService
â”œâ”€â”€ sources: List[Literal["arxiv", "github", "rag", "document", "web"]]
â”œâ”€â”€ llm_analyzer: LLMClient (for gap analysis, next-step decisions)
â”œâ”€â”€ run_chain(topic, max_iterations, coverage_threshold) -> ResearchBundle
â””â”€â”€ ResearchBundle: {snippets, citations, synthesis, gaps_remaining}
```

**Flow:**
1. User provides topic (e.g. "FastMCP 3.1.1+ agentic workflows")
2. For each configured source, call existing tools (adn_arxiv, adn_github, adn_rag, etc.)
3. After each batch: LLM analyzes findings, outputs `{synthesis_summary, gaps: [...], next_sources: [...]}`
4. If gaps remain and iterations left: run next sources
5. Return aggregated ResearchBundle

**LLM prompts (structured):**
- `ResearchGapAnalysis`: synthesis (str), gaps (list[str]), next_sources (list[str]), coverage_score (float)
- `CoverageThreshold`: 0.0â€“1.0; stop when coverage_score >= threshold

---

### Phase 2: adn_skills_research Tool

**New MCP tool:** `adn_skills_research` (or operation in `adn_research` / `make_skill_advanced`)

**Parameters:**
- `topic`: str (required)
- `sources`: list[str] = ["arxiv", "github", "web", "rag"]  # configurable
- `max_iterations`: int = 3
- `coverage_threshold`: float = 0.85
- `output_format`: "bundle" | "skill_draft"  # bundle = raw research; skill_draft = pre-filled SKILL.md skeleton

**Returns:**
- `research_bundle`: {snippets, citations, synthesis, coverage_score}
- `skill_draft` (optional): SKILL.md with instructions derived from synthesis

**Integration:** Call ResearchChainService, optionally pass bundle to LLM for draft generation.

---

### Phase 3: Reference Scaffolding

**New function:** `scaffold_references_from_research(skill_path, research_bundle)`

- Creates `skill_path/references/`
- Writes `REFERENCE.md` with synthesized content, key concepts, citations
- Optionally: `SOURCES.md` (bib-style), domain-specific files (e.g. `fastmcp.md`)
- SKILL.md body references: `See [references/REFERENCE.md](references/REFERENCE.md) for details`

**Progressive disclosure:** Keep SKILL.md <500 lines; move heavy content to references/

---

### Phase 4: Spec Validation

**Extend** `validate_skill` in `skill_creator`:

- Name: 1â€“64 chars, lowercase, hyphens, matches directory
- Description: 1â€“1024 chars, non-empty
- Body: optional checks (e.g. max length warning)
- Optional: call `skills-ref validate` if available (soft dependency)

**New validation result fields:**
- `spec_compliant`: bool
- `warnings`: list[str] (e.g. "description too short for discovery")
- `agentskills_checks`: dict (per-field pass/fail)

---

### Phase 5: Research-First Creator Mode

**New operation in `make_skill_advanced`:** `research_first_create`

**Workflow:**
1. **Research** â€“ Run adn_skills_research(topic) -> ResearchBundle
2. **Draft** â€“ LLM generates SKILL.md from ResearchBundle (name, description, body, When to Use, Instructions)
3. **Scaffold** â€“ Create skill dir, references/, populate from research
4. **Validate** â€“ Run spec validation
5. **Review** â€“ LLM reviews draft against research; suggests fixes
6. **Iterate** (optional) â€“ Apply fixes, re-validate
7. **Finalize** â€“ Write SKILL.md, references/*

**Parameters:**
- `topic`: str
- `skill_name`: str (optional; derived from topic if omitted)
- `research_sources`: list[str]
- `max_research_iterations`: int
- `enable_review_loop`: bool = True
- `output_path`: str

---

## Implementation Order

| Phase | Effort | Dependencies | Deliverable |
|-------|--------|--------------|-------------|
| 1. ResearchChainService | 2â€“3 days | LLMClient, existing adn_* tools | `skill_research_chain.py` |
| 2. adn_skills_research tool | 1 day | Phase 1 | New tool or operation |
| 3. Reference scaffolding | 1 day | Phase 1 | `scaffold_references_from_research()` |
| 4. Spec validation | 0.5 day | skill_creator | Extended validate_skill |
| 5. research_first_create | 2 days | Phases 1â€“4 | make_skill_advanced operation |

**Total estimate:** ~7 days

---

## Data Structures

### ResearchBundle
```python
@dataclass
class ResearchBundle:
    topic: str
    snippets: list[dict]  # {source, content, url, relevance}
    citations: list[str]
    synthesis: str  # LLM summary of findings
    gaps_remaining: list[str]
    coverage_score: float
    iteration_count: int
    sources_used: list[str]
```

### ResearchGapAnalysis (Pydantic)
```python
class ResearchGapAnalysis(BaseModel):
    synthesis: str
    gaps: list[str]
    next_sources: list[str]
    coverage_score: float
    should_continue: bool
```

---

## LLM Prompts (Templates)

### Gap Analysis (after each research batch)
```
You are analyzing research findings for a skill about: {topic}

Findings so far:
{snippets}

Synthesize what we know, identify gaps (missing concepts, unclear areas, needed depth),
and recommend which sources to query next (arxiv, github, rag, web, document).
Output structured: synthesis, gaps, next_sources, coverage_score (0-1), should_continue.
```

### Draft Generation (from ResearchBundle)
```
Using this research bundle for topic "{topic}":
{synthesis}
{citations}

Generate a complete SKILL.md following agentskills.io spec:
- name (slug)
- description (1-1024 chars, what + when to use)
- Body: When to Use, Core Expertise, Instructions, Response Guidelines
- Reference heavy content in references/REFERENCE.md
Keep main body under 300 lines; put detailed references in REFERENCE.md.
```

---

## Files to Create/Modify

| File | Action |
|------|--------|
| `src/advanced_memory/services/skill_research_chain.py` | Create |
| `src/advanced_memory/mcp/tools/adn_skills_research.py` | Create (or extend portmanteau) |
| `src/advanced_memory/services/skill_creator/` | Add `reference_scaffolder.py`, extend `validate_skill` |
| `src/advanced_memory/mcp/tools/make_skill_advanced.py` | Add `research_first_create` |
| `docs/skills/ADN_SKILLS_DEEP_RESEARCH_IMPLEMENTATION_PLAN.md` | This plan |

---

## Success Criteria

1. Single tool call can produce a deeply researched skill from topic string
2. Research loop stops when coverage >= threshold or max iterations
3. references/ populated automatically from research
4. Spec validation catches name/description/size issues
5. Existing tools (adn_research, make_skill_advanced) remain backward-compatible

---

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| LLM cost/latency in loop | Cap max_iterations; use smaller model for gap analysis |
| Over-researching | coverage_threshold and early exit |
| Spec drift | Pin to agentskills.io spec; add validation tests |
| Tool bloat | Consolidate into make_skill_advanced + adn_research operations |

---

## References

- [agentskills.io specification](https://agentskills.io/specification)
- [anthropics/skills](https://github.com/anthropics/skills)
- [RESEARCH_DRIVEN_SKILLS.md](../../advanced-memory-mcp/docs/RESEARCH_DRIVEN_SKILLS.md) (existing)
- [make_skill_advanced](../../advanced-memory-mcp/src/advanced_memory/mcp/tools/make_skill_advanced.py)
- [portmanteau_research](../../advanced-memory-mcp/src/advanced_memory/mcp/tools/portmanteau_research.py)

