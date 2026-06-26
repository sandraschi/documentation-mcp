---
tags:
  - skills
  - skills-factory
  - adn-content-status
  - status-report
timestamp: 2026-02-10
---

# ADN Content Status Report: Skills Factory

**Last Updated:** 2026-02-10  
**Status:** Phase 1-2 complete, Phase 3-5 pending

---

## Summary

Skills Factory applies the Dark App Factory specialist-council pattern to skill creation in Advanced Memory MCP. Status of implementation and ingestion readiness.

---

## Implementation Status

| Phase | Component | Status | Notes |
|-------|-----------|--------|-------|
| 1 | ResearchChainService | Done | `skill_research_chain.py` – run_chain, ResearchBundle, gap analysis |
| 2 | adn_skills_research tool | Done | MCP tool + adn_skills operation "research" |
| 3 | Reference scaffolding | Done | scaffold_references_from_research(); adn_skills_research(output_path=...) |
| 4 | Spec validation | Done | validate_skill_agentskills(); adn_skills_creator(validate) returns spec_compliant, warnings, agentskills_checks |
| 5 | research_first_create | Pending | End-to-end workflow in make_skill_advanced |

---

## Completed (2026-02-10)

- **skill_research_chain.py** – Chains arxiv, github, rag, web; LLM gap analysis after each batch; loop until coverage threshold or max_iterations
- **adn_skills_research** – Standalone MCP tool (FULL mode) and adn_skills(operation="research")
- **reference_scaffolder.py** – scaffold_references_from_research(); creates references/REFERENCE.md and references/SOURCES.md from ResearchBundle
- **adn_skills_research** – When output_format="skill_draft" and output_path provided, scaffolds references/ automatically
- **validate_skill_agentskills()** – agentskills.io baseline checks (name 1-64, description 1-1024, name matches dir)
- **adn_skills_creator(validate)** – Returns spec_compliant, warnings, agentskills_checks
- **Docs** – SKILLS_FACTORY_RESEARCH_DARK_APP_PATTERN.md, ADN_CONTENT_NOTE_SKILLS_FACTORY.md, SKILLS_FACTORY_TODO.md
- **Handoff** – TODO plans in advanced-memory-mcp and mcp-central-docs for Antigravity/Gemini continuation

---

## Pending

1. research_first_create operation (full pipeline: research -> draft -> scaffold -> validate -> review -> finalize)

---

## Ingestion Notes

- **Primary repo:** advanced-memory-mcp
- **Docs repo:** mcp-central-docs/docs/skills/
- **Reference pattern:** dark-app-factory (no code dependency)

---

## References

- [SKILLS_FACTORY_RESEARCH_DARK_APP_PATTERN.md](SKILLS_FACTORY_RESEARCH_DARK_APP_PATTERN.md)
- [ADN_CONTENT_NOTE_SKILLS_FACTORY.md](ADN_CONTENT_NOTE_SKILLS_FACTORY.md)
- [SKILLS_FACTORY_TODO.md](SKILLS_FACTORY_TODO.md)
- [advanced-memory-mcp/docs/SKILLS_FACTORY_TODO.md](../../../advanced-memory-mcp/docs/SKILLS_FACTORY_TODO.md)
