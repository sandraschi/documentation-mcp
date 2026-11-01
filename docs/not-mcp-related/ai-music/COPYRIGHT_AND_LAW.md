# AI Music Copyright & Legal Landscape

> Last updated: 2026-03-04

The legal battle over AI music generation training data is the defining fight of 2024–2026 in the music industry. Here's what actually happened, where it stands, and what it means.

---

## The core legal question

Can an AI company train on copyrighted music without a license, claiming fair use?

The music industry says: no. Training creates unauthorized copies. The output competes with the original works. This is mass copyright infringement.

AI companies say: training is transformative, like reading a book to learn to write. No direct copying reaches users. This is fair use.

Courts have not fully resolved this. The cases are settling before final rulings — which is itself informative.

---

## The RIAA complaints (June 24, 2024)

The Recording Industry Association of America, on behalf of Universal Music Group, Sony Music Entertainment, and Warner Music Group, filed parallel lawsuits in US federal courts against **Suno** and **Udio** on the same day.

**Against Suno** (US District Court, Massachusetts — Chief Judge F. Dennis Saylor IV):
- Alleged "willful copyright infringement at an almost unimaginable scale"
- Evidence: targeted prompts (decade + topic + genre + artist descriptors) produced outputs closely resembling copyrighted recordings
- An early Suno investor had stated that "if [Suno] had deals with labels when this company got started, I probably wouldn't have invested in it"

**Against Udio / Uncharted Labs** (Southern District of New York — Judge Alvin K. Hellerstein):
- Same allegations — training on mass-scraped copyrighted recordings
- Udio at launch was reportedly generating 864,000 audio files per day
- Udio deflected by claiming training data was "competitively sensitive" and "trade secrets" despite describing it as "publicly available" music

Both companies defended on **fair use** grounds.

---

## The fair use defense — why it's weak

US copyright fair use is a four-factor test:

1. **Purpose and character of use** — commercial use, not educational/research
2. **Nature of copyrighted work** — creative works get stronger protection
3. **Amount taken** — training ingests entire recordings
4. **Market effect** — this is the killer: does it harm the market for the original?

Factors 1, 2, and 3 all favor the plaintiffs. Factor 4 is the crux.

Suno/Udio's argument: the output is different enough that it doesn't substitute for the original. The "transformative use" argument.

The plaintiffs' argument: the output directly substitutes for licensed music in the same markets — background music, sync licensing, streaming. The market harm is demonstrable and ongoing.

Legal precedent is evolving but trending against broad fair use for commercial AI training. The Thomson Reuters v. Ross Intelligence case (legal research AI) set a concerning precedent for AI companies in 2025.

---

## Settlements timeline

**October 2025 — UMG settles with Udio:**
- UMG, Sony, Warner had all sued Udio
- UMG settled first (Oct 26-29, 2025), announced at earnings
- Terms: undisclosed monetary compensation + licensing agreement for UMG's recorded music AND publishing catalogues
- Future platform: new subscription service in 2026, trained on "authorised and licensed music" with artist opt-in
- Artists who opt in will be paid for training use AND when their music is used by subscribers to create new works
- Sony and Warner cases against Udio: presumably following — nothing confirmed as of Mar 2026

**November 2025 — Warner settles with Suno:**
- Warner Music became the first major label to settle with Suno (Nov 26, 2025)
- Terms: undisclosed financial settlement + partnership for a licensed AI music platform in 2026

**As of March 2026 — still active:**
- Sony Music v. Suno: ongoing
- Universal Music v. Suno: ongoing
- Independent artist class actions v. Suno AND Udio (filed Oct 2025): ongoing — see below

---

## Independent artist class actions (October 2025)

A group of independent musicians (David Woulard, Stan Burjek, James Burjek, and others) filed parallel class action lawsuits against both Suno and Udio on October 15–16, 2025.

**Allegations:**
- Lyrics scraped from lyrics websites
- Audio obtained via YouTube stream-ripping
- Loss of licensing revenues and commissions
- Privacy and right of publicity claims (Udio specifically)
- Illinois Right of Publicity Act violations

**Class certification sought:** All independent artists with registered copyrights in sound recordings made after February 15, 1972, whose music was used for training.

**Why this matters:**
- Not the RIAA/majors — these are individual working musicians
- Thousands of potential class members
- If certified and successful, potential damages in the hundreds of millions
- Specifically alleges the "market harm" argument: AI outputs are "competitive, radio-quality substitutes" that reduce demand for human-created music

