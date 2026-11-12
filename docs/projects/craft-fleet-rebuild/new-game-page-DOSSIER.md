# gamecraft NEW-game page — Dossier (draft 2026-11-02)

Source: `gamecraft-cli new --prompt|--from-spec --provider auto|local|openai|anthropic [--model] [--endpoint]`, `gamecraft-forge::create` (GameSpec, never GDScript), `gamecraft-mcp` catalog tools (`game_list/report/verify/create`), `web/serve.ts` + `index.html` + `scripts/verify.ts`, `apps/gamecraft-desktop` (Play/Watch demo/Run tests, no New dialog).
Target: `web/new.html` + `serve.ts` routes + job runner + desktop New dialog stub. All three land in `depot/games/<slug>/` (Godot) or `web/games/<slug>/` (three.js) with same gates.

## 1. Why this is the killer feature

Nobody has prompt→verified depot. Godot path proves completable (gap-policy in Rust before write, `scene_lint` clean, Godot boots, `GameCraft: goal reached`). Web path proves boot + tour + checkpoints + `thumb.png/shots/` (Playwright SwiftShader, zero console errors). Both write `verify.json`, `thumb.png`, `lint.json/trace.json/commands.jsonl` (Godot) or `shots/` (web). A page that does that in 10 min for <$10 is a demo no one else can give.

## 2. Current gaps

- Godot `new` is CLI-only (`docs/NEW_GAME.md`). 8 archetypes now (`platformer/runner/pong/maze/flight/driving/chess/talk`), not 1. Still no `zelda`/`sokoban` archetype — spec has no enemies/keys/pushables. Web RPGs (Mossbrook) are session-built (Claude Opus 5.5, Emberwick 4 prompts), not `new --prompt`.
- Arcade `index.html` = grid + Play/Watch tour only. No `/new`. Desktop = Library grid + Editor (scene tree, viewport, inspector, lint, trace scrubber) + Game settings overlay (speed/gravity/jump multipliers), no New Game dialog.
- MCP: `game_create` exists, but `forge_new/create_game` not reachable from Claude Desktop/shell-less clients (KIBITZ defect). So agents can't trigger it either.

## 3. Proposed UX (baited breath, not blind wait)

`GET /new` — one page, no framework (like `index.html`, 50 lines + module script):
- Prompt box (prefill per preset, editable, 4-prompt Emberwick style for web, 1-sentence spec for Godot)
- Preset buttons: `Emberwick Village` (Mossbrook verbatim 4 prompts), `Space Station` (same 4, reskinned: angled top-down, companions=crew, buildings=modules with transparent camera-side wall, upstairs=upper deck, basement+tunnel=service ducts, mountain+troll=asteroid + sleeping alien, 4× area + plot + magic=tech), `Pirate Ship` (decks+rigging, cabins, hold tunnel, island cave+kraken), `Zelda-like` (overworld + 3 shrines + keys + pushable stones + boss door), `Sokoban` (5×5→9×9 crates, undo, par)
- Provider select: `Opus` (Anthropic, `ANTHROPIC_API_KEY`), `Fable` (OpenAI-compatible, `OPENAI_API_KEY` or LM Studio 1234), `Argon` (local Ollama 11434 / Strata 8080, `format:json`). Model string + endpoint fields, defaults from `NEW_GAME.md` table. Auto-probe like `--provider auto` (Ollama→LM Studio).
- Archetype select (Godot: 8; Web: `rpg-village` (Mossbrook fork), `zelda-like`, `sokoban`, `seek-find` (Benny), `sim` (Kaffeehaus)). Family radio: Godot vs three.js (different gates, different budgets).
- Budget cap: `$10` default, tokens + $ live. Godot spec path: in ~3k + out ~2k + 1 repair = <$0.10 gpt-4o / <$2 Opus. Web RPG path: 50-100k out over 4 rounds = $5-10 Opus. Cap rounds at 4, no textures in v1 (NEW_GAME.md limit). Abort + keep partial `run.json` when cap hit.
- Progress: stream `run.json` tail (spec→compile→lint→trace→boot→thumb), checkpoint dots, `shots/` thumbs as they land, elapsed + cost, Cancel button. Same tour markers as `verify.ts` (`GameCraft: ...`, checkpoints). `?autoplay=1` link when done, `Play` + `Watch demo` buttons like desktop.
- On success: `game.json` + `verify.json` + `thumb.png` written, appear in `/api/games` grid without restart (precache hash bump in `pwa.ts`). On fail: exact reason + furthest x (gap-policy) + one-click Retry with repair prompt (compiler already does 1 retry — surface it).

`serve.ts` additions:
- `GET /new` → `page(new.html)`, `GET /api/presets` (Emberwick ×5 + Zelda + Sokoban JSON), `POST /api/new/start` {prompt|prompts[], provider, model, endpoint, archetype, family, budget_usd} → `{jobId}`, `GET /api/new/stream?jobId=` (SSE: logs + cost + checkpoints + shots URLs), `POST /api/new/cancel`.
- Job runner: child `gamecraft-cli new --prompt ... --provider ...` (Godot) OR session runner for web (see §4). Timeout 10 min default, kill + `proc_guard` Job Object (CHANGELOG 0.13.0 leak fix — reuse it). Never leak Godot/Chromium (21 windows bug 2026-10-31).
- Auth: keys from env only, never logged, redacted in `run.json` (same rule as democraft sim).

