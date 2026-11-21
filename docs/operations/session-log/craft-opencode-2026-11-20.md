# craft-opencode 2026-11-20: showcase topbar and hero copy (Sandra request)

Agent: opencode. Claim: craft-showcase (devcraft_claim, 2026-11-20).
Freeze basis: Sandra asked in-session, so allowed per CRAFT_FLEET_RULES section 1.

## Session-log review (last 3 days, before touching)
- 2026-11-19 wip-snapshot: craft-showcase snapshot 6 files (auto snapshot, no copy discussion).
- 2026-11-18 craft-claim-agy: agy claims shopcraft, webshop family, aicraft, craft-ai, musiccraft. No craft-showcase. No conflict.
- 2026-11-17 craft-phase1-safe: craft-showcase got .gitattributes LF commit. No pending copy work.
- No other agent is working in craft-showcase. Single-agent rule ok.

## Changes in craft-showcase (web/index.html only, 2 lines)
Previous turn (already unstaged, kept):
- Topbar nav: removed duplicate `Live WASM Demo` link to #wasm-demo.
- Topbar CTA: `Launch WASM Sandbox` renamed to `Launch in Sandbox`.
This turn:
- Hero CTA: `Open In-Browser WebAssembly Studio` renamed to `Open In-Browser Sandbox`.
Reason: WASM is jargon, Sandbox is understood. One sandbox entry in topbar.
Kept the blue button (not the small nav link) because the nav link is hidden on mobile (hidden md:flex) and the button is always visible.

Not changed (left for Sandra to decide):
- Hero paragraph still says `in-browser WebAssembly workstations`.
- Section heading `WebAssembly Preview Sandbox` and badge text unchanged.

## Pre-existing dirty state (not mine, not committed)
- craft-showcase has other unstaged edits from an earlier session: CHANGELOG.md, scripts/serve.py, start.ps1, plus untracked README_20261112_120058.md.bak and crates/craft-showcase-wasm/Trunk.toml.
- I commit only web/index.html. The .bak and Trunk.toml are never committed per fleet rules.
- Hygiene gap for O3: craft-showcase .gitignore covers only /target/, wasm dist, *.rs.bk, DS_Store, Thumbs. It is missing the fleet baseline: dist/, *.exe, *.zip, *.mcpb, *.pdb, *.bak, *.bak.*, .env. Left for the O3 rollout, not mixed into this copy commit.
- .gitattributes LF present. No em dash used in edits or this log.

## Tests
- cargo test --workspace: not run. No Rust code touched, web copy only, so counts are unchanged. No test claim made.
- Verification: not done by me per no-self-verification rule. Needs a different agent or Sandra to refresh http://localhost:11270/ and confirm one topbar CTA labeled `Launch in Sandbox` and hero button `Open In-Browser Sandbox`.

## Plan tick
- No consolidation-plan phase box ticked. This is a Sandra-requested copy fix outside Phases 0-5, logged here as a freeze exception.

## Left
- Commit and push web/index.html (1 file) in craft-showcase, then devcraft_release.
- This log file committed in mcp-central-docs.
- Optional follow-up: align hero paragraph and section heading if Sandra wants all WASM wording gone.

## 2026-11-20 follow-up: align leftovers + video plan (same claim)
Copy alignment done in web/index.html (3 replacements, 1 file):
- Hero paragraph: `in-browser WebAssembly workstations` to `in-browser sandbox workstations`.
- Section heading: `WebAssembly Preview Sandbox` to `In-Browser Sandbox Preview`.
- HTML comment: `LIVE IN-BROWSER WASM SANDBOX SECTION` to `LIVE IN-BROWSER SANDBOX SECTION`.
No em dash used. Tests: not run, web copy only, counts unchanged.

Video audit (no render yet, plan only per Sandra request):
- Page promises: 2.5-minute cinematic pitch, 4 acts with fixed voiceover lines, `4K 60FPS Native`, `Industrial Ambient Synth (120 BPM)`.
- Reality: web/media is 2.5 MB total, narration.yaml targets 65s at 720p with bg_music false and voice `heart`, vtt has 7 cues over about 68s about 52 apps and shop craft, which does not match the 4-act boardroom script on the page. So the page overclaims on runtime, resolution, music, and script. Voice sounds robotic with flat prosody.
- Proposed plan phases: A honesty hotfix on the spec labels, B script lock to the 4-act page lines at about 150s, C voice shootout with samples of the Act I line (Sandra record vs neural with SSML pacing), D scripted Playwright captures per act, E edit with ducked music bed plus synced vtt and fresh poster, F verification by a different agent on a fresh clone.
- Open decisions for Sandra: keep or downgrade the 4K and music labels now, runtime target 68s vs full 2.5 min, voice choice, music licensing.
- Left: commit web/index.html, commit this log, push both, release claim.
