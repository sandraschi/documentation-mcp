---
title: "Renovate Bot Standards (SOTA 2026)"
category: standards
status: active
audience: mcp-dev
last_updated: 2026-07-21
---

# Renovate Bot Dependency Standards

**Version**: 1.0  
**Status**: RECOMMENDED (for all public and free repositories in the fleet)

## 1. Overview
In our fleet execution model (where we manage 250+ active repositories), **Dependabot** generates excessive noise, individual PR notifications, and continuous CI runner build triggers.
To keep repositories clean, updated, and secure without manual bottleneck fatigue, **Renovate Bot** is the standardized choice for automated dependency management.

## 2. Renovate vs. Dependabot
Compared to Dependabot, Renovate provides critical advantages:
- **Cohesive Grouping**: Combines related packages (e.g. all development tools like `pytest` and `ruff`) into a single consolidated PR rather than opening 10 separate PRs.
- **Lockfile Maintenance**: Auto-detects and updates lockfiles (`uv.lock`, `package-lock.json`, `pnpm-lock.yaml`) seamlessly.
- **Configurable Auto-Merge**: Safe patch and minor updates can be merged automatically if the repository CI test suite passes.
- **Zero-Day Supply Chain Defense**: Supports `minimumReleaseAge` to delay new package updates until they have been tested in the wild, avoiding compromised package updates that are yanked by registries within 24-72 hours.

## 3. Canonical Repository Config (`renovate.json`)
Every public fleet repository adopting Renovate should place a `renovate.json` configuration file in the repository root.

### Standard Template:
```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:recommended"
  ],
  "minimumReleaseAge": "14 days",
  "packageRules": [
    {
      "matchUpdateTypes": ["pin", "digest", "patch", "minor"],
      "matchDepTypes": ["devDependencies"],
      "groupName": "devDependencies (non-major)",
      "automerge": true,
      "minimumReleaseAge": "7 days"
    },
    {
      "matchUpdateTypes": ["patch"],
      "matchDepTypes": ["dependencies"],
      "groupName": "dependencies (patch)",
      "automerge": true
    }
  ],
  "timezone": "Europe/Vienna"
}
```

## 4. Operational Best Practices
- **Timezone**: Set to `Europe/Vienna` to align updates with local offline operational windows.
- **Auto-Merge**: Only enable `automerge: true` if the repository has a robust CI test suite configured on GitHub Actions.
- **Release Age (Defense-in-Depth)**: Ensure `minimumReleaseAge` is set to at least `14 days` for production dependencies. This ensures that zero-day compromised packages are flagged and removed from upstream registries (PyPI, npm, RubyGems) before the bot updates your codebase.
- **Private Repositories**: Refer to `GITHUB_ACTIONS_NO_PRIVATE_CI.md` — if GitHub Actions are disabled on a private repository, ensure `automerge` is disabled or runs via manual checkpoints to prevent pushing untested package lock updates.
