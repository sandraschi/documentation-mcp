# -phile fleet pattern

**Status:** ACTIVE (template) · **Reference implementation:** [japanophile-mcp](./README.md) · **Sister plan (MCD):** [PHILE_SISTERS_PLAN.md](../PHILE_SISTERS_PLAN.md) (austrophile-mcp, sinophile-mcp)

## Idea

One git repo per culture you care about deeply. Not a thin API wrapper — a **local-first workstation** that outlives tab chaos: study daily, read curated culture pages, plan trips, and keep a diary of progress. Agents use the same tools via MCP; humans use webapp + optional Tauri winapp.

## Four faces (every -phile repo)

| Face | User job | Typical tools / UI |
|------|----------|-------------------|
| **Learn** | Language, drills, games | Portmanteau MCP tools, SRS, static or React drills |
| **Know** | Trustworthy culture/history/economy | Vendored HTML/Markdown box, `knowledge/list|get`, citations |
| **Plan** | Travel, transit, bookings | Itinerary tools (often crossconnect to transit MCPs) |
| **Remember** | Streaks, diary, reviews | SQLite progress, diary MCP, FSRS/SM-2 scheduler |

Same sidebar mental model on every webapp: **Language · Knowledge · Practice** (plus Travel, Diary, MCP Tools — see japanophile v0.3.x). Legacy label **Learn · Know · Plan · Remember** maps to those faces.

## Three surfaces (fleet standard)

1. **MCP server** — stdio for Claude Desktop / Cursor; dialogic tool returns.
2. **HTTP bridge** — FastAPI REST mirroring tool impl; static assets for legacy drills; `/mcp` streamable HTTP.
3. **Human shell** — Vite React dashboard + optional Tauri NSIS winapp + `.mcpb` bundle.

Implement business logic once (`server.py` tool functions); HTTP and MCP both call into it.

## Data tiers

| Tier | Commit to git? | Example |
|------|----------------|---------|
| Seeds | Yes (cap ~5–10 MB each) | Quiz DB, compact dictionaries |
| Big corpora | No — fetch script | Full vocab/JMdict, Wakan |
| Runtime | No — gitignored | `progress.db`, diary, SRS state |

Missing big data → **fetch hint in message**, never a traceback.

## Crossconnects (not duplication)

- **Games vs learning:** playable arcade titles stay in [ai-games-collection](../ai-games-collection/); learning canonical in `{culture}ophile-mcp`.
- **Speech:** [speech-mcp](../speech-mcp/) for listen/speak drills.
- **Chat/workflows:** [local-llm-mcp](../local-llm-mcp/) + repo skill (`skills/{culture}-expert/SKILL.md`) routes to tools and Know pages.
- **Read:** [calibre-mcp](../calibre-mcp/) for the culture's literature, textbooks, and manga library — enrichment for Learn/Know, not a reader built into the -phile repo.
- **Watch:** [plex-mcp](../plex-mcp/) for the culture's movies and shows (japanophile: JP cinema/anime) — same rule, enrichment not duplication.
- **External intel:** [aiwatcher-mcp](../aiwatcher-mcp/), arxiv/notebooklm — enrichment with citations, not replacement for Know box.
- **Discord:** [discord-mcp](../discord-mcp/) for reminders/community; curriculum stays in repo.
- **Plan:** reuse patterns from [publictransport-mcp](../publictransport-mcp/), [gtfs-mcp](../gtfs-mcp/), email/calendar MCPs as needed.
- **Voice:** registered as a Voice Command Bus receiver (`japanophile` entity,
  direct route — see `standards/VOICE_COMMAND_BUS.md` §4c) so *"japanophile
  kanji water"* etc. can route through fleet-agent/speech-mcp — separate
  mechanism from the Speech crossconnect above (that's TTS/STT the webapp
  calls out to; this is fleet-agent calling *in* to japanophile-mcp's own
  tools). **Not yet functional**: japanophile-mcp's `/mcp` mount currently
  fails session init, blocking `fleet_call_tool` from reaching it.

As of 2026-09-15 (japanophile-mcp v0.3.1), Chat/workflows (local-llm-mcp), Speech,
Read (calibre-mcp), and Watch (plex-mcp) are all wired via a new `crossconnect`
MCP tool + `/api/crossconnect/*` HTTP routes that thinly proxy each peer's REST
API — see `docs/TOOLS.md` in the repo. External intel and Discord crossconnects
remain undone. Wiring calibre-mcp and plex-mcp surfaced real bugs in both
(query/media_type filters silently ignored server-side) — worked around
client-side in japanophile-mcp, flagged as follow-ups in their own repos.

## Replication checklist (austrophile-mcp, …)

1. Register **new** backend/frontend ports in [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md).
2. Add `fleet-registry.json` + `projects/{repo}/` + `FLEET_INDEX.md` row ([PROJECT_PAGE_STANDARD.md](../../standards/PROJECT_PAGE_STANDARD.md)).
3. Copy scaffold: pyproject, justfile, `.gitignore`-first, five-tool minimum + `{name}_help`, HTTP module, webapp catch-them-all.
4. Ship culture pack: seeds, knowledge HTML, skill editorial line, fetch script for big DBs.
5. Document crossconnects in MCD project README.

## Editorial

Culture guides are **sourced and neutral** — document with references; decline propaganda or glorification (see japanophile-expert skill in repo).

## Related

- [PHILE_SISTERS_PLAN.md](../PHILE_SISTERS_PLAN.md) — austrophile-mcp + sinophile-mcp draft plan (ports, curriculum, stages)
- [japanophile-mcp PRD](./PRD.md) §2
- [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) (11193/11194)
