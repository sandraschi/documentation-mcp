# Promotion playbook — from 2 stars to discovered (execution companion to FLEET_PROMOTION)

**Status:** Playbook v1 2026-10-04 · implements [standards/FLEET_PROMOTION.md](../standards/FLEET_PROMOTION.md) (policy: useful pointer, not spam)
**Tags:** [fleet, promotion, discovery, stars, runbook]

The standard says *what is allowed*. This says *in what order, in one evening each*.

## Positioning worksheet (do first, 20 minutes)

Stars price distribution of desire, not goodness. Answer in one line each:

1. Whose problem, in their words? (not "MCP voice bus" — "talk to any AI agent stack out loud")
2. What is the 60-second win? (clone → hear a voice / see the artifact)
3. Who already wants the wrappee? (their forum, subreddit, Discord — that is your audience, not "AI Twitter")
4. What is the one universal pain this repo owns? (if none: promote the *workflow post*, not the repo)

Worked example — speech-mcp: nobody wants "a fleet voice bus." Many want "an MCP-native voice layer for any agent stack" (pipecat owns framework, nobody owns the MCP layer). Position the gateway, not the bus. Same code, different door.

## Phase 0 — honesty gate (blocks everything after)

- README Preview screenshots real, How-it-runs true, `.mcpb` installs on a naked PC, `llms.txt` accurate. FakeFind-clean.
- If the gate fails, promote nothing — fix first. A discovered runt earns issues, not stars.

## Phase 1 — one-hour discovery baseline

1. GitHub About: concrete capabilities, no paradigm-shift language. Topics: `mcp`, `fastmcp`, wrappee tag, domain tag (`text-to-speech`, `voice-cloning`…).
2. `glama.json` current; submit/update listing (see ecosystem/glama/REGISTRY_GUIDE.md).
3. Release with `.mcpb` attached. Releases are landing pages.
4. `projects/{repo}/README.md` mirror in mcd.

## Phase 2 — the 60-second demo (the actual multiplier)

- One GIF or silent 60s video: problem → command → artifact. No talking head, no thread.
- README top, release notes, Glama screenshots. inkscape/blender (82/53 ★) both teach this: show the *made thing*, not the tool list.
- Cost: one evening. Yield: every later post links here instead of explaining.

## Phase 2b — humor lane (fantasy/niche repos: openbci and friends)

GitHub is greybeard dev central: it prices sincerity by utility and has no shelf for skullcap jokes. A fantasy wrapper promoted straight-faced earns 2 stars and pity. Promoted *as comedy that works*, it earns links.

- Position the joke, ship the function: "read your mind (terms and conditions: mind must be within 2cm of electrodes, thinking in Morse)". The demo is funny; the code underneath is real and installable.
- Meme demo > straight demo: 30 seconds, punchline first, install command last frame. Post where humans gather (not GH topics): maker forums, relevant subreddits, Hackaday-style outlets, the wrappee's own community.
- Rule: the humor must respect the reader's intelligence — laugh *with* the niche, never at the user. One joke per repo, then the honest docs take over.

## Phase 2c — human website lane (Hostinger, solo-dev style)

Neckbeards browse GitHub; humans browse the web. For repos with any non-dev audience:

- Generate the site with our own tooling: `meta_mcp` LandingPageBuilder (static HTML or React/Tailwind, `generate_landing_page`) — dogfood first.
- Host static on Hostinger like every solo dev: one small site per flagship repo, or one fleet-showcase site with per-repo pages for the long tail (cheaper, and the long tail cross-links).
- Site content = Phase-2 demo + install one-liner + honest screenshots + link back to GH. No blog unless someone volunteers to feed it (dead blogs cost more than none).
- Measure: referrer stars/issues via gitops. A site that sends zero visitors in 3 months gets archived, not fed.

## Phase 3 — outward, one channel per week max (humans included, not just GH)

1. **Awesome-list PR** (awesome-mcp, domain awesomes): one line, honest description. Maintainers merge usefulness.
2. **Wrappee forum answer**: respond to an existing "how do I X with voice/agents" question with the workflow + link. Never cold-post the pitch.
3. **Release-note round**: Glama/Smithery update + short changelog post where users already gather.
4. Never: mass cross-posting, emoji threads, "game changer" language — see standard.

## Phase 4 — measure with gitops (monthly, 5 minutes)

- `github_ops repo_list` / `show_repo`: stars, forks, open issues, traffic where available.
- Scorecard popularity column = stars + external issues/PRs. No vibes.
- Star flat for 3 months after Phases 1–3? Positioning is wrong (redo worksheet) or audience doesn't exist (accept Tier-0 obscurity — some repos are infrastructure, and that's fine).

## Non-goals

No spam, no launch theater, no promoting past the honesty gate, no star-chasing rewrites of working code. Some repos (handbrake, openbci) are correctly at 2 ★ — the playbook is for repos with a universal pain and no distribution, not for manufacturing desire.
