# MCP Servers Plan: High-Info Free Resources & FOSS Wrappers

**Focus:** Free resources, high information density, popular FOSS apps, community hubs. Obscure/niche welcome where interesting.

---

## Fleet requirements (MANDATORY)

**Every server in this plan MUST extend the fleet** and meet the following. No exceptions.

1. **Fleet integration**
   - Repo under the same org/root as existing MCP fleet; follows [STANDARDS.md](../STANDARDS.md) and [operations/WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md).
   - On release: add to [FLEET_INDEX.md](FLEET_INDEX.md), [integrations/README.md](../integrations/README.md) (or equivalent), and [operations/fleet-registry.json](../operations/fleet-registry.json) / [operations/webapp-registry.json](../operations/webapp-registry.json) as applicable.

2. **Proper webapp (required)**
   - Each server MUST ship a SOTA webapp: React + Tailwind, dark theme, retractable sidebar (localStorage), layout consistent with calibre-mcp / discord-mcp style.
   - Pages for all major tools/capabilities; no “API-only” servers without a dashboard.
   - Start via `start.ps1` (and `start.bat` where relevant); kill-port or equivalent before bind; no Linux-only scripts in repo.

3. **Ports**
   - Backend and frontend MUST use an **allocated adjacent pair** from the fleet range (10700–10800+ per WEBAPP_PORTS.md).
   - Reserve below before implementation; on first run, add the pair to WEBAPP_PORTS.md and webapp-registry.json.

4. **Robofang integration (required)**
   - Every server MUST integrate with **Robofang** (fleet supervisor). Register the server in Robofang’s config/registry so it is discoverable, startable, and monitorable from the Robofang dashboard.
   - No server is considered “shipped” until it is present in the Robofang fleet and can be launched and supervised from Robofang.

**Reserved ports (planned)** — use these when implementing; add to WEBAPP_PORTS.md and registry when the server ships.

| Server | Backend | Frontend |
|--------|---------|----------|
| wikipedia-mcp | 10758 | 10759 |
| hacker-news-mcp | 10760 | 10761 |
| wordpress-mcp | 10768 | 10769 |
| rss-mcp | 10770 | 10771 |
| internet-archive-mcp | 10774 | 10775 |
| tvtropes-mcp | 10964 | 10965 |
| annas-archive-mcp | 10778 | 10779 |
| stack-exchange-mcp | 10780 | 10781 |
| arxiv-mcp | 10783 | 10784 |
| semantic-scholar-mcp | 10785 | 10786 |
| lobsters-mcp | 10787 | 10788 |
| reddit-mcp | 10790 | 10791 |
| ghost-mcp | 10793 | 10794 |
| bookstack-mcp | 10795 | 10796 |
| gitea-forgejo-mcp | 10797 | 10798 |
| musicbrainz-mcp | 10800 | 10801 |
| open-library-mcp | 10802 | 10803 |
| podcast-index-mcp | 10804 | 10805 |
| pinboard-mcp | 10806 | 10807 |
| wikidata-mcp | 10808 | 10809 |
| zotero-mcp | 10810 | 10811 |
| obsidian-mcp | 10812 | 10813 |
| joplin-mcp | 10814 | 10815 |

*(Letterboxd, Goodreads, KeePass: reserve on implementation; same rules apply.)*

**Note:** Confirm each pair is still free in [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md) at implementation time (gaps may be reused). When the server ships, add the pair to that doc and to [webapp-registry.json](../operations/webapp-registry.json).

---

## 1. Reference & Knowledge (high info density, free)

