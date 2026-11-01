# 14 - Legal Deep Dive: Adobe vs CUA Clean Room

Date: 2026-10-11. NOT LEGAL ADVICE. Working analysis to hand to counsel.
Companion to `projects/reversal-targets/02-legal-cease-desist.md` (the fleet's
general framework); this file is ArtCraft-specific and goes deeper on doctrine.

## 0. Status check (verified 2026-10-11)

- **No Adobe cease-and-desist, takedown, or suit has been reported.** Coverage
  through ~Oct 8 explicitly notes no Adobe statement. Treat any C&D rumor as
  unverified until a primary source (letter, docket, GitHub DMCA repo entry)
  exists. GitHub publishes DMCA notices at github.com/github/dmca - watch it.
- **No 2026 Supreme Court ruling decides software UI reimplementation.** The
  claim that "a recent SCOTUS ruling hands him victory" did not check out.
  The 2026 copyright rulings found:
  - *Cox Communications v. Sony Music* (decided 2026-03-25, unanimous):
    contributory infringement requires inducement or a service tailored to
    infringement. Helps GitHub, hosts, and the project as a distributor of a
    general-purpose tool. Does not touch the clone itself.
  - *Thaler v. Perlmutter*: cert denied 2026-03-02. Human-authorship
    requirement stands. Cuts AGAINST ArtCraft's own copyright in purely
    AI-generated code (thin or no protection for unedited model output), which
    matters for enforcing its license, not for Adobe's claims.
  - The controlling high-court case is still *Google v. Oracle* (2021).
  If someone names a specific 2026 case, verify docket and holding before use.
- Scope is wider than Adobe: storytold also hosts wordcraft (Word), gridcraft
  (Excel), deckcraft (PowerPoint), cadcraft (AutoCAD), soundcraft (Pro Tools).
  Microsoft, Autodesk and Avid legal are potential parties too.

## 1. What Adobe owns and whether the clone touches it

