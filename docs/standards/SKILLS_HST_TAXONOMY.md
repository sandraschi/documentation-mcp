# Hierarchical Skill Trees (HST) — Fleet Taxonomy Standard

**Status**: Active Fleet Standard
**Last Updated**: 2026-05-21
**Scope**: Skill directory organization, discovery, and delegation at scale (100+ skills)

---

## 1. Definition

Hierarchical Skill Trees (HST) is a **directory-level taxonomy** for organizing
agent skills into domain-branching trees. It is orthogonal to the Anthropic
`agent_skills_spec.md` (which governs the *inside* of a SKILL.md) — HST governs
how skill *directories* are nested, discovered, and routed.

A leaf skill at `linguistic/japanese-grammar-master/SKILL.md` inherits the
domain context of `linguistic/` without repeating it in every leaf. The path
*is* the context injection chain.

---

## 2. The Scaling Problem

Flat skill registries hit a ceiling at ~50-100 skills:

| Problem | Flat List | HST |
|---|---|---|
| **Selection** | Model must scan all skills; degrades with count | Prune branches by domain, then select within |
| **Context cost** | Every leaf repeats domain framing | Parent provides domain context once |
| **Extension** | Merge conflicts, central registry edits | Drop a new leaf into the right branch |
| **Discovery** | O(n) linear scan | O(log n) branch elimination |

