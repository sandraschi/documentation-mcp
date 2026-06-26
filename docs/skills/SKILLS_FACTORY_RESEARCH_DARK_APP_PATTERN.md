# Skills Factory Research: Dark App Factory Pattern Applied to Skill Creation

**Date:** 2026-02-10  
**Status:** Research complete, implementation in progress  
**Handoff:** Antigravity/Gemini can continue from TODO plans in advanced-memory-mcp and mcp-central-docs

---

## Executive Summary

Apply the **Dark App Factory** architectural pattern (Vibe -> Spec -> Specialist Council -> Validate -> Output) to **skill creation** within Advanced Memory MCP. The result: a **Skills Factory** that produces deeply researched, spec-compliant Claude/agent skills from a topic string, using research chaining, LLM-guided looping, and a tiered specialist council.

---

## Problem Statement

Current ADN skills tools:
- `adn_skills_creator` â€“ One-shot scaffold/validate/package; no research phase
- `make_skill_advanced` â€“ `research_driven_skill` uses web search only; no arxiv/github/rag chaining
- `adn_research` â€“ `research_orchestrate` is single-pass; no LLM-guided loop

Gaps:
1. No **research chaining** (arxiv -> github -> rag -> web in configurable pipelines)
2. No **LLM analysis along the path** (gap analysis, next-source decisions)
3. No **looped refinement** until coverage threshold
4. No **reference scaffolding** (auto-populate references/ from research)
5. No **spec validation** (agentskills.io compliance)
6. No **specialist council** pattern (domain-specific research + synthesis)

---

## Dark App Factory Architecture (Reference)

**Source:** `D:\Dev\repos\dark-app-factory`

### Pipeline
```
vibe.md  -->  [foreman enrich]  -->  enriched_vibe.md
                                        |
                                        v
          [foreman plan]  -->  specs.md + scenarios.md
                                        |
                                        v
                                 Worker Council (Specialist Council)
                                   Tier 0: Professor (skill battery)
                                   Tier 1: Plumber, Sculptor, Raggy, WebFinder, Archivist, etc.
                                   Tier 2: Librarian, Shakespeare, Morpheus, etc.
                                   Tier 3: Propagandist
                                   Tier 4: Generalist
                                        |
                                        v
                                 Judge (Satisficer) -> PASS/FAIL
```

### Key Patterns
- **Specialist base class:** `generate(specs, shared_context)` -> `{file_path: content}`
- **Dependency injection:** `get_dependency_context(shared_context)` â€“ upstream outputs capped at 8k chars
- **Validation hooks:** `validate(file_path, code, specs)` -> `(bool, str)`; retry on failure
- **declare_files():** Keyword-triggered mandatory files
- **Temperature per specialist:** Deterministic (0.1â€“0.2) for core; creative (0.6â€“0.7) for copy

### Components
- **Foreman:** Enrich vibe, plan specs, conduct research (Oracle)
- **Worker:** Orchestrate specialist council, run tiers in parallel via asyncio.gather
- **Judge:** Playwright + LLM verdict on generated app
- **Factory:** Full pipeline orchestrator

---

## Skills Factory: Pattern Mapping

| Dark App Factory | Skills Factory Equivalent |
|------------------|---------------------------|
| Vibe (vibe.md) | Topic string (e.g. "FastMCP 3.1.1+ agentic workflows") |
| Foreman enrich | Research chain: arxiv, github, rag, web, document |
| Foreman plan | Synthesis specialist: gap analysis, next sources |
| Professor (Tier 0) | Synthesis specialist â€“ consumes raw research, outputs ResearchBundle |
| Plumber/Sculptor | Draft specialist â€“ generates SKILL.md from ResearchBundle |
| Raggy, WebFinder | Research specialists â€“ arxiv, github, web, rag, document |
| Librarian | Reference scaffolder â€“ populates references/REFERENCE.md |
| Judge | Spec validator â€“ agentskills.io compliance, coverage check |
| Output app | Output skill â€“ SKILL.md + references/ |

---

## Research Specialists (Proposed)

| Specialist | Source | Temperature | Output |
|------------|--------|-------------|--------|
| ArxivSearcher | adn_arxiv_research | 0.1 | Snippets, citations from academic papers |
| GithubSearcher | adn_github_research | 0.1 | Code examples, repo summaries |
| RagSearcher | adn_rag | 0.1 | Knowledge graph / ingested content |
| WebSearcher | adn_web_search | 0.2 | Web search results |
| DocumentIngester | adn_document_ingest | 0.1 | Extracted text from PDF/EPUB |
| SynthesisSpecialist | LLM | 0.2 | ResearchBundle: synthesis, gaps, next_sources, coverage_score |
| DraftSpecialist | LLM | 0.4 | SKILL.md body + frontmatter |
| ReferenceScaffolder | â€” | â€” | references/REFERENCE.md, SOURCES.md |

---

## Data Structures

### ResearchBundle
```python
@dataclass
class ResearchBundle:
    topic: str
    snippets: list[dict]  # {source, content, url, relevance}
    citations: list[str]
    synthesis: str
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

## Implementation Location

**Primary:** Advanced Memory MCP (`D:\Dev\repos\advanced-memory-mcp`)

Rationale:
- Skills tools already exist (adn_skills_creator, make_skill_advanced, adn_research)
- Research sources (arxiv, github, rag, web) implemented
- MCP is the consumption interface
- Skills are knowledge artifacts; knowledge graph integration natural

**Reference only:** Dark App Factory â€“ import the **pattern**, not the codebase. No hard dependency.

---

## Handoff Notes for Antigravity/Gemini

1. **TODO plans:** See `advanced-memory-mcp/docs/SKILLS_FACTORY_TODO.md` and `mcp-central-docs/docs/skills/SKILLS_FACTORY_TODO.md`
2. **Implementation order:** Phase 1 (ResearchChainService) -> Phase 2 (adn_skills_research tool) -> Phase 3 (Reference scaffolding) -> Phase 4 (Spec validation) -> Phase 5 (research_first_create)
3. **Existing tools:** Reuse `adn_arxiv_research`, `adn_github_research`, `adn_rag`, `adn_web_search`, `adn_document_ingest` via imports; do not duplicate
4. **LLM client:** Use `advanced_memory.services.llm_client.LLMClient` for gap analysis and draft generation
5. **No emojis** in Python/logger per project rules
6. **PowerShell syntax** â€“ no `&&`, use `;` or separate lines

---

## References

- [ADN_SKILLS_DEEP_RESEARCH_IMPLEMENTATION_PLAN.md](ADN_SKILLS_DEEP_RESEARCH_IMPLEMENTATION_PLAN.md)
- [Dark App Factory Architecture](../../../dark-app-factory/docs/ARCHITECTURE.md)
- [RESEARCH_DRIVEN_SKILLS.md](../../../advanced-memory-mcp/docs/RESEARCH_DRIVEN_SKILLS.md)
- [agentskills.io](https://agentskills.io)

