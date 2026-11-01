# Possible projects — MCP ideas not yet built

**Status:** LIVING  
**Purpose:** Single place for “we might build this” MCP repos — before a full `projects/<name>/` pack or PRD.  
**Not for:** multi-server chains → [gestating-chains/](./gestating-chains/); gap closure PRDs → [operations/planning/](../operations/planning/README.md).

**Last updated:** 2026-07-26  

**Absorbed:** Oct 2025 [WRAPPEE_CANDIDATES_ANALYSIS.md](../docs-private/WRAPPEE_CANDIDATES_ANALYSIS.md) (archived / stale FastMCP notes). Survivors live **here**; that file now points here.

---

## How to use

| Column | Meaning |
|--------|---------|
| **Idea** | Proposed repo name |
| **Lane** | Fleet mission lane |
| **Why** | One-line value |
| **Blocker / note** | Honest friction |
| **Status** | `idea` · `promising` · `deferred` · `skip` · shipped pointer |

When a repo ships: move the row under **Shipped from this list** and link the real project.

**Assfix-zero bar when scaffolding:** [NEW_REPO_BUILD_COMPLETE.md](../standards/NEW_REPO_BUILD_COMPLETE.md).

---

## Promising leftovers from wrappee candidates (2025 → 2026 triage)

Fleet already ate most of the “must wrap” list. What’s left and still interesting:

| Idea | Why still interesting | Dupes / notes | Status |
|------|----------------------|---------------|--------|
| **spotify-mcp** | Playlist/library curation for DJ + ai-producer lane; great API (`spotipy`) | No `spotify-mcp`. Not suno / reaper / mixxx. | `promising` |
| **youtube-mcp** | Data API search + playlist + channel research for arxiv/fleet-PR | Prefer official Data API for metadata; downloads → **yt-dlp-mcp** (below). No youtube-mcp today. | `promising` |
| **yt-dlp-mcp** | FOSS download/archive of allowlisted URLs (research clips, talks) | Replaces “4K Video Downloader” wrappee. Handbrake = transcode only. | `promising` |
| **reddit-mcp** | Research + engagement; PRAW; dry-run + outbox like mastodon | No reddit-mcp. ToS/rate limits — human approve for posts. | `promising` |
| **audacity-mcp** | FOSS audio edit via mod-script-pipe / macros | No audacity-mcp. Complements reaper/handbrake/speech, doesn’t replace. | `promising` |
| **trello-mcp** | Lightweight kanban boards for personal/project ops | No trello-mcp. Notion ≠ boards. | `promising` |
| **wolfram-mcp** | Computational queries / units / closed-form helpers | No wolfram-mcp. leanforge/mathops ≠ Wolfram knowledge API. Needs AppID. | `promising` |
| **inno-setup-mcp** | `iscc.exe` — scripted Windows installer builds for Tauri/NSIS adjacent tooling | Niche but fits Windows fleet packaging. | `idea` |
| **twixxer-mcp** | X/Twitter (“Twixxer”) — complete social trio with mastodon + bluesky | **No useful free API (2026)** — pay-per-use. Dry-run/outbox free; live = meter. | `idea` |

### Wrappee items — already shipped or superseded (do not rebuild)

| Old candidate | Reality in fleet |
|---------------|------------------|
| Jellyfin | **jellyfin-mcp** |
| Beyond Compare | **beyondcompare-mcp** |
| AutoHotkey | **autohotkey-mcp** |
| GitHub | **git-github-mcp** |
| Notion | **notion-mcp** |
| Discord | **discord-mcp** |
| Adobe Acrobat / PDF CLI | **pdf-mcp** (+ Ghostscript patterns) |
| ABBYY FineReader | **ocr-mcp** (multi-engine) |
| OpenWeatherMap | **glance-mcp** (Open-Meteo) + **netatmo-weather-mcp** |
| Bulk Rename Utility | **filesystem-mcp** / **fastsearch-mcp** |
| Conda / CMake | Prefer **uv** + existing build tooling — low agent value |
| BlueStacks / VPN RGB / Armoury | Still **don’t wrap** |

---

## A dozen (plus) new ideas — not duplicating the fleet

Chosen against a Jul 2026 `*-mcp` directory scan. Prefer FOSS / agent-useful / Sandra-shaped (home, research, media, Vienna life).