Desktop stub (same contract, native):
- Menu `Game > New game…` → dialog: prompt box, preset dropdown (same 7), provider dropdown (Opus/Fable/Argon) + model/endpoint, family radio, budget spin ($10), Start/Cancel. Progress: reuses `verify_job` spinner pattern (`Run tests` → `Running...` + `row.spinner()` in `detail_buttons`), streams to Findings pane + Inspector `run.json` view. No engine work in v1 — dialog shells to `gamecraft-cli new` (like `just forge`), shows logs. Full in-process compile in v2.

## 4. Web RPG presets (copy-paste ready, from Mossbrook verbatim + reskins)

Emberwick Village (baseline, `web/games/mossbrook/game.json` prompts 1-4 verbatim):
1. angled top-down RPG, fantasy village, 1-2 companions, camera-side wall transparent on enter
2. NPCs, furniture, building types, some upstairs
3. non-flat, 2 basements + tunnel, rocky mountain + cave + sleeping troll
4. 4× area, fun mechanics, non-cliche plot + twists, magic system, really good

Space Station (same beats, new skin):
1. angled top-down RPG: player + 1-2 crew walk a ring station, entering a module turns camera-side wall transparent
2. NPC crew, consoles/bunks/labs, module types, some with upper deck
3. non-flat (split levels, ramps), 2 service ducts joined by tunnel, asteroid with cave holding sleeping alien
4. 4× modules, fun mechanics (oxygen, mag-boots, hacking), mutiny plot + twists, tech system, really good

Pirate Ship:
1. angled top-down RPG: player + mates walk a galleon, entering cabin turns camera-side wall transparent
2. NPC crew, hammocks/cannons/galley, deck types, some with orlop below
3. rolling sea (non-flat), 2 holds joined by tunnel, island mountain + cave + kraken
4. 4× ship+island, fun mechanics (rigging, cannon, parley), cursed-gold plot + twists, sea-magic, really good

Zelda-like (new archetype proposal):
- Overworld 64×64, 3 shrines (push stone → switch → key), locked boss door, hearts, 1 boss. Win: all shrines + boss. Self-test: BFS solver proves completable (reuse `gamecraft-sim` maze/crate solvers, extend to keys/doors). Step budget 60k. Thumb: boss door.

Sokoban (new archetype proposal):
- 5×5 tutorial → 9×9 vault, crates on targets, undo, par. Win: all targets. Solver: crate-push BFS (already in `gamecraft-sim`). Step budget 20k. Thumb: solved vault.

All presets emit `game.json` with `slug/title/category/family/entry/experiment/author/prompts/win_marker/thumb_checkpoint/step_budget` (Mossbrook schema). `win_marker="GameCraft: tour complete, win"`, checkpoints assert real state (layer drawn, wall opacity, floor height — `verify.ts` rule).

## 5. Cost control (tenner holds)

- Godot spec: small JSON, 1 repair round. Measured: `gemma4:12b` 11s but truncates/prose without `format:json`; `qwen3.8:27b` never loads (420s). Hence cloud-first default (`NEW_GAME.md`). gpt-4o <$0.10, Opus <$2.
- Web RPG: full three.js, 4 rounds, 50-100k out. Opus $15/$75/MTok → $5-10. Cap: max 4 rounds, no textures v1, `step_budget` per preset (Mossbrook 11537, Kaffeehaus 45001, Zelda 60k proposed). Abort on cap, keep partial.
- UI shows tokens in/out + $ live (price table in code, editable), Cancel kills child + Job Object (no 21-window leak).

## 6. Gates (same as depot + web, no new leniency)

- Godot: `scene_lint` clean, trace completes, Godot boots, `goal reached`. `thumb.png/play.gif/lint.json/trace.json/commands.jsonl` written (Prompt-to-Depot Visual Parity 0.13.0).
- Web: `window.__gamecraft` contract, headless Chromium zero errors, win tour in budget, `thumb.png + shots/` (verify.ts). `selfTest()` required for sims (Kaffeehaus rule: good bot beats random).
- `cargo test --workspace`, `clippy pedantic`, `fmt`, `just replays-check`, `bun run verify` (Node 24, not Bun — Playwright hangs under Bun), `pwa-check`. Never fake green.
- MCP: expose `forge_new/create_game` so shell-less clients can trigger (KIBITZ defect fix). CLI stays for humans/CI.

## 7. Risks

- Web RPGs are vibe-coded three.js — fun/complexity not provable, only boot/tour/checkpoints. Say so (web README already does: “does NOT prove fun or good code”).
- Long runs leak processes (Godot windows, Chromium). Reuse `proc_guard` Job Object + `verify.bat` detached pattern.
- Token burn without cap. Budget enforced server-side, not just UI hint.
- `.bak` sprawl (103 in forge once). `.gitignore` covers, clean before commit. Max 10 files per commit.
- Goliath stale python.exe hundreds (HANDOVER) — ram weeder before long verify runs.

## 8. Next (concrete, in order)

1. `web/new.html` + `serve.ts` routes + job runner (Godot path first, web path shells to session runner). Presets JSON from §4.
2. Desktop `Game > New game…` dialog stub (prompt + preset + provider + budget, shells to CLI, streams to Findings).
3. MCP `forge_new/create_game` (fix KIBITZ asymmetry).
4. New archetypes: `zelda-like`, `sokoban` (spec + solver + gate, then `new --prompt` supports them).
5. `just new-game --preset space-station --provider opus --budget 10` (CI-friendly entry, same as `just forge`).

*Seed: Mossbrook game.json (Emberwick 4 prompts verbatim), Kage-e/Benny/Kaffeehaus verify.json (all pass 2026-11-02), NEW_GAME.md provider table, verify.ts gate, desktop detail_buttons spinner pattern.*
