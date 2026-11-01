# Free Claude Code Evaluation (free-claude-code)

**Date:** 2026-10-14
**Status:** Evaluated - trial-approved in isolation, NOT installed on fleet hosts yet
**Sources:**
- https://github.com/Alishahryar1/free-claude-code (60,221 stars, 9,435 forks, v6.16.4 on 2026-10-13)
- `scripts/install.ps1` at main, 1996 lines, statically reviewed, NOT executed
- README via fetch, 2026-10-14

---

## 1. What it is

Local proxy + Admin UI + per-harness launchers. Sits between coding harnesses
and model providers and presents one model catalog.

- **11 harnesses:** Claude Code (`fcc-claude`), Codex (`fcc-codex`), Pi
  (`fcc-pi`), OpenCode 2 (`fcc-opencode`), Cline, Hermes, DeepSeek Harness,
  Grok Build, Muse Code, Aider, VS Code Chat.
- **61 providers:** NVIDIA NIM (default `nvidia_nim/nvidia/nemotron-3-super-120b-a12b`),
  OpenRouter, Groq, Together, DeepInfra, SiliconFlow, Chutes, Kimi, MiniMax,
  Cerebras, Ollama Cloud + local Ollama / LM Studio / llama.cpp, plus OAuth
  paths for ChatGPT subscription and GitHub Copilot subscription.
- **Claim:** 1.3B+ free tokens/month by aggregating free tiers. Free-tier
  limits are provider-controlled and may change.
- **Extras:** ordered Fallback Models across providers, per-tier routing
  (MODEL_FABLE / OPUS / SONNET / HAIKU), reasoning-effort override,
  optional RTK + Headroom token compression, browser-native Codex sessions,
  Discord/Telegram bots, voice notes via NIM or local Whisper.
- **License:** AGPL-3.0-only. Fine to run as a tool. Do NOT copy code into
  fleet repos.

## 2. Sandbox review - install.ps1 (static, no execution)

Reviewed `scripts/install.ps1` as fetched 2026-10-14. No code was run on
Goliath. Summary:

- **User-scope install, no elevation observed:** installs via
  `uv tool install --force --refresh-package free-claude-code --python
  cpython-3.14.7-windows-x86_64-none`. Isolated uv tool env, not system
  Python. Requires uv >= 0.12.13, bootstraps from `https://astral.sh/uv/install.ps1`
  if missing.
- **Upstream agent installs use official URLs:** `claude.ai/install.ps1`,
  `chatgpt.com/codex/install.ps1`, `pi.dev/install.ps1`,
  `opencode.ai/files/bin`, `hermes-agent.nousresearch.com/install.ps1`,
  `x.ai/cli/install.ps1`, npm `@deepseek-ai/dsh`, uv-tool Aider. Supply chain
  is upstream-official plus FCC itself.
- **Downloader hygiene is decent:** downloaded PowerShell is validated as
  valid PowerShell before invoke (rejects HTML proxy-replacement pages).
  Installer log goes to `~/.fcc/logs/install-<timestamp>-<guid>.log`.
- **Desktop integration is shortcuts only:** creates
  `~/Desktop/Free Claude Code.lnk` and Start Menu `Free Claude Code.lnk`
  pointing at `fcc-desktop.exe`, exports icon to `~/.fcc/app-icon.ico`.
  No HKLM writes, no scheduled task, no service, no firewall rule found in
  the script body. Leaves existing non-FCC shortcuts alone.
- **Interactive + DryRun:** prompts per-harness (at least one required),
  optional RTK+Headroom prompt, `-VoiceLocal` / `-TorchBackend cu130` /
  `-RtkHeadroom` / `-DryRun` flags. `-DryRun` prints commands without running.
- **Runtime shape (from README, not yet observed live):** `fcc-server`
  starts local proxy + opens Admin UI. Tray icon for open Admin / restart /
  quit. `fcc-server --version` for version check. `fcc-doctor` bundle for bug
  reports. `fcc-update` for updates. Proxy Authentication bearer-token option
  exists in Admin UI - enable it.

Not verified yet: default listen port(s), Admin UI auth default, exact env
rewrites per launcher (`ANTHROPIC_BASE_URL` style), uninstall completeness
(claims to remove `~/.fcc/` + launchers, keep uv/Python/agents).

