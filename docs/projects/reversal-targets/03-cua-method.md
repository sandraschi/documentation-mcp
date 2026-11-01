# 03 - CUA Method: The Autoclicker Training Loop

The core claim: any Windows app on Goliath is trainable because Win32 and UIA
expose everything, and pywinauto-mcp turns exposure into specs at machine
speed. No Ghidra, no decompiler, no EULA friction. Watch, record, specify,
rebuild, pixel-diff.

## The loop (five stations, all exist today)

1. **Probe.** `pywinauto window list + inspect` dumps the target's control
   tree as JSON plus screenshots plus OCR text. One evening maps an entire
   application shell. Baseline committed as evidence.
2. **Crawl.** `automation_mission` walks every menu, tab, and slider,
   screenshotting before and after, saving every file the app produces
   (presets, configs, exports). Macro recorder stores the replay. Precedent:
   the 100-installer unattended sweep at ~$2 LLM cost.
3. **Spec.** Mission output plus official docs plus tutorial transcripts become
   SPEC.md per dialog: inputs, outputs, shortcuts, file effects, with source
   log (doc URLs, screenshot hashes, zero code origins). Specs are the legal
   armor from file 02 and the contributor bait from the funnel analysis.
4. **Rebuild.** Fresh implementation from spec only, fleet styling, divergent
   chrome. Thin Rust where hot, Python MCP as agent contract, webapp per
   SOTA standard.
5. **Diff-pair verify.** The same mission drives original and rebuild;
   screenshots compared by template match, files compared by round-trip diff,
   results logged to SQLite. Missions become permanent regression tests per
   `standards/rules/cua_nsis_smoke_testing.md` and
   `standards/rules/cua_webapp_testing.md`.

## The opencode exemplar

Opencode reversed Cursor the same way: behavior-level clone of an
AI coding IDE, built by watching what the app does rather than reading how
it does it, now with hundreds of collaborators. Three lessons transfer
directly. First, the wedge was not the whole IDE on day one, it was
compatibility plus freedom (own models, own keys, own config). Second,
every Cursor behavior is UI-observable, so reversal speed equals crawling
speed, and crawling speed is now an agent problem with a $2 price tag.
Third, the cause (free the agent from the subscription) recruited the swarm
that finished the long tail. Any Tier 0 or Tier 1 target in file 01 can run
the identical playbook with a smaller crowd and a narrower wedge.

## Why training on Goliath works

Goliath is both the gym and the opponent's home field: 5900X with headroom,
4090 for local vision models judging screenshots, 280 GB free on D, two
snapshotted glass boxes (win11-automated :3390, ubu-2404-lts :3391) for
containment, and the apps themselves installed where the missions can see
them. The drill for any candidate: install in the glass box, snapshot clean,
crawl, spec, rebuild outside, diff-pair inside. Nothing touches bare metal
until the method is proven behind glass. Digitale Bibliothek 5 is the
designated first drill precisely because it is small, German (matches the
calibre corpus need), probably orphaned, and utterly unthreatening: if the
loop cannot digest a CD-ROM library, it cannot digest VirtualDJ.

## Cost and speed envelope (measured, not projected)

- 100 unattended installer runs: ~$2 (pywinauto exhibit A).
- Full OS installs tonight (Win11 26H2, Ubuntu 24.04 + desktop): zero
  clicks, screenshot-verified, snapshotted.
- Spec emission per dialog: one mission plus one synthesis pass; Opus-class
  models write the SPEC from mission artifacts without human drafting.
- The bottleneck is not crawling or coding. It is merge bandwidth and test
  maintenance, exactly as the funnel analysis predicts. Plan staffing (even
  volunteer staffing) around review, not production.

## What to build next in the fleet

- `spec_emit` op in pywinauto-mcp: UIA dump plus screenshots plus macro to
  SPEC.md skeleton, automatically. STILL OPEN.
- `diff_pair` op: same mission on App A versus App B, screenshot plus file
  diff bundle out. STILL OPEN.
- Nightly `suite` op with honest coverage semantics (looked-and-clean versus
  never-looked). STILL OPEN.
- Per-target spec directories under this section, one per engagement, each
  with source logs suitable for counsel on day one.

## Status 2026-10-10: hardened, parked

Resource hardening LANDED in pywinauto-mcp (commit feat(safety), BUG-071):
watcher caps (8 / 0.5 s / 3600 s), max 2 concurrent missions, rotating server
log, host snapshot plus watcher census in safety status, 6 new tests green,
SAFETY.md section 7. Meanwhile the opencode `cua` entry is DISABLED again
after a same-day hard hang on Goliath (causation unproven, no logs). Re-entry
checklist, in order: HTTP mode isolated with resource monitoring, review
startup for hook/camera/OCR preload, stdio-spawn only on a quiet box, generous
timeout. Do not skip the order.
