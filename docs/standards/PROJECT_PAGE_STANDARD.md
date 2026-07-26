# Fleet Project Page Standard

**Status**: ACTIVE — applies to all sandraschi MCP server repos
**Adopted**: 2026-07-18
**Trigger**: learnbot-mcp existed on disk since 2026-07-15, with 22+ real
commits, and had no `projects/learnbot-mcp/` page, no `fleet-registry.json`
entry, and no `FLEET_INDEX.md` row — three weeks in, discovered only by
accident when a *different* new repo's port collided with it.

---

## The Problem

A repo can be real, committed, and running, and still be functionally
invisible to the fleet: not searchable via `mcp-central-docs`, not listed
in `FLEET_INDEX.md`, not carrying a port reservation, and not covered by
the docs-sync tooling. This isn't hypothetical — three separate, independent
checks all confirmed learnbot-mcp's total absence:

- `fleet-registry.json` (the curated master list): zero matches for `learnbot`.
- `projects/` (the synced-docs catalog): no `learnbot-mcp` directory at all.
- `FLEET_INDEX.md` (the human-readable table): no row.

The existing tooling (`sota-scripts/sync-project-docs.ps1`,
`scripts/operations-scripts/sync-fleet-registry.ps1`) is real and works,
but it is **manually triggered and not scheduled**. Evidence it's been
neglected, not just missed once:
`scripts/operations-scripts/output/FLEET_INDEX.pending.md` — the queue of
repos discovered-on-disk-but-not-registered — was last generated
**2026-06-05** and lists 25 repos still sitting unreviewed, over six weeks
later. `sketchboard-excalidraw-mcp`, created 2026-07-17, only discovered
learnbot-mcp existed because its day-one port assignment (11101) collided
with learnbot-mcp's — an accident, not a process working as intended.

**The rule: registration happens at repo creation, not in a periodic batch
sweep that depends on someone remembering to run two PowerShell scripts.**

---

## Required Layers

A repo is NOT fully registered until all three of these exist. Partial
registration (e.g., a port reservation with no project page) is exactly
the failure mode that caused this standard to be written — don't consider
the job done until all three are checked.

### 1. `fleet-registry.json` entry

Path: `mcp-central-docs/operations/fleet-registry.json`

```json
{
  "id": "repo-name",
  "name": "Human-Readable Name",
  "description": "One or two sentences: what it does, what makes it distinct. Not 'MCP server discovered on disk; not yet in fleet-registry.json' — write a real sentence.",
  "port": 12345,
  "repo_path": "D:/Dev/repos/repo-name",
  "category": "AI | Media | Creative | Robotics | Control | Knowledge | Comms | Transit | Infra | Dev | Gaming",
  "icon": "lucide-react icon name (optional)",
  "fastmcp": "3.2"
}
```

**Rules:**
- `port` must not collide with any existing entry — check
  `operations/WEBAPP_PORTS.md` AND every other `fleet-registry.json`
  entry before assigning. This is the single most common failure (see
  learnbot-mcp/sketchboard-excalidraw-mcp collision above, and the
  earlier games-app port collision documented in learnbot-mcp's own
  CHANGELOG.md — this class of bug has now recurred at least three times).
- `category` picked from the same taxonomy `sync-fleet-registry.ps1`
  already uses (see its `Get-CategoryFromName` function) — don't invent
  a new category ad hoc.
- `description` is written by a human or by an agent that has actually
  read the repo, never left as the discovery-script's placeholder text.

### 2. `projects/<repo-name>/` synced docs directory

Path: `mcp-central-docs/projects/<repo-name>/`

Populated by `sota-scripts/sync-project-docs.ps1`, which copies these
files from the source repo if they exist:

| Source file | Synced as |
|---|---|
| `README.md` | `README.md` |
| `PRD.md` or `docs/PRD.md` | `PRD.md` / `docs_PRD.md` |
| `CHANGELOG.md` | `CHANGELOG.md` |
| `STATUS.md` | `STATUS.md` |
| `INSTALL.md` | `INSTALL.md` |
| `docs/TOOLS.md` | `docs_TOOLS.md` |
| `docs/CONFIGURATION.md` | `docs_CONFIGURATION.md` |
| `docs/DEVELOPMENT.md` | `docs_DEVELOPMENT.md` |
| `docs/TROUBLESHOOTING.md` | `docs_TROUBLESHOOTING.md` |
| `llms.txt` / `llm.txt` | as-is |
| `pyproject.toml` / `config.yaml` / `config.json` | as-is |

