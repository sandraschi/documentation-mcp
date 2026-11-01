# ADN 2026-09-26-003 - CUA-first plan (cua_ops high)

Tags: plan, cua, robofang, cost, parity
Project: main (memops fallback)

Decision: robofang cua_ops P0. Thin glue over pywinauto-mcp 10789 (cua_env/HUD/vision/OCR/HITL) + uitars-mcp 10976 (mss+pyautogui, Playwright, qwen2.5-vl:7b local) + speech-mcp 10909 (FunASR :10914, voice bus) + deepfang 10956 gate + secrets-mcp resolve-never-raw.

1A observe-only 1d 0 cost: screenshot+ground, no clicks.
1B gated action 2d cents: click/type/browser + confirm queue + snapshot, deterministic locator first then VLM, HITL kill-switch.
1C voice loop 1-2d: wake->intent->cua->speak.

Then: deepfang POLICIES+checkpoint+per-agent lease 2-3d, fritz destructive via deepfang + zoning + templates 2d, robofang Bastio+container-per-skill+budgets+QR bind 2d, aiwatcher rotate+gate 4h.

Critical path ~6-7d to voice CUA + safe fritz. Local-first 0 marginal, DeepSeek cents/1k HIGH only.

Full: research/2026-09-26-fleet-cua-first-implementation-plan.md
