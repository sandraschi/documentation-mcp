# VBA compatibility harness - design sketch

**Status**: design sketch, 2026-10-25. Not started.
**Question it answers**: is VBA support actually arriving, or is it forum threads
forever? A runtime without an oracle is a wish; with one, it is a queued project.
**Success criteria (2026-12-25)**: GridCraft #2139 closed (UDF formulas show cached
values, not `#NAME?`); macro parts byte-identical on round-trip (WordCraft #3629
class of fix); a differential gate runs somewhere in this pipeline (fleet or
upstream) and reports a compat score per build.

## Why this harness, why now

A VBA runtime is an oracle problem, not a code-volume problem: nobody has a spec,
the spec is thirty years of Office behavior, and correctness means bug-compatibility
with it. The team that ships the runtime will be the team that can check
compatibility fast. Storytold already builds oracles-as-commands - `gridcraft check`
is a cached-value calc oracle plus XLSX round-trip fidelity that exits 1 on any
difference. This harness is the VBA edition of that pattern, and it is the missing
piece the open issues (#1143, #2139, #356, wordcraft #80) are all actually waiting for.

## Levels (each is a gate, in order)

- **L0 file fidelity**: open a `.xlsm`/`.docm`, save it, macro parts byte-identical.
  No execution. This alone kills the "Word ate my macros" class of reports.
- **L1 cached values**: formulas calling VBA UDFs display their last computed value,
  the way Excel behaves with macros disabled. This is #2139, the highest-value fix
  on the board, and it needs no runtime at all.
- **L2 record/replay parity**: `tools.macros` (WordCraft) and `automate.*`
  (GridCraft) round-trip: record in Office, replay the command list in the Craft app
  and diff the resulting document; record in the Craft app, replay in Office.
- **L3 execution differential**: run the macro in Office, run it in the candidate,
  diff the effects (cell values, formatting, resulting file bytes normalized).

L0 and L1 are worth building even if L3 never happens: they convert the two most
common VBA complaints into passing tests.

## Corpus (in priority order)

1. **The #2139 class first**: UDF-heavy workbooks where formulas show `#NAME?`
   today. Small, real, and each one is a regression test the day it passes.
2. **LibreOffice's QA tree**: mine it for VBA-bearing test documents. Even where
   LibreOffice fails a test, the test itself is a checked-in oracle with a known
   answer - that is free specification.
3. **Public macro corpora**: GitHub `.xlsm`/`.docm` files with macros, capped at a
   few hundred, only files whose licence permits testing. Record provenance
   (repo, commit, licence) per file; the corpus index is committed, the blobs are
   content-hashed so a takedown removes exactly one file.
4. **Synthetic API coverage**: generated macros that walk the object-model surface
   (every `Range`/`Worksheet`/`Document` member at least once), to find the gaps
   real files do not happen to touch.
5. **Fleet files**: any macro-bearing Office file already in the fleet's orbit.

## Oracle setup

- One Windows VM with a licensed Office, updates frozen, fixed locale. Driven over
  COM. Snapshot reset between runs so one macro cannot poison the next.
- Second oracle: LibreOffice. Where it agrees with Office, the test is portable;
  where it disagrees, the test is marked Office-only. Disagreement itself is data.
- Determinism rules, enforced before any diff: normalize timestamps, author names,
  printer settings, and calc-chain order. A diff on metadata is a harness bug,
  not a product bug - fix the normalizer, not the app.

## Diff loop

For each macro: run the oracle, capture (a) normalized result-file bytes, (b) a
cell-value dump, (c) error class or clean run. Run the candidate, capture the same.
Classify: pass / value-diff / error-diff / crash. New diffs become issues with the
minimal repro attached - agents are good at this triage, and each one is either a
real compat bug or a normalizer fix.

The output that matters is a single number per build: **compat % over the corpus**,
tracked over time. That number is what turns "VBA someday" into a release gate, and
it is also what makes a future runtime reviewable: every behavioral claim arrives
with the corpus slice that proves it.

## Where it lives

One repo, `D:\Dev\repos\vba-harness\` (infrastructure, not a wrappee):

- `corpus/` - the index (provenance + hashes) and the blobs.
- `oracle/` - the COM driver, the LibreOffice driver, the normalizers.
- `diff/` - the runner, the classifier, the score dashboard.
- An MCP face (`compat_check` for a build, `compat_score` for the trend), because
  in this fleet anything an agent cannot invoke does not get invoked.
- A democraft flow (`vba-roundtrip`) that consumes the gate, so the check runs
  where the demos run.

Propose the gate upstream in their idiom: a `check`-style command, the way
`gridcraft check` already works. If they adopt it, the fleet harness becomes the
acceptance suite; if they do not, it remains ours.

## Phases (8 weeks to 2026-12-25)

- **Weeks 1-2**: L0 + L1, corpus from items 1-2 above. This alone settles half the
  open VBA complaints and needs no runtime, no VM beyond a file share.
- **Weeks 3-4**: oracle VM + normalizers + dashboard; L2 record/replay both
  directions. First corpus score published, however low.
- **Weeks 5-6**: L3 loop on a 100-macro pilot corpus. Expect the triage firehose;
  that is the point - each diff is a filed, minimal, actionable bug.
- **Weeks 7-8**: corpus to 1000+, gate in CI (fleet first, proposed upstream
  second), first fixes landing with gate numbers attached.

Explicitly **not** in 8 weeks: full object-model coverage, COM interop edge cases,
a macro security model, signed-macro trust. Those are 2027. What the 8 weeks buy
is L0/L1 green, L2 measured, L3 started - i.e., VBA stops breaking files, which is
what every open issue is actually asking for.

## Cost

- One Office licence and one VM (or an existing licensed host with snapshots).
- Agent time, concentrated in corpus mining and normalizers; the runner itself is
  small. The expensive part is triaging the first hundred diffs - budget for it,
  because an untriaged corpus is a number nobody trusts.
- The alternative cost is the status quo: every VBA report re-litigated by hand,
  forever.
