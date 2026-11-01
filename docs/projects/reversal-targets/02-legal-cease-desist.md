# 02 - Legal Framework: Hitting Without Letters

Not legal advice. A working framework for staying on the safe side of
clean-room reversal, with the statutes to hand to counsel if a letter ever
arrives. The short version: behavior is free, expression is not, and builders
who diverge chrome while documenting sources almost never get successfully sued.

## What is actually protected

- Copyright covers expression (code, assets, text, icons), never ideas,
  procedures, or functionality. Reimplementing what a menu does is legal.
  Copying its icon is not.
- Patents cover specific claimed inventions, rarely UI flows, and software
  patents are weak in the EU. Check, do not assume.
- Trademarks cover names, logos, trade dress (distinctive visual identity).
  This is the live wire: a pixel-identical Premiere layout is Tetris-case
  bait even with clean code. Diverge spacing, fonts, icons, theme. Keep
  shortcuts (functional) and file compatibility (interoperability).
- EULA anti-reverse clauses are contract claims against licensees, not
  universal prohibitions, and they bow to statutory interoperability rights
  where those exist.

## The shields, by strength

1. **Dead or FOSS targets (Tier 0).** No plaintiff, no suit. Trademark can
   theoretically outlive a company, so still rename, but the risk rounds to
   zero. Abandonware is not a legal category; treat it as low-risk, not
   no-risk, and keep provenance records.
2. **Black-box clean room.** Observe the running app (screens, UIA tree,
   files, docs), write specs, reimplement from specs, never touch a
   decompiler. No copied expression exists to infringe. This is the fleet
   default method (03) and the strongest practical shield.
3. **EU Software Directive Art. 6.** Expressly permits decompilation where
   necessary for interoperability, regardless of EULA clauses. Goliath sits
   in Vienna: this is home law. Document the interoperability purpose
   (file round-trip, plugin compat) contemporaneously.
4. **US fair use for reverse engineering.** Sega v. Accolade (9th Cir. 1992):
   disassembly for interoperability is fair use. Persuasive, not universal,
   and trade dress remains separately actionable.
5. **Specs, papers, standards.** PSD spec (published by Adobe), DSP
   textbooks, colorimetry standards, DSP papers (Demucs, Spleeter): building
   from public sources needs no shield at all. Prefer this path wherever it
   exists, which for shallow targets is everywhere.

## Practical rules (non-negotiable)

- New names, new icons, fleet dark theme. Never the incumbent's skin.
- No copied assets: no icon files, no font files, no sample content, no help
  text pasted. Rewrite every string.
- Keep a source log per spec: screenshot hash, doc URL, tutorial timestamp.
  No code origins, ever. The log is what you show counsel.
- MIT/Apache output only, SPDX headers, no Fair-Source-style use restrictions
  that complicate downstream adoption.
- File formats: round-trip fidelity is the goal and the legal justification
  (interoperability). Test corpora pinned with hashes.
- Do not poke DRM, license checks, activation, or anti-cheat. Ever. Different
  statutes (EU InfoSoc Art. 6, US DMCA 1201) with real teeth. Targets whose
  value lives behind circumvention are Tier 3 by definition.

## If a letter arrives anyway

1. Do not respond emotionally or publicly for 48 hours. Do not delete
   anything (spoliation is worse than infringement).
2. Freeze the accused surface (stop shipping that screen/asset), keep
   everything else moving.
3. Pull the source log for the accused work plus the divergence record
   (screenshots side by side showing different chrome).
4. Counsel first, then decide: rename/restyle is cheap, fights are not.
   Most C&Ds die at step 4 when the log shows clean-room plus divergence.
5. Log the letter (redacted) in this section. A fleet that shares
   threat intelligence gets harder to bully with every letter.
