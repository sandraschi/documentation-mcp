# Artist Resistance to AI Music Generation

> Last updated: 2026-03-04

The opposition to AI music generation ranges from principled artistic objection to cold economic self-interest, and the two are not always aligned. Here's what's actually happening and how effective it's been.

---

## "Say No to Suno" (February 2026)

Just as Google launched Lyria 3 and acquired ProducerAI, a coalition of artist representatives published an open letter calling on the music community to "Say No to Suno."

The letter described Suno as a "brazen smash and grab" that "floods platforms with AI slop and dilutes the royalty pools of legitimate artists."

**Effectiveness:** Limited. The letter got press coverage and reinforced the industry narrative. It didn't affect Suno's user numbers, valuation, or legal position. The Warner settlement a few months earlier had already established that labels were willing to deal with Suno commercially — the "no negotiation" stance was always more posture than policy.

---

## The major labels' campaign: litigation as leverage, not principle

The RIAA, UMG, Sony, and Warner positioned their lawsuits as protecting artists. Their public communications emphasized:
- Artists' rights to control their work
- The harm to human creativity
- The "unlicensed" nature of AI training

What they were actually doing: establishing leverage for licensing negotiations.

Within 18 months of filing, two of the three major labels had settled and entered commercial partnerships with the very companies they had sued. The third (Sony with Suno) is presumably in negotiation.

The labels don't want to kill AI music — they want a share of its revenue. The lawsuit was a negotiating tactic that worked. They're now in a position to collect training royalties AND per-generation micro-royalties from "responsible" licensed platforms.

Artists signed to those labels will benefit — if they opt in. Artists who opt out, or who aren't signed to majors, are not part of the deal.

---

## Independent artist actions

**The class action lawsuits (October 2025)**

The most significant independent artist action: a group of indie musicians filing class action lawsuits against both Suno and Udio, seeking to represent all independent artists with registered copyrights used in AI training.

Key allegations specific to indie artists:
- Lyrics scraped from lyrics websites without permission
- Audio obtained via YouTube stream-ripping (circumventing technological protection measures)
- Loss of licensing revenues: AI outputs directly substitute for sync licenses that would have gone to these artists
- Privacy/publicity violations (Udio specifically): claiming Udio produced content implicating artists' likenesses

**Status:** Class certification pending. If certified, thousands of musicians could join, massively increasing damages exposure. But class certification is hard — plaintiffs must demonstrate common questions of law and fact across a diverse class.

**Why indie artists face structural disadvantage:**
- Not part of the major label settlements (those only cover UMG/Sony/Warner catalog)
- Can't afford the litigation costs that the RIAA funded for the majors
- Fragmented: thousands of small claimants rather than three powerful entities
- Class action is the only viable path, and class certification for AI training cases is legally novel

---

## Koda (Denmark)

Koda, representing 52,000 Danish musicians and composers, sued Suno in Copenhagen City Court (November 2025).

Their characterization: "the biggest theft in music history."

Evidence presented included AI tracks closely resembling works by:
- Aqua ("Barbie Girl" etc.)
- MØ
- Other Danish artists

Commissioned IFPI Denmark report: $680M projected damage to Danish music industry 2025–2030 (28% revenue loss).

**Why the Danish case matters:**
- Different legal system — no fair use doctrine equivalent
- Danish and EU copyright law is more protective of authors
- Could establish a precedent that has extraterritorial effect on how European services treat AI music
- Koda is well-funded and organized — not going away

---

## GEMA (Germany)

Germany's music licensing organization GEMA has been the most aggressive European rights holder:

- Sued Suno for copyright violations (separate from the US RIAA cases)
- Also won a separate lawsuit against OpenAI for **reproducing lyrics without permission**
- The OpenAI lyrics win is directly relevant to AI music: if displaying lyrics from AI training is infringement, then generating AI music that incorporates lyric patterns is also suspect