| Server | Source / API | Why | Tools (conceptual) |
|--------|--------------|-----|--------------------|
| **Wikipedia MCP** | MediaWiki API (free, no key) | Dense, cross-linked, multi-language. Perfect for fact-check, definitions, "get me a summary of X". | search, get_page, get_summary, get_links, get_categories, random_article, lang variants |
| **TVTropes MCP** | Scraping or community API if any | Narrative/story patterns, character archetypes, "like X but Y". Huge for writers and critics. | search_tropes, get_trope, get_work, trope_relations, examples |
| **Anna's Archive MCP** | Public search/index (respect robots, rate limit) | Metadata/search over books and papers. Discovery only; no distribution. High sensitivity: legal/ToS. | search_books, search_papers, get_metadata, format_list (no download tools) |
| **Wikidata / DBpedia MCP** | SPARQL endpoints (free) | Structured knowledge graph: entities, relations, facts. Complements Wikipedia with queryable triples. | sparql_query, get_entity, get_entities_by_label, suggest_entity |

**Implementation notes:** Wikipedia and Wikidata have official APIs; TVTropes may need careful scraping + cache; Anna's Archive needs a strict "metadata-only, no piracy" policy and possibly proxy/rate limits.

---

## 2. Community & News (free, high signal)

| Server | Source / API | Why | Tools (conceptual) |
|--------|--------------|-----|--------------------|
| **Hacker News MCP** | Official Firebase/API (free) | Simon Willison, indie dev, FOSS culture. Front page, user threads, comments, search (Algolia). | get_front_page, get_item, get_user, get_thread, search_hn, best Show HN |
| **Lobsters MCP** | Lobste.rs (RSS/JSON, open) | Tech link aggregator, invite-only but API open. Less noise than HN for some topics. | get_hot, get_recent, get_tag, get_story, get_comments |
| **Reddit MCP** (read-only) | Reddit JSON API (no key for read) | Subreddits as interest clusters. Top/popular, search, thread + comments. Rate limits. | get_subreddit, get_post, get_comments, search_reddit, get_user_posts |
| **RSS/Atom MCP** | Any public feed URL | Universal: blogs, news, GitHub releases, YouTube. One server, many sources. | add_feed, list_feeds, get_items, search_items, export_opml |

**Implementation notes:** HN has simple REST-like APIs; Lobsters has a public JSON API; Reddit read-only is well documented; RSS is trivial with feedparser.

---

## 3. Content & Publishing (FOSS apps to wrap)

| Server | App / API | Why | Tools (conceptual) |
|--------|-----------|-----|--------------------|
| **WordPress MCP** | WP REST API (self-hosted or .com with token) | Huge CMS. Draft posts, media, taxonomies, site structure. Good for "blog from AI" and site introspection. | get_posts, create_post, update_post, get_media, get_categories, get_pages, search |
| **Ghost MCP** | Ghost Admin API | Modern blogging, newsletters. Clean API. | get_posts, create_post, get_pages, get_tags, get_members (if applicable) |
| **BookStack MCP** | BookStack API | Wiki-style books/shelves/pages. FOSS, self-hosted. Great for internal docs. | list_books, get_page, create_page, search, export |
| **Gitea / Forgejo MCP** | Git hosting API | Lightweight GitHub alternative. Repos, issues, PRs, releases. FOSS. | list_repos, get_repo, get_issues, create_issue, get_releases, search_code |

---

## 4. Media & Archives (free / FOSS)

| Server | Source / API | Why | Tools (conceptual) |
|--------|--------------|-----|--------------------|
| **Internet Archive MCP** | archive.org APIs | Wayback, books, media. Legal, free, massive. | wayback_snapshot, wayback_available, search_archive, get_metadata, get_item_files |
| **MusicBrainz MCP** | MusicBrainz XML/JSON (free) | Authoritative music metadata: artists, releases, recordings. No audio. | search_artist, search_release, get_recording, get_relations |
| **Open Library MCP** | Open Library API | Books metadata, covers, "read" links (legal). | search_books, get_work, get_edition, get_author |
| **Podcast Index MCP** | Podcast Index (free API key) | Open podcast search and metadata. Alternative to proprietary directories. | search_podcasts, get_episodes, get_episode_by_id, trending |

