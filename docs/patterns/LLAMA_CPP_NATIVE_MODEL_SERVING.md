# Serving a bleeding-edge GGUF model natively with llama.cpp (fleet pattern)

**Established:** 2026-08-11 (Muse Glimmer 30B breakthrough)
**Reference impl:** `D:\Dev\models\muse-glimmer\` + proxy at
`C:\Users\<user>\AppData\Local\Temp\opencode\muse-proxy\proxy.py`

**Goal:** Run a just-released model at full GPU speed when Ollama and llama.cpp
*releases* do not support it yet, and integrate it with opencode without the
integration falling over.

## When to use

- Model released < 72h ago, GGUF uses a quant format or architecture that
  `ollama create` rejects (`failed to validate GGUF with llama-quantize`) or
  llama.cpp release builds do not know (`unknown model architecture`)
- User needs the model NOW, not "when the ecosystem catches up"

## Decision: Ollama vs native llama.cpp

| Check | Verdict |
|-------|---------|
| `ollama create` succeeds | Use Ollama (port 11434), done |
| `ollama create` fails on quant format | Native llama.cpp server |
| Release llama-server says `unknown model architecture` | **Build from master** with CUDA |

## Build from master (Windows, CUDA, ~30 min)

```powershell
# 1. CUDA toolkit (needs UAC): winget install Nvidia.CUDA --accept-package-agreements --accept-source-agreements --silent
# 2. Clone + build in ONE shell with vcvars env (env does not persist between shells)
git clone --depth 1 https://github.com/ggml-org/llama.cpp D:\Dev\tools\llama.cpp\src
# in one command: parse vcvars64.bat env to temp file, apply, then:
cmake -B build -G Ninja -DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release `
  -DCMAKE_CUDA_COMPILER="C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.3\bin\nvcc.exe" `
  -DCUDAToolkit_ROOT="C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.3" `
  -DCMAKE_CUDA_ARCHITECTURES=89   # single arch = fast build; 89 = RTX 4090
cmake --build build --parallel 16
```

**Gotcha:** freshly built exes crash with `0xC0000135` (DLL not found). The CUDA
toolkit installs no runtime DLLs into its bin. Download the matching
`cudart-llama-bin-win-cuda-13.3-x64.zip` release asset and copy
`cublas64_13.dll`, `cublasLt64_13.dll`, `cudart64_13.dll` next to the exes.

## Server flags that matter (Muse Glimmer example)

```powershell
llama-server.exe -m model-kquant-17gb.gguf --mmproj mmproj-kquant.gguf `
  --model-draft dflash-kquant.gguf --port 11439 --host 127.0.0.1 -ngl 99 `
  --ctx-size 131072 --chat-template-file muse-template.jinja `
  --reasoning on --reasoning-format deepseek --reasoning-budget 1024
```

| Flag | Why |
|------|-----|
| `--chat-template-file` | GGUF's embedded jinja may fail to load (`chat_format: Content-only` in /props) -> broken prompts. Extract via mmap from the GGUF (`tokenizer.chat_template` key) and pass explicitly |
| `--reasoning on --reasoning-format deepseek` | Reasoning models: thoughts land in `reasoning_content`, content stays clean |
| `--reasoning-budget 1024` | Template forces high reasoning strength; without a budget the model thinks for 4K+ tokens before answering |
| `--model-draft` | DFlash/speculative drafter: ~3x tokens/s |
| `--jinja` | Deprecated in master; use --chat-template-file |

## The opencode integration problem

opencode **ignores `limit.context`** for custom providers: it sends the full
session (~208K tokens for a heavy session) regardless of the configured limit,
and its 409-tool MCP catalog adds ~102K tokens of schemas per request.

**Solution: truncating reverse proxy on the port opencode already uses.**
opencode keeps pointing at :11435; the real server moves to :11439; the proxy
rewrites requests. No opencode restart needed after moving the server.

Proxy responsibilities (all four are required):

1. **Truncate the system prompt** to ~10K chars and prepend a direct-chat
   directive. The full fleet instructions (77K) trigger agent-init behavior
   ("Ready.", "context loaded", "let me load the standards first") on
   agent-trained models - including announcing tool actions it cannot take.
2. **Pin the last user message** - never let history trimming eat the actual
   prompt (this produced silent "nothing happens" failures).
3. **Count and trim tools**: `POST /tokenize` on the tools JSON; trim history
   with tools cost included. When the full catalog is too big, **filter to a
   curated whitelist** (`bash`, `read`, `write`, `edit`, `glob`, `grep`,
   `todowrite`, `question`, `skill`, `apply_patch`, `webfetch`) - ~10-15K tokens
   fits under budget and keeps the model capable of real work. Only drop all
   tools when even the whitelist does not fit.
4. **Append a "you have NO tools" note** to the system prompt whenever tools
   were dropped entirely - otherwise the model believes it has tools (the
   truncated system text says so) and announces actions it cannot perform.

Extra guardrails: count tokens via the upstream `/tokenize` endpoint (not
chars/4 - the 200K-vocab tokenizer is not 4 chars/token for all text, though
measured 1.0x on fleet markdown); keep the last user message in all cases.

## Verification checklist

- [ ] `GET /health` on proxy AND server
- [ ] Non-stream + stream chat through the proxy both return content
- [ ] Huge history (200K+) request through proxy answers correctly
- [ ] Huge tools array request through proxy answers (tools dropped)
- [ ] Reasoning present in `reasoning_content`, content clean, `finish: stop`
- [ ] No "Ready"/"context loaded"/announce-then-stall responses

## Fleet registrations (after model works)

- `opencode.json`: provider entry (`local-llama`), `limit.context` = model window
- `local-llm-mcp/config.yaml`: `providers.local-llama` entry (requires the
  `providers` field on `Config` - it was being silently dropped by pydantic)
- `advanced-memory-mcp adn_llm`: add a provider probe mirroring the lmstudio block
