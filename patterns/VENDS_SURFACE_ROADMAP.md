# VENDS surface roadmap — what else could be vendored

Companion to `VENDS_SOP.md`. Records the current surface list, the
promotion history, and the ranked candidates for future surfaces.
Decisions, not just inventory: each candidate names its extraction
precondition (no surface gets invented without a proven reference).

## Current surfaces (2026-09-29)

| Surface | Automation | Ships via |
|---|---|---|
| `apps` | Fully scripted | `vendor-apps-page.ps1` (default `-Pages apps`) |
| `chat` | Scripted page, hand content | `vendor-apps-page.ps1 -Pages chat` (promoted 2026-09-29; was `-Pages`-only before) |
| `llm` | Merge only | SOP Phase 2 + 2b (fold-in) — judgment required |
| `speech` | Fully scripted | `patterns/templates/speech-crossconnect/` |

Default run stays `apps,llm`. Everything else is opt-in per run.

## Promotion history

- 2026-09-06: SOP built vendoring arxiv-mcp (Apps hub + LLM).
- 2026-09-15: `speech` surface extracted from japanophile-mcp.
- 2026-09-29: `chat` promoted to first-class surface (was already
  scripted as `-Pages chat`; promotion = surfaces list + dispatch +
  NEXT STEPS, not new machinery). Same day: Phase 2b fold-in added
  after inkscape-mcp fossilized on a separate AI Settings page.

## Candidates (ranked by readiness)

### 1. `tools-page/` — most vendorable thing left
Every catch-them-all webapp needs a Tools catalog and it discovers
from the MCP server, so the page is ~90% standard. Same shape as
`apps`: scripted page + thin backend probe. Template exists at
`templates/tools-page/`. Precondition: confirm the probe endpoint
contract across 2–3 repos (pilot: any repo with a Tools page that
already discovers dynamically).

### 2. `dashboard-kpis/` — hero + KPI layout
Layout is standard; only the numbers are per-repo. Template exists
at `templates/dashboard-kpis/`. Lower value than tools-page (every
dashboard already has something shaped like this; vendoring saves
less). Pilot on next new-repo scaffold instead of retrofit.

### 3. Skills page — standard demands it, no template yet
`WEBAPP_SOTA_STANDARDS.md` catch-them-all requires Skills, but there
is no `templates/skills*/` to extract from. Precondition: pick the
best existing Skills page in the fleet, extract it like speech was
extracted from japanophile. Do not write one from scratch — surfaces
come from proven references, never greenfield.

### 4. RAG / semantic-search page — backend work too, correctly judged
Needs an index pipeline, embeddings, LanceDB, ingest sweeps — a
`llm`-style surface (engine + endpoints + page), not an `apps`-style
page drop. No template exists. Precondition: a proven reference
implementation to extract from (arxiv-mcp or docs-mcp are the
obvious pilots). Scope when asked; do not vend before the reference
exists.

## Already covered elsewhere (not surfaces)

- `logs` page: `-Pages logs` via the same vendor script.
- Error telemetry: copy/vendor `templates/fleet_error_telemetry.py`
  per `patterns/FLEET_ERROR_TELEMETRY.md`.
- Onboarding docs: `templates/ONBOARDING.md` + `ONBOARDING_STANDARD.md`.
- Pre-commit/CI/packaging: `templates/` + just recipes, not vends.

## Rules for adding a surface

1. Proven reference first — extract, never invent.
2. Scripted halves go in `scripts/just/vends.ps1` + valid surfaces list.
3. Merge halves get an SOP phase with gates, like Phase 2/2b.
4. Macro mirror in `standards/rules/agentic_macros.md` §vends.
5. Default run stays `apps,llm` — new surfaces are opt-in.
6. Max 5 repos per fanout run (batch rule).
