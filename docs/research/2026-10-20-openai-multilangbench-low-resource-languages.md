# OpenAI MultiLangBench + COBOL migration eval: what is actually worth stealing

**Date:** 2026-10-20 (Europe/Vienna)
**Source:** https://openai.com/index/low-resource-programming-languages/ (published 2026-10-19)
**Harness:** https://github.com/openai/MultiLangBench (released with per-language results)
**Status:** assessment only. Nothing adopted, nothing run. Filed because one design idea
in it is better than what the fleet currently uses for gating. Deferred actions in section 7.

---

## 1. What was published

Two evaluations, framed around "low-resource programming languages" (COBOL, Fortran,
Visual Basic, OCaml - languages with less training code than Python/JS).

**MultiLangBench.** The model must build a SQLite-compatible database engine from scratch
in a named language: organise a codebase, manage state, handle errors, add features without
breaking existing ones. Scored by running the candidate program against SQLite's own
(adapted) test suite. 20 languages: C, C#, C++, COBOL, Common Lisp, Fortran, Go, Java,
JavaScript, Lean, OCaml, PHP, PowerShell, Python, Ruby, Rust, Scala, Swift, Visual Basic, Zig.

| Metric | Value |
|---|---|
| GPT-6 Astra avg pass rate | 87.4% (from 26.8% for GPT-5.6 Sol) |
| Astra coverage | >83% in 19 of 20 languages |
| Astra worst language | COBOL, 72.1% (from 10.9%) |
| Astra other jumps | OCaml 25.6 -> 85.8, Fortran 21.4 -> 83.5, VB 27.5 -> 89.4 |
| GPT-6 Luna avg | 40.3% at ~$0.77/sample vs $3.48 (-78%) |

**COBOL migration eval.** Migrate COBOL programs to C++, Java, Kotlin, Python or Rust with
behaviour preserved. Hidden tests require **byte-for-byte parity on observable outputs**;
a migration counts only if every test passes. GPT-6.1 Sol: 86.6% at low reasoning effort
(from 5.4% for GPT-5.6 Sol, at 61% of the cost), 97.9% at high effort.

The worked failure mode they call out is worth remembering in its own right: COBOL
fixed-point arithmetic **truncates** excess decimal digits unless rounding is explicitly
requested. A rewrite that rounds instead runs clean, raises no error, and produces
different financial numbers. That is the archetype of a migration bug that tests-without-
parity will not catch.

---

## 2. The idea worth stealing: the artifact is the interface

MultiLangBench does not inspect the candidate's source. It does not lint it, count
functions, or check for idiomatic style. It hands the program a database file and a query,
then compares the **resulting database** against real SQLite.

That makes the same tests valid across 20 languages, and it makes the score a statement
about behaviour rather than about shape. The interface is a file; the grader is a diff.

Contrast with what the fleet gates on. `standards/FLEET_GRADING_STANDARDS.md` section 2's
Industrial Health Metric awards 100% for five artifacts *existing*: `glama.json` with the
right keys, a `just test` recipe that runs pytest, `llms.txt` + `llms-full.txt`,
`start.ps1` + `start.bat`, `pyproject.toml` using `uv`. A repo where every tool raises
`NotImplementedError` and every test is skipped scores 100. That is the fleet's own
documented failure mode - "a gate that reports success having examined nothing" - sitting
in a standard.

The fix does not have to be MultiLangBench-scale. Any gate whose assertion is
"given input X, the observable output is Y" beats a gate whose assertion is "file F
exists". The MCP surface makes this cheap: connect over stdio, call the portmanteau op
with a dry-run or read-only argument, assert the response envelope has the declared keys
and the declared values. That is the same trick - fixed interface, diffed behaviour.

Not proposing a change today. Noting that the fleet already has the machinery
(`fleet-gate/`, `expectations.json`, `baseline.py`) to do artifact-diff grading, and that
MultiLangBench is a clean worked example of the pattern at the far end of the difficulty
curve.

---

## 3. The parity lesson (applies well beyond COBOL)

