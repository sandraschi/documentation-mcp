# DeepSeek Local Inference — Status (DS4 / DwarfStar4)

**Last updated:** 2026-08-29
**Relates to:** [awesome-deepseek-agent-overview.md](awesome-deepseek-agent-overview.md), `ecosystem/opencode/local-backend-status.md`

## Cloud usage (unaffected, for contrast)

DeepSeek V4 Pro/Flash mix is the daily driver in OpenCode, cloud API, ~€80/month. Stable for months, on par with Opus 4.8 for coding.

**Standing risk flag:** DeepSeek V4 Flash has a documented silent subsampling failure on full-fleet scans — it will quietly process a subset of repos/files and report as if complete. This is exactly what the fleet rule "all means all, no subsampling allowed" exists to counter. Spot-check coverage on any multi-repo scan before trusting a "done" report.

**Deprecation note:** `deepseek-chat` / `deepseek-reasoner` aliases deprecated 2026-07-24 — cross-reference `ecosystem/opencode/local-backend-status.md`, same action item, don't fix it in two places without syncing.

## Local inference track: antirez/ds4 (DwarfStar4)

Separate from the OpenCode local-backend effort (which uses Qwen models as a substitute) — this track is specifically about running **DeepSeek V4 Flash itself** locally.

**Status as of last check (2026-07-17 — likely stale, re-verify before acting on it):**
- CUDA backend landed May 11, 2026.
- Currently targeting DGX Spark as the first-viable platform, not a solo 4090.
- Checking weekly for solo-4090 viability and Windows CUDA build maturity — no confirmation yet that a single 4090 can run it.
- KV-disk feature flagged as a good fit for Goliath's 4TB NVMe, if/when solo-4090 becomes viable.
- Dual DGX Spark (TP=2, ~20-40 tok/s projected) deferred to Q1 2027 — fallback if solo-4090 never pans out. Own assessment: Spark GPU is "slow as molasses," so this is a hedge, not an enthusiastic pick.

## Action item

The "checking weekly" cadence implies this status may already be stale. Re-check antirez/ds4 repo activity and Windows CUDA build maturity before assuming anything above still holds.

## How this differs from the other two local-LLM threads

1. **OpenCode backend** (`ecosystem/opencode/local-backend-status.md`) — any capable model, goal is cost reduction, not DeepSeek specifically.
2. **DS4/DwarfStar4** (this doc) — the actual DeepSeek V4 Flash weights, blocked on hardware/CUDA maturity.
3. **Dual DGX Spark** — long-term hardware bet for #2, Q1 2027.
