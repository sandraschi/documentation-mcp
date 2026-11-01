# 15 - Trajectories: How the ArtCraft Story Ends (or Does Not)

Date: 2026-10-11. Companion to 07 (strategy/timing), 10 (InterPositive), 11
(contributor funnel), 13 (business model), 14 (legal). Probabilities are
subjective 12-month odds, opinion, NOT exclusive (a VC round can precede an
acquisition). Re-score monthly in HANDOVER.

## 0. Ground truth at time of writing (GitHub API, 2026-10-11 10:11 UTC)

- Org storytold: 56 repos, **114,580 stars total**, 33,089 forks. Not 300k
  (that figure circulated in chat and does not check out on GitHub; may be a
  cross-platform or forecast number - treat as unverified).
- photocraft 44,167 (was 25,798 on 2026-10-08: +18.4k in 3 days), artcraft
  15,570, lightcraft 9,427, filmcraft 9,139, pdfcraft 8,519, vectorcraft 6,519,
  effectcraft 4,795, wordcraft 3,760, designcraft 2,720, cadcraft 2,098,
  gridcraft 2,094, deckcraft 1,583, soundcraft 1,462, craft-launcher 739.
- Core artcraft relicensed Fair Source -> MIT OR Apache-2.0 on 2026-10-10
  (PR #2043). `artcraft-services` (hosted backend) is NOASSERTION.
- No Adobe legal action reported (see 14 section 0).

## 1. The reaction spectrum and what each camp predicts

| Camp | Who | What they say | What it predicts |
|---|---|---|---|
| Inchoate hatred | Adobe staff and partners, anti-AI artists, people whose skills are the moat being drained | "theft", "slop", "manic founder", astroturf accusations | Pressure on the person, not the code (see 11: ad hominem arrives when PRs are unattackable). Risk: burnout, platform reports, harassment |
| Jubilation | Subscription refugees, FOSS crowd, Global South users priced out | "the wicked witch is dying", cancellation-fee stories | Stars, installs, contributors. Fickle: week-2 retention depends on installers that actually work |
| Skepticism | Devs who assume reimplementation = reading source | "impossible without decompiling", "fake clean room", "toy" | Half right: the clean-room label is legally imperfect (14 section 6), but the method is real. They misread CUA behavior harvesting + differential testing as hype |

Note the overlap problem: a meaningful share of the jubilant Adobe-haters are
also anti-AI. ArtCraft's revenue product is AI. The free offline Crafts keep
them; the credits page may lose them.

## 2. What is actually acquirable

Since 2026-10-10 the code is permissive. Anyone can fork all 56 repos today.
An acquirer cannot buy exclusivity over the apps. What it can buy:

1. **People and the method**: Brandon Thomas plus whoever runs the
   CUA-reversal pipeline. "Trillions of tokens" of operational know-how on
   turning closed desktop software into open native code is the scarce asset.
2. **Brand**: ArtCraft name + logos (reserved by NOTICE), the Craft family
   naming, 114k-star distribution, the Discord.
3. **Hosted services**: `artcraft-services`, auth, billing, credit ledger,
   paying customers, provider contracts.
4. **Narrative**: "built with Opus 5.5" / "software is over" is marketing worth
   real money to an AI lab.
5. **Not** the code, and not the community (it can fork away).

### Comparable deals (verified)

| Deal | When | Price | Shape | Relevance |
|---|---|---|---|---|
| Netflix - InterPositive (Affleck) | 2026-03 | ~$587M cash | 16-person AI film-tech team, founder becomes senior adviser | AI creative-pipeline price anchor (file 10) |
| Canva - Serif/Affinity | 2024-03 | ~$380M reported (unconfirmed) | Bought pro desktop suite; 2025-10-30 made Affinity "free forever", Canva AI paywalled | **Closest business-model twin**: free pro apps, paid AI layer |
| Anthropic - Bun | 2025-12-02/03 | undisclosed | Bought MIT runtime used by Claude Code, stayed MIT, team intact | AI lab buys FOSS infra and keeps it open |
| OpenAI - Steinberger (OpenClaw) | 2026-02 | undisclosed (hire) | Founder joins lab, project moves to foundation, stays open | The person-not-company path |
| Google - Windsurf | 2025-07 | ~$2.4B license fee | Non-exclusive tech license + founders to DeepMind, company left as shell | Reverse-acquihire, avoids merger review |
| Microsoft - Inflection | 2024-03 | ~$650M | Same reverse-acquihire shape | Same |
| Adobe - Figma | 2022-09 to 2023-12 | $20B, abandoned | Killed by UK CMA / EC scrutiny | Adobe's antitrust scar tissue |

## 3. Trajectories

### A. Destroyed by Adobe (12-month odds: 5 to 10 percent)

What "destroyed" can even mean when the code is MIT with 33k forks: not the
code, only the person and the company. Paths: patent letters that make the
credits business uninsurable; a trade-dress injunction against specific
apps' chrome; a grinding suit whose cost exceeds the credits revenue; personal
burnout under coordinated hostility.

Why unlikely: Adobe gains little (forks survive any judgment), loses a lot of
PR (FTC cancellation-fee settlement 2026, Figma failure), and has weak
copyright claims (14). More likely Adobe aims letters at a future commercial
acquirer than at a free repo.

Signals: entry in github/dmca for storytold; restyle or rename commits under
time pressure; Adobe patent letter mentioned by the founder; sudden removal of
the credits page; founder going quiet.

Fleet impact: the code persists. Keep local mirrors (section 7). Chilling
effect on Tier 3 targets in reversal-targets/01; Tier 0 unaffected.

### B. Hoovered by Adobe (5 percent)

Adobe buys storytold or hires the team, Embrace-Extend-Extinguish style, or as
a settlement disguised as an acquisition.

Why unlikely: founder's stated motive is anti-Adobe (cancellation fee). Even if
it happened, the MIT code forks the same day (precedent: Oracle-Sun ->
LibreOffice from OpenOffice, MariaDB from MySQL). Adobe would be buying a
team and a brand with a community that just walked out. The only rational Adobe
version is buying the **method** to accelerate their own work (e.g. native
ports, legacy code migration), not burying the apps.

Signals: Adobe hiring storytold contributors; Adobe announcing a free
Photoshop tier or "Photoshop Express Pro" right after a quiet storytold
period; founder rhetoric softening.

Fleet impact: fork point. Whoever hosts the first credible community fork wins
the contributor graph. Our mirrors + contributions would matter.

### C. Hoovered by an AI corp, company-level (15 to 25 percent)

Candidates, in order of fit (opinion):

1. **Canva** (not an AI lab, but the most natural buyer): Affinity playbook
   already proven - free pro apps, paid AI. ArtCraft brings an AI studio,
   native Rust apps on all platforms including Linux and Web, and an army of
   contributors. Risk for Canva: two free pro suites to maintain.
2. **Anthropic**: Bun precedent (buy MIT infra, keep it MIT). "Seven Adobe apps
   rebuilt by Opus 5.5" is the best possible Claude Code ad. But a consumer
   creative suite is off-strategy; more likely a partnership, credits deal, or
   case study than a purchase. A purchase would be about the reversal method
   as an enterprise product ("migrate your legacy apps").
3. **Google**: Nano Banana and Veo are core providers; embarrassing Adobe is a
   bonus; Windsurf-style license + hire is their proven structure.
4. **OpenAI**: GPT-Image/Sora as providers, consumer creative push, Steinberger
   precedent for taking builders with communities.
5. **xAI**: Grok already a provider; "software is over" is on-brand.
6. **ByteDance**: Seedance + CapCut fit perfectly on paper; politically toxic
   for a US company, CFIUS-shaped problems. Low.

Price band, if it happens: $100M to $1B (InterPositive and Affinity bracket),
higher only if enterprise migration revenue appears. Reverse-acquihire
(license + hire) is the likeliest structure because there is no exclusive code
to buy anyway.

Signals: a provider becoming "default" or discounted in ArtCraft; joint launch
posts; enterprise "secure models" tier gaining named customers; storytold
hiring freeze; founder visits to SF labs.

Fleet impact: if Anthropic, our Claude-centric fleet gains an official
reference implementation of agentic reversal; if Google/OpenAI, provider bias
enters the apps. Either way the MIT code stays forkable.

### D. Main dev hoovered, project to foundation (20 to 25 percent)

The Steinberger path: Clawdbot -> Moltbot (rename under Anthropic trademark
pressure) -> OpenClaw -> founder joins OpenAI in Feb 2026 to lead
personal-agent work; OpenClaw moves to a foundation, stays open. Steinberger's
stated reason: changing the world interested him more than building a big
company.

Fit: Brandon Thomas is the person who ran trillions of tokens through a CUA
reversal pipeline and shipped 12+ native apps. Every lab building "agents that
replace software" wants exactly that. The relicense to MIT/Apache on
2026-10-10 makes a foundation handoff trivial (no license fight). Note 07 already
calls him Peter's brother in spirit.

Signals: foundation announcement or "governance" doc; lieutenants with merge
rights (11); founder posting about "next chapter"; craft-launcher and
services moved to a neutral org.

Fleet impact: best case for us. Foundation-run MIT Crafts with a governance
model = stable upstream to bridge (MCP wrappers) and contribute to.

### E. Pipeline sale, InterPositive style (10 percent)

ArtCraft started as an AI film/creative IDE with feature-film ambitions
(ROADMAP: "content studio + AI feature film"). A distributor or platform
(Netflix, Amazon, Apple, a game-engine company) buys the AI studio and
service layer; the Craft apps spin out to a foundation. Netflix already paid
$587M for 16 people doing AI post-production.

Signals: film-festival entries made in ArtCraft; studio partnerships; the
credits product drifting toward pro film workflows (relight, repose, identity
transfer).

### F. Stays king: raise, build, maybe Blender-style (30 to 40 percent for a
priced round; long-run king-status unknowable)