---

## 5. Niche & Curated (obscure but high value)

| Server | Source / API | Why | Tools (conceptual) |
|--------|--------------|-----|--------------------|
| **Pinboard MCP** | Pinboard API (paid but cheap) | "Anti-social bookmarking." Dense, tag-based, power-user. | get_recent, get_all, search, get_notes, suggest_tags |
| **Letterboxd MCP** (read) | Scraping or unofficial (ToS care) | Film lists, reviews, "films like X." Strong for recommendations. | search_film, get_film, get_lists, get_reviews (if feasible) |
| **Goodreads MCP** (read) | Unofficial / scraping | Book reviews, shelves, "books like X." Same caution as above. | search_books, get_book, get_reviews, get_author |
| **Stack Exchange MCP** | SE API (free, quota) | Q&A across sites (SO, Super User, etc.). High signal for technical answers. | search_questions, get_question, get_answers, get_user, top_questions |
| **arXiv MCP** | arXiv API (free) | Preprints: CS, physics, math. Citations, abstracts, categories. | search, get_paper, get_citations, list_categories |
| **Semantic Scholar MCP** | Semantic Scholar API (free) | Paper metadata, citations, TL;DRs. Good for "summarize this paper" flows. | search_papers, get_paper, get_citations, get_authors |

---

## 6. Local / Desktop FOSS (wrap existing apps)

| Server | App | Why | Tools (conceptual) |
|--------|-----|-----|--------------------|
| **Zotero MCP** | Zotero (local DB + API) | Reference manager. Sync with Zotero desktop/web. | get_collections, get_items, search, add_item, get_attachment_list |
| **Obsidian MCP** (enhanced) | Obsidian vault (files + plugins) | Many exist; align with fleet: graph, backlinks, search, create note from AI. | read_note, write_note, search_vault, get_backlinks, get_graph |
| **Joplin MCP** | Joplin (API or local DB) | E2EE notes, markdown. FOSS. | list_notes, get_note, create_note, search, get_notebooks |
| **KeePass / KeePassXC MCP** | CLI or DB (read-only focus) | Password/secret store. Read-only "lookup entry" safer than write. | list_groups, get_entry (masked), search_entries (titles only) |

---

## Priority Order (suggested)

1. **Wikipedia MCP** — Zero cost, instant value, well-defined API.
2. **Hacker News MCP** — Small API surface, high relevance to dev/AI crowd.
3. **WordPress MCP** — Huge install base, REST API standard.
4. **RSS/Atom MCP** — One server, infinite feeds; universal.
5. **Internet Archive MCP** — Unique resource, clear APIs.
6. **TVTropes MCP** — Differentiator; scraping/cache strategy needed.
7. **Anna's Archive MCP** — Metadata-only, strict policy; high value for researchers.
8. **Stack Exchange / arXiv / Semantic Scholar** — Deep-dive knowledge.
9. **BookStack, Gitea/Forgejo, Ghost** — Self-hosted ecosystem.
10. **Pinboard, Podcast Index, MusicBrainz, Open Library** — Niche but dense.

---

## Cross-Cutting

- **Robofang:** All servers must be registered in Robofang and startable/monitorable from the Robofang dashboard.
- **RAG:** Where it fits (Wikipedia, HN, SE, arXiv), add optional LanceDB ingest so "search my ingested X" is consistent with discord-mcp RAG pattern.
- **Ports:** Allocate from fleet range (e.g. 10700–10800) per WEBAPP_PORTS.md.
- **SOTA:** FastMCP 3.1, portmanteau tools, required webapp (React + Tailwind), no emojis in logs/code.
- **Legal/ToS:** Scraping-only servers (TVTropes, Letterboxd, Goodreads) need robots.txt and rate limits; Anna's Archive must be metadata-only and compliant with local law.

---

*Document: plan only. Implementation per repo; update FLEET_INDEX and integrations when servers ship.*