"All tests pass or the migration failed" is the correct pass criterion for any rewrite,
and it is not how migrations in this fleet are usually judged. The Starlette-to-FastAPI
and Python-2-residue migrations elsewhere in the repo set were validated by "does it still
run and do the obvious endpoints answer" - which is exactly the standard that lets a
rounding/ordering/serialisation difference through.

Generalised rule, cheap to state and cheap to enforce where a golden artifact exists:
capture the old system's output for a fixture set **before** touching it, then diff
byte-for-byte (or field-for-field, with normalisation stated explicitly) after. If no
golden artifact can be produced, that is itself the finding - the behaviour is unmeasured.

---

## 4. Cost-per-sample alongside pass rate

The post reports $0.77 vs $3.48 per sample next to the accuracy numbers, and Luna exists
purely as the cheap lane (40.3% at 78% lower cost). That is the honest comparison format
and it matches `standards/TOOLING_COST_MODEL.md` and `LOCAL_LLM_FIRST_DOCTRINE.md`: quality
alone is not a selection criterion, quality-per-dollar is. When the next local-model
argument happens in this repo, the shape of the table should be theirs, not
pass-rate-alone.

---

## 5. Why it mostly does not apply here

- **No COBOL, no Fortran, no Visual Basic in the fleet.** 190+ repos are Python/Rust/
  TypeScript. Nothing to maintain or migrate in those languages.
- **The task shape is wrong for the fleet's work.** MultiLangBench measures long-horizon
  persistence on a system far bigger than one MCP server. Fleet work is mostly small,
  convention-bound servers where the hard part is port registry, tool design and packaging,
  not raw code volume. A model that can build SQLite is not thereby better at following
  `TOOL_DESIGN_STANDARDS.md`.
- **It is a vendor benchmark.** Self-reported, unreproduced, and scored by the company
  selling the model. GPT-6 Astra's 87.4% is a marketing number until someone runs the
  published harness.

---

## 6. The one directly comparable datapoint

**PowerShell and Rust are both in the 20 languages.** Those are two of the languages this
fleet actually ships in. That makes MultiLangBench the only published eval seen so far
where a local model can be placed on the same axis as a frontier model in a language that
matters here - a per-language number, not a blog-post average.

Given `research/2026-10-14-local-llm-dev-failure.md` (all four local lanes failed for real
dev work, cloud remains the daily driver), the useful question is not "is Strata good" but
"at what task shape does Strata stop being good". A published, language-specific,
reproducible harness is a better probe than another afternoon of vibes.

---

## 7. Deferred actions (do not start now)

1. Clone `openai/MultiLangBench`; read the PowerShell and Rust fixtures first - they are
   the ones with fleet relevance. Check what a single-language run costs in time and tokens
   before committing to anything.
2. If it runs cheaply: one PowerShell run and one Rust run against the Strata lane, recorded
   in `research/`, so the local lane has a number instead of an opinion.
3. Separately and independently of OpenAI: consider whether the Industrial Health Metric
   (section 2 above) should gain one behavioural component. This is a change to a MANDATORY
   standard - needs its own decision, not a drive-by edit.
4. Do not adopt MultiLangBench as a fleet gate. It grades general coding capability, not
   fleet compliance. The idea is the transferable part; the benchmark is not.

---

## 8. What would change the assessment

- If the harness turns out to be a thin wrapper that needs `$OPENAI_API_KEY` and an
  internal scoring service, it is not reproducible in-fleet and drops to "read the results
  table, ignore the rest".
- If a local 100B-class model lands in the 80%+ range on Rust or PowerShell while remaining
  cheap, that is a genuine argument for revisiting the local-first doctrine - and would
  deserve its own writeup rather than an edit to this one.
- If someone shows the COBOL parity tests are easier than they sound (e.g. outputs are
  heavily normalised before comparison), the migration half of the post is mostly
  presentation.

---

## Cross-references

- `standards/FLEET_GRADING_STANDARDS.md` - section 2 Health Metric, section 5 grader blind spots
- `standards/TOOLING_COST_MODEL.md`, `standards/LOCAL_LLM_FIRST_DOCTRINE.md` - cost-per-quality framing
- `research/2026-10-14-local-llm-dev-failure.md` - why the local lane is not trusted today
- `standards/VERIFICATION_STANDARDS.md` - "prove changes by running them"
