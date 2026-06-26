# Anna’s Archive — MCP fit, public domain vs in-copyright, fleet stance

**Status:** Central documentation (policy + product assessment), not an MCP server spec.  
**Audience:** Fleet maintainers, future-you, and anyone asking “why isn’t there `annas-archive-mcp` in the hub?”

**Not legal advice.** This is engineering and risk communication. Laws differ by country, work, and facts—consult a qualified lawyer for decisions that matter.

---

## 1. What Anna’s Archive is (neutral description)

**Anna’s Archive** is a search-and-discovery layer over aggregated bibliographic records and file pointers to third-party hosts. It is widely described as a **“grey library”**: it mixes **public-domain** texts, **openly licensed** material, and **in-copyright** works depending on what users search for and what upstream mirrors expose.

That mixture is exactly why **automation** (especially headless download orchestration) is treated differently from **human browsing** in product-risk terms—not because browsing is “legal” and automation is “illegal” in all cases, but because **tools that scale access** attract different scrutiny (rightsholders, platforms, GitHub, ISPs).

---

## 2. Assessment: do you *need* an MCP server?

### 2.1 Browser UX is already strong

For many workflows, **the website is enough**: search, filters, format choice, and manual download are straightforward. An MCP layer adds:

- **Maintenance** (HTML/DOM changes, anti-bot behavior, ToS friction).
- **Liability optics** (“this repo automates access to grey aggregators”).
- **Little unique value** unless you truly need **unattended** or **scripted** pipelines (e.g. batch acquisition on a headless box—which is also where risk concentrates).

**Conclusion:** A first-party **fleet** MCP server for Anna’s Archive is **not compelling on UX grounds alone**. Natural-language convenience (“get me X from Anna’s”) is real, but it can often be satisfied with **browser + bookmarks + PD-first APIs** (below) without shipping scraper logic in a public repo.

### 2.2 Where MCP *would* help (hypothetically)

Legitimate *technical* reasons people want MCP anyway:

- **Headless / agentic** workflows (no GUI).
- **Unified tool surface** next to Calibre, OCR, Plex, etc.
- **Structured metadata** returned to the agent (title, format, mirror hints)—still sensitive if it drives mass download of in-copyright material.

Those are valid *engineering* desires; they don’t automatically justify **hosting** the integration on **US platform GitHub** under a **public** fleet banner without a clear legal and maintenance strategy.

---

## 3. The “prompt fantasy” — two very different asks

Agents are good at turning vague intent into actions. Two examples clarify why **one MCP** cannot be “neutral” for both:

