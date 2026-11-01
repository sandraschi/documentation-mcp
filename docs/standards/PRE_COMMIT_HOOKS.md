---
title: "Pre-Commit & Commit Hook Mechanics (SOTA 2026)"
category: standards
status: reference
audience: mcp-dev
last_updated: 2026-07-31
---

# Pre-Commit & Commit Hook Mechanics

**Status:** Reference — decide per-repo, not fleet-mandatory (see [GIT_WORKFLOW.md](./GIT_WORKFLOW.md) key principle: no process that benefits the tool over the developer)

Git and GitHub give you several distinct hook points. They run at different times and catch different problems — don't conflate them.

---

## 1. `pre-commit` hook (client-side, runs before you write the message)

Runs on `git commit`, before the editor even opens. Best for: linting, formatting, secret scanning on **staged files only**.

Two ways to implement:

### a) Raw git hook
`.git/hooks/pre-commit` — not version-controlled by default (lives in `.git/`, not the repo). Fine for solo use, invisible to contributors unless you symlink it in via `core.hooksPath`.

### b) `pre-commit` framework (Python, recommended for this fleet)
Since we're `uv` + `ruff` fleet-wide, the [pre-commit](https://pre-commit.com) framework is the natural fit — config lives in `.pre-commit-config.yaml`, versioned with the repo:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: https://github.com/biomejs/pre-commit
    rev: v0.5.0
    hooks:
      - id: biome-check
```

```powershell
uv tool install pre-commit
pre-commit install          # wires .git/hooks/pre-commit
pre-commit run --all-files  # manual full-repo run
```

### c) Node/JS equivalent: husky + lint-staged
Relevant for any repo with a webapp/Tauri frontend (React, biome). `lint-staged` restricts formatting/linting to staged files only, `husky` wires the git hook:

```powershell
npm install --save-dev husky lint-staged
npx husky init
```

---

## 2. `commit-msg` hook (client-side, runs after message is written)

Covered in depth already — validates/rewrites the message itself (conventional commits format). See implementation snippet below; this is the one from last night's decision.

```bash
#!/bin/bash
# .githooks/commit-msg
MSG=$(cat $1)
if ! echo "$MSG" | grep -qE "^(feat|fix|chore|docs|test|refactor)(\(.+\))?:"; then
  echo "Commit must start with: feat: fix: chore: docs: test: refactor:"
  exit 1
fi
```

JS-stack alternative: **commitlint** (usually paired with husky's `commit-msg` hook) — more configurable than a grep script, understands scopes, breaking-change footers, etc.

```powershell
npm install --save-dev @commitlint/cli @commitlint/config-conventional
```

---

## 3. `pre-push` hook (client-side, runs before push)

Cheaper than CI for catching obvious breaks before they leave your machine — run the fast test subset or a build check. Good candidate for repos where NSIS/mcpb builds are expensive and you don't want a broken build reaching `main`.

```bash
#!/bin/bash
# .githooks/pre-push
just test-fast || exit 1
```

---

## 4. GitHub-side complements (not git hooks, but same job)

These run server-side / on GitHub, after push — the enforcement layer once contributors exist:

- **Required status checks** (branch protection) — CI must pass before merge; see [GIT_WORKFLOW.md](./GIT_WORKFLOW.md#github-specific)
- **Required signed commits** — `Settings > Branches > Require signed commits`; verifies GPG/SSH-signed commits, catches spoofed authorship
- **CODEOWNERS** — forces review from specific people/teams on matching paths
- **GitHub Actions** — the actual CI runner; see [GITHUB_ACTIONS_NO_PRIVATE_CI.md](./GITHUB_ACTIONS_NO_PRIVATE_CI.md) for fleet policy on what runs where

---

## Fleet recommendation

| Hook | Solo/experimental repos | User-facing / production repos |
|---|---|---|
| pre-commit (lint) | optional, low friction if added | yes — `ruff` + `biome` via `pre-commit` framework |
| commit-msg (conventional commits) | skip | yes — enables changelog automation |
| pre-push (fast tests) | skip | optional, if test suite is fast enough not to annoy |
| branch protection / required checks | n/a (no contributors) | yes, once a second contributor exists |

Same hybrid logic as the git-workflow doc generally: add process when it starts paying for itself, not before.
