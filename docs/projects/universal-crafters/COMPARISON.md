# Universal Crafters — Head-to-Head Comparison

**Date:** 2026-11-07 · **Evidence:** live GitHub + fal.ai + rea.tools fetches same day,
local `_upstream/` checkouts, fleet `research/2026-11-01-*` teardowns.

Thesis first: **makers make from zero, cloners start from something that works.**
A bookkeeping app from a prompt is a maker demo. Cloning YOUR bookkeeping
website, keeping its flows, then making it better — that is the new category.
Only two FOSS projects do it end-to-end. Everything else is a part.

## 1. The matrix

| Dimension | REA `morluto/rea` (rea.tools) | Craft Anything `storytold/craft-anything` | fal.ai | Classic makers (v0 / Lovable / Bolt / Replit / same.new) | FOSS screenshot-to-code |
|---|---|---|---|---|---|
| **Job** | Understand anything. Oracle. | Understand → rebuild your own. Cloner. | Render any asset. Foundry. | Generate from prompt. Maker. | Prompt-or-shot → code. Starter. |
| **Input** | Binary, APK, ASAR, URL, HAR, pcap, firmware | URL, app window, binary, game, folder | Prompt / image / LoRA | Prompt (+ screenshot in newer versions) | Screenshot / URL |
| **Output** | Pseudocode, call graph, evidence ledger | Fresh project in `app/` + `checks/` diffs + `craft.json` | PNG / MP4 / GLB URL | Deployed web app (React/Next) | HTML/Tailwind/React |
| **Rebuild loop** | No. You + agent rebuild by hand (showcases prove it: DX-Ball C, Notion clipboard). | Yes. Study → Build → Check → Ready, agent-driven, 3-width visual diff, refine. | No. Single inference call. | Yes but shallow: prompt → deploy → prompt again. No evidence ledger. | No. One shot. |
| **Stack** | TypeScript/Node 22/24/26, Turborepo, bridges to Hopper/Ghidra/IDA/Kuna/JADX | 100% Rust, 13 crates, own disassembler/decompiler, egui + CLI + MCP (320 tools = 1 tool × 3 surfaces) | Hosted GPUs, OpenAPI per model, `llms.txt` per endpoint | Hosted React/Next, proprietary | Python + VLM (GPT-4V/Claude), local or hosted |
| **AI model** | Bring your agent (Claude Code, Codex, Cursor, Gemini, Grok). REA is tools, not brain. | Bring your coder: Claude Code `claude` natively (your sign-in, never sees account); Codex experimental; Copilot/Grok via ACP; local OpenAI-compat for Q&A. Heavy use = your subscription/key. | Per-model weights (Flux, Kling, Trellis-2, Meshy, Tripo, Hunyuan). Billed per output. | Their cloud model (baked into seat price). | Your VLM key. |
| **Locality** | Analysis runs locally. Agent's model policy is yours. | Engine local. Builder local. Optional fal.ai pictures/3D = your fal key, off by default. | Cloud by default. BYO-cloud via Serverless GPUs ($1.99–$12.99/h). Self-host weights yourself if you have VRAM. | Cloud. Export sometimes. | Fully local-capable (Ollama vision + code model works, quality gap noted). |
| **Legal posture** | Investigator-responsible. Disclaimer + SECURITY. Supports IDA (bring own license). | **Clean-room default** (refuses internals; screenshots/layout/fonts only) + Deep opt-in (Ghidra auto-install, no IDA — avoids piracy/liability). Rebuilds told NOT to copy logos/photos/text without ownership. | Standard gen-AI ToS + Verify fal-Generated Content. | Their ToS, their hosting. | Yours. |
| **Stars / forks** | 439k / 108.8k (outlier — ecosystem effect + 6,640 commits) | 19.3k / 3.6k (468 commits, early alpha, Nov 2026) | Private co. (1.5M devs claimed) | Private cos. | 5k–80k depending on repo |
| **License** | MIT (third-party notices; commercial engines BYO-license) | MIT OR Apache-2.0, brand-gated (forks strip ArtCraft marks) | Proprietary API + open weights proxied (Flux schnell etc.) | Proprietary | MIT/Apache mostly |
| **Price** | Free + your agent sub. Hopper optional paid. | Free + your Claude sub/API + optional fal cents. | Pay-per-output (e.g. Trellis-2 $0.25–0.35) + optional GPU hours. No seats. | $20–$50/seat/mo + overages. | Free + your VLM cents. |
| **Physical things** | No. Binaries, not bodies. | No (explicit: no JTAG/SWD/PCB/Gerber/silicon; build outputs software only). | Partial: image-to-3D (Trellis-2/Meshy/Tripo/Hunyuan → GLB) but no CAD-edit, no slice, no print. | No. | No. |

