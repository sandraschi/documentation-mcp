# calibre-mcp — Promotion Playbook

**Repo**: `D:\Dev\repos\calibre-mcp` (also published as **calibremcp**)  
**Backend ports**: 10720 / 10721 (verify in repo before wiring)  
**Fleet standard**: [FLEET_PROMOTION.md](../../standards/FLEET_PROMOTION.md)

---

## Positioning (not rah-rah)

**One line:** Open-source MCP server for your **existing** Calibre library — search, metadata, exports, and agent workflows without replacing Calibre.

**Not:** “AI reads all your books.” **Is:** “Automate the chores around a library you already curate.”

---

## Audience segments

| Segment | Cares about | Message |
|---------|-------------|---------|
| Calibre power users | Bulk metadata, search, Content server | FTS phrase jump, RAG over your library |
| Self-hosters | Tailscale, homelab | MCP + webapp on fixed ports; no cloud upload |
| Claude/Cursor users | Tool integration | Option A `.mcpb`, documented tools |
| CalFolio / iOS readers | Companion app | Same backend (calibreops); app is frontend |
| Goodreads active readers | Lists, discovery | Bridge reading life ↔ owned library (careful tone) |

---

## Goodreads (primary niche channel)

Goodreads is **not** a dev forum — readers, lists, and reviews. Fit when the post is about **reading workflow**, not “AI product launch.”

### What works

| Tactic | Example |
|--------|---------|
| **Listopia / List** | “Tools for managing a large personal ebook library (2026)” — include Calibre + one line on MCP automation |
| **Profile / blog post** (if you use GR blog) | “How I sync highlights from X into Calibre shelves” — link GitHub at bottom |
| **Group discussion** | Only in groups that allow tool posts; search “Calibre”, “ebooks”, “self-hosted” |
| **Review cross-link** | Review a **book about productivity/PKM**; mention your Calibre setup in one paragraph — not the whole review about MCP |

### Goodreads tone

- Write as a **reader who self-hosts**, not as a startup
- Mention **Calibre first**, MCP second (“I also wired Claude Desktop for batch metadata fixes”)
- No “AI will read books for you” — emphasize **library management**
- Link to GitHub once; don’t paste install instructions in GR comments

### What to avoid on Goodreads

- Mass friend requests with promo links
- Reviewing your own “virtual book” or spam listings
- Posting identical text in 20 groups
- Arguing about AI in unrelated threads

### Goodreads checklist

- [ ] Profile has calm one-liner (optional): “Self-hosted ebook library / Calibre enthusiast”
- [ ] One Listopia list with Calibre ecosystem tools (Calibre, plugins, **optional** calibre-mcp)
- [ ] One group post drafted; read group rules first
- [ ] No post until README Preview screenshot exists (library dashboard)

---

## Wrappee: Calibre (kovidgoyal/calibre)

Calibre upstream is **large and pragmatic** — not uniformly anti-AI, but **issues are for bugs/features**, not ads.

| Channel | Recommendation |
|---------|----------------|
| **calibre-plugin forum (MobileRead)** | Better for “external automation tool” than GitHub issues |
| **GitHub Discussions** | If enabled — “Community integrations” |
| **GitHub Issues** | **Avoid** pure promotion; OK for “MCP bridge breaks on Calibre X.Y” bug report with repro |

**Template (MobileRead / forum):**

> I wrote a FastMCP server that talks to Calibre’s library DB and Content server for batch metadata search and exports. It’s MIT, not official. Works with Claude Desktop via MCP. Link: {url}. Looking for feedback from other Calibre power users — especially around metadata workflows you still do by hand.

---

## Other channels

| Channel | Notes |
|---------|-------|
| **r/calibre**, **r/selfhosted** | Single post; flair “Tool”; answer questions in comments |
| **Glama / Smithery** | Factual listing; category Productivity or Media |
| **CalFolio / Apple docs** | Cross-link in `projects/apple/CALFOLIO.md` (fleet internal) |
| **translate-mcp / speechops chain** | Hands-out: EPUB chunks → translate → TTS (document in fleet index) |

---

## Content ideas (technical, shareable)

1. “Find every book mentioning {phrase} across 10k titles in under 2s” (FTS demo)
2. “Export a reading list to CSV for book club” (screenshot of webapp)
3. “Agent fixed 200 wrong ASINs — what I asked Claude to do” (concrete prompt, no hype)
4. CalFolio + Tailscale: iPad on sofa, library on Goliath (for apple project docs)

---

## Before any public push

- [ ] README has Preview screenshot ([WEBAPP_SCREENSHOTS](../../standards/README_WEBAPP_SCREENSHOTS.md))
- [ ] INSTALL Option A tested on clean machine
- [ ] `glama.json` description matches actual tools
- [ ] Post reviewed against [FLEET_PROMOTION tone checklist](../../standards/FLEET_PROMOTION.md#tone-checklist-read-before-any-public-post)

---

## Metrics (optional)

| Signal | Where |
|--------|-------|
| Glama installs | Glama dashboard |
| GitHub stars / issues | Repo |
| Goodreads list saves | Manual check |
| CalFolio TestFlight interest | Apple project STATUS |