German copyright law:
- No US-style fair use
- The EU Copyright Directive's text and data mining exception (Article 4) applies only to non-commercial research purposes
- Commercial AI training on copyrighted music has no safe harbor in German law
- GEMA's opt-out mechanism: rightsholders can opt out of the Article 4 exception even for research — and GEMA has done this on behalf of its members

---

## Artist sentiment: more nuanced than the campaigns suggest

Public polling and survey data (various, 2024–2025) shows:

**Artists most opposed to AI music:**
- Older, established artists whose income comes from existing catalogs
- Session musicians (instrumentalists, backing vocalists) — their work is most directly displaced
- Lyricists and composers who license to other artists
- Artists with strong personal brand connected to their sonic identity

**Artists more open to AI music tools:**
- Younger producers and beatmakers — see AI as another production tool
- Artists in genres that already use heavy production (EDM, hip-hop, pop)
- Independent artists who can't afford session musicians
- Artists interested in experimental/generative forms

**The production tool vs. replacement distinction:**
Many working musicians oppose "AI songs made from stolen data" (Suno/Udio) while being entirely comfortable with AI-assisted tools in their own production workflow (Auto-Tune, AI stem separation, sample clearing assistance). The objection is training data legitimacy and output competition, not AI per se.

---

## What has actually worked

**Streaming platform restrictions:**
- Spotify, Apple Music, and others have added detection for AI-generated bulk uploads
- Apple Music flagged ~2 billion fraudulent streams in 2025
- TikTok removed millions of AI-generated tracks uploaded to game streaming counts
- These measures reduce the royalty dilution problem at the platform level, but don't stop the underlying generation

**Watermarking (SynthID):**
- Google's SynthID survives MP3 compression and analog re-recording
- If universally adopted, allows platforms to identify and filter AI content
- If not universally adopted (Suno and ACE-Step don't use it), partial solution only

**The settlements:**
- Did extract money from Udio and (partially) Suno
- Did establish opt-in licensing frameworks for future training
- Did not address indie artists, did not address FOSS models, did not address Chinese jurisdiction

---

## What hasn't worked and won't work

**Appeals to consumer conscience:**
- "Stream human music, not AI slop" campaigns have no measurable effect
- Most consumers can't distinguish good AI music from human-created
- The listeners who care are already the core music fans who stream heavily regardless

**Platform bans:**
- Impossible to reliably detect AI music on upload without 100% false positive rate
- Even with detection, users re-upload under different accounts
- ACE-Step outputs carry no watermark — undetectable by current methods

**Calling it "theft":**
- Rhetorically powerful, legally contested
- Even if technically accurate (and courts haven't ruled this way cleanly), it doesn't help indie artists who lack the resources to litigate

**Stopping the FOSS/local generation:**
- Cannot be done by legal means once weights are distributed
- Cannot be regulated into non-existence — it's software on your GPU
- The entire Western IP enforcement apparatus is irrelevant to a MIT-licensed model maintained by Chinese companies and downloaded by users globally

---

## The realistic outlook for artists

**Artists with leverage (major label signed, catalog owners, famous):** Will be compensated via the licensing deals the labels negotiate. Opt-in structure means they choose whether their music trains future models.

**Indie artists with registered copyrights:** Class action lawsuits are their only path to compensation for past training. Future licensed platforms will need to include Merlin (indie label aggregator) — ElevenLabs already did a Merlin deal. But the FOSS models don't care.

**Working session musicians:** Facing direct economic displacement in low-end sync and background music markets. No legal remedy — ACE-Step doesn't owe anyone money. The economic argument ("AI is stealing my livelihood") is real but not legally actionable when the model was trained on licensed data and you're being displaced by legitimate competition.

**The honest assessment:** The fight has succeeded in extracting licensing revenue from US-based commercial platforms. It has failed — and will continue to fail — against FOSS distribution and Chinese jurisdiction. The economic disruption to the bottom half of the music earnings distribution is real and ongoing, and the legal tools available to address it are mostly exhausted.

This is analogous to the Napster moment — the labels won the Napster lawsuits and it didn't stop music piracy or digital disruption. History is rhyming.
