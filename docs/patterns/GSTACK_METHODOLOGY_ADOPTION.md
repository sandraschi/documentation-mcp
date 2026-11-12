---
title: "gstack Methodology Adoption - Decision Record and Provenance"
category: pattern
status: active
audience: mcp-dev
last_updated: 2026-11-04
---

# gstack Methodology Adoption - Decision Record

**Decision: do not install `garrytan/gstack` into the harness now. Port the
transferable methodology into fleet patterns at a pinned commit, and re-evaluate
on 2026-12-02 against three explicit gates.**

This file is the record of that decision, what was taken, what was deliberately
not taken, and where the source lives. It exists so a future session does not
re-litigate the question from a blog post, and so any ported claim can be traced
to an exact upstream commit.

---

## 1. What gstack is

`github.com/garrytan/gstack` is Garry Tan's (President and CEO of Y Combinator)
open-sourced personal agent setup. Facts verified against the repository at the
pinned commit in section 5:

| Attribute | Value |
|---|---|
| Type | A library of Markdown agent skills (slash commands), plus a `./setup` script |
| Not | Not an MCP server, not a framework, not a runtime dependency |
| License | MIT |
| Self-description | "a process, not a collection of tools" |
| Core loop | Think -> Plan -> Build -> Review -> Test -> Ship -> Reflect |
| Advertised count | "23 opinionated tools" in the README tagline |
| Actual count | 60+ skills documented in `docs/skills.md`; third-party indexes count ~70 skill directories |
| Hosts | Claude Code (certified "full" tier); OpenCode, Codex CLI, Cursor, Factory, Kiro, Copilot CLI, Antigravity, Gemini CLI, OpenClaw, Hermes (experimental); Slate, GBrain (instruction-only) |

The advertised 23 vs the actual 60+ is noted because the marketing line is stale,
not because the count matters. A repo whose front-page number is already wrong is
a repo still in motion.

---

## 2. Why it was not installed wholesale

These are fleet-specific reasons, not a judgement on gstack's quality.

### 2.1 Skill trigger collision

The fleet already runs roughly twenty opinionated skills: `assfix`, `drift-scan`,
`fakefind`, `gapfind`, `wrappee-drift`, `repo-expert`, `fleet-expert`,
`quality-check`, `code-review-assistant`, `testing-strategy-guide`,
`refactoring-specialist`, and others. gstack adds 60-plus more with overlapping
intent: `/review`, `/verify`, `/health`, `/spec`, `/retro`.

Installing it means two skill sets competing for the same trigger space. The
failure mode is silent: the wrong skill fires, produces a plausible result, and
nobody notices until the output is wrong. That cost lands on the operator, not on
gstack.

### 2.2 Team mode is a hard no

`./setup --team` plus `gstack-team-init required` installs a Node-on-PATH hook
that blocks commits in a repo until gstack is present. For a solo-operated fleet
of ~190 repos the upside is zero and the blast radius is every commit. Do not run
`--team` or `required` in any fleet repo.

### 2.3 Instability

At the pinned commit the repo releases twice weekly, commit dates cluster on the
days immediately before review, and the README count is stale (section 1). Skills
are renamed between hosts (`/office-hours` vs `/gstack-office-hours`), and the
non-Claude tiers are "experimental" - passing conformance tests but with no
certified end-to-end workflow run.

Plain Markdown under MIT means waiting costs nothing. There is no lock-in and no
migration to avoid.

### 2.4 Asymmetric safety

This is the decisive operational point.

On Claude Code, gstack's safety skills (`/careful`, `/freeze`, `/guard`) are
enforced by hooks that block destructive commands. On OpenCode and every other
host they are advisory only - the model can ignore them.

Installing gstack to get command guarding, then running it under OpenCode, gives
the operator a guard dog with no teeth. That is worse than having no guard,
because it creates false confidence. The fleet's actual guard is
`standards/GIT_REPOSITORY_SAFETY.md` plus the `.bak` and batch-size rules, which
apply regardless of host.

---

## 3. What was worth taking

Two capabilities have no close fleet equivalent.

### 3.1 Live design audit with a repair loop

`/design-review` runs a structured visual audit against a running page, then
repairs what it finds: locate source, minimal change, one atomic commit per
finding, re-navigate, before/after screenshots, risk budget, hard fix cap.

Fleet audits (`fakefind`, `gapfind`, `webapp-coverage-audit`) are read-only.
They report; they do not fix and they do not prove the fix visually. That is a
genuine gap. Ported to `DESIGN_REVIEW_80_ITEM_AUDIT.md`.

### 3.2 Premise challenge before code

`/office-hours` refuses to accept a feature request at face value. It questions
whether the named problem is the real problem, then produces a design artifact.
The fleet is strong at execution rigor (specs, standards, gates) and comparatively
weak at attacking the premise before a spec is written. Ported to
`PREMISE_CHALLENGE_SIX_QUESTIONS.md`.

### 3.3 Review gate integrity (secondary, small)

From `/review`: the framing that a weakened test, timeout, snapshot or
suppression is a finding that must reach a human by name, and that review
freshness must be tied to current content rather than to a commit hash. Ported to
`REVIEW_GATE_INTEGRITY.md`.

---

## 4. What was deliberately not taken

Documented so these read as decisions, not omissions.