With 114k stars in two weeks, venture money will be offered. The Steinberger
PSPDFKit path (indie, profitable, own an unsexy universal layer, take growth
capital late) or the Blender path (foundation + development fund + corporate
patrons) are both available. The relicense suggests he is optimizing for
adoption over control, which fits Blender more than VC. The credits business
plus enterprise could fund a real team if subsidy economics hold (13 section 5).

Signals: priced round announcement; hiring page; corporate sponsors
(hardware vendors, Linux distros, education); Development Fund style donations
page; installers fixed and week-4 retention claims.

### G. Fizzle (15 to 20 percent)

Alpha never reaches daily-driver parity for pros; installer and auth bugs
erode week-2 retention (01, 07 gates); credits subsidy bleeds; contributor
funnel saturates on merge bandwidth (11); attention moves to a fork or a
copycat with more funding. Code survives, momentum does not.

Signals: release cadence dropping below weekly; PR queue latency rising;
issues closed as stale; star velocity collapsing below 500/day on photocraft.

## 4. Most likely composite (opinion)

Raise or partner in Q4 2026 (F or C-lite), founder and method courted by labs
within 6 to 12 months (D), Crafts drift into a foundation either way. Adobe
stays legally quiet and competes on product (free tier, AI bundling).
Probability that the Craft code disappears: near zero.

