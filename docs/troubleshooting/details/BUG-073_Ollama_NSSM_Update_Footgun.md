# BUG-073 — NSSM-wrapped Ollama + Inno auto-update = headless engine, green health checks

**Date:** 2026-10-10
**Severity:** P1 (all Ollama inference fleet-wide dead; `/api/tags` still 200 masked it)
**Component:** Goliath Ollama install (`%LOCALAPPDATA%\Programs\Ollama`), deleted `ollama-serve` NSSM service
**Status:** Fixed (service deleted 2026-10-10; stock autostart owns :11434)

## Symptom

`monitoring-mcp` chat logged `AI call failed, returning tool list: Server error
'500 Internal Server Error' for url 'http://127.0.0.1:11434/api/generate'`.
Direct repro returned:

```json
{"error": "error starting llama-server: llama-server binary not found
(checked: .../Ollama/llama-server.exe, .../Ollama/lib/ollama/llama-server.exe, ...).
Run 'cmake -S llama/server --preset cpu && cmake --build --preset cpu' first"}
```

Meanwhile `GET /api/tags`, `ollama show`, and `ollama ps` all worked, `loaded`
was `[]`, VRAM sat 22/24 GB free. Catalog reads need only manifests; only
inference needs the runner — so every fleet health probe that checks tags
reported healthy while every generate/chat call 500'd.

## Timeline (evidence)

- `ollama.exe` dated 2026-10-02, `ollama app.exe` 2026-10-08 18:17, `lib/`
  gutted (only `Ollama.lnk` left) 2026-10-08 23:48. Partial Inno update.
- `is-*.tmp` debris in the install dir dated May / Aug / Sep 2026: the updater
  had been failing the same way for months.
- Defender exonerated: no `ollama`/`llama` hits in `Get-MpThreatDetection` or
  the Defender Operational log. `OllamaZombieSweep`
  (`arxiv-mcp/scripts/Remove-OllamaZombies.ps1`) exonerated: kills processes
  only, never deletes files.
- `ollama-serve` NSSM service (System event 7045) created **2026-10-10 04:42**,
  running `ollama.exe serve` as LocalSystem FROM the install dir. It did not
  cause the Oct 8 damage, but re-armed the identical trap for the next update.
- Binary is genuine (Authenticode: Ollama Inc., DigiCert, valid 2026–2029);
  the `cmake ... first` string is stock Ollama's generic runners-missing
  fallback, not a dev build.

## Root cause

Inno Setup deletes old files before writing new ones, with no atomic
rollback. Our NSSM service held `ollama.exe` locked as SYSTEM from inside the
install dir; the user-context updater could not stop it (it does not know our
custom service exists — stock Ollama only manages its own per-user
processes), skipped the locked files, reported success, and left `lib/`
gutted. Crash-protection was never needed: `ollama serve` has no crash
history on this box, and stock Ollama already autostarts twice
(`Ollama.lnk` → `ollama app.exe`, `OllamaServer.lnk` → `ollama.exe serve`).
The NSSM wrapper additionally caused a login-time double-bind race for :11434
(two listeners observed) and SYSTEM-owned processes that fleet tooling cannot
inspect or kill gracefully.

## Resolution (2026-10-10)

1. `sc.exe stop ollama-serve` (old PID drained), winget upgrade to 0.40.2,
   verified `lib/ollama/` repopulated (cuda_v12, cuda_v13, rocm_v7_1, vulkan).
2. `sc.exe stop` + `sc.exe delete ollama-serve` (1060 confirms gone).
3. Single stock user-mode `ollama.exe serve` owns :11434 (one `::` listener);
   `/api/generate` smoke test 200 (`llama3.2:3b` replied OK).
4. New guard script `arxiv-mcp/scripts/Update-OllamaSafe.ps1`: stop service,
   winget, VERIFY runners before restart (refuses to restart headless), start,
   verify port owner + real inference. Syntax-checked, zero errors.

## Sibling audit (Bug Discovery Protocol)

All other NSSM services with binaries under `C:\Users`
(arxiv-mcp, discord-mcp, email-mcp, fastsearch-mcp, fleet-hub, LiveKitSFU,
mcp-federation-hub, mcp-pywinauto-mcp) wrap fleet repos under `D:\Dev\repos`
— our code, no vendor auto-updater fighting them. `ollama-serve` was the only
service wrapping a self-updating third-party binary. No further action.

## Rules

1. **Never NSSM-wrap a self-updating vendor binary.** If the vendor updater
   cannot see and stop your service, the next update runs against locked files.
2. Ollama updates go through `Update-OllamaSafe.ps1` only, never unattended
   auto-update against a live server.
3. An Ollama health check that only hits `/api/tags` is a false-green
   machine (same class as BUG-021/024). Smoke-test real inference
   (`/api/generate`, tiny prompt) or check the error body for
   `llama-server binary not found`.
