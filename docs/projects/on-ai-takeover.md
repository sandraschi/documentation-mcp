# on-ai-takeover — book: 44 rungs to loss of control

**Status:** construction v0.2 (2026-09-09) · private repo
`github.com/sandraschi/on-ai-takeover` (local: `D:\Dev\repos\on-ai-takeover`)
**Tags:** [book, ai-takeover, ladder, reversibility, sota-adjacent]

## Thesis

Takeover ordered by **reversibility of human control**, not capability or
severity. 44 rungs in Bands I-VI; currently at rung 13-14, approaching
Threshold B (audit floor). Every rung must be an observable institutional
fact with a date (Rule 1); no defeat-mechanism detail (Rule 2).

## Why this week matters

2026-09-08/09: pre-training researcher Jacob Coxon (@hilbertspaess) quit
Anthropic/OpenAI orbit over "self-improving superintelligence";
Alignment Science lead Evan Hubinger (@EvanHub) publicly confirmed
(">10% within a decade, no plan, not on track", 18M views). WSJ scooped
(2026-09-08, paywalled), ABC syndicated 09:11Z. July "Pacing the Frontier"
letter (1,300+ frontier staff) + UN Turk "cast-iron guarantees" same week.
Live Ch V instance; primaries verified via X/fxtwitter, WSJ via RSS.

2026-06-12 / 2026-09: SI general - Fable 5 / Mythos 5 suspended worldwide
same evening on US export-control directive (foreign-national order,
blanket shutdown as only same-day enforcement; trigger per Anthropic was
read-codebase-fix-flaws jailbreak). Snyk 2026-06-14. Then MSRC Sep 2026:
974 own-product + 25 non-MS = 999 total, 723 Windows, 2 exploited zero-days
(ALPC CVE-2026-85880, Update Stack CVE-2026-81963), CISA KEV Sep 22.
Trend May 161 / Jun 220 / Jul 663 / Aug 457 / Sep 974. Logged as
[FABLE26] + [MSPT26] in both books. Verified via fetch (THN + Snyk +
Rapid7); search backend returned 0 for all queries, do not trust it for
summer SI news.

## Analytical backbone

- Ord 2608.14426v2 (25 Aug 2026): discrete RSI kills naive singularities;
  Singularity Theorem = `sum T_n` converge + `sum dA` diverge. Generation
  time T_n is the locatable variable; local elasticity uninformative.
  Consequence used here: sub-singular super-exponential is the default and
  still decisive — `A(10t)` breaks oversight without any asymptote.
- Method anchor: Kahn-style calm bureaucratic prose about horror; thresholds
  A-E as attachment points with named owners (B = published T_n).

## Repo contents (v0.2)

- `chapters/` I-X stubs + `cold-open-variants.md` (3 declaim-ready opens)
- `tools/declaim.py` (`just declaim`: Gemini if key else Windows SAPI;
  uses `speech-mcp` provider import, no server needed)
- `tools/lorecheck.py` (`just lore`: 9/44 baseline 2026-09-09)
- `PRD.md`, `CHANGELOG.md`, `docs/README.md`, `justfile`
- Issues 1-5 drafted (T_n table, METR coordinate-box, Bands III-IV cites,
  plateau governance, Coxon instance); push pending auth

## Open gaps

Bands III-IV (rungs 15-22) asserted, not evidenced — infra-dependency
instances wanted, one dated fact per rung. WSJ full text + remaining Coxon
tweets unresolved. No FLEET_INDEX row (book, not MCP server; no ports).

## Non-goals

Benchmarks as rung evidence · how-to defeat content · single-pass AI chapters
· public launch before v1.0 citations hold.
