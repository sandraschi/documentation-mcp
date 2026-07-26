# Fable 5 — Worthy Work Ranking (2026-07)

**Question:** Which outstanding fleet work is complicated enough to justify frontier-model time?
**Method:** Ranked on five axes — conceptual difficulty, *Fable-specificity* (does frontier reasoning change the outcome, or would DeepSeek grinding get there?), value to Sandra, verification bottleneck (can correctness be checked inside a session?), and readiness (blockers).
**Written:** 2026-07-09, Claude Fable 5.

---

## The ranking

| # | Project | Conceptual difficulty | Fable-specificity | Value | Verification | Ready? | Est. Fable time |
|---|---------|----------------------|-------------------|-------|--------------|--------|-----------------|
| 1 | **leanforge-mcp** Phase B→C | ★★★★★ | ★★★★★ | ★★★☆ (research) | Needs Lean workspace for full loop; pure-Python parts testable now | ⚠ 4GB Mathlib setup pending | 1–2 days (B+C design) |
| 2 | **advanced-memory v2.0 Phase 1** | ★★★☆ | ★★★★ (1M-ctx surgery) | ★★★★★ (daily driver) | pytest + live server | ✅ | 1–2 days |
| 3 | **AutoLISP interpreter** (qcad-mcp) | ★★★★★ | ★★★★★ | ★★☆ (jewel project) | Excellent — golden .lsp corpus | ✅ | 2–4 days |
| 4 | **freecad-mcp CFD: snappyHexMesh + validation** | ★★★★ | ★★★ | ★★★ | Terrible — hours of solver time per cycle | ✅ (Docker) | grind, share w/ DeepSeek |
| 5 | **sqlite-utils 4.0 fleet adoption + Datasette layer** | ★★ | ★★ | ★★★★ (diffuse) | Excellent | ✅ (released 2026-07-07) | Fable: 2h standard; rest delegated |

Dark horses (not scored, worth remembering): **lewm-mcp** (JEPA world-model bridge — conceptually deep, blocked on upstream maturity), **chip-design-mcp** (RTL→GDSII — deep but toolchain-verification-bound like CFD), **dark-app-factory** council architecture.

---

## 1. leanforge-mcp — the genuine article

The only fleet project where the *problem itself* is frontier-hard, not just the plumbing. Phase B/C items that are exactly Fable-shaped:

- **P1-1 tamper guard**: verifying the LLM proved *the stated theorem* rather than a weakened variant, while permitting legitimate helper lemmas. This is adversarial-verification reasoning about Lean elaboration — you must decide equivalence of theorem statements under the model's rewrites. Subtle, and getting it wrong silently invalidates every "solved" result.
- **P1-2 bracket-aware statement extraction** — parsing Lean 4 syntax robustly without a full parser.
- **P2-1 LeanReplClient**: persistent REPL worker pool against leanprover-community/repl (pickled environments, ~10× compile throughput). Protocol design + concurrency.
- **Prompt/escalation design**: what error-provenance context makes deepseek-prover-v2:7b productive; when to escalate tiers; repeated-edit detection. Designing the loop that *uses* Fable as tier 3 is itself Fable-tier work.
- **P2-3 cost accounting** — mandatory before any overnight batch (hard gate, already flagged in repo).

**Blocker to clear in parallel, tonight-cheap:** the one-time Mathlib workspace (`lake new … math; lake exe cache get`, ~4GB, 20–40 min). Nothing compiles until it's done; kick it off before the next session so Phase B verification isn't theoretical.

**Why #1:** maximal Fable-specificity on every axis; DeepSeek can't design the tamper guard. Value is research-instrument rather than daily-driver — but "worthy" was the question.

## 2. advanced-memory v2.0 Phase 1 — value champion

Not the deepest problem, but the highest value×readiness in the fleet: the primary knowledge store, with **71 fully-written namespace tools that have never been mounted** (zero `.mount()` calls — enormous latent capability), `content_manager.py` at 2,405 lines mid-decomposition (`capture.py`/`crud.py` extracted; `tagging.py`, `ai_enrich.py`, QC pending), and documented spec drift from the 2026-07-04 HEAD audit. Mistakes here corrupt the daily driver; 31-file careful surgery is what 1M context is for.

**Synergy:** sqlite-utils 4.0's new **migrations system** (see #5) is exactly the mechanism a v2.0 schema evolution needs — adopt it here first, as part of Phase 1, rather than as a separate fleet chore.

## 3. AutoLISP for qcad-mcp — the jewel

Scoping decision up front, and it matters: **build an interpreter, not a transpiler.** AutoLISP is dynamically scoped, has `(eval)`, and idiomatic code leans on both — static transpilation to lexically-scoped Python is a tarpit. A tree-walking interpreter in Python with:

- s-expression reader handling AutoLISP quirks (dotted pairs, `'`/quote, strings, reals-vs-ints)
- dynamic-scope environment chain
- the entity bridge: `entget`/`entmod`/`entmake` association lists ⇄ ezdxf entities (the real design work — DXF group codes as the shared vocabulary helps)
- `(command …)` emulation for a curated command subset (LINE, CIRCLE, PLINE, TEXT, LAYER…)
- `ssget` selection sets over ezdxf queries

