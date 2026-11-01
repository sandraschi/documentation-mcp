# SOP Architecture — Macros, SOPs, and Skills

**Established**: 2026-07-22
**Status**: Active

## The Three Layers

| Layer | File | Lives in | Versioned | Purpose |
|-------|------|----------|-----------|---------|
| **Macro** | `standards/rules/agentic_macros.md` | mcd (git) | Yes | Trigger phrase → expanded steps that call SOPs |
| **SOP** | `patterns/*.md` | mcd (git) | Yes | Canonical procedure text, the single source of truth |
| **Skill** | `.opencode/skills/*/SKILL.md` or `.claude/skills/*/SKILL.md` | local only | No | Loaded on demand by the agent for task-specific context or workflow guidance |

No layer calls the next. SOPs are the source. Macros are thin wrappers that read and execute SOPs. Skills are irrelevant for SOPs — they're for complex domain workflows (Zettelkasten, paper ingestion, multi-step email) where the agent needs inline instruction, not a reference to a versioned file.

## Chaining Convention

- SOPs reference other SOPs by file path: `Read patterns/DOC_SYNC_SOP.md`
- The agent resolves the path at execution time by reading from `mcp-central-docs/`
- Macros do NOT contain SOP text inline — always delegate to the SOP file
- SOPs may call sub-SOPs the same way — the graph resolves at read-time
- There is no macro nesting or SOP invocation at the framework level; resolution is purely the agent following textual instructions

## Why Not Skills for SOPs?

Skills are tempting because they're designed for multi-step procedures. But:

| Concern | SOP (git) | Skill (local) |
|---------|-----------|---------------|
| Versioned? | Yes — commit history, PR review | No — local file, drifts silently |
| Fleet-wide? | Yes — every agent reads mcd | No — per-machine config |
| Searchable? | Yes — mcd docs are LanceDB-indexed, searchable from the mcd webapp semantic search page | No |
| Reviewable? | Yes — PRs change SOPs | No — changes are invisible |
| Survives context reset? | Yes — re-read from git | Yes — re-read from disk |
| Friction to update? | PR + merge | Direct edit (easier, but that's the trap) |

Skills shine for **domain guidance** that's tightly coupled to the agent's behavior (e.g., a skill that says "when the user asks to research a paper, always use `fetch_full_text` first, then `find_connected_papers`"). They fail for **procedures** that need review, history, and fleet consistency.

## Lifecycle of a Procedure

```
Need identified → Write SOP in patterns/*.md → Add macro reference in agentic_macros.md
                                                        ↓
                                              PR review (git gate)
                                                        ↓
                                              Merged → indexed in LanceDB
                                                        ↓
                                              Agent reads SOP at execution time
```

## When to Create Each

| Create a... | When... |
|-------------|---------|
| **SOP** | The procedure is repeatable, needs to be correct, and benefits from version history |
| **Macro** | A user trigger phrase should expand to multi-step work that calls one or more SOPs |
| **Skill** | The content is agent-behavioral guidance tied to a specific task, not a fleet procedure |

## How to Write a SOP

1. Start with `# {NAME} — {description}` and an `**Established**:` date header
2. List any **Callers** (macros or other SOPs that reference this one)
3. Define **Variables** the caller must substitute (`{repo}`, `{version}`, etc.)
4. Write phases as `## Phase N — {title}` with clear step-by-step instructions
5. End with a **Verification** checklist
6. Keep it self-contained — the reader has only this file

SOPs are ingested into mcd's LanceDB index, so they're full-text and semantically searchable from the mcd webapp.