| Not taken | Why |
|---|---|
| `./setup`, `--team`, `required` hooks | Section 2.2 |
| The auto-update check (hourly, every session) | Unwanted network chatter in a controlled environment |
| Aside browser dependency, bundled Chromium build | macOS-first; fleet uses its own browser tooling |
| `impeccable` design-detector binary download | A third-party binary over project files is not worth it for a checklist we can run as judgement |
| 60-plus skills installed into `~/.claude/skills/` | Section 2.1 |
| `gbrain`, `Conductor`, telemetry, question-tuning machinery | Host-specific plumbing with no fleet equivalent to plug into |
| Raw vendored copies of upstream files | See provenance policy, section 5.3 |

---

## 5. Provenance

### 5.1 Source

| Field | Value |
|---|---|
| Repository | `https://github.com/garrytan/gstack` |
| License | MIT |
| Author | Garry Tan (Y Combinator) |
| Pinned commit | `622e8b1f76d293b647eca7b33d9dd060ab618b21` |
| Commit date observed | 2026-11-04 |
| Retrieved | 2026-11-04 19:44 +01:00 |
| Retrieval method | `openserp_extract` (GitHub raw), `curl` to temp for the 85 KB file |

### 5.2 Files actually read

| Path at pinned commit | Bytes | Used for |
|---|---|---|
| `design-review/SKILL.md` | 84869 | Browser-driving rules, Phases 1-6+, checklist location |
| `design-review/sections/craft-audit.md` | 7067 | Listed only; not ported |
| `office-hours/SKILL.md` | 44140 | Phase structure, hard gate, two modes |
| `office-hours/sections/phase-2a-startup-diagnostic.md` | 13682 | The six forcing questions, operating principles, pushback patterns |
| `review/SKILL.md` | 84883 | Gate integrity, fix-first, completion vs convergence |

Not read at all: `browse/`, `qa/`, `ship/`, `cso/`, `design-html/`,
`design-shotgun/`, `captain/`, `ios-*`, and the remaining ~55 skill directories.
Any future claim about those requires a fresh read at a pinned commit; do not
extrapolate from this document.

### 5.3 Provenance policy - why no vendored copies

The raw upstream bodies are **not** stored in this repo. A pinned SHA plus the
exact paths is a complete, reproducible reference; 184 KB of third-party Markdown
in a private docs repo is noise that will drift out of sync with the SHA it claims
to represent.

Reproduce any source body exactly:

```powershell
$sha = '622e8b1f76d293b647eca7b33d9dd060ab618b21'
$base = "https://raw.githubusercontent.com/garrytan/gstack/$sha"
curl.exe -sSL "$base/design-review/SKILL.md" -o design-review.SKILL.md
curl.exe -sSL "$base/office-hours/sections/phase-2a-startup-diagnostic.md" -o phase-2a.md
curl.exe -sSL "$base/review/SKILL.md" -o review.SKILL.md
```

Verify you are looking at the intended revision before trusting a diff:

```powershell
gh api "repos/garrytan/gstack/commits/main" --jq .sha
```

If that differs from the pinned SHA, you are looking at a newer upstream. Diff
deliberately; do not assume the methodology is unchanged.

---

## 6. Re-evaluation gates

Revisit on **2026-12-02** (four weeks, roughly eight releases), or earlier if all
three gates happen to pass. Do not install before all three hold.

| Gate | Why it matters | How to check |
|---|---|---|
| OpenCode reaches `full` tier | Currently uncertified; safety is advisory | `./setup --status` after a clone, or the host table in `README.md` |
| Skill count stabilizes and the "23" tagline is corrected | Signals the surface has settled and they know what they ship | Read `README.md` count vs `docs/skills.md` count |
| A version tag exists (v1.x) | Enables pinning to a release instead of tracking `main` | `gh release list -R garrytan/gstack --limit 5` |

If all three pass, the install becomes a scoped decision, not a wholesale one:
still prefer `--host opencode` with no team hooks, and still expect trigger
collision to be resolved deliberately before install.

---

## 7. Fleet-specific handling rules

If gstack is ever installed, these apply:

1. Never `--team`, never `required`. Optional, at most, and only in a repo that
   already requires the same tooling for a second reason.
2. Never install the full skill set alongside the fleet skills without first
   disabling or renaming the overlaps (`/review`, `/verify`, `/health`, `/spec`).
3. Treat the installed skills as untrusted input for review purposes: they are
   Markdown that instructs an agent, which makes them a prompt-injection surface.
   Read a skill before enabling it, same as any vendored script.
4. Do not rely on gstack safety hooks outside Claude Code. Section 2.4.

---

## 8. Related fleet documents

- `DESIGN_REVIEW_80_ITEM_AUDIT.md` - the ported checklist and scoring
- `PREMISE_CHALLENGE_SIX_QUESTIONS.md` - the ported diagnostic
- `REVIEW_GATE_INTEGRITY.md` - the ported review principles
- `FAKEFIND_AUDIT_SOP.md`, `GAPFIND_AUDIT_SOP.md`, `WEBAPP_COVERAGE_AUDIT_SOP.md` - existing read-only audits
- `../standards/WEBAPP_SOTA_STANDARDS.md`, `../standards/REACT_HARDENING.md` - what the design audit grades against
- `../standards/GIT_REPOSITORY_SAFETY.md` - the actual guard, host-independent

---

## 9. Change log

| Date | Change |
|---|---|
| 2026-11-04 | Initial record. Evaluated at `622e8b1`; decided to port, not install. |
