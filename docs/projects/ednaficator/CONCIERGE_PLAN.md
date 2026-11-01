# Edna Concierge Plan (summary)

**Canonical doc:** [ednaficator/docs/CONCIERGE_PLAN.md](https://github.com/sandraschi/ednaficator/blob/main/docs/CONCIERGE_PLAN.md) in the repo.

Edna widens from Plex-only to a **family concierge**: media (Tier 0), email (Tier 1), news/TTS (Tier 2), optional calendar later (Tier 3). Dev tools (KiCad, winops, git, docker) stay out of concierge paths.

## Key mechanism

- `EDNA_CONCIERGE_TOOLS` — concierge allowlist by tier
- `EDNA_MCP_ALLOWLIST` — orchestrator dev mode only
- Direct Python adapters (like `plex_tools.py`), not MCP stdio on family hot paths

## Phases

1. **Plex REST** — done (`/api/concierge/*`)
2. **Email adapter** — send + read summaries
3. **aiwatcher digest + TTS** — read news aloud
4. **`EDNA_MODE=concierge`** — chat + Telegram routing

See repo doc for exclusions, env vars, and file references.