| Asset | Protection | Touched? | Exposure |
|---|---|---|---|
| Source code | Copyright | No evidence of access. Rust from observed behavior will not match Adobe C++ | Low. Needs access + substantial similarity |
| Algorithms, features, workflows | Not copyrightable (17 USC 102(b), Baker v. Selden) | Yes, deliberately | None under copyright. **Patents are the issue** (section 4) |
| Menu hierarchy, command names, shortcuts | Lotus v. Borland (1st Cir. 1995, aff'd by 4-4 SCOTUS 1996): method of operation, uncopyrightable | Yes, "familiar by design" | Low in 1st Cir., contested elsewhere |
| Overall UI look and feel | Apple v. Microsoft (9th Cir. 1994): analytic dissection, thin protection | Partly (FilmCraft screenshots read as Premiere per 01) | Medium. Expressive selection/arrangement can survive dissection |
| Icons, splash art, illustrations, sample content, help text | Copyright, full strength | Should not be. Icons are original engraved animals | High IF anything was lifted. Audit assets |
| Product names, logos | Trademark | No. "Craft" names, own logos | Low |
| "Photoshop reimplementation" in READMEs | Trademark, nominative use | Yes | Low if no implied endorsement (New Kids on the Block test) |
| Trade dress (overall product image) | Lanham Act 43(a) | Possibly | Medium. **Most likely C&D lead** (section 3) |
| File formats (PSD, AI, PRPROJ, AEP, INDD) | Formats per se not protected (SAS v WPL in EU); spec license terms may bind | PSD from Adobe's published spec | Low to medium: check the PSD spec's own license terms |
| EULA anti-RE clauses | Contract, against licensees | CUA operated licensed apps | Medium US, ~zero EU (section 5) |
| Activation / DRM | DMCA 1201, InfoSoc Art. 6 | Not if licenses were paid | Low unless circumvented |

## 2. The Google v. Oracle argument fits unusually well

Oracle held Google's copying of Java API declaring code was fair use as a
matter of law, reasoning about **reimplementation that lets people carry
existing skills into a new platform**. The Court weighed the investment
programmers had made in learning the interface. PhotoCraft's own pitch is
"The menus, shortcuts, panels and tools your hands already know. Productive on
day one, no retraining." That is the Oracle factor-one/factor-four story told
for end users instead of programmers.

Limits: Oracle was about code (declaring code) and expressly did not decide
copyrightability; it is a fair-use holding on its facts. Applying it to visual
UI is an extension, persuasive not binding. And it does nothing for trade
dress or patents.

## 3. Trade dress: the most likely opening shot

Lanham Act 43(a) unregistered trade dress for **product design** requires:
1. Secondary meaning (Wal-Mart v. Samara, 2000) - consumers associate the
   design itself with Adobe. Plausible for Photoshop's overall look.
2. Non-functionality (TrafFix v. Marketing Displays, 2001) - a feature is
   functional if essential to use or purpose, or affects cost/quality. A UI
   copied *so users can operate it without retraining* is the functionality
   argument. "Familiar by design" is both his marketing and his defense, and
   Adobe will argue the familiarity is aesthetic brand recognition, not
   function. This is where the fight would be.
3. Likelihood of confusion - free, open-source, differently named, differently
   iconed, differently branded apps cut against confusion. Post-sale and
   initial-interest confusion theories are Adobe's stretch options.

Practical defense: diverge chrome (colors, spacing, fonts, iconography,
splash, panel headers) while keeping layout logic, shortcuts and behavior. The
engraved-animal icons already do this. FilmCraft's Premiere-like screenshots are
the weakest point (see 01).

## 4. Patents: the risk clean room does not touch

Independent creation is **no defense** to patent infringement. Adobe holds a
large portfolio covering imaging and editing techniques (content-aware fill,
healing, selection refinement, raw processing, video effects are plausible
candidates; verify specific patents and expiry before claiming any). Software
patents are weaker post-Alice (2014) and much weaker in the EU, but a patent
letter is the one weapon that works regardless of how clean the room was.
Cost-benefit for Adobe: slow, expensive, and suing a free MIT project on TV is
a PR loss. For forks with revenue (credits), the calculus changes.

## 5. The CUA method under each legal regime

What the method is: agents operating licensed Adobe apps through screenshots
and (presumably) UI automation, recording action workflows, producing
behavioral specs, then implementing in Rust. Claimed: no IDA Pro, Ghidra,
Hopper, or any disassembler/decompiler. Reported tokens: trillions since
winter 2025/26 (founder claim, unverified).

### US

- **Screenshots are copies** of copyrighted UI images. Intermediate copying for
  the purpose of understanding unprotectable elements has been held fair use
  (Sega v. Accolade, 9th Cir. 1992; Sony v. Connectix, 9th Cir. 2000), both
  stronger cases (they disassembled). Black-box screenshot observation is
  milder than what those courts allowed.
- **EULA**: Bowers v. Baystate (Fed. Cir. 2003) enforced a shrinkwrap
  anti-reverse-engineering clause. Counter: watching the UI and recording what
  it does is ordinary *use*, arguably not "reverse engineering" as the clause
  defines it. Read Adobe's General Terms for clauses on automated access,
  benchmarking, or developing competing products; those are the risky ones.
  Breach of contract yields damages against the licensee, not an injunction
  against the clone's code.
- **CFAA / anti-bot**: not applicable to local desktop software under a
  license (Van Buren, 2021, narrowed "exceeds authorized access").

### EU (home law for us in Vienna)

- **Software Directive 2009/24/EC Art. 5(3)**: a licensee may "observe, study
  or test the functioning of the program in order to determine the ideas and
  principles which underlie any element of the program" while doing acts it is
  entitled to do (loading, displaying, running). **Art. 8: contractual terms
  contrary to Art. 5(3) are null and void.** CUA observation is textbook 5(3).
- **SAS Institute v World Programming (CJEU C-406/10, 2012)**: functionality,
  programming language and data file formats are not protected expression; a
  licensee observing a learning edition to reproduce functionality is within
  5(3) and the license cannot override it. Closest precedent on earth to the
  ArtCraft method. (UK courts applied it in 2013; post-Brexit UK still follows.)
- **Art. 6 decompilation** is allowed only for interoperability, only what is
  necessary, results not usable to make a substantially similar program. Note
  the asymmetry: EU law is MORE permissive for observation (5(3)) than for
  decompilation (6). The "no Ghidra" claim keeps him in the stronger lane.
- **UI under EU law**: BSA v Ministry of Culture (CJEU C-393/09, 2010) - a GUI
  is not a computer program under the Directive but can be protected under
  InfoSoc as an author's own intellectual creation; elements dictated by
  technical function are excluded. Same functional/expressive line as the US.

## 6. The "clean room" claim itself, honestly assessed

Classic clean room (Phoenix BIOS, 1984): **two teams, a wall between them.**
The dirty team studies the original and writes a functional spec; a lawyer
vets it; the clean team, which never saw the original, implements from spec.
The wall exists to rebut the copying inference (access + similarity).

Where the AI version is weaker than the label:
1. **No demonstrable wall** if the same model context both observed the app
   and wrote code. Two agent instances with separate contexts and a vetted spec
   handoff would rebuild the wall; whether he did this is unknown.
2. **Weights contamination**: the model was trained on public internet data
   including Photoshop tutorials, documentation, screenshots, forum code, and
   conceivably leaked material. "Clean" cannot be proven at the weights level.
   Counter: training exposure is not copying of expression unless the output
   reproduces it; similarity analysis on output is still the test.
3. **Discovery cuts both ways**: trillions of tokens of transcripts, if
   preserved, are the best possible evidence of what was (not) seen. Any
   transcript where an agent ran `strings` on a binary, read a disassembly,
   pasted Adobe help text, or opened a leaked source tree becomes Exhibit A for
   Adobe. Spoliation (deleting them after a letter) would be worse.

Where it is stronger than skeptics think: clean room is an **evidentiary
practice, not a legal requirement**. Adobe must still show similarity of
protected expression. Fresh Rust against decades-old C++ will not show it.
Phoronix and others questioned the label; nobody has shown copied code.

### Why the skeptics misread the method

The skeptical camp assumes "reimplementing Photoshop" requires reading
Photoshop's code. The CUA method replaces code reading with **behavior
harvesting at machine scale**: every menu, dialog, slider and shortcut
exercised, before/after screenshots and output files captured, specs
synthesized, implementation verified by differential testing (same action on
original and clone, compare pixels/files). The 134/135 PSD round-trip number is
the output of that loop. It is the same black-box method that built Phoenix
BIOS, Samba, Wine, and LibreOffice's DOC filters, minus the decade of human
labor. What changed is cost, not legality.

## 7. Likely Adobe playbook, ranked by probability (opinion)

1. **Nothing public, internal monitoring** - suing a free MIT project with
   114k stars on the heels of the 2026 FTC cancellation-fee settlement is a
   Streisand gift. Most likely while the apps stay alpha.
2. **Targeted DMCA 512 takedowns** on GitHub against specific assets (icons,
   screenshots in READMEs, sample files) if any Adobe expression is found.
   Counter-notice process exists; GitHub has defended reimplementations.
3. **Trade dress / trademark C&D** - cheap, deniable, aimed at FilmCraft's
   chrome and README phrasing. Response: restyle, which is cheap.
4. **Patent letter** - only if a commercial entity (credits, acquirer)
   materializes. More likely aimed at an acquirer than at a free repo.
5. **Full copyright suit** - least likely without evidence of code access.
6. **Embrace**: hire, acquire, or compete (free Photoshop tier). See 15.

## 8. If we build the same thing (fleet rules, additive to reversal-targets/02)

- Two-agent wall enforced in code: observer agent outputs functional spec
  only; implementer agent receives spec only (open design item, see
  HANDOVER).
- Keep and hash all transcripts and capture bundles. Never delete after a
  letter.
- No disassembly in any lane whose output feeds a reimplementation.
- Expressive assets: zero imported. Fleet theme, own icons, rewritten strings.
- EU 5(3) as the documented legal basis for observation; log it per session.
- Patents: out of scope for tooling. README disclaimer. Prefer techniques from
  papers older than 20 years or explicitly open.
