# Spec-First Interview — SOP

**Trigger**: `spec <feature-name>`
**Reference macro**: `agentic_macros.md` → `spec`
**Scope**: Lock requirements before writing any code. Prevents building the wrong thing.

---

## Why spec-first

LLMs are eager to please. Asked to build a feature, they generate code immediately — often the wrong code, because they guessed the requirements instead of asking. The Spec-First Interview forces a **requirements lock** before any code is written. It costs 2-5 minutes of conversation and saves hours of rework.

The deliverable is a `SPEC.md` file at the repo root that survives context resets, can be reviewed by humans, and prevents the model from introducing hallucinated features during implementation.

---

## Phase 1 — Interview

Ask clarifying questions until all of these are answered. Do NOT proceed to Phase 2 until every question has a concrete answer.

### 1A. What

| Question | Why | Must-have? |
|----------|-----|------------|
| What exactly should this feature do? (1-2 sentences) | Core scope | ✅ |
| What is the user's workflow? (step-by-step) | Context | ✅ |
| What existing feature is this most similar to? | Pattern reference | ✅ |
| Does this change an existing component or create a new one? | Architecture | ✅ |
| What data does it read/write? | Data model | ✅ |

### 1B. Why

| Question | Why | Must-have? |
|----------|-----|------------|
| What problem does this solve? | Motivation | ✅ |
| Who is the end user? | Audience | ✅ |
| What happens if we don't build it? | Priority signal | Recommended |
| Is this a nice-to-have or a blocker? | Priority signal | Recommended |

### 1C. How

| Question | Why | Must-have? |
|----------|-----|------------|
| Any constraints? (performance, security, compatibility) | Guardrails | ✅ |
| Which existing files will change? | Change scope | ✅ |
| Any new dependencies? | Bloat check | ✅ |
| Should this be behind a feature flag? | Rollout | Recommended |
| How will we test it? | Test plan | ✅ |
| What could go wrong? (edge cases, failure modes) | Resilience | Recommended |

### 1D. Non-goals

| Question | Why | Must-have? |
|----------|-----|------------|
| What is explicitly NOT in scope? | Scope fence | ✅ |
| What follow-up work is deferred? | Honesty | Recommended |

---

## Phase 2 — Write SPEC.md

Write to `{repo-root}/SPEC.md`. Template:

````markdown
# SPEC: {Feature Name}

**Status**: Draft / Approved / Implemented
**Date**: {ISO date}

## Goal

{1-2 sentences}

## Requirements

- [ ] {requirement 1}
- [ ] {requirement 2}

## Non-goals

- {explicitly excluded}

## API / Interface

{If a REST endpoint: method, path, request body, response shape.
 If a function: signature, params, return type.
 If a UI component: props, slots, events.}

## Data model

{New types, tables, or fields.}

## Files changed

- {path/to/file.py} — {what changes}
- {path/to/file.tsx} — {what changes}

## Dependencies

{Any new library, tool, or service. If none, say "None."}

## Test plan

{How to verify correctness.}

## Open questions

- {anything not yet decided}
````

---

## Phase 3 — Present & Gate

1. Present the SPEC.md to the user in a readable format
2. Ask: "Does this spec look correct? Shall I proceed with implementation?"
3. **Do NOT start coding until the user explicitly approves.** An ambiguous "looks good" is not approval — the user must say "yes" or "approved" or "proceed"
4. Once approved, update STATUS in SPEC.md to "Approved" and begin implementation
5. If the user requests changes during review, update SPEC.md and re-present

---

## Phase 4 — Implementation guard

During implementation, the SPEC.md is the **source of truth**:

- Every feature must trace to a requirement in the spec
- New requirements discovered during implementation go through the interview again (add to Open Questions → update spec → get approval)
- If the scope creeps beyond what the spec describes, stop and flag it
- Do NOT add features not in the spec, no matter how tempting

---

## Phase 5 — Close

When implementation is complete:

1. Update `SPEC.md` status to "Implemented"
2. Mark all requirements as done
3. Optionally commit SPEC.md alongside the implementation for audit trail

---

## Anti-patterns

| Anti-pattern | Why it fails |
|-------------|-------------|
| **Skipping the interview** | Coding the wrong thing faster is not progress |
| **Writing the spec yourself** | The user's answers to the interview are the value — don't substitute your guesses |
| **Ambiguous requirements** | "Fast" and "secure" mean different things to different people — quantify |
| **No non-goals section** | Without explicit exclusion, everything is in scope |
| **Coding before approval** | The gate exists for a reason — an approved spec prevents 3AM rewrites |
| **Silent scope creep** | The spec says one thing, the code does more — the reviewer catches this and trust erodes |