**This table has already changed once** — `STATUS.md`, `INSTALL.md`, and
the four `docs/*.md` files are new as of this standard and did not exist
in the script's `$DocsToSync` list before 2026-07-18 (see
[README_STRUCTURE.md](./README_STRUCTURE.md), which made `INSTALL.md` and
the four `docs/*.md` files required repo files). **Whoever updates
README_STRUCTURE.md's required-files list must update
`sync-project-docs.ps1`'s `$DocsToSync` array in the same change** — these
two standards drift apart if maintained separately, which is exactly the
kind of gap this document exists to close.

Plus, auto-generated (not copied — built by the script):

```json
{
  "id": "repo-name",
  "path": "D:\\Dev\\repos\\repo-name",
  "github_url": "https://github.com/sandraschi/repo-name.git",
  "last_sync": "2026-07-18 12:00:00"
}
```

### 3. `FLEET_INDEX.md` row

Path: `mcp-central-docs/projects/FLEET_INDEX.md`

```
| [repo-name](file:///D:/Dev/repos/repo-name) | Type | Status | Description |
```

**Rules:**
- `Type`: `MCP Server` for anything registering MCP tools, `Experiment`
  for scaffolds/prototypes not yet promoted.
- `Status`: one of `Active`, `Inactive`, `Deprecated`, `**Day 1 scaffold**`,
  or a bolded custom status if there's something the reader needs to see
  immediately (e.g. `**Active — fleet voice layer**` for speech-mcp).
  Never leave this blank.
- `Description`: same bar as the registry description — a real sentence
  describing what's actually implemented, not aspirational copy. Include
  real port numbers, real tool counts verified against source (not copied
  from a stale README), and known limitations if they matter (see the
  `sdr-mcp` row for the pattern: "P1 bugs: ... Needs P1 fixes ... to be
  useful" — this fleet's index tells the truth about broken things, it
  doesn't just list features).
- Never write "No description available." — if you don't know enough
  about the repo to describe it, that's a signal to go read it first, not
  to ship a placeholder.

---

## Registration Timing

**Registration is part of creating a repo, not a follow-up task.**

If you're using `new-mcp-server-intelligent.ps1` (or whatever the current
new-repo scaffold script is), registration in all three layers above
should be a step in that script, not something deferred to the next time
someone happens to run `sync-project-docs.ps1` across the whole fleet.

If a repo already exists and isn't registered (the learnbot-mcp case),
fix it now — don't add it to a pending queue that might not get reviewed
for six weeks. Concretely:

1. Add the `fleet-registry.json` entry by hand (check the port first).
2. Run `sync-project-docs.ps1` scoped to just that one repo, or copy the
   files by hand if you can't run PowerShell from your current
   environment.
3. Add the `FLEET_INDEX.md` row by hand.
4. Delete the repo's line from `FLEET_INDEX.pending.md` if it's there.

---

## Ongoing Sync

`sync-project-docs.ps1` re-copies files on every run — it's safe to run
repeatedly and will pick up doc changes made after initial registration.
It is **not currently scheduled**. Until it is, treat "did I re-run the
docs sync" as part of any PR/session checklist for a repo whose
README/CHANGELOG/STATUS changed materially — the same discipline gap that
let learnbot-mcp's actual code and docs drift a full day ahead of its
last commit (see the emergency-commit incident, 2026-07-18) applies here
too: work that isn't synced doesn't exist for anyone who isn't looking at
your local disk.

**Recommendation, not yet implemented**: add `sync-project-docs.ps1` and
`sync-fleet-registry.ps1` to a scheduled task (daily is enough) so
registration gaps surface within a day instead of being discovered by
accident weeks later. Until that exists, this is a known, disclosed gap
in the standard's own enforcement — not a solved problem.

---

## Validation

No automated checker exists yet for this standard (unlike
[README_STRUCTURE.md](./README_STRUCTURE.md), which has
`scripts/check-readme-structure.ps1`). A minimal version would:

- [ ] For every `*-mcp`/`*_mcp` directory under `D:\Dev\repos`, confirm a
      matching `id` exists in `fleet-registry.json`
- [ ] For every `fleet-registry.json` entry, confirm a `projects/<id>/`
      directory exists with at least `README.md` and `metadata_sync.json`
- [ ] For every `fleet-registry.json` entry, confirm a `FLEET_INDEX.md`
      row exists (grep for the id)
- [ ] Flag any `FLEET_INDEX.md` row whose Description is empty or is the
      literal string `No description available.`
- [ ] Flag any two `fleet-registry.json` entries sharing a port

This is `sync-fleet-registry.ps1`'s diff logic, mostly already written —
it needs a `-Strict` mode that exits non-zero on any gap, the same
pattern `check-readme-structure.ps1` already uses, so it can run in CI
instead of only producing a diff file nobody reviews.
