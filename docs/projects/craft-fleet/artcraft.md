# ArtCraft — Assessment

**Repo:** `D:\Dev\repos\artcraft` · **Date:** 2026-11-05 · **Grade: A (reference, not fleet-owned)**

## What it is

Storytold's creative-media suite: design, publishing, variable-data typesetting,
slide decks (DesignCraft, WordCraft, DeckCraft, GridCraft, FilmCraft + more) —
16 `*-cli.exe` installed under `C:\Program Files\*Craft`. This is the **upstream
reference implementation** of the ArtCraft pattern, not a sandraschi fleet repo.

## Model / verbs

- **Model:** document/project per app (`*.cany` for Craft Anything).
- **Verbs per CLI:** `run` (one-shot), `serve`/`--connect` (sessioned),
  `mcp` (agent protocol), `tools` (surface inventory) — see rebuild PLAN App. B
  matrix (measured 2026-11-02): CAD/Effect/Film/Photo `run`-only; Deck/Fig/Sound/
  Texture `serve`; Design/Grid/Light/Vector/Word bridge-to-open-window.
- Registry precedent: `democraft-mcp` `crafts.py` (exe, verbs, HERO, family) +
  `recipes.py` + `data/craft_compat.json` (104 verbs across 13 CLIs).

## Architecture

Rust monorepo: `artcraft-native` (pure-Rust egui desktop, no Tauri/webview),
`crates/{api_clients,desktop,lib,schema,testing,vendor}`, `frontend/`,
`Cargo.lock`, `rustfmt.toml`, SonarCloud, Cranky. Confinement flags
(`--automation-read-root/--write-root`, `--allow-path`, `--root`) are the
pattern every fleet craft copies.

## Strengths

- The pattern donor: one binary = human CLI + agent MCP; headless-first;
  `serve` only when startup >200 ms or screenshots mid-run are needed.
- Real desktop apps + real CLIs + CI + Sonar — the bar the fleet measures against.
- Democraft integration is live (gallery, contact sheets, Ctrl+K).

## Gaps / risks (for the fleet, not upstream)

- Not ours: never modify, never fork-casually; read-only unless a reason exists.
- 16 CLIs create enablement confusion in `opencode.json` (currently: design/fig/
  pdf/solid/game/democraft/craft-anything/texture on; cad/deck/effect/film/grid/
  light/photo/sound/vector/word installed-but-off). Keep the on/off rationale written.
- License/patent posture of upstream outputs (LEN lesson) stays the fleet's problem
  when crafts consume ArtCraft artifacts.

## Next 3 steps (fleet side)

1. Keep the Appendix-B serve/connect matrix current (re-measure on CLI upgrades).
2. Keep `craft_compat.json` baselines green after every upstream CLI update.
3. Document the on/off enablement policy next to `opencode.json`, not in chat.

## Verdict

Grade A as reference, ungraded as fleet property. Every craft spoke cites it;
none of them re-implements it. Treat accordingly.
