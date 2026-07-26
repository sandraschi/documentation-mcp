# getbooks-mcp (planned)

**Concept:** One MCP that discovers and retrieves **books from multiple rights-respecting sources** — **not** a scraper for grey aggregators.

> Prefer this direction over **`annasarchive-mcp`**: same “agent, get me a book” ergonomics, **lower** copyright/platform ambiguity when sources are **APIs and official PD corpora**.

---

## Summary

| Item | Details |
|------|---------|
| **Repo** | *Not created yet* — central design lives here until scaffolded under `D:\Dev\repos\getbooks-mcp`. |
| **Stance** | **Safe-by-design:** only sources with **clear APIs or documented PD distribution** (see below). **No Anna’s Archive** in core. |
| **Related** | [Anna’s Archive — MCP stance](../../integrations/annas-archive-mcp-stance.md) · [glance-mcp POLICY](https://github.com/sandraschi/glance-mcp/blob/main/docs/POLICY_NO_SCRAPE.md) |

### Fleet priority (parallel / contrast)

| MCP class | Cadence | Rationale |
|-----------|---------|-----------|
| **arxiv-mcp** (or equivalent preprint bridge) | **Daily** | New **multi-agent**, RL, systems papers land constantly; staying current is a **recurring** workflow — high ROI for automation. |
| **getbooks-mcp** | **Occasional** | “**Newest Paul Halter**” (or any living author’s latest) is **not** a daily fleet need; browser + retailer / library is fine. PD discovery (“Orczy”, Gutenberg) is also **sporadic**. |

So **getbooks** stays **planned / low urgency** until book lookup from agents becomes painful **often** — not because it’s a bad idea, but because **throughput and freshness demands** are lower than **arXiv-style** tooling.

---

## Why multiple sources

- **Single corpus** (Gutenberg-only, etc.) misses **Standard Ebooks** quality, **Open Library** metadata, **Internet Archive** lending/scans.
- **Routing** by query: “Orczy” → PG/SE; “ISBN lookup” → Open Library; “public scan” → IA (where license allows).
- **No one site** is authoritative for every “safe” book; **provenance** in the tool response matters more than brand.

---

## Candidate “SAFE” sources (v1 design space)

| Source | Role | Access pattern | Notes |
|--------|------|----------------|--------|
| **Project Gutenberg** | PD text / epub | **Catalog API** (search, metadata), direct `gutenberg.org` files | US-PD focus; [not universal](https://www.gutenberg.org/policy/license.html) — document “US PD” in responses. |
| **Standard Ebooks** | Curated PD EPUBs | **OPDS / RSS / site** (check current [terms](https://standardebooks.org/) & robots) | Prefer **official API/feed** if documented; avoid raw HTML scraping if unstable. |
| **Open Library** | Metadata, editions, borrow links | **Open Library API** (`openlibrary.org`) | Returns **links** and **IDs**; borrowing may be **controlled digital lending** — surface as **user action**, not silent download. |
| **Internet Archive** | Scans, audio | **IA API** (metadata + file identifiers) | Many items **PD** or **CC**; **not all** — filter by license metadata when available. |
| **National / library OPDS** | Regional PD (e.g. **Europeana** APIs) | **Registered APIs** only | **Territorial** PD; **never** claim “global safe.” |

**Non-goals (core):** Anna’s Archive, LibGen mirrors, random file-host search — **out of scope** for the default tool surface; keeps **GitHub + fleet** story clean.

---

## Suggested tools (portmanteau sketch)

- **`getbooks_search(query, sources?, limit?)`** — federated search; returns **normalized rows**: `title`, `authors`, `source`, `source_id`, `url`, `rights_note` (e.g. `US_PD`, `CC_BY`, `borrow_ia`).
- **`getbooks_resolve(source, source_id)`** — metadata + **best download or read URL** (no bypass of paywalls).
- **`getbooks_explain`** — short **static** help: Gutenberg ≠ EU everywhere; translations; **not legal advice**.

Implementation detail: **httpx** + **rate limits** + **cache**; **no** headless browser in v1.

---

## Risks to document in-repo

- **“Gutenberg = safe everywhere”** — **No**; see [annas-archive-mcp-stance §5–6](../../integrations/annas-archive-mcp-stance.md) and central FAQ.
- **Translator / edition** — Same as classical corpus discussion (Ovid, etc.): **edition-level** provenance when possible.
- **ToS** — Each API has **terms**; respect **robots** and **bulk** limits.

---

## Next steps

1. Reserve **ports** in [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) when a repo exists (suggest **10780** / **10781** per adjacency rule — not allocated until confirmed).
2. Scaffold **FastMCP 3.1** repo + `Webapp` + `glama.json` + tests.
3. Ship **search** only for **Gutenberg + Open Library** first (best API docs); add **IA** and **Standard Ebooks** feeds second.

---

**Last updated:** 2026-03-20