## 5. The bigger story: the method is the product

All trajectories that pay big are about the **CUA reversal pipeline**, not the
apps. If an agent can turn any closed desktop app into an open native
equivalent in weeks, the market is not "free Photoshop", it is "migration off
every vendor": internal line-of-business apps, VB6 and Delphi relics, SAP GUI
fronts, abandoned vertical software. That is an enterprise services market
measured in tens of billions, and it is why labs (C, D) are the natural
endgame. This is also the positioning question for reversing-mcp: we are
building pieces of that pipeline (pywinauto-mcp missions, reversal-targets/03,
reversing-mcp Tier 3). The legal hygiene that pipeline needs to be sellable
is in 14 section 8 and reversal-targets/02.

## 6. Watch list (weekly, record deltas in HANDOVER)

- Stars/forks/contributors per repo (gh api loop from HANDOVER 0.3).
- github/dmca entries mentioning storytold.
- Commits touching NOTICE, LICENSE*, branding, chrome/theme in FilmCraft.
- Pricing page changes (credit-per-unit tables, model removals).
- Foundation, governance, or funding announcements.
- Founder posts mentioning labs, "next chapter", or hiring.
- Adobe product moves: free tiers, price cuts, AI bundling, cancellation-fee
  policy changes.
- New targets: gridcraft/deckcraft/wordcraft (Microsoft), cadcraft (Autodesk),
  soundcraft (Avid) star velocity and any letters from those vendors.

## 7. Fleet actions from this file

1. **Mirror insurance**: `git clone --mirror` of photocraft, artcraft,
   craft-launcher, pdfcraft, lightcraft, filmcraft to D:\Dev\repos\_upstream
   weekly. Legal under MIT/Apache, cheap, protects against A/B. Needs Sandra's
   go (disk + scheduled task).
2. **Bridge, do not clone**: wrap `photocraft-cli` ("headless CLI for scripts
   and agents", shipped with v0.5.0) in an MCP server once its command surface
   stabilizes. Run wrappee-drift on it before building. Free, offline,
   Photoshop-class image ops over MCP.
3. **Contribute outward** (11): one fleet PR to photocraft in our strongest
   area (PSD, color, imaging) builds the relationship that pays off under D/F.
4. **Keep our own reversal pipeline lane-clean** so it is sellable in any
   trajectory (14 section 8).
