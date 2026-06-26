# Agent Skills Ecosystem Assessment

**Date:** 2026-02-10  
**Subject:** 128-skill collection in `~/.claude/skills/` (Cursor surfaces from `.claude/skills`)

---

## Scope

A user-level skills collection at `C:\Users\<user>\.claude\skills\` with ~105-128 skills across eight categories. Cursor aggregates from `.claude`, `.cursor`, and `.codex` directories, hence the higher count.

---

## Structure

- **Format:** SKILL.md with YAML frontmatter (`name`, `description`)
- **Sections:** When to Use, Core Expertise, Instructions, Response Guidelines
- **Categories:** creative (12), culinary (14), linguistic (12), mathematics (19), nonsense (14), philosophy (11), sciences (12), technical (12)

---

## Strengths

| Aspect | Assessment |
|--------|------------|
| **Organization** | Clear category hierarchy; INDEX.md (105 total as of 2025-10-21) |
| **Coverage** | Broad domain spread; technical skills well aligned with coding |
| **Naming** | Distinct "When to Use" triggers for relevance matching |
| **Nonsense** | Separate label for astrology/tarot/etc.; intentional categorization |

---

## Weaknesses

| Issue | Detail |
|-------|--------|
| **Shallow content** | Core Expertise often placeholder: "[This skill provides expert guidance based on best practices...]" with little domain-specific material |
| **Boilerplate** | Many skills share identical Instructions/Response Guidelines; differentiation mainly via name and "When to Use" |
| **Context overhead** | 128 skills = many descriptions considered for relevance; can bloat context |
| **Name mismatch** | e.g. japanese-grammar-master has `name: 日本語文法マスター-japanese-grammar-master` in frontmatter; Cursor 2.4 expects `name` to match folder |

---

## Recommendations

1. **Enrich high-value skills** – Add real domain knowledge to technical skills (api-design, docker, python-debugging, mcp-server-developer, full-stack-developer) instead of generic boilerplate.
2. **Use `disable-model-invocation: true`** – For niche skills (culinary, philosophy, nonsense) so they load only when explicitly invoked via `/skill-name`.
3. **Fix frontmatter names** – Ensure `name` matches folder name for Cursor 2.4 skill discovery.
4. **Update INDEX.md** – Sync count and categories with actual directory state.

---

## Source

- **Origin:** Advanced Memory MCP (adn_skills)
- **Path:** `~/.claude/skills/` (Windows: `C:\Users\<user>\.claude\skills\`)
