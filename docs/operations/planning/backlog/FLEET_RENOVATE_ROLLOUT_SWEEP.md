# Fleet Renovate Rollout Sweep

**Priority:** P2
**Scope:** All fleet repos with `.github/workflows/ci.yml`
**Added:** 2026-07-29 (switched from Dependabot to Renovate same day)

## Problem

GitHub Actions deprecate runner Node versions silently. `actions/setup-node@v4` with `node-version: "20"` started failing in July 2026. Without automated version bumps, every repo's CI decays individually until it breaks.

Renovate (over Dependabot) because: `stabilityDays` supply-chain cooldown, PR grouping to reduce noise, rules-based auto-merge, cron scheduling.

## Why not Dependabot

- No supply-chain cooldown (`stabilityDays`) — PRs land the moment a release drops
- No PR grouping — one PR per dep, flooding repos
- No rules-based auto-merge
- `reviewers` is the only safety knob, and it's human-blocking

## Per-repo checklist

- [ ] `renovate.json` at repo root
- [ ] `stabilityDays: 3` (3-day supply-chain cooldown)
- [ ] `prConcurrentLimit: 3` (caps the flood)
- [ ] `schedule: ["before 6am on Monday"]`
- [ ] `automerge: true` for `github-actions` manager only
- [ ] Labels: `dependencies`

## Template

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "stabilityDays": 3,
  "prConcurrentLimit": 3,
  "schedule": ["before 6am on Monday"],
  "labels": ["dependencies"],
  "packageRules": [
    {
      "matchManagers": ["github-actions"],
      "automerge": true,
      "automergeType": "pr",
      "platformAutomerge": true
    }
  ]
}
```

## Canary (10 repos, done 2026-07-29)

pywinauto-mcp, arxiv-mcp, plex-mcp, advanced-memory-mcp, multi-backup-mcp,
local-llm-mcp, bookmarks-mcp, freecad-mcp, gazebo-mcp, depot-mcp

(Also requires Renovate GitHub App installed on the sandraschi account.)

## Trigger

`node-version: "20"` deprecation (2026-07-29), `actions/checkout@v4` → `v5`, `setup-python@v5` → `v6`.