## 2b. DryRun pre-flight 2026-10-14 (Goliath, no changes)

Ran local copy of `install.ps1 -DryRun` via pwsh 7. Result: `Dry run
complete. No changes were made.` Key lines:

- Plan: verify/install Claude Code, Codex, Pi, OpenCode, Cline, Hermes,
  DeepSeek Harness, Grok, Muse, Aider
- Already on PATH: `claude`, `aider` (verified via `--version`);
  OpenCode v1 found at `C:\Users\<user>\.opencode\bin\opencode.exe` (installer
  would install stable v2 / migrate)
- Would fetch: `pi.dev/install.ps1`, `hermes-agent.nousresearch.com/install.ps1`,
  `x.ai/cli/install.ps1`, `install-muse.ps1`, npm `cline` + `@deepseek-ai/dsh@latest`
- Would run: `uv tool install --force --refresh-package free-claude-code
  --python cpython-3.14.7-windows-x86_64-none free-claude-code`
- Would verify: `fcc-desktop, fcc-server, fcc-claude, fcc-codex, fcc-pi,
  fcc-opencode, fcc-cline, fcc-hermes, fcc-dsh, fcc-grok, fcc-muse, fcc-aider`
  in uv tool bin, plus `fcc-server --version`
- Would create: `C:\Users\<user>\.fcc\app-icon.ico` + 2 shortcuts (Desktop +
  Start Menu) to `fcc-desktop.exe`

## 3. Fleet fit

| Need | Does it solve it? |
|---|---|
| Give opencode / Claude Code access to free cloud models | Yes - `fcc-opencode`, `fcc-claude` are first-class |
| Local-first (Ollama, LM Studio, llama.cpp) | Yes - documented prefixes `ollama/`, `lmstudio/`, `llamacpp/` |
| Strata reuse | Plausible via Providers -> Custom providers with OpenAI-compatible base URL (`http://127.0.0.1:8080/v1`), then manual `<provider-id>/<model-id>`. NOT tested |
| Outage resilience via fallback list | Yes, in principle - ordered fallback models with per-fallback effort/key |
| Token cost reduction | Optional RTK 0.44.2 + headroom-ai[mcp]==0.40.0 path exists, opt-in at install |
| Fleet gateway / auth / spend control | No - single-user desktop proxy, not a multi-user gateway like LiteLLM |

## 4. Concerns

- **Release churn:** ~20 releases in 3 days up to v6.16.4 (2026-10-13).
  Actively maintained but fast-moving. Pin a version for any trial, do not
  auto-update mid-work.
- **Trust boundary:** full MITM over keys + ChatGPT/Copilot OAuth tokens.
  Treat host as sensitive while FCC runs. Use throwaway keys first, enable
  Proxy Authentication, keep `~/.fcc/` out of backups/repos.
- **AGPL-3.0-only:** run it, do not vend it.
- **Free-tier fragility:** quotas and model IDs change provider-side. The
  provider table in README will rot. Expect model-picker drift.
- **Windows specifics:** cpython-3.14 x64 even on ARM (emulation note in
  script). Local Whisper on Windows needs `-VoiceLocal`, CUDA via
  `-TorchBackend cu130`. Keep terminal open for `fcc-server` on Linux;
  Windows/macOS use desktop launcher + tray.

## 5. Recommended trial (NOT done yet)

1. Pre-flight: re-fetch `scripts/install.ps1`, run installer with `-DryRun`
   first and read the plan.
2. Isolated host or VM first, NOT Goliath main. Pin version if possible.
3. Install with minimal harnesses (e.g. OpenCode only), skip
   `-VoiceLocal` and `-RtkHeadroom` on first pass.
4. Start `fcc-server`, enable Proxy Authentication, add ONE throwaway key
   (NVIDIA NIM from `build.nvidia.com`), set MODEL, Apply.
5. Test `fcc-opencode` against a scratch repo. Then test Custom provider
   pointing at Strata. Record actual ports + env rewrites.
6. `fcc-doctor` output saved with the trial notes before any fleet rollout.

## 6. Decision

Trial-approved in isolation. No install on Goliath or fleet hosts until step
5 notes exist. Next action is a VM trial with `-DryRun` log + `fcc-server`
port/env capture.