---

## International cases

**Denmark (November 2025) — Koda v. Suno:**
- Koda (Denmark's music rights organization, 52,000 members) sued Suno in Copenhagen City Court
- Called it "the biggest theft in music history"
- Evidence presented: AI-generated tracks resembling Aqua, MØ, and other Danish artists
- IFPI Denmark report: unlicensed AI music could cost Danish music industry $680M between 2025–2030, a 28% revenue loss

**Germany — GEMA v. Suno:**
- GEMA (Germany's music licensing organization) sued Suno for copyright violations
- GEMA also won a separate lawsuit against OpenAI for reproducing lyrics without permission
- German copyright law is notably stricter than US fair use doctrine

**EU context:**
- The EU AI Act (2024) requires transparency about training data for high-risk AI systems
- Whether music gen falls under the relevant provisions is being actively debated
- The EU Copyright Directive (2019) includes a text and data mining exception for research, but NOT for commercial AI products — which arguably covers Suno/Udio directly

---

## The AI music copyright output question

Separate from the training question: who owns the output?

**US Copyright Office position:** AI-generated works without meaningful human creative contribution are not copyrightable. Dr. Stephen Thaler's SCOTUS cert petition (Oct 2025) challenging this was pending as of early 2026.

**Practical implication:**
- Pure AI-generated music is in the public domain (in the US)
- You can't register copyright in a Suno output
- BUT if you substantially edit or arrange it with human creative input, that portion may be copyrightable
- The line is unclear and being litigated

**For FOSS local generation (ACE-Step etc.):**
- Same copyright status for the output applies
- However: no platform owns your output, no TOS to worry about, no data rights ceded to anyone

---

## The "stream ripping" amendment (late 2025)

The RIAA amended its lawsuits against both Suno and Udio to add accusations that they sourced training data through illegal stream-ripping from YouTube. This is a separate legal claim (DMCA § 1201 circumvention) on top of the copyright infringement claim, and potentially more straightforward to prove — it's not about fair use, it's about how the data was obtained.

This amendment gave the majors additional leverage in settlement negotiations.

---

## What the settlements actually mean

The Warner/Suno and UMG/Udio settlements establish a template:
1. **Monetary compensation** (undisclosed amounts, but presumably significant given Suno's $2.45B valuation)
2. **Licensing for the past** (retroactive coverage of the infringing training)
3. **New licensed platform** for the future (opt-in artist royalties, controlled environment)
4. **Strategic partnership** (labels get a stake in the AI music future they just fought)

This is what the industry actually wanted — not to kill AI music, but to be paid for enabling it. The litigation was leverage, not an existential goal.

---

## What the settlements do NOT solve

1. **Suno/UMG case continues** — no settlement yet; Sony also still litigating
2. **Independent artists got nothing** from the major label settlements — their class actions are separate
3. **FOSS models are completely outside this framework** — ACE-Step doesn't have US assets to sue, trained on licensed data, weights irrevocably MIT-licensed
4. **Opt-in vs opt-out** — the Udio platform's opt-in structure means the majority of catalog that doesn't opt in still isn't covered for new training
5. **Non-US jurisdiction** — GEMA, Koda, and future EU enforcement operate independently

---

## The practical forecast

**Short term (2026):**
- Sony and UMG will likely settle with Suno — the Warner precedent makes it economically rational
- New "licensed" platforms from both Suno and Udio launch, with complex opt-in royalty structures
- Independent artist class actions drag on; certification is uncertain
- GEMA and Koda cases set European precedents, possibly requiring EU-specific licensing

**Medium term (2027–2028):**
- Licensed AI music platforms coexist with FOSS alternatives
- Labels collect training royalties and per-generation micro-royalties from licensed platforms
- FOSS/local generation (ACE-Step and descendants) captures the users who won't pay per-song royalties
- Geopolitical bifurcation: US/EU "responsible AI music" ecosystem vs. Chinese FOSS models that simply don't participate

**The asymmetry that won't resolve:**
The labels can negotiate with Suno because Suno is a US company with investors, employees, and assets. They cannot negotiate with ACE-Step. The weights are already out there. No court order can un-release a MIT-licensed model distributed globally by a Chinese company.

This is the structural reality the labels haven't fully confronted yet. The lawsuit strategy worked — against US-based startups with VC backers who needed to avoid existential legal risk. It is powerless against a Chinese open-source model with clean training data.