| Intent (example) | What’s going on | PD-first alternative (no Anna’s required) |
|------------------|-----------------|-------------------------------------------|
| **“Latest book by Randall Munroe from Anna’s”** (often misspelled *Russell Munroe*) | **In-copyright** popular science / humor books (*What If?, Thing Explainer*, etc.) in typical editions | Buy or borrow (library); use publisher or retailer metadata. **Do not** assume “easy in browser” ⇒ “safe to automate at scale.” |
| **“Baroness Orczy book from Anna’s”** | **Emma Orczy** (*The Scarlet Pimpernel*, etc.): many editions are **public domain** in several jurisdictions (term-dependent; verify for **your** edition and country) | **[Project Gutenberg](https://www.gutenberg.org/)**, **[Standard Ebooks](https://standardebooks.org/)**, **[Internet Archive](https://archive.org/)**, **[Open Library](https://openlibrary.org/)** (API-friendly patterns), **national libraries**—these are **better MCP targets** for PD text acquisition than a grey aggregator. |

**Key point:** For **public-domain** literature, you usually want **`gutenberg-mcp`**, **`openlibrary` HTTP tools**, or a **Calibre + OPDS** path—not Anna’s Archive. Anna’s may *list* PD works, but it is not the cleanest **rights-aligned** source for automation.

For **in-copyright** works, an MCP that **automates** locate-and-fetch from a grey aggregator is **high facilitation risk** for a public repo, regardless of personal views on enforcement where you live.

---

## 4. Fleet / MCP Central Docs stance (what we ship vs what we document)

### 4.1 Default posture

- **MCP Central Docs** and the **fleet utilities** (e.g. **glance-mcp**) **do not** ship **scrapers** or **download automation** targeted at Anna’s Archive.
- Rationale is **threefold**:
  1. **Product:** Browser UX is adequate for manual use; PD workflows have better primary sources.
  2. **Maintenance:** Aggregator sites change; scrapers rot.
  3. **Platform / legal optics:** **GitHub** is **US-operated**; repos are subject to **DMCA**, **ToS**, and complaints **even when contributors are outside the US**. See also **glance-mcp** [`docs/POLICY_NO_SCRAPE.md`](../../glance-mcp/docs/POLICY_NO_SCRAPE.md) (path assumes sibling clone `glance-mcp`; same content idea: [fleet policy](https://github.com/sandraschi/glance-mcp/blob/main/docs/POLICY_NO_SCRAPE.md) when published).

### 4.2 This is not a moral claim about Austria—or anywhere else

Low **public criminal** priority in a given country **≠** safe for every **civil** claim, **rightsholder** letter, or **platform** action. **EU copyright** framework still applies in Austria; exceptions are **narrow and fact-specific**. Conversely, **public-domain** use is **not** “automatically fine” if the **edition** (translation, typography, cover art) has **new rights**.

We document this so **you** can separate **“what I do in a browser”** from **“what I glue into a reproducible MCP repo on GitHub.”**

---

## 5. Hypothetical `annasarchive-mcp` with an “out of copyright” filter

Some designs try to **assuage conscience and risk** by restricting tools to **“legal” / public-domain** material only (e.g. filter by publication year, match against known PD corpora, or refuse downloads unless a record passes heuristics). That is **not crazy as engineering intent**, but it is **not a complete legal shield**.

### 5.1 What a PD filter can improve

- **Intent signal:** The project can honestly say it **does not aim** to automate access to obviously modern in-copyright bestsellers.
- **User friction:** Extra checks may reduce casual misuse (not provably, but product-wise).
- **Documentation hook:** Forces you to document **what “PD” means** in your filter (jurisdiction, edition, translation).

### 5.2 What a PD filter does *not* fix

| Pitfall | Why “PD-only” still trips |
|--------|----------------------------|
| **Bad or sparse metadata** | Aggregators inherit messy records. A year field or “Gutenberg-ish” title match can be **wrong**. False positives and false negatives both hurt trust. |
| **Territorial public domain** | A work **PD in the US** (pre-1928 rule-of-thumb era) may **not** be PD everywhere **life + 70** applies to a different author/date. A global MCP implies **extra care** in labeling. |
| **Translation / adaptation** | The **underlying** classical text (e.g. **Ovid** in Latin) may be ancient and free of **copyright in the text itself**—but a **modern translation**, **critical apparatus**, **introduction**, and **compilation** can each attract **new copyright**. A bundle marketed as “Ovid’s collected works” is often a **new edition**, not a raw PD file. |
| **Neighboring rights / packaging** | **Cover art**, **typography**, **footnotes**, **e-book encoding** as a **database** or **compilation**—fact-specific. |
| **Site ToS and technical policy** | Even for PD content, **automated bulk access** may still violate **terms** or trigger **blocking**—orthogonal to copyright. |

So: a **“PD filter”** is a **risk reducer for narrative and diligence**, not a **theorem** that every returned file is lawful for every user in every use case.

### 5.3 Ovid (example you raised)

**Publius Ovidius Naso** died ~17 CE; the **Latin** text is not under modern copyright. But **“get Ovid’s collected works”** from *any* aggregator usually resolves to a **specific file**: often a **translated** or **annotated** modern volume. That translation or editorial layer can be **in copyright** until its own term expires. The MCP cannot wave that away with a single **year < 1928** rule without **edition-level** provenance.

**Practical implication:** For classical corpora, **Project Gutenberg**, **Perseus**, **Open Library**, or **library-linked** PD scans are usually **more auditable** than a grey aggregator’s blob—*even if* you slap a PD filter on the latter.

### 5.4 Fleet posture (unchanged, but nuanced)

An **`annasarchive-mcp` + PD filter** could exist as **third-party or private** tooling with **explicit** “metadata may be wrong; verify edition” disclaimers. **MCP Central Docs** still **prefers PD acquisition via PD-native sources** (§6) for **maintainability and clarity**. If someone ships PD-filtered Anna’s automation publicly, the **maintenance and ToS** story remains non-trivial.

### 5.5 Preferred alternative: **`getbooks-mcp`** (planned)

Instead of wiring agents to a **grey aggregator**, the fleet design direction is **[getbooks-mcp](../projects/getbooks-mcp/README.md)** — one MCP that federates **Gutenberg**, **Open Library**, **Internet Archive** (metadata-first), **Standard Ebooks** (where official feeds/APIs allow), and similar **documented** channels. Same ergonomic goal (“get me this book”), **different** risk profile: **APIs + PD-native corpora**, **no Anna’s in core**, explicit **`rights_note`** on each hit.

---

## 6. If you still want agentic “get a book” workflows

Prefer this order:

1. **Public domain / open license:** **Open Library API**, **Gutenberg**, **Standard Ebooks**, **Internet Archive**—expose **identifiers** (ISBN, OLID, Gutenberg id) in tool responses so the **human** can verify rights.
2. **Library lending / retail:** Deep link to **library OPAC** or retailer; MCP returns **metadata + URL**, not a scraped file.
3. **Private / local tooling:** A **personal** script or **private** fork (not in the public fleet) where **you** accept operational and legal responsibility—**do not** present it as a maintained fleet standard.

---

## 7. LLM “guardrails” vs repository policy (short)

Some cloud models refuse or hedge on **copyright-adjacent** automation. That behavior is **vendor policy + training**, not a substitute for **your** repo policy.

- **Local inference** (Ollama, etc.) changes **who moderates the API call**, not **whether** your GitHub repo is a good place to host **high-risk automation**.
- **Chinese vs Western models** is not a reliable axis for “will help me scrape”—alignment varies by **model card**, not flag.

**Engineering stance:** Write **clear docs** (this file, `POLICY_NO_SCRAPE.md`) and use **rights-respecting** sources for **MCP**; keep **grey-aggregator** access **manual** or **out of public fleet** unless you have **explicit legal clearance**.

---

## 8. Related documents

| Document | Role |
|----------|------|
| glance-mcp [`docs/POLICY_NO_SCRAPE.md`](../../glance-mcp/docs/POLICY_NO_SCRAPE.md) (same on GitHub: [sandraschi/glance-mcp](https://github.com/sandraschi/glance-mcp/blob/main/docs/POLICY_NO_SCRAPE.md)) | Short fleet policy: TV Tropes + Anna’s Archive not shipped; legal disclaimer skeleton |
| [integrations/README.md](README.md) | Integration catalog index |
| [projects/xkcd-mcp/README.md](../projects/xkcd-mcp/README.md) | **xkcd** via **official JSON API**—example of “only sanctioned API” integration |

---

## 9. Changelog (central doc)

| Date | Note |
|------|------|
| 2026-03-20 | Initial write: MCP fit, PD vs in-copyright, fleet stance, alternatives. |
| 2026-03-20 | §5: Hypothetical PD-only filter; translator/edition limits; Ovid example. |
