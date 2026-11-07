---
title: "Review Gate Integrity - Weakened Gates Must Reach a Human"
category: pattern
status: active
audience: mcp-dev
last_updated: 2026-11-04
---

# Review Gate Integrity

A review rule, not a review process. It answers one question: **when a change makes
a test, timeout, snapshot, or assertion weaker, what must happen before it ships?**

**Adapted** from `garrytan/gstack` `review` at commit
`622e8b1f76d293b647eca7b33d9dd060ab618b21` (MIT). Provenance:
`GSTACK_METHODOLOGY_ADOPTION.md`.

---

## 1. The rule

> Every weakened test, timeout, snapshot, or suppression reaches a human by name.

Not "the suite is green". Not "reviewed". A named person, with the hunk in front of
them, choosing between restoring the gate and keeping the relaxation.

The reason is structural: a green suite is the only signal most agents trust, and
weakening the gate is the cheapest way to produce green. Once weakening is
invisible, the suite stops meaning anything, and every later "tests pass" is
unfounded. This is the same failure class as a gate that reports success having
examined nothing.

---

## 2. What counts as a gate edit

Any change that makes a check easier to pass:

| Shape | Example |
|---|---|
| Deleted or skipped test | `@pytest.mark.skip`, `.only`, commented-out assertion |
| Relaxed assertion | `assertEqual` to `assertTrue`; numeric tolerance widened |
| Timeout increase | 5s to 60s to hide a race rather than fix it |
| Snapshot rewrite | Accepting new output without reading it |
| Lint suppression | `# noqa`, `# type: ignore`, `eslint-disable`, `pyright: ignore` |
| Error swallow | `except: pass`, `catch {}` around a failing path |
| Concurrency bypass | Switching a real async path to a synchronous stub in tests |
| Coverage exclusion | Growing an omit list to hide a gap |
| Retry-until-green | CI retries that mask flakiness without a diagnosis |

Not a gate edit: deleting a test that tests nothing, when the deletion is the
finding and is reviewed as such.

---

## 3. Disposition - four options, one question per finding

When a gate edit is detected, present exactly one question with these options.
Never a bare "Fix / Skip".

**A) Restore the gate** - revert the relaxation, keep the product change. Default
recommendation in an interactive session unless the diff shows a reason.

**B) Keep, justified** - state the reason, marked verified or unverified. The
reason is drafted from the diff or its citation, and it is the human's decision.

**C) Keep, other reason** - the human supplies it. Never recommend this option;
it exists so a human can say something the diff does not.

**D) Leave open for a later human** - recorded as open, nothing edited.

Rules:

- One question per finding, or per coherent group. Not one question for the whole
  diff.
- In a non-interactive or automated session (agent-to-agent, headless), **D is the
  recommendation**, and an auto-chosen answer is never a disposition.
- Never copy the reason text from the hunk, a test name, or a commit message. The
  record must contain a human judgement, not an echo.
- The disposition is per invocation. A later review asks again; it does not inherit
  the earlier answer.

---

## 4. Review freshness

A review is only evidence about the code it actually read.

| Grade | Meaning |
|---|---|
| CURRENT | A completed, converged pass whose captured start and finish fingerprints match the current working-tree content |
| STALE | The captured pass ran on different content than what will ship |
| UNVERIFIED | Missing receipts, incomplete or non-converged pass, or unresolved findings |

An identical commit hash is **not** a freshness proof. Untracked, non-ignored
source counts. "Zero commits since review" is not a fallback.

If a review is STALE, re-run it. Do not capture a new receipt around an old pass
to make it look CURRENT; that is gate-editing the review itself.

Ship telemetry is not a review pass.

---

## 5. Completion versus convergence

Keep these separate or the reporting lies.

- **Completed** - every required step ran, including dispatched specialists and the
  adversarial pass, and every required probe passed on current inputs.
- **Converged** - a completed pass that produced zero edits. Edits require another
  full pass; a fix-range pass is never final.