## 2. What each one is NOT (the common confusion)

- **fal.ai is not a universal crafter.** It never studies, never checks, never
  refines. It is the tile oven Craft Anything optionally fires pots in. Pricing
  table 2026-11-07: Trellis-2 GLB $0.25–0.35, Nano Banana Pro $0.15/img,
  Kling v3 Pro $0.14/sec, H100 serverless $4.50/h list. No seats, no free tier
  on the public page. Correct mental model: inference wholesaler.
- **REA is not a builder.** Its RL-environments export (`session.har` → runnable
  AgentEnv) looks like building but it builds a *test harness*, not your app.
  The build step is always your agent reading REA evidence. That is why REA has
  350+ tools and zero `rebuild` commands, while Craft Anything has `rebuild`.
- **Craft Anything is not a maker.** `rebuild - "A snake game in Rust"` works,
  but the happy path is `rebuild https://example.com "Recreate this website"`.
  Evidence records carry confidence/coverage/limitations — maker tools never
  show you what they didn't see.

## 3. Moats, honestly scored

1. **REA moat = breadth + community proof.** 30+ target classes (Go modules,
   CUDA fatbins, GGUF, IL2CPP v24–39, Godot PCK 2–4, Rust auditable, PE certs,
   BEAM, WASM, EVM, SQLite, PyInstaller, JEB, Flutter, Binwalk/Unblob,
   TShark, sigrok). No one reproduces that matrix in a quarter. Weakness:
   Node.js weight + commercial-engine licensing friction (Hopper/IDA/JEB BYO).
2. **Craft Anything moat = loop + law.** The Check step (perceptual diff at 3
   widths, game self-test, runtime run) is what makers skip and REA leaves to
   you. Clean-room enforcement is a legal feature, not a filter: corporate
   users can run it without a lawyer in the room. Weakness: alpha, Claude-first
   (Codex/Copilot/Grok adapters unverified or thin), website checks ahead of
   app/game behaviour checks.
3. **fal moat = speed + catalog.** 1,000+ models, 10× inference claim, 99.99%
   uptime claim, post-trained variants (FLUX 3 Max, H3 Max) co-optimized with
   their stack. Weakness: pure toll road — no lock-in beyond speed, weights
   leak to self-hosters (LTX-2.5 is open-source on their own platform).
4. **Makers moat = deploy.** v0→Vercel, Bolt→StackBlitz, Replit→Replit — one
   click live. FOSS cloners have no deploy. Craft Anything previews locally;
   REA doesn't deploy at all. Whoever adds one-click deploy to a clean-room
   cloner eats the makers' lunch from below.

## 4. Gold-rush map (where the money/proliferation is)

- **Layer 1 — Oracles (FOSS, free):** REA, Craft Anything engine (inspect half).
  Proliferation driver: MCP made tools portable; every agent wants them.
- **Layer 2 — Brains (BYOK, sub/API):** Claude Code, Codex, Copilot, Grok,
  local Qwen/GLM via OpenAI-compat. Proliferation driver: heavy use is now
  normal — a single clone-check-fix loop burns 10–50k tokens; subscriptions
  beat per-seat builders.
- **Layer 3 — Ovens (pay-per-asset):** fal.ai, Replicate, Together, self-hosted
  Trellis/Hunyuan. Proliferation driver: pictures + 3D on demand, cents each.
- **Layer 4 — Verifiers (missing, opportunity):** visual diff, behaviour test,
  license scrub, print-slice check. Craft Anything started it (checks/); no
  one productizes it standalone yet.
- **Layer 5 — Bodies (missing, biggest gap):** photo → mesh → editable CAD →
  slicer → makerspace. See PHYSICAL_LOOP.md. No cloner touches it.

Bottom line for Sandra: bet on Layer 1 local + Layer 2 BYOK + Layer 3 cents.
Avoid Layer-0 mistake: paying a seat to a maker that can't clone what you own.