At 470+ skills (the fleet's on-disk collection), flat selection already degrades.
At 1,000+, it's unusable. HST keeps it tractable.

---

## 3. Relationship to Existing Specs

| Spec | Scope | HST Interaction |
|---|---|---|
| `agent_skills_spec.md` (Anthropic) | SKILL.md format: YAML frontmatter, Markdown body | **Orthogonal** — HST nests valid SKILL.md files; no format change |
| `SKILLS_ECOSYSTEM_2026.md` (Fleet) | Lifecycle, packaging, security, IDE parity | **Additive** — HST is the organizational layer beneath packaging |
| `fastmcp/skills-and-prompts.md` | MCP server-side skill exposure | **Compatible** — `SkillsDirectoryProvider` roots can point to tree nodes |

HST does **not** require changes to any upstream spec. It is a filesystem-level
convention that composes cleanly with the existing stack.

---

## 4. Directory Convention

```
skills/                          ← Root (agent skills depot)
├── _GATEKEEPER.md               ← Top-level routing instructions (optional)
│
├── linguistic/                  ← Domain branch
│   ├── _CONTEXT.md              ← Domain framing: "You are a language coach..."
│   ├── japanese-grammar-master/  ← Leaf skill (standard SKILL.md inside)
│   │   └── SKILL.md
│   ├── french-language-coach/
│   │   └── SKILL.md
│   └── polyglot-learning-strategies/
│       └── SKILL.md
│
├── mathematics/
│   ├── _CONTEXT.md
│   ├── calculus-tutor/
│   │   └── SKILL.md
│   ├── linear-algebra-expert/
│   │   └── SKILL.md
│   └── number-theory-explorer/
│       └── SKILL.md
│
├── technical/
│   ├── _CONTEXT.md
│   ├── api-design-architect/
│   ├── code-review-assistant/
│   └── git-workflow-specialist/
│
├── culinary/
├── philosophy/
├── sciences/
├── creative/
└── nonsense/                    ← Esoteric/metaphysical skills
```

### Rules

1. **Branch directories** (`linguistic/`, `mathematics/`) contain no SKILL.md
   at their root. They *may* contain a `_CONTEXT.md` for domain-level framing.
2. **Leaf directories** are standard Anthropic-compliant skill folders with
   a `SKILL.md` entry point.
3. **Depth is unbounded** but practical depth is 1-3 levels. The fleet
   currently operates at depth 2 (domain → skill).
4. **Naming**: Branch names are lowercase hyphen-case, same as skill names.
   Prefix underscores (`_CONTEXT.md`, `_GATEKEEPER.md`) mark meta-files that
   are not skills themselves.

---

## 5. Inheritance & Context Economics

When an agent activates a leaf skill at `linguistic/japanese-grammar-master`,
the loading sequence is:

```
1. skills/_GATEKEEPER.md          → "You have access to a skill tree..."
2. linguistic/_CONTEXT.md         → "You are a language coach. Use these patterns..."
3. japanese-grammar-master/SKILL.md → "Japanese grammar specifics: particles, keigo..."
```

The leaf does **not** repeat domain framing. The parent provides it once.
At 1,000+ skills, this saves massive context window space compared to flat
files where every skill redundantly includes "You are a language expert..."

---

## 6. Delegation Pattern (Parent as Router)

A parent branch can act as a **dispatcher** rather than requiring the model
to scan all leaves:

```markdown
# linguistic/_CONTEXT.md

You are a language coach. When the user asks about a specific language,
route to the appropriate specialist:

- Japanese grammar → `linguistic/japanese-grammar-master`
- French conversation → `linguistic/french-language-coach`
- Spanish tutoring → `linguistic/spanish-language-tutor`
- General strategies → `linguistic/polyglot-learning-strategies`
```

This is a convention, not a protocol change. The model reads the parent
context and self-routes. No tool calls, no API — just structured context.

---

## 7. Fleet Deployment (Current State)

The fleet's active skill depot at `C:\Users\sandr\.claude\skills\` already
implements HST with the following branches:

| Branch | Leaf Count | Examples |
|---|---|---|
| `linguistic/` | 16 | japanese-grammar-master, french-language-coach, kanji-etymology-expert |
| `mathematics/` | 18 | calculus-tutor, linear-algebra-expert, probability-theory-expert |
| `philosophy/` | 13 | analytic-philosophy-expert, buddhist-philosophy-teacher, ethics-moral-philosophy |
| `culinary/` | 11 | italian-cooking-expert, french-pastry-master, asian-fusion-chef |
| `technical/` | 13 | code-review-assistant, database-optimization-guru, security-best-practices |
| `sciences/` | 11 | biology-comprehensive-guide, physics-fundamentals-tutor, neuroscience-fundamentals |
| `creative/` | 8 | graphic-design-fundamentals, photography-composition-guide, uiux-design-consultant |
| `nonsense/` | 8 | tarot-reading-expert, astrology-interpretation-guide, dream-interpretation-analyst |

**Total**: ~98 active skills across 8 domain branches, depth 2.

The archived ~470-skill collection at `not-mcp-related/claude-skills/`
prefigures the same pattern with domain grouping (`official/`, `community/`,
`daft/`). The `INDEX.md` references 1,832 scraped community entries but
only ~470 are actual SKILL.md files on disk.

---

## 8. Extension Rules

Adding a new skill to the tree:

1. **Identify the domain.** If no branch exists, create one with a `_CONTEXT.md`.
2. **Drop the leaf.** Create `domain/new-skill-name/SKILL.md` following the
   Anthropic spec (YAML frontmatter + Markdown body).
3. **No central registry.** The filesystem *is* the registry. No manifests to
   update, no merge conflicts.
4. **Update the parent context** if the delegation table needs a new entry.

Adding a new domain branch:

1. Create `new-domain/_CONTEXT.md` with domain framing and delegation table.
2. Register the branch in the fleet standard (this document, §7).
3. Branches should represent coherent domains with at least 3-5 expected
   leaves. Avoid single-leaf branches (merge into nearest neighbor).

---

## 9. Why Not a Flat Registry?

- **JSON/YAML registries** require central updates, cause merge conflicts,
  and don't survive multi-IDE deployments.
- **Database-backed discovery** adds a runtime dependency that breaks offline
  and air-gapped workflows.
- **The filesystem is the universal API.** Every IDE, every agent framework,
  every OS reads directory trees. HST works everywhere with zero tooling.

This aligns with the "Karpathy wiki" philosophy: a small, curated root that
branches into increasingly specific expertise. The tree structure *itself*
is the selection mechanism — no external index needed.

---

## 10. Future: Proposal to Anthropic

HST could be proposed as a **Recommended Practice** appendix to the Agent
Skills Spec, but only after:

1. Fleet proves it at 1,000+ skill scale in daily use.
2. Interoperability is demonstrated across Antigravity, Cursor, Windsurf,
   and Zed (all of which already support nested directory structures).
3. The delegation pattern is battle-tested for routing accuracy vs. flat
   selection baselines.

The Anthropic spec is intentionally minimal (55 lines). HST adds value
without adding complexity to the core spec — it can remain a fleet
standard indefinitely without upstream adoption.

---

**Author**: Sandra Schipal (HST concept), fleet deployment 2025-2026
**References**: `SKILLS_ECOSYSTEM_2026.md`, `anthropic-skills/agent_skills_spec.md`
