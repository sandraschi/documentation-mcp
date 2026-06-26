---
tags:
  - skills
  - skills-factory
  - dark-app-factory
  - adn-content-note
  - research-chaining
  - implementation
timestamp: 2026-02-10
---

# ADN Content Note: Skills Factory (Dark App Factory Pattern)

## Summary

Apply Dark App Factory specialist-council pattern to skill creation within Advanced Memory MCP. Produces deeply researched, spec-compliant skills from a topic string via research chaining, LLM-guided looping, and tiered specialists.

## Key Concepts

- **Research chaining:** arxiv -> github -> rag -> web -> document in configurable pipelines
- **LLM analysis along the path:** After each batch, LLM does gap analysis, picks next sources
- **Looped refinement:** Repeat until coverage >= threshold or max iterations
- **Reference scaffolding:** Auto-populate references/ from ResearchBundle
- **Specialist council:** ArxivSearcher, GithubSearcher, RagSearcher, WebSearcher, SynthesisSpecialist, DraftSpecialist, ReferenceScaffolder

## Implementation Location

- **Primary:** `D:\Dev\repos\advanced-memory-mcp`
- **Docs:** `D:\Dev\repos\mcp-central-docs\docs\skills\`
- **Reference (pattern only):** `D:\Dev\repos\dark-app-factory`

## Status (2026-02-10)

- **Done:** ResearchChainService, adn_skills_research tool, adn_skills(operation="research")
- **Pending:** scaffold_references_from_research, spec validation, research_first_create

See [ADN_CONTENT_STATUS_SKILLS_FACTORY.md](ADN_CONTENT_STATUS_SKILLS_FACTORY.md) for full status.

## Actions

1. ~~Implement ResearchChainService (skill_research_chain.py)~~
2. ~~Add adn_skills_research tool or operation~~
3. Add scaffold_references_from_research()
4. Extend validate_skill with spec compliance
5. Add research_first_create operation to make_skill_advanced

## References

- [SKILLS_FACTORY_RESEARCH_DARK_APP_PATTERN.md](SKILLS_FACTORY_RESEARCH_DARK_APP_PATTERN.md)
- [ADN_SKILLS_DEEP_RESEARCH_IMPLEMENTATION_PLAN.md](ADN_SKILLS_DEEP_RESEARCH_IMPLEMENTATION_PLAN.md)
- [advanced-memory-mcp/docs/SKILLS_FACTORY_TODO.md](../../../advanced-memory-mcp/docs/SKILLS_FACTORY_TODO.md)
