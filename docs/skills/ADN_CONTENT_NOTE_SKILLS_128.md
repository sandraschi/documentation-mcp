---
tags:
  - skills
  - agent-skills
  - cursor
  - adn-content-note
  - assessment
timestamp: 2026-02-10
---

# ADN Content Note: 128-Skill Collection Assessment

## Summary

Assessment of the user-level skills collection in `~/.claude/skills/` (128 skills surfaced by Cursor). Cursor aggregates from `.claude`, `.cursor`, and `.codex` directories.

## Findings

- **Structure:** Consistent SKILL.md format; YAML frontmatter; When to Use, Core Expertise, Instructions, Response Guidelines
- **Strengths:** Broad coverage, clear categories, technical skills useful for coding
- **Weaknesses:** Shallow content (placeholder Core Expertise), heavy boilerplate, context overhead, some name mismatches

## Actions

1. Enrich high-value technical skills with real domain knowledge
2. Add `disable-model-invocation: true` for niche skills
3. Fix frontmatter `name` to match folder names
4. Sync INDEX.md with actual count

## Reference

Full assessment: [AGENT_SKILLS_ECOSYSTEM_ASSESSMENT.md](AGENT_SKILLS_ECOSYSTEM_ASSESSMENT.md)
