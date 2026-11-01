# ADN-2026-06-12-002 — ittybitty Fable 5 status note + global shutdown

**Type:** Status note (agent session handoff) + external event record  
**Author:** Fable 5 (validation session) · ADN merge Sandra + Cursor  
**Status:** Closed — agent unavailable; work preserved in repo  
**Repo:** [ittybittyvideos / videogen-mcp](https://github.com/sandraschi/ittybittyvideos)  
**Prior:** [ADN-2026-06-12-001](ADN-2026-06-12-001-ittybitty-fable5-live-validation.md)

---

## Session status (2026-06-13 ~02:30 Vienna)

Fable 5 completed **live end-to-end validation** of R1/R2/R3 before timing out on changelog/docs.

| Area | Result |
|------|--------|
| **R1 alignment + karaoke** | Validated on real run |
| **R2 beat snap + duck** | Validated with BGM |
| **R3 screening room** | Validated — run `a9e798ffba86`: `gemma4:e4b` flagged hook scene, clip replaced, recomposed |
| **Harness** | `scripts/validate_fable.py` |
| **Code fixes merged** | `dc7eaa9` — align CUDA→CPU, librosa/NumPy tempo, planner JSON tolerance |

### Open follow-ups (not blockers for 0.2.0)

- Swap VLM default to `gemma4:12b` when pull completes (`e4b` works; 26b does **not** fit 4090).
- **Known:** scenes with empty narration (`voice_006` gap) → A/V drift after that scene (subtitle offsets assume contiguous audio).
- **Known:** transient ffmpeg `Conversion failed` under system load — stderr now written to `*.ffmpeg-error.log`.
- Webapp: surface critique report on job detail (R3 UI).
- R3 checklist item “live VLM validation” can be marked done for the short pipeline path.

Fable did **not** finish updating `CHANGELOG.md` before session end — Cursor backfilled from this note.

---

## External event: Fable 5 withdrawn (2026-06-12 ~17:21 ET)

Commerce issued an export-control directive: **no foreign national** may use Fable 5 or Mythos 5, including foreign nationals **inside the United States**. Anthropic cannot nationality-gate at runtime → **disabled both models for everyone**.

Official: [Anthropic statement](https://www.anthropic.com/news/fable-mythos-access)

### Fleet impact

- **Vienna / EU builders:** lost access to the agent that ran this validation pass. The **artifacts remain** (commits, harness, TODO entries).
- **`validate_fable.py`:** keep the filename as historical credit; successor naming e.g. `validate_live.py` is fine when someone cares.
- **Next validation agent:** Cursor/Opus, local tooling, or whatever frontier is reachable without export-control theater.

---

## Opinion (explicitly allowed to rant)

This is **not** a claim that the United States as a country is evil. It **is** a claim that **aspects of the current executive apparatus** are behaving in ways that are evil, incoherent, and — if the jailbreak story were taken seriously — **criminally negligent in the wrong direction**.

The logic does not hold:

1. **If** a competitor demo showed a dangerous jailbreak on a frontier model, the honest safety response is **restrict or recall the capability for everyone** until fixed — not “foreigners may not use it inside America.”
2. **If** the jailbreak is narrow and non-universal (Anthropic’s read; comparable to everyday red-team work on other frontier models), then the directive is **not safety policy** — it is **pressure on Anthropic** (Pentagon blacklist, Commerce letter, models live three days then global kill switch).
3. **“Foreign nationals in the US shall not use Fable”** is **unenforceable** without invasive identity infrastructure. The compliance path Anthropic had to take — **turn it off for all customers** — was predictable. That is not accidental; it is the feature.

Smells like Hegseth-era national-security performance art: spike a lab you already feuded with, launder a competitor’s jailbreak anecdote into export control, and call it patriotism.

**Obvious beneficiary:** anyone not subject to US hegemony over frontier deployment — PRC included. You do not have to admire Beijing to notice that kneecapping your own frontier labs while demanding they still win the race is idiotic statecraft.

Fable was **good while it lasted** — serious live validation, real bugs found, no provider confusion. The work survives. The agent does not. Document that split so the next session does not waste time wondering why the frontier reviewer vanished.

---

## Links

- Session tracker: `videogen-mcp/TODO.md` → “Validation complete 2026-06-13 02:30 (Fable)”
- Changelog: `videogen-mcp/CHANGELOG.md` [Unreleased]
- Anthropic: https://www.anthropic.com/news/fable-mythos-access
