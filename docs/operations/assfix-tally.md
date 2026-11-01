# Assfix Tally — Fleet-Wide Running Ledger

**Purpose**: Track assfix runs, priority, urgency, and token spend across the fleet. assfix is token-hungry (~150–250k tokens/repo estimate); this ledger keeps the queue honest and the budget visible.

**Update protocol**: after EVERY assfix run, append to the Token Ledger + mark the repo done in the Priority Queue + update Summary counters. Refresh the scan with `assfixstat`-style enumeration (`Get-ChildItem -Filter .assess-fix-timestamp`).

---

## Summary (as of 2026-08-07)

| Bucket | Count | Meaning |
|--------|-------|---------|
| Total project repos tracked | ~240 | pyproject.toml / package.json / README.md present |
| **Never assessed** | **177** | no `.assess-fix-timestamp` (nontrivial subset curated below) |
| Assessed, stale (>3 weeks) | 20 | last pass 2026-07-13 … 07-18 |
| Assessed recently (≤3 weeks) | 44 | |
| **Score 0 or critically low** | **0 — queue empty** | All four runts cleared 2026-08-07: system-admin-mcp 78, gtfs-mcp 78, dreame-mcp 96 SOTA, notepadpp-mcp 70 (mujoco-mcp is 9/**10** — good shape, scan misread) |

---

## Priority Queue

### Tier A — CRITICAL (agent/infra, never assessed, fleet-critical)

| Repo | Why | Action |
|------|-----|--------|
| fleet-agent-mcp (Fritz) | Core agent, NSSM services, coworker flows | assfix next |
| godot-mcp | 95+ tools, flagship game pipeline | assfix |
| resonite-mcp | 44 tools, live-verified, no timestamp | assfix |
| pywinauto-mcp | Fleet reference implementation (Tauri/CUA) | assfix |
| depot-mcp | Artifact depot (infra) | assfix |
| secrets-mcp | Credential vault bridge (infra) | assfix |
| monitoring-mcp / observability-mcp | Fleet observability (infra) | assfix |

### Tier B — FLAGSHIP user-facing, never assessed

qcad-mcp · jellyfin-mcp · obs-mcp · handbrake-mcp · davinci-resolve-mcp · blender-mcp · gimp-mcp · inkscape-mcp · unity3d-mcp · vrchat-mcp · virtualdj-mcp · steam-mcp · suno-mcp · mastodon-mcp · repomix-mcp · readly-mcp · sakana-mcp · podman-mcp · forgejo-mcp · toolbench-mcp

### Tier C — NEW repos (should have been assessed at birth)

| Repo | Born | Action |
|------|------|--------|
| ms-graph-mcp | 2026-08-04 (P7 spec → BUILT) | assfix |
| huggingface-mcp | 2026-08-05 v0.1.0 | assfix |
| unsloth-mcp | 2026-08-05 | assfix |
| cline-mcp | 2026-08-07 webapp registered | assfix |

### Tier D — STALE re-runs (assessed >3 weeks ago, still active)

advanced-memory-mcp · virtualization-mcp · avatar-mcp · devices-mcp · windows-operations-mcp · arxiv-mcp · calibre-mcp · discord-mcp · docker-mcp · plex-mcp · tailscale-mcp · speech-mcp · home-assistant-mcp · meta_mcp · aiwatcher-mcp · scraper-mcp · winrar-mcp · robotics-mcp · pinokio-mcp · bumi-mcp (last pass 2026-07-13…07-18)

**URGENT within Tier D — score 0 on last pass (runt, fails fleet bar):**

| Repo | Report | Gap profile |
|------|--------|-------------|
| ~~system-admin-mcp~~ | ~~0/100~~ → **78/100 (2026-08-07)** | **DONE** — pyright 0, CI blocking, cov gate, CUA recipes; remaining: testids/fonts/prints/resources (MEDIUM) |
| ~~gtfs-mcp~~ | ~~0/100~~ → **78/100 (2026-08-07)** | **DONE** — 4 CRITICAL + 22 HIGH all resolved; persistence test fixed, /api/shutdown added, dead backend deleted; remaining: fonts/prefab/resources/zustand (MEDIUM) |
| ~~notepadpp-mcp~~ | ~~0/100 "runt by checklist arithmetic"~~ → **70/100 (2026-08-07)** | **DONE** — 3 CRITICAL + 18 HIGH resolved; pyright 139→0, 118 tests pass; remaining: cov gate/e2e/annotations/webapp polish (MEDIUM) |
| ~~dreame-mcp~~ | ~~0/100 "clamped; 209 points"~~ → **83/100 SOTA (2026-08-07)** | **DONE** — 08-06 cloud-control burst (Hoover/LiDAR) verified: 13 HIGH closed, gates green; remaining: testids/examples/bun/chat indicator (MEDIUM) |

Correction 08-07: mujoco-mcp is **9/10** (very good shape) — the earlier tally misread the score as 9/100.

### Tier E — LOW / optional (rest of the 177)

Infrastructure daemons (health-mcp, cursor-mcp, goose-mcp, llm-txt-mcp, openrouter-mcp), bench/test repos, niche wrappers, non-MCP projects (FluidX3D, deepfang, myai — **myai: NOT before secret scrub**, see flags). Triage these only when Tiers A–D are clean.

---

## Token Ledger

Planning estimate: **150–250k tokens per assfix run** (assess + fix + lint + docs + build). Log actuals here.

| Date | Repo | Tokens (est/actual) | Score | Notes |
|------|------|---------------------|-------|-------|
| 2026-08-07 | — | ~20k (baseline scan) | — | Tally doc created; queue curated from 08-07 scan |
| 2026-08-07 | system-admin-mcp | ~120k (pyright 149→0 pass) | 78 | De-runt: CI gates blocking, coverage gate, CUA recipes; 5 MEDIUM + 2 LOW deferred (testids/fonts/prints/resources) |
| 2026-08-07 | gtfs-mcp | ~60k | 78 | Persistence test fix, /api/shutdown, dead web_sota/backend deleted; 5 MEDIUM + 1 LOW deferred (fonts/prefab/resources/zustand) |
| 2026-08-07 | dreame-mcp | ~40k (re-assessment) | 83 | **SOTA** — 08-06 burst (Hoover control + LiDAR map) verified to close 13 HIGH + most MEDIUM; 4 MEDIUM + 1 LOW deferred (testids/examples/bun/chat indicator) |
| 2026-08-07 | dreame-mcp (polish) | ~35k | **96** | Testids 13→35 all pages, bun.lock, examples+provider dot were false negatives. **Comeback of the day: user had given up on it months ago.** |
| 2026-08-07 | notepadpp-mcp | ~90k (pyright 139→0) | 70 | 3 CRITICAL + 18 HIGH resolved by 08-03 burst; this pass: pyright 139→0, pytest 118 pass, pyrightconfig; 6 MEDIUM deferred (cov gate/e2e/annotations/webapp polish) |

---

## Assessed History (what was ever done)

Sorted by last pass. Score = SOTA Score from `reports/assess-*.md` (blank = no score found).

| Repo | Last pass | Score | | Repo | Last pass | Score |
|------|-----------|-------|-|------|-----------|-------|
| advanced-memory-mcp | 07-13 | | | bench-orchestrator-mcp | 07-24 | 68 |
| virtualization-mcp | 07-13 | | | kicad-mcp | 07-24 | |
| avatar-mcp | 07-13 | | | reversing-mcp | 07-25 | |
| bumi-mcp | 07-13 | | | ocr-mcp | 07-25 | |
| devices-mcp | 07-13 | | | nekomimi-mcp | 07-25 | |
| windows-operations-mcp | 07-13 | | | fleet-public-relations-mcp | 07-25 | 55 |
| pinokio-mcp | 07-13 | | | alexa-mcp | 07-25 | |
| robotics-mcp | 07-13 | | | robofang | 07-29 | |
| arxiv-mcp | 07-14 | | | local-llm-mcp | 07-29 | |
| calibre-mcp | 07-14 | | | git-github-mcp | 07-29 | 58 |
| discord-mcp | 07-14 | | | moltbot-mcp | 07-29 | 22 |
| docker-mcp | 07-14 | 12 | | tvtropes-mcp | 07-29 | |
| tailscale-mcp | 07-14 | | | dark-app-factory | 07-29 | 55 |
| plex-mcp | 07-14 | | | sfx-mcp | 07-30 | |
| meta_mcp | 07-16 | | | overte-mcp | 07-30 | |
| aiwatcher-mcp | 07-16 | | | vfx-mcp | 07-30 | |
| speech-mcp | 07-16 | | | mujoco-mcp | 07-31 | 9 |
| home-assistant-mcp | 07-16 | | | email-mcp | 07-31 | |
| scraper-mcp | 07-17 | | | onenote-mcp | 08-01 | 42 |
| winrar-mcp | 07-18 | | | opencode-cli-mcp | 08-01 | |
| notion-mcp | 07-21 | | | filesystem-mcp | 08-01 | |
| obsidian-mcp | 07-21 | | | ai-games-collection | 08-02 | 42 |
| osc-mcp | 07-21 | | | system-admin-mcp | 08-02 | 0 |
| resolume-mcp | 07-21 | | | streamfog-mcp | 08-03 | |
| reaper-mcp | 07-21 | | | teleoperator-mcp | 08-03 | 41 |
| documentation-mcp | 07-23 | 60 | | gtfs-mcp | 08-03 | 0 |
| ring-mcp | 07-23 | 32 | | benny-the-dog-mcp | 08-03 | 56 |
| bench-camera-mcp | 07-24 | 66 | | bluesky-mcp | 08-03 | 100 |
| grandorgue-mcp | 07-24 | 62 | | notepadpp-mcp | 08-03 | 0 |
| freecad-mcp | 07-24 | | | vienna-life-assistant | 08-03 | |
| mixx-dj-mcp | 07-24 | | | rtorrent-mcp | 08-05 | |
| | | | | immich-mcp | 08-06 | |
| | | | | dreame-mcp | 08-06 | 0 |

---

## Flags & Caveats

- **myai**: do NOT assfix-to-public — real secrets in tracked `.env*` + history; needs untrack + `git filter-repo` + key rotation first (see fleet-dev-status-2026-08-07 §7.3)
- **Scan artifacts**: ~10 stray dirs caught in enumeration that aren't repos (path-fragment dir `DDevrepossysinternals-mcpweb_sota`, `giskard-mcp`, `status-mcp`, `loona-mcp`, `pico-tailscale-setup`, `tiny-mcp-servers` — no `.git`) — candidates for deletion, not assfix
- **Last-commit ranking is polluted** by the 2026-08-07 fleet-wide checkpoint sweep; use tier + criticality, not recency, until the next natural commit wave
- **Archived & pending manual deletion**: hasleo-backup-mcp, obsidianmcp, obsmcp (workflow collapse skipped; deletion pending user)
