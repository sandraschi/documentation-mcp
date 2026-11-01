# 07 - Strategy and Timing: Why Now, Why Him, Why This Target

Date: 2026-10-08. Note: "Petes brother" is a joke. Brandon Thomas is a brother
in spirit to Peter Steinberger, not in blood. Same school: indie, native,
Rust-level polish, PDF-first thinking, bootstrap-to-monster without permission.

## The new road to success

Single dev or band of brothers (Tsinghua dorm, Vienna basement, anywhere)
plus a trillion-token model. That is the whole company now.

Remember Manus: tiny team at Butterfly Effect that shipped the first viral
general FOSS agentic demo and reset expectations for everyone. No 200-person
org, no platform team, no design committee. Small elite loop + frontier model
+ shameless distribution. ArtCraft is Manus applied to Creative Cloud.

Pattern:
1. One hated rent-extractor everyone understands in 10 seconds.
2. One frontier model that can just hold the whole workspace (Opus 5.5 since Feb).
3. One hub, one Discord, one Installers Ready button for Mac/Win/Linux/Web.
4. Ship half-cooked, recruit users as QA, let burn-down slope do the talking.

Stars 7.3k today -> 10k per day for a few days after Ars + HN + Reddit + demo
is the OpenClaw curve. TV follows because lone dev kills Adobe with AI is a
producer package. Retention decides week 2, when MSI still silently exits.

## Why Adobe is the perfect target

Nothing so massive exists in PC software with this combination:

- Universal: students, YouTubers, Global South, hobbyists, pros. 100M reachable
  even if 1B is hype. Office is bigger but defended by enterprise + cloud lock-in.
  Autodesk is deep but niche. Adobe is broad + visible + hated.
- Rental pain with a name: cancellation fee dark pattern. Thomas cites being bit
  one too many times. Everyone has the story. Distribution writes itself.
- Fully visible surface: Win32/Qt desktop, menus, panels, shortcuts, presets,
  XMP, PSD, AEP on disk, 30 years of manuals and tutorials. Not SaaS. No server
  logic to guess. Wide open to black-box crawling (screens + UIA + configs +
  workflows + docs). No Ghidra needed.
- Asleep on agents: no real CLI + JSON + MCP contract. ArtCraft promises all three
  on every Craft from day one. Next workflows get built on the scriptable base.

## Why launching half-cooked is rational, not sloppy

1. Opus window: 6 months ago the model could not hold a 100k-line Rust workspace.
   6 months from now 50 teams can. First mover takes namespace, stars, contributors.
2. Spec harvest: 2000 issues in days = 2000 free parity specs with screenshots.
   Bug-counting misses that discovery parallelizes to users, fixing parallelizes
   to agents, fixes compound across shared Rust core + WASM + agent contract.
3. Legal sympathy: better to be sued as free MIT kid on TV than as funded Series A
   with revenue to squeeze. Nervousness about competitors outrunning him is correct
   prioritization. Speed is the moat for 90 days.

Judge by 90-day issue burn-down slope, not day-3 screenshots. 80 percent + free +
local + scriptable beats 99 percent for everyone except finishing houses.

## The Peter path: how he gets very very rich or stays king

Peter Steinberger path (PSPDFKit/Nutrient): own an unsexy universal layer, stay
indie, out-execute incumbents on files and polish for a decade, become inevitable.

Brandon variant: own canvas + file round-trip + agent contract for 7 crafts.

Acquisition logic if he survives trade dress:
- Anthropic: Opus Jesus showcase. Best marketing for code models ever.
- Google: embarrass Adobe, feed Veo/Seedream/NotebookLM funnel.
- Adobe: acquihire to bury. Most expensive, most likely to leak and backfire.
- Black Forest Labs / Stability successors: model + editor vertical.

He either takes the big bid or pulls a Peter and stays king. Both require surviving
the next 3 gates below.

## Three gates before the billion

1. Trade dress, not copyright. Functional clean-room is legal (EFF FAQ, N64 precedent).
   Pixel-identical Premiere chrome is Tetris-case bait. Fix: diverge spacing, fonts,
   icons, theme now. Keep shortcuts and behavior. Paper every panel with SPEC source
   log (screenshot hash + doc URL + tutorial timestamp, zero decompiled code).
2. Installers that work for mom. MSI silent exit (#1990), signup failure (#2004),
   localStorage mount block (#1984), canvas flicker (#1983) kill retention faster
   than missing features. Fleet TAURI_PRODUCTION_PITFALLS A-J + BUILD_LOG.md +
   desktop-session-regression.md is the unsexy edge. Our NAKED_PC install standard
   and start.ps1/start.bat discipline is ahead here. His Installers Ready button
   must become Double-Click Works reality.
3. Token subsidy durability. Free MIT apps funded by ArtCraft generation tokens
   works while hype pays GPU bill. If local 4090 (comfyops + civitai + Wan LocalGen)
   commoditizes generation, subsidy thins. Hedge is BYO providers + local-first
   paths already promised. Watch bill per generation vs willingness to pay.

Foundation + CLA needed now if PRs go 100 per day. Half will be poisoned or
copyrighted without gates.

## What this means for the fleet

We had the same idea last year and sat on hands. He shipped the wedge, we built
the roads. Both matter, roads win longer.

Fleet is a precursor IF we fill gaps and mesh everything and do easypeasy
oneclick install:

- Mesh the 4 we have (blender + gimp + comfyops + videogen, davinci as pro finish)
  with one location/character/shot object and one depot. See 03.
- One double-click per repo that works for mom. No port squats, no Python homework.
  claim_ports.py + START_SCRIPT_STANDARD + MCPB wipe+recopy discipline.
- Let him burn Adobe legal budget opening the trail. Walk through with MIT bridges,
  not rewrites. Wrap wins tomorrow, thin Rust only where hot.
- Do not chase 7 clones menu-for-menu. Chase the contract: every fleet media server
  gets CLI + JSON + MCP + snapshot + mission + library, uniform names, Prefab cards.

Target selection lesson: attack where megacorp cannot defend (visible UI, rental
hate, agent gap) and need is millions strong. Office and CAD are next per 04, but
none is as massive and legible as Adobe. That is why he picked correctly.

## Opus actions from this file

- Add trade-dress divergence checklist to every SPEC template (names, icons, spacing,
  theme changed; behavior and shortcuts kept; screenshots attached).
- Add weekly tracker: stars, releases, issue burn-down, installer fix status,
  license verification (see 06 appendix), any Adobe contact or restyle commits.
- If burn-down holds 90 days, propose Phase 2 panel expansion. If MSI/auth still
  broken after 30 days, deprioritize mesh interop and fix install first. Distribution
  beats parity until install works.
