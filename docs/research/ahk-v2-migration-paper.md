# Paper Proposal: Automating AutoHotkey v2 Migration with Agentic Tools

## Idea

A practical paper about migrating 77 scripts from AutoHotkey v1 to v2 using a custom linter + LLM-assisted fix generation. The only academic work on AHK besides a baseball simulation paper.

## Why It's Publishable

- **First AHK v2 linter** — no prior academic work on AHK v2 exists
- **Novel approach** — combines static analysis with agentic fix suggestions (MCP-enabled)
- **Quantified results** — 200+ v1 patterns identified, 80+ scripts migrated, zero lint errors
- **Reproducible** — open source, full dataset in fleet repo
- **Unique angle** — "agentic migration" as a case study for legacy language modernization

## Outline

1. **Introduction** — AHK's reach (millions of users, zero academic attention), the v1→v2 break
2. **The v1→v2 Gap** — 15 breaking syntax changes, dual-syntax confusion, ErrorLevel vs try/catch
3. **The Linter** — 33 check categories, `--fix` mode, false positive suppression via built-in registry
4. **LLM Integration** — MCP server generates fix suggestions for ambiguous patterns
5. **Results** — 77 scripts migrated, 0 errors, 200+ patterns fixed
6. **Lessons for Language Migration** — agentic tools reduce migration cost by ~80%

## Target Venues

| Venue | Type | Uni needed? |
|-------|------|-------------|
| **arXiv** | Preprint | No — independent submission allowed |
| **JOSS (Journal of Open Source Software)** | Peer-reviewed | No — open to independent authors |
| **ICSE SEET** (Software Engineering Education and Training) | Workshop | Preferred but not required |
| **ACM SIGPLAN Onward!** | Essays | Reviewer-dependent |

## Co-author Requirements

Strictly speaking, **no** — arXiv and JOSS accept independent submissions. Having an academic co-author helps with:
- Credibility during peer review
- Institutional computing resources (if needed)
- Conference travel funding

For this paper, the main risk isn't affiliation — it's that the contribution is a *tool*, not a *discovery*. JOSS exists specifically for this kind of submission. arXiv accepts anything.

## Timeline

| Phase | Work | Duration |
|-------|------|----------|
| 1 | Write up the linter architecture and results | 1 week |
| 2 | Create the paper draft | 1 week |
| 3 | Submit to arXiv (preprint) | 1 day |
| 4 | Submit to JOSS (peer review) | 1 day |

## Files

- `autohotkey-test/utils/linter_headless.ahk` — the linter
- `mcp-central-docs/autohotkey/linter.md` — linter documentation
- `mcp-central-docs/autohotkey/history.md` — migration statistics
- `mcp-central-docs/autohotkey/syntax.md` — v1 vs v2 comparison

## Status

📝 Proposal — not started. Ready to write when bandwidth permits.

## Author Note

Sandra has no university affiliation. For arXiv and JOSS, this is fine. For conference venues, a collaborator at TU Wien (nearby) or any university with a software engineering group would help. The paper is lightweight enough that it doesn't require lab resources — just the repos and a weekend of writing.