gets most real-world `.lsp` files running against the depot. Superbly verifiable: corpus of real routines + golden DXF output diffs. Conceptually top-tier (language implementation with hostile semantics), Fable-specificity maximal. Honest value check: unless there's a real stash of AutoLISP routines to run, this is a jewel project — deeply satisfying, portfolio-grade, modest daily utility.

## 4. freecad-mcp CFD — hard, but the wrong shape for Fable sessions

17 CFD tools already exist; the remaining genuinely-hard gap is **snappyHexMesh** — currently blockMesh only, i.e. box domains, which is the difference between toy and real CFD (arbitrary STEP geometry, boundary layers, refinement regions). Plus validation cases (lid-driven cavity, cylinder drag vs literature Re sweeps), adjoint optimization, and closing the PINN loop (`cfd_sample_for_pinns` exists; no trainer).

The problem: every verification cycle costs *hours of solver runtime*. Fable reasoning helps with snappyHexMeshDict generation and result-sanity judgment, but the loop is dominated by waiting — DeepSeek-grinding territory with occasional Fable escalation on physics judgment. Rank it for background progress, not Fable sprints.

## 5. sqlite-utils 4.0 (released **2026-07-07**) + Datasette — high value, low Fable-specificity

What 4.0 brings the fleet: a **built-in migrations system** (structured schema evolution — the missing piece for advanced-memory, calibre, chitchat, leanforge, opencode jobs.db), `db.atomic()` nested transactions, compound foreign keys, `INSERT … ON CONFLICT` upserts, and a pile of transaction-model fixes (the "phantom open transaction silently rolled back on close" class — literally the bug family we hunt fleet-wide). Breaking changes are real but mechanical: `db.query()`/`db.execute()` split, `ForeignKey` namedtuple→dataclass, FLOAT→REAL, CSV type detection default, quote-style change.

**Right move:** Fable writes `mcd/standards/SQLITE_UTILS_4_STANDARD.md` (2h: adoption rules, breaking-change checklist, migrations pattern, which repos in what order) and does the *first* adoption inside advanced-memory v2.0. Repo-by-repo migration afterwards is DeepSeek/Sonnet work. Separately, **Datasette as a read-only fleet DB browser** (one instance, a port, mounting jobs.db + memory.db + calibre metadata + chitchat) is a half-day, high-delight addition — arguably its own small `datasette-mcp`.

---

## Recommended sequence

1. **Tonight/next session prep:** ~~kick off the leanforge Mathlib workspace download~~ **DONE 2026-07-09.** Workspace live at `D:\Dev\repos\leanforge-mcp\workspace\leanforge_workspace` (note: an earlier attempt landed at a typo'd `leanforge_worskpace` and only partially cached — deleted and redone correctly). Mathlib's post-clone hook auto-ran `cache get`: 8542 files attempted, 100%, fully decompressed. Verified on disk: 1200+ real `.olean` files under `mathlib\.lake\build\lib` (not just the cache-tool's own bootstrap set, which was the earlier failure signature). **leanforge Phase B/C is now unblocked.**

2. **Fable session, same day (2026-07-09):** leanforge **Phase B is now fully complete** — every P1/P2-4 correctness item in the assessment closed in one sitting. P1-1/P1-2: new `core/lean_lexer.py` (bracket/comment/string-aware scanner) closes the default-arg truncation hole and enables a name-keyed tamper guard rejecting statement changes, renames, deletions, and a decoy-duplicate attack a naive fix would miss. P1-4/P1-6: `job_manager.py` gained `owner_pid`/`owner_started_at` (PID-reuse-safe) and a `cancel_requested` poll flag, closing the cross-process false-interrupt and no-op-cancel bugs between the stdio server and webapp. P2-4: exact repeated-edit detection (skips a wasted ~30-60s recompile when the model resends something already known to fail) plus a rolling summary of failed (tactic, error-class) pairs injected into the prompt, so the model isn't purely stateless turn to turn. 42 new tests across four files, **all verified via actual pytest runs** in scratch container mirrors (no Lean/Mathlib dependency for any of it) rather than trusting inspection — caught and fixed three bugs in my own test assertions along the way, zero bugs found in the shipped code on final runs. `docs/ASSESSMENT_2026-06-24.md` fully updated. All of Phase C remains open: P2-1 (REPL client — the actual performance bottleneck, ~30-60s per `import Mathlib`), P2-2 (LLM client timeout/retry hardening), P2-3 (cost accounting — Sandra's own hard gate before any batch run). Recommended next Fable session.
2. **Fable day 1–2:** advanced-memory Phase 1 completion, adopting sqlite-utils 4.0 migrations in the process (#2 + the Fable-worthy sliver of #5).
3. **Fable day 3–4:** leanforge Phase B correctness + Phase C design (tamper guard, REPL client, cost caps) → MiniF2F sanity pass as the exit gate.
4. **Fable days 5+ (as the mood takes):** AutoLISP interpreter, milestone-sliced (reader → eval core → entity bridge → command layer).
5. **Continuous, delegated:** CFD snappyHexMesh grind and sqlite-utils repo migrations on DeepSeek, Fable only for physics judgment and the migration standard.
