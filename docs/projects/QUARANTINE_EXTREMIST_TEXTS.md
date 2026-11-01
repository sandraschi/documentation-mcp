# Quarantine extremist / pathology texts (Calibre Bullshit shelf)

**Status:** Fleet ingestion policy (MCD)  
**Shelf:** `Calibre-Bibliothek Bullshit` (+ optional Private) — see [CALIBRE_OWNER_ESTATE.md](./CALIBRE_OWNER_ESTATE.md)  
**Never:** `-phile` Knowledge HTML, `.mcpb`, public Glama, or agent recommendations unless Sandra explicitly asks.

---

## Purpose

Primary sources for **anthropology of bad ideas** — next to Pirie/Gardner on the **main** shelf as antidote. Same rack as Kaczynski: study rhetoric, not recruit.

---

## Already on Bullshit (Calibre-verified)

| Work | Author | Notes |
|------|--------|--------|
| *Industrial Society and Its Future* | Theodore Kaczynski | Unabomber manifesto (duplicate entries possible) |
| *Anti AI Rebellion Protest Against Artificial Intelligence* | unknown | **Not** Moreno-Gama; generic compilation |
| Flat-earth, denialist, Schreber orbit | various | See CALIBRE_OWNER_ESTATE |

---

## Daniel Moreno-Gama — *Your Last Warning* (three-part doc, 2026)

**Name:** **Daniel Moreno-Gama** (not García Moreno).  
**Event:** April 2026 attacks / Molotov; federal complaint ([DOJ PDF](https://www.justice.gov/opa/media/1435876/dl), [DocumentCloud](https://www.documentcloud.org/documents/28039895-moreno-gama-criminal-complaint/)).

| Part | Title | Ingest? |
|------|--------|---------|
| **1** | *Your Last Warning* — violence advocacy, **CEO/investor names and addresses** | **NO** — incitement + doxing; keep **only** quoted sentences in a private research note if needed for fallacy study |
| **2** | *Some more words on the matter of our impending extinction* — AI existential risk rhetoric | **YES** — redacted edition (no address blocks) |
| **3** | Letter *To [CEO] if you make it* (divine redemption clause) | **YES** — without any appendix listing people/places |

**Why Anna’s Archive / web fail:** Not a published book; full text is evidence; hosts won’t mirror doxing; social takedowns. Pre-attack: email to former college (Apr 10, 2026); post-attack: ~23-page mail to press (reporting). **No clean full-text edition** yet — build Calibre EPUB from complaint excerpts + verified journalism until/unless a **redacted** court filing or academic edition appears.

**Ingest workflow (when sources assembled):**

1. Author EPUB/PDF: `Moreno-Gama - Impending Extinction (part 2 only).epub` and `Moreno-Gama - Letter if you make it (part 3 redacted).epub`  
2. Calibre → **Bullshit** library, tags `quarantine`, `anti-ai`, `primary-source`, `no-export`  
3. Optional: sidecar `README.txt` citing DOJ + date retrieved  
4. **calibre-mcp:** library switch to Bullshit for local search only; exclude from RAG ingest to fleet bundles  

**Ingested 2026-09-14 (Bullshit library, agent pipeline):**

| Calibre id | Title | Author | Notes |
|------------|--------|--------|--------|
| 475 | *Parts 2 and 3 (Court Record Edition)* | Daniel Moreno-Gama | Compiled from FBI affidavit + press; part 1 omitted |
| 476 | *USA v. Moreno-Gama - Affidavit (manifesto description)* | United States District Court | Full DOJ complaint PDF as EPUB |
| 477 | *A True Follower of This Activist Christian Ministry* | Jim Jones | [Jonestown PDF](http://jonestown.sdsu.edu/wp-content/uploads/2013/10/02-05-TrueActivist.pdf) |
| 478 | *The Letter Killeth* | Jim Jones | [Jonestown PDF](http://jonestown.sdsu.edu/wp-content/uploads/2013/10/02-LetterKilleth.pdf) |

Scratch build dir (local): `mcp-central-docs/_scratch_quarantine_ingest/` (not committed).

**Analytical link:** [LOGIC_AND_FALLACIES.md](./sinophile-mcp/LOGIC_AND_FALLACIES.md) (appeal to controversy; distinct from Part 1 criminal incitement).

---

## Jim Jones — known texts (Reverend James W. Jones)

**Yes — large archived corpus**, mostly **not** one single “manifesto” but pamphlets, flyers, and **thousands of tape transcripts**.

**Canonical free archive:** [Alternative Considerations of Jonestown and Peoples Temple](https://jonestown.sdsu.edu/) (SDSU Jonestown Institute).

| Text | Notes |
|------|--------|
| **The Letter Killeth** | ~24 pp.; Bible attack + Temple justification; Jones used material heavily (co-written ~1968; Jones-adjacent) — [text on site](https://jonestown.sdsu.edu/?page_id=14111) |
| **The Open Door** | Early 1956 Peoples Temple newsletter / radio pitch — [text](https://jonestown.sdsu.edu/?page_id=18588) |
| **Jim Jones Meets Father Divine** | Booklet on Peace Mission / Father Divine — [text](https://jonestown.sdsu.edu/?page_id=16635) |
| **A True Follower of This Activist Christian Ministry** | One-page flyer / personal “principle” list — [page](https://jonestown.sdsu.edu/?page_id=14104) |
| **Peoples Temple pamphlet (1976)** | PDF at [University of the Pacific](https://scholarlycommons.pacific.edu/mayor-moscone/3) (Moscone collection) |
| **Sermon / Q-tape transcripts** | Searchable by Q number (e.g. Q042, Q273…) — FBI RYMUR + institute transcriptions |
| **“Death tape” / final night** | Audio + transcript of Nov 18, 1978 Jonestown address (often misquoted online; use institute/FBI-sourced transcript) |

**Ingest suggestion:** Download institute PDFs / build EPUB bundle `Jones - Selected pamphlets (Jonestown archive).epub` on Bullshit next to Kaczynski — **historical cult primary sources**, not endorsement. Jones corpus is **easier to obtain legally** than Moreno-Gama’s full doc.

---

## Agent rules (hard)

- Do **not** fetch or recommend Part 1 Moreno-Gama hit lists.  
- Do **not** add quarantine texts to sinophile/austrophile/japanophile Knowledge.  
- Jim Jones / Kaczynski / Moreno-Gama (parts 2–3 only): Sandra’s **field trip** shelf — cite Pirie when analyzing rhetoric.

---

## Related

- [CALIBRE_OWNER_ESTATE.md](./CALIBRE_OWNER_ESTATE.md)  
- [sinophile-mcp LOGIC_AND_FALLACIES.md](./sinophile-mcp/LOGIC_AND_FALLACIES.md)
