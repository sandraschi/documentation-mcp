# Skills Factory TODO (mcp-central-docs)

**Date:** 2026-02-10  
**Handoff:** Antigravity/Gemini can continue implementation in advanced-memory-mcp using this plan.  
**Implementation repo:** `D:\Dev\repos\advanced-memory-mcp` – see `docs/SKILLS_FACTORY_TODO.md` there.

---

## Docs Tasks

- [ ] Add SKILLS_FACTORY_RESEARCH_DARK_APP_PATTERN.md to skills README table
- [ ] Add ADN_CONTENT_NOTE_SKILLS_FACTORY.md to skills README table
- [ ] Add SKILLS_FACTORY_TODO.md to skills README table
- [ ] Update ADN_SKILLS_DEEP_RESEARCH_IMPLEMENTATION_PLAN.md with Dark App Factory alignment section
- [ ] Create skills/patterns/skills-factory-dark-app-pattern.md (condensed reference for agents)

---

## Reference Links

| Doc | Purpose |
|-----|---------|
| [SKILLS_FACTORY_RESEARCH_DARK_APP_PATTERN.md](SKILLS_FACTORY_RESEARCH_DARK_APP_PATTERN.md) | Full research: Dark App Factory pattern applied to skills |
| [ADN_CONTENT_NOTE_SKILLS_FACTORY.md](ADN_CONTENT_NOTE_SKILLS_FACTORY.md) | ADN content note for Advanced Memory ingestion |
| [ADN_SKILLS_DEEP_RESEARCH_IMPLEMENTATION_PLAN.md](ADN_SKILLS_DEEP_RESEARCH_IMPLEMENTATION_PLAN.md) | Original implementation plan |
| [advanced-memory-mcp/docs/SKILLS_FACTORY_TODO.md](../../../advanced-memory-mcp/docs/SKILLS_FACTORY_TODO.md) | Implementation checklist |

---

## Handoff Checklist for Antigravity/Gemini

1. Implementation lives in **advanced-memory-mcp**; mcp-central-docs holds docs only
2. Start with Phase 1 (ResearchChainService) in advanced-memory-mcp
3. No emojis in Python/logger; PowerShell uses `;` not `&&`
4. Reuse existing adn_* research tools; do not duplicate
5. Use LLMClient from advanced_memory.services.llm_client
