# Universal Crafters — Economics & BYOK (heavy AI, local control)

**Date:** 2026-11-07 · **User constraint:** heavy AI use, needs powerful models,
but must run locally with BYOK. This note shows the math.

## 1. The cost shape of a clone (real numbers)

A single website clone → improve loop (Craft Anything, Claude Code builder):

- Study: ~5–15k tokens (DOM/CDP/evidence summaries, not raw dumps — paging via
  `core_evidence_browse` keeps it bounded).
- Build × N rounds (N=2–4 typical): 30–120k tokens (agent writes a whole app).
- Check diffs + fixes: 10–40k tokens.
- **Total: ~50–175k tokens per finished clone.** At Claude Sonnet API rates
  (~$3/$15 per M in/out, blended ~$6–9/M for this mix) = **$0.30–$1.60 code
  cost**. With a Claude Pro/Max subscription ($20–$200/mo) driving the CLI,
  marginal cost → €0 until the seat cap.

A single matrioska lift (photo → GLB):

- fal Trellis-2: **$0.25 (512p) / $0.30 (1024p) / $0.35 (1536p)** — fixed,
  no subscription, counts against project budget (`project_assets_budget`).
- Local TRELLIS/Hunyuan-mini: **€0** after one-time setup on the 4090.
- Nano Banana Pro picture for Craft Anything: **$0.15**; plain Nano Banana
  **$0.0398** — use cheap for drafts, Pro for hero shots.

A maker seat (Vercel v0 / Lovable / Bolt / Replit, $20–$50/mo) buys ~100–300
generations then meters. One serious clone month = one seat + overages, and
you still can't self-host, still can't Deep-inspect, still can't print bodies.

## 2. BYOK doctrine (fleet position)

1. **Brain BYOK:** Craft Anything never sees your Claude login — it shells to
   YOUR `claude` CLI, YOUR `copilot`/`grok` ACP, YOUR `OPENAI_COMPATIBLE`
   endpoint (Ollama Qwen/GLM local). Revoke centrally, audit locally. No
   vendor holds the keys to your shelf scans.
2. **Oven pay-per-fire:** fal.ai/Replicate hold NO subscription. Fund a small
   prepaid balance, set per-project asset budgets (Craft Anything already
   tracks spend vs budget), route drafts local / finals hosted.
3. **Engine local:** REA + Craft Anything inspect on Goliath (no upload).
   REA states it; Craft Anything enforces Clean-room in-code. Model-provider
   data policy (Anthropic/OpenAI/your Ollama) is the ONLY exfil surface —
   document it per run for customer work.
4. **Heavy is fine when metered:** a 125B local model (Strata/Qwen-Flash on
   the 4090, see `research/2026-10-05-strata-*`) + cloud frontier for codegen
   is cheaper than any seat-wall once you pass ~10 clones/mo. Rule of thumb:
   <5 clones/mo → subscription only; 5–20 → sub + fal cents; 20+ or daily
   figurines → add local weights (TRELLIS-mini, Hunyuan-mini, Qwen-Coder).

## 3. What to never pay for twice

- Don't pay a maker seat AND fal cents for the same picture — Craft Anything
  generates via YOUR fal key at cost; makers mark the same call up inside
  the seat.
- Don't pay Hopper AND Ghidra for the same binary — REA drives either;
  Craft Anything auto-installs Ghidra free and skips IDA deliberately
  (license + piracy liability). One free engine per target.
- Don't pay cloud GPU hours for a mesh you can lift overnight — queue local
  TRELLIS for drafts (4090 idle = free), reserve fal Trellis-2/Meshy-T2.5 for
  the one glamour pass before the makerspace.

## 4. Budget template (copy into `craft.json` / project notes)

```json
{
  "code_budget_tokens": 200000,
  "asset_budget_usd": 5.0,
  "asset_costs": { "trellis2_1024": 0.30, "nano_banana_pro": 0.15, "meshy_t2": 0.20 },
  "route": "drafts local (TRELLIS-mini/Hunyuan-mini/Ollama), finals via fal + Claude sub",
  "usb_note": "makerspace print cost separate (filament + machine time)"
}
```

## 5. Bottom line

Maker seats tax curiosity. BYOK + local engine + per-asset oven taxes only
success. For Sandra's volume (dozens of sites/apps/games + shelf figurines),
the fleet bet is: **Claude subscription (brain) + Goliath 4090 (muscle) +
fal prepaid (oven)**. Everything in this section is chosen to keep that bill
under €50/mo excluding filament.

## 6. fal.ai rent check (2026-11-07 addendum — Sandra's call, verified direction)

fal's catalog lead is real: props, styles, scenes, worlds, character/reference
pipelines no FOSS hub matches in one API. That breadth is WHY the toll works:
one endpoint per trick, each metered (Trellis-2 $0.25–0.35/pop, image edits
$0.04–0.15, video $0.01–0.14/sec, GPUs $2–13/h). No seats, no free tier on the
public page, prepaid credits that evaporate per click. Brutally expensive at
volume, textbook rent on other people's weights + their serving stack.

Prediction logged: no physical-make support today (no slicer, no tolerance,
no mill/print routing), but it is the obvious next endpoint family — fal +
2–3 physical-maker corps (US print/mail + PRC mill/fulfilment) as
`print-this-GLB` / `mill-this-STEP` paid calls. Convenient, and the highest
margin in the chain (atoms cost more than tokens, failures cost postage).
Fleet stance: never route a body through a toll endpoint that cannot show
watertight + walls + scale first. Keep lift/repair/CAD/BIM/slice local
(splatcraft/makercraft/modcraft/cadcraft, TRELLIS-mini/Hunyuan-mini,
Blender/trimesh/Orca, IfcOpenShell), spend fal cents only on the glamour
render or the final texture pass. If fal ships print endpoints, consume them
like any vendor: one `checks/body.md` line per dollar, local fallback always
green, USB-stick-to-makerspace as the free exit.
