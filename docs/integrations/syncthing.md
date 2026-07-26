---
title: "Syncthing — P2P folder sync (reference)"
category: integration
status: active
audience: mcp-dev
related:
  - standards/GIT_REPOSITORY_SAFETY.md
  - standards/GITIGNORE_STANDARDS.md
  - patterns/README.md
last_updated: 2026-06-28
---

# Syncthing — Reference

**P2P continuous file sync** — no central server, encrypted, open protocol.
Useful for the fleet when you need a repo folder available on multiple
workstations (Goliath, MiniPC, etc.) without a cloud middleman.

| Fact | Value |
|---|---|
| Latest stable | v2.1.1 (2026-06-02); v2.1.2-rc.4 in testing |
| Cadence | ~monthly patches, 1-2 feature releases per year |
| Engine | Go |
| License | **MPL 2.0** (true FOSS) |
| Owner | The Syncthing Foundation (Swiss non-profit) |
| Stars | 85.9k |
| Repo | github.com/syncthing/syncthing |
| Docs | docs.syncthing.net |
| Windows | Native x64, no WSL; tray icon + browser GUI on `127.0.0.1:8384` |
| Docker | `docker.io/syncthing/syncthing` / `ghcr.io/syncthing/syncthing` |
| Privacy | Zero data on third-party servers. Every device has a crypto ID. |

## How it works

Each device is identified by a **device ID** (a long hash derived from its TLS
certificate). You share a folder by adding the remote device ID to your folder's
share list. Discovery happens over LAN broadcast; if they're on different
networks, Syncthing uses global discovery servers (just to find each other) and
relay servers (if direct connection fails). All traffic is TLS 1.3 with perfect
forward secrecy.

## Why the fleet cares

Our problem: `D:\dev\repos` lives on Goliath with ~40 MCP repos. MiniPC and
other machines need the same tree. GitHub push/pull works but:

- You must remember to push before switching machines.
- Branches, stashes, and uncommitted work don't transfer.
- AI agent state files and `.opencode/` caches aren't in git.

Syncthing addresses the **read-only sync** use case: repos are always present
on all machines, up to date within seconds. But **git operations should still
go through GitHub** — Syncthing is for the working tree, not for distributed
git history management.

## Docker usage

```powershell
docker run -d \
  --name syncthing \
  -p 8384:8384 `    # Web UI
  -p 22000:22000 `  # TCP sync protocol
  -p 21027:21027/udp ` # LAN discovery
  -v D:\dev\repos:/var/syncthing:rw `
  docker.io/syncthing/syncthing:2
```

Or with explicit config/data dirs:

```powershell
docker run -d \
  --name syncthing \
  -p 8384:8384 -p 22000:22000 -p 21027:21027/udp \
  -v D:\dev\repos:/var/syncthing \
  -v C:\Users\Sandra\.config\syncthing:/var/syncthing/config \
  docker.io/syncthing/syncthing:2
```

## Windows native (no Docker)

Download the [latest Windows x64
exe](https://github.com/syncthing/syncthing/releases/latest) — it's a single
binary, no installer needed. Run it and open `http://127.0.0.1:8384` in the
browser.

```powershell
# Start (first run generates cert + config)
syncthing.exe
# GUI at http://127.0.0.1:8384
```

Recommended: run as a background task at login so sync is always active.

## Fleet setup for `D:\dev\repos`

### Step-by-step

1. **Install Syncthing** on Goliath and MiniPC (and any other machine).
2. **Goliath:** In the web UI, add `D:\dev\repos` as a shared folder.
   - Folder ID: `dev-repos`
   - Label: `MCP Fleet Repos`
   - **File pull order:** `NewestFirst` (important for .git safety)
3. **MiniPC:** Add the same folder ID, point it to `D:\dev\repos` (or wherever
   you want the tree).
4. **Exchange device IDs** — Goliath shows its ID in the web UI; enter it on
   MiniPC as a remote device and vice versa.
5. **Share** the `dev-repos` folder with each other's device IDs.

### .stignore (critical)

Syncthing supports an `.stignore` file in the root of a synced folder. For a
git repo tree, **do not ignore `.git/`** — you want the git metadata synced or
the repo is useless. Instead, ignore only what would cause trouble:

```
# .stignore — place in D:\dev\repos
# Never sync agent temp / build artifacts across machines
node_modules/
.venv/
target/
__pycache__/
*.pyc
*.pyo
.env
*.log
htmlcov/
.coverage
dist/
*.mcpb
```

**.git is intentionally NOT in .stignore.** Without it, `git log` on the
receiving end sees an empty repo. The risk is real but manageable — see
"Caveats" below.

## v2.1 new features

| Feature | What it does |
|---------|-------------|
| **Folder grouping** | GUI now supports `group` attribute to organize folders into collapsible sections |
| **HTTP/HTTPS CONNECT proxy** | `all_proxy=https://proxy:3128` — works where SOCKS doesn't (corporate networks) |
| **Configurable block indexing** | `blockIndexing=true/false` per folder — turn off to reduce DB size if you don't need block-level delta sync |
| **Session cookie config** | `sessionCookieDurationS` (default 604800 = 1 week), `sessionCookiePath` — useful for long-running headless setups |

## Release cadence

Syncthing is mature (v1.0 was 2018). The project follows a conservative cadence:

- **Minor releases** (v2.0 → v2.1): every 8-14 months.
- **Patch releases** (v2.1.0 → v2.1.1): roughly monthly.
- **Release candidates**: ~2-4 weeks of RC testing before each stable.
- **Long-term stability**: go.dev security patches are applied quickly, but
  feature churn is low. The protocol (BEP v1) has been stable for years.
- **Security**: CVEs are rare; when they happen, patches ship within days.

## Caveats — read before syncing git repos

### Syncing an open .git is risky

Syncthing syncs file-by-file. If a git operation (rebase, commit with large
objects, gc) is in progress on one machine while the other pulls changes, the
`.git/objects/pack/` directory can arrive in an inconsistent state. **Symptoms:
`fatal: bad object`, `fatal: packfile cannot be mapped`, missing refs.**

Mitigations:
- **Never have both machines running opencode/Cursor on the same repo
  simultaneously.**
- **Push/pull through GitHub for actual git operations.** Treat Syncthing as
  "the tree is there when I open the laptop" — not as a distributed git
  transport.
- Set `File Pull Order: NewestFirst` so the most recently modified version wins.
- If `.git` gets corrupted: `git reset --hard origin/main` or re-clone.

### What Syncthing is good for

- Having the full `D:\dev\repos` tree warm on MiniPC when you switch seats.
- Syncing `.opencode/` state, recent context files, and non-git config across
  machines.
- Pre-seeding a new machine: install Syncthing, let it pull ~40 repos, then
  only fix per-machine `.env` files.

### What Syncthing is NOT

- Not a backup (deletions sync too).
- Not a git replacement (GitHub remains the source of truth).
- Not a collaboration tool (use GitHub for multi-user; Syncthing is single-user
  multi-device).

## Quick mental model

```
git push/pull  = source-of-truth, intentional, for history
Syncthing     = warm cache, automatic, for working tree
```

Both. Git for versioned data, Syncthing for "I don't want to `git pull` 40
repos manually."

## References

- Releases — github.com/syncthing/syncthing/releases
- Docs — docs.syncthing.net
- Getting started — docs.syncthing.net/intro/getting-started.html
- Protocol spec — docs.syncthing.net/specs/bep-v1.html
- .stignore — docs.syncthing.net/users/ignoring.html
