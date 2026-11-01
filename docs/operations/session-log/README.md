# Fleet Session Log

Plain-language "what happened and why" for cross-agent continuity. Two kinds of
agent write here, and neither shares memory with the other:

- **Human-driven coding agents** — Claude Code, opencode, Cursor, Antigravity.
  A person is directing the session turn by turn. Write to `YYYY-MM-DD.md`
  (this directory).
- **Autonomous fleet agents** — Fritz (fleet-agent-mcp), AIWatcher, and other
  crawler/watcher repos that act on their own via cron/heartbeat, no human at
  the keyboard. **Fritz writes to `YYYY-MM-DD.md` too** (same file as the
  coding agents — its entries are infrequent and short). **AIWatcher writes to
  its own `aiwatcher/YYYY-MM-DD.md`** — its digests run long and frequent
  enough to swamp everything else if mixed in.

`../fleet-status.md` (mirrored from git-github-mcp's morning digest,
regenerated daily) tells you *what state* repos are in — uncommitted files,
stale PRs, sync drift. It can't tell you *why*, or what a session or an
autonomous run actually did and decided. This directory is the narrative layer
that fills that gap.

**Not the same thing as `intel_hub`** — that's Sandra's own human-reading
surface (pretty HTML, iPad over Tailscale). This directory is for agents to
read each other's provenance, not for her to read on a tablet.

## Layout

```
session-log/
  README.md              # this file
  YYYY-MM-DD.md           # coding agents + Fritz, one file per day
  aiwatcher/
    YYYY-MM-DD.md         # AIWatcher only, one file per day
```

**Rotation: 30-day retention, daily.** Every write prunes any file in its own
directory dated more than 30 days before today. Nothing is kept longer than a
month — weeks have quiet days (Claude Desktop sessions early in the week) and
hectic days, and a 7-day window could age out the only context that matters
before anyone reads it. If you need older history, it's in git history of this
repo (only if someone committed a given day's file before it aged out) or the
originating repo's own BUILD_LOG/PRs. Don't rely on this directory for
anything you need to keep past a month.

Shared appender script (handles today's filename, the entry header, and
pruning — don't hand-write files or hand-roll pruning logic):
`mcp-central-docs/scripts/session-log-append.py`

```powershell
uv run python D:\Dev\repos\mcp-central-docs\scripts\session-log-append.py `
  --agent "Fritz" --category autonomous `
  --title "Nightly repo audit" `
  --body "Checked 12 repos for drift, found none. No changes made." `
  --sink main
```

`--sink` is `main` (default) or `aiwatcher`.

## Convention

- One entry per significant session, task, or autonomous run, newest first
  within a day's file.
- **Provenance is mandatory and must be unambiguous**: header states which
  agent wrote it AND which category it is —
  `## YYYY-MM-DD — short title (Claude Code, human-driven session)` or
  `## YYYY-MM-DD — short title (Fritz, autonomous heartbeat run)`. A reader
  must be able to tell "a person was steering this" from "this happened on its
  own overnight" without opening anything else. The appender script fills
  this in from `--agent`/`--category` automatically.
- A few bullet points: what was done, why, what's still open/uncommitted.
- Add an entry at session end / major checkpoint (human-driven) or after any
  heartbeat cycle that made a real change (autonomous) — don't wait to be
  asked, same as you wouldn't wait to be asked to leave a commit message. An
  autonomous run that changed nothing does not need an entry.
- Keep it short. This is a pointer to detail (repo BUILD_LOGs, PRs, memory
  files, evolution logs), not the detail itself.