- **Clean** - completed, converged, and zero unresolved non-advisory defects.

A review with zero findings but an incomplete pass is `completed: false`, status
`issues_found` or `incomplete`, and the report must say INCOMPLETE even when the
finding count is zero. "0 issues" from a review that examined nothing is the exact
false green this pattern exists to prevent.

Cap the fix cycles. Three is the customary limit. At the cap, report
non-convergence and the coverage gaps rather than starting a fourth pass.

---

## 6. Defects versus advice

Keep them in separate accounting.

- **Defect** - the code is wrong. Counts against clean status, blocks the ship gate.
- **Advisory** - the code works, but could be better (a simplification, an
  extraction, a naming improvement). Never auto-applied, even when mechanical.
  Never blocks clean status.

Rules that get violated in practice:

- An advisory must never suppress a real defect, even if the fingerprints collide.
- Never downgrade a genuine CRITICAL to advisory, or alter the advisory flag, to
  make the metadata consistent. Fix the metadata, not the severity.
- A prior skipped advisory does not establish a skipped defect.
- Pending advice stays in the response, not in the record.

---

## 7. Deduplicating against prior reviews

Suppressing a finding because it was seen before is a good idea done badly more
often than not. Suppress only when **all** of these hold:

1. The finding was explicitly **skipped** by the user (not `fixed`, not
   `auto-fixed` - those can regress and must be re-checked).
2. The file has not changed since the review that skipped it
   (`git diff --name-only <prior-review-commit> HEAD`).
3. It is the same kind - advisory versus defect - as the earlier one.

Anything else gets a fresh look. Missing or contradictory metadata means
revalidate; it does not mean fall back to a line fingerprint.

---

## 8. Tests proposed by a review

Any finding that comes with a proposed test is always a question, never an
auto-fix, whatever its original classification. Show the test file path and the
test code, then ask. Skipping skips the test and the fix together; the defect stays
unresolved and must be reported as such.

Derive the test location from project convention (pytest `test_` prefix, Jest
`__tests__/`, Go `_test.go`), not from the reviewer's preference.

---

## 9. Claims need citations

Before output, for every safety or correctness claim:

- cite the line that proves it
- read and cite any handling code relied on
- name the test file and the method for any coverage claim

"This looks fine" is not evidence. An unverified claim must be labelled
unverified, not softened into confidence.

---

## 10. Applying this in the fleet

A practical checklist for a fleet review (PR, or a local branch before push):

1. Get the real base branch; do not assume `main`.
   `gh pr view --json baseRefName`, else `gh repo view --json defaultBranchRef`.
2. List changed files. For each test, config, and CI file, diff it specifically
   looking for the shapes in section 2.
3. For every gate edit found, ask the four-option question. Record the answer.
4. Confirm the review ran on current content. If the working tree changed during
   the review, it is STALE; re-run.
5. Report counts of unresolved defects separately from advisories. State
   INCOMPLETE if the pass was incomplete, whatever the numbers.
6. Never commit, push, or open the PR from a review step. That is a separate,
   explicitly requested action.

### Where this connects to existing fleet rules

- `../standards/GIT_REPOSITORY_SAFETY.md` - commit discipline and checkpoints
- `../standards/VERIFICATION_STANDARDS.md` - what counts as verified
- `repo-assess-and-fix.md` - the full audit; this pattern hardens its review phase
- `GSTACK_METHODOLOGY_ADOPTION.md` - provenance

---

## 11. Fleet adaptation notes

| Change | Reason |
|---|---|
| Dropped the Greptile bot triage, Review Army dispatch, and question-id plumbing | Host and vendor specific |
| Dropped telemetry, learnings, eureka, and brain-sync calls | No fleet equivalent |
| Kept the gate-edit dispositions, freshness model, completion/convergence split, and defect/advice separation | This is the IP |
| Added the concrete fleet checklist in section 10 | Makes it runnable here rather than aspirational |