| # | Idea | Lane | Why | Blocker / note | Status |
|---|------|------|-----|----------------|--------|
| 1 | **zotero-mcp** | Research | Citation library, collections, CSL export — papers live here, books in Calibre | Zotero local API / Web API; pairs with arxiv-mcp ingest | `promising` |
| 2 | **paperless-ngx-mcp** | Home docs | Self-hosted document archive (OCR’d PDFs, tags, correspondents) | Needs running Paperless; complements ocr-mcp + pdf-mcp | `promising` |
| 3 | **beets-mcp** | Music library | Smart music library tagger/organizer (not a streamer) | CLI-first; feeds Navidrome/Plex/Jellyfin | `promising` |
| 4 | **navidrome-mcp** | Music | Self-hosted Subsonic-compatible streamer control | If you run Navidrome; else defer to plex/jellyfin | `idea` |
| 5 | **trakt-mcp** | Media taste | Watch history / scrobble / watchlist across Plex+Jellyfin | Trakt API; not a media server | `promising` |
| 6 | **tmdb-mcp** | Media metadata | Movie/TV metadata + images for fleet media tools | Free API key; used by *arr already — agent-facing catalog still useful | `idea` |
| 7 | **anki-mcp** | Learning | Spaced-repetition decks (JP / fleet flashcards) | AnkiConnect local HTTP; ties ai-games-collection / linguistic skills | `promising` |
| 8 | **searxng-mcp** | Agent search | Private metasearch for agents (no Google ToS scrape) | Self-hosted SearXNG; complements scraper-mcp | `promising` |
| 9 | **syncthing-mcp** | Sync | Device sync status, folders, conflicts, restart | Syncthing REST; home multi-PC hygiene | `promising` |
| 10 | **proxmox-mcp** | Infra | PVE VMs/LXC/storage — virtualization-mcp is VBox/Hyper-V only | Needs Proxmox API token; homelab gold | `promising` |
| 11 | **pihole-mcp** (or **adguard-mcp**) | Home net | DNS blocklist stats, allow/deny, query log for agents | Pick one DNS product you actually run | `idea` |
| 12 | **matrix-mcp** | Comms | Open federated chat (Element homeserver / Matrix.org) | Complements discord; P4-comms is Telegram-first — Matrix is different protocol | `promising` |
| 13 | **lemmy-mcp** | Fediverse | Link aggregator (ActivityPub) — not microblog | Sibling to mastodon-mcp; communities ≠ toots | `idea` |
| 14 | **peertube-mcp** | Fediverse | Federated video host | Sibling lane; downloads/watch later | `idea` |
| 15 | **wallabag-mcp** (or **omnivore**/FOSS read-later) | Reading | Self-hosted read-later → Calibre/NotebookLM | Prefer FOSS; Readly is a different product (readly-mcp exists) | `promising` |
| 16 | ~~**civitai-mcp**~~ | GenAI | → **SHIPPED** [civitai-mcp](./civitai-mcp/README.md) | | shipped |
| 17 | **pubmed-mcp** | Research | Biomedical literature (vs arxiv-mcp’s CS/physics) | NCBI E-utilities; rate limits | `idea` |
| 18 | **typst-mcp** | Docs | Modern typesetting (reports, one-pagers) from agent drafts | Complements libreoffice-mcp / pandoc; Typst CLI | `promising` |
| 19 | **musescore-mcp** | Music notation | Score open/export/playback hooks | MuseScore 4 CLI/plugin surface TBD | `idea` |
| 20 | **darktable-mcp** | Photo | RAW develop / export batch for Immich pipeline | darktable CLI; Immich is gallery not RAW | `idea` |
| 21 | **firefly-iii-mcp** | Life admin | FOSS personal finance (accounts, budgets) | Self-hosted Firefly; Vienna-life adjacent | `idea` |
| 22 | **nextcloud-mcp** | Life admin | Files / Calendar / Contacts on your cloud | WebDAV + OCS APIs; don’t rebuild filesystem-mcp | `idea` |
| 23 | **sharex-mcp** | Windows capture | Trigger ShareX profiles, last capture path → OCR/Immich | Windows-only; greets screenshot→agent loops | `idea` |
| 24 | **bandcamp-mcp** | Music discovery | Artist/album search + collection (API/scrape carefully) | ToS; discovery not DJ control | `idea` |

**Shortlist if you only pick three next:** `zotero-mcp`, `searxng-mcp`, `spotify-mcp` (or `proxmox-mcp` if homelab itch is louder).

---

## Social / Comms context (already shipped)

| Repo | Protocol | Notes |
|------|----------|--------|
| mastodon-mcp | ActivityPub microblog | Full client + agent MCP |
| bluesky-mcp | AT Proto | Assfix-zero scaffold |
| discord-mcp | Discord REST | Comms lane |
| colony-mcp | Colony social | Agent social network |
| P4 [comms-mcp](../operations/planning/specs/P4-comms-mcp.md) | Telegram → Signal/WhatsApp | Messaging bridge — **not** birdsite |

---

## Shipped from this list

| Idea | Where |
|------|--------|
| **civitai-mcp** | [projects/civitai-mcp/README.md](./civitai-mcp/README.md) · ports 11124/11125 · comfyops complement |

---

## Related

- [gestating-chains/](./gestating-chains/) — multi-step pipeline ideas  
- [WRAPPEE_CANDIDATES_ANALYSIS.md](../docs-private/WRAPPEE_CANDIDATES_ANALYSIS.md) — archived 2025 wrappee dump (canonical triage = **this file**)  
- [FLEET_INDEX.md](./FLEET_INDEX.md) — what already exists  
- [NEW_REPO_BUILD_COMPLETE.md](../standards/NEW_REPO_BUILD_COMPLETE.md) — scaffold bar  
