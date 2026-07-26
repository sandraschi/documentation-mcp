# Fleet Tool & Library Glossary

A crammable aide-memoire of every tool, library, and runtime in the fleet.

---

## Package Managers & Runtimes

| Tool | What | Command |
|------|------|---------|
| **uv** | Astral's blistering-fast Python package manager. Replaces pip/poetry. Lockfile: `uv.lock`. | `uv sync`, `uv run`, `uv add`, `uv build` |
| **npm** | Node.js package manager. Lockfile: `package-lock.json`. Fleet webapps use npm (not pnpm/yarn). | `npm install`, `npm run build`, `npx` |
| **bun** | All-in-one JS runtime + bundler + package manager. Not yet fleet-wide but preferred for new JS work. Lockfile: `bun.lock`. | `bun install`, `bun run`, `bunx` |
| **PyPI** | Python Package Index. `pip install` source. `pyproject.toml` declares deps; `uv sync` resolves against it. | `uv add package` |
| **pip** | Legacy Python installer. Still present on every machine. Fleet uses uv instead. | `pip install` (avoid) |

## Build & Distribute

| Tool | What | Command |
|------|------|---------|
| **hatchling** | Python build backend. Declared in `pyproject.toml` `[build-system]`. Produces wheels. | `uv build` |
| **PyInstaller** | Freezes Python apps into single .exe. Used for Tauri backend embedding. `strip=False, upx=False` mandatory on Windows. | `pyinstaller spec.spec --clean` |
| **Tauri** | Rust desktop app wrapper (v2). Replaces Electron. ~5 MB shell + WebView2. NSIS installer output. | `npx tauri build --bundles nsis` |
| **Vite** | JS/TS bundler and dev server. Fleet webapp standard. Fast HMR, Rollup-based prod build. | `vite --port 10949`, `vite build` |
| **Babel** | JS transpiler. Not used directly — Vite uses esbuild/Rollup instead. Legacy. | — |
| **esbuild** | JS bundler (Go). Used internally by Vite. Fleet never calls it directly. | — |
| **Rollup** | JS bundler (JS). Vite's production build engine. | — |

## Linters & Formatters

| Tool | What | Command |
|------|------|---------|
| **ruff** | Python linter + formatter (Rust). Replaces flake8 + isort + black. Fleet standard. Config in `pyproject.toml` `[tool.ruff]`. | `ruff check src/`, `ruff format src/` |
| **biome** | JS/TS/JSON linter + formatter (Rust). Replaces eslint + prettier. Fleet webapp standard. Config: `biome.json`. | `biome check --write src/` |
| **PSScriptAnalyzer** | PowerShell linter. Fleet standard for `.ps1` files. | `Invoke-ScriptAnalyzer -Path . -Recurse` |
| **markdownlint** | Markdown linter. | `markdownlint README.md` |
| **yamllint** | YAML linter. | `yamllint docker-compose.yml` |
| **taplo** | TOML linter/formatter. | `taplo format pyproject.toml` |
| **hadolint** | Dockerfile linter. | `hadolint Dockerfile` |
| **shellcheck** | Shell script linter (used in CI). | `shellcheck script.sh` |
| **actionlint** | GitHub Actions workflow linter. | `actionlint .github/workflows/*.yml` |

## Testing

| Tool | What | Command |
|------|------|---------|
| **pytest** | Python test runner. Fleet standard. Async tests via `pytest-asyncio`. Config in `pyproject.toml` `[tool.pytest.ini_options]`. | `pytest tests/ -v` |
| **Playwright** | Browser E2E testing. Fleet standard for webapp regression tests. Headless Chromium. | `npx playwright test` |
| **pywinauto** | Windows GUI automation (CUA smoke tests). Used for pre-release NSIS installer cert. | via `just cua-nsis-test` |
| **Tesseract** | OCR engine. Used by CUA smoke tests for screenshot verification. | `tesseract image.png stdout` |

## MCP Stack

| Tool | What | Notes |
|------|------|-------|
| **FastMCP** | Python MCP server framework. Fleet standard `>=3.4.4,<4`. Tools via `@mcp.tool()`, prompts via `@mcp.prompt()`, resources via `@mcp.resource()`. | `from fastmcp import FastMCP, Context` |
| **prefab-ui** | Rich in-chat UI cards for MCP tools. `@mcp.tool(app=True)` + `PrefabApp`. Fleet dependency `>=0.14.0`. | `from prefab_ui.app import PrefabApp` |
| **mcpb** | Anthropic's MCP bundle packer. Produces `.mcpb` files for Claude Desktop distribution. Manifest v0.2. | `mcpb pack . dist/name.mcpb` |
| **glama** | MCP registry indexer. `glama.json` at repo root for visibility. | — |
| **MetaMCP** | Fleet meta orchestrator (port 10718). Tool suites via registries. | `meta_mcp/tools/registries/` |

## Web Stack

| Tool | What | Notes |
|------|------|-------|
| **React** | UI framework. Fleet webapp standard (v18). | `createRoot`, functional components |
| **TailwindCSS** | Utility CSS framework. Fleet standard v3 (webapp), v4 (meta-mcp). | `bg-zinc-900 text-zinc-100` |
| **Framer Motion** | React animation library. Fleet standard for page transitions. | `motion.div`, AnimatePresence |
| **Lucide** | Icon library. Fleet standard. | `import { Send } from "lucide-react"` |
| **Zustand** | React state management. Fleet standard. Replaces Redux/Context. | `import { create } from "zustand"` |
| **react-router** | Client-side routing. Not always used — some webapps use switch/case. | `BrowserRouter`, Routes, Route |
| **react-query** | Server state / data fetching. TanStack Query v5. Used in goose-mcp, fleet-pr-mcp. | `useQuery`, useMutation |
| **date-fns** | Date utility library. | `format`, parseISO |
| **clsx** | Conditional class builder. | `clsx('base', isActive && 'active')` |

## Backend Stack

| Tool | What | Notes |
|------|------|-------|
| **FastAPI** | Python REST framework (on Starlette). Used when auto-docs needed. Fleet standard for REST-heavy servers. | `from fastapi import FastAPI`, auto-Swagger |
| **Starlette** | ASGI framework. Preferred over FastAPI for simple servers (≤5 routes, no Swagger needed). | `from starlette.applications import Starlette` |
| **uvicorn** | ASGI server. Runs all fleet HTTP backends. | `uvicorn.run(app, host, port)` |
| **httpx** | Async HTTP client. Fleet standard for outbound requests. | `await client.get(url)` |
| **curl_cffi** | Cloudflare-resistant HTTP client. Used for scraping Discourse/Reddit. | — |
| **SQLite** | Embedded database. Fleet standard for stateful MCP servers. WAL mode, busy_timeout=5000. | `sqlite3` (stdlib) |
| **LanceDB** | Vector database. Used for local RAG in arxiv-mcp, advanced-memory-mcp. | — |
| **pydantic** | Data validation. v2 mandatory. `model_dump()` not `dict()`. `model_validate()` not `parse_obj()`. | BaseModel, Field, Annotated |
| **python-dotenv** | `.env` file loader. Standard for config. Use `load_dotenv()` before reading. | `from dotenv import load_dotenv` |
| **Pillow** | Image processing (CUA smoke test screenshots). | `ImageGrab.grab()` |
| **psutil** | System metrics (CPU, memory, disk, processes). Used by monitor tools. | `cpu_percent()`, `virtual_memory()` |
| **pywin32** | Windows API bindings. Used for service control, event logs, ACLs. | `win32serviceutil`, `win32security` |
| **aiofile** | Async file I/O. Used in server modules. | `async_open` |

## Fleet Tools

| Tool | What | Command |
|------|------|---------|
| **just** | Command runner (Rust). Fleet standard. Recipes in root `justfile`. | `just lint`, `just test`, `just serve` |
| **fd** | Fast file finder (Rust). Fleet replacement for `Get-ChildItem -Recurse`. | `fd -e py src/` |
| **rg** | ripgrep — fast content search (Rust). Fleet replacement for `Select-String`. | `rg "pattern" src/` |
| **gh** | GitHub CLI. Used for PRs, issues, releases, CI checks. | `gh pr create`, `gh workflow run` |
| **ty** | Astral's Python type checker (rust-based). CI only, `continue-on-error: true` until green. | `ty check src/` |
| **pre-commit** | Git hook runner. Optional fleet standard with ruff. | `pre-commit install` |
| **py** | Windows Python launcher. | `py -3.12` |

## Windows-Specific

| Tool | What | Notes |
|------|------|-------|
| **NSIS** | Nullsoft Scriptable Install System. Tauri produces NSIS `.exe` installers. Hooks in `windows/hooks.nsh`. | — |
| **WebView2** | Edge-based webview runtime. Required by Tauri apps. Bundled on Win11+. | — |
| **WiX** | Windows MSI builder. Optional for enterprise deployment. | — |
| **Docker Desktop** | Local container runtime. Used for container stack repos (games-app, myai). | `docker compose up` |
| **winget** | Windows package manager. | `winget install Tesseract-OCR` |
| **scoop** | Windows user-mode package manager (without admin). | `scoop install just` |
| **OpenSSH** | SSH client/server. Built into Win10+. Used for Tailscale + remote access. | `ssh user@host` |

## Monitoring & Observability

| Tool | What | Notes |
|------|------|-------|
| **Prometheus** | Metrics collection. Fleet unified stack on ports 12000-12010. | `node_exporter`, `blackbox_exporter` |
| **Grafana** | Dashboarding. Fleet unified Grafana on port 12000. | — |
| **Loki** | Log aggregation. Fleet unified Loki on port 12002. | Promtail ships logs |
| **aiwatcher** | Fleet event router / webhook receiver. `GET /api/fleet/priority` on port 10717. | — |
| **admiral-mcp** | Alert escalation. Receives high-competency PR alerts. Port 11089. | POST `/api/fleet/alert` |

## Machine Learning & GPU

| Tool | What | Notes |
|------|------|-------|
| **PyTorch** | Deep learning framework. GPU-accelerated tensor compute. Fleet uses for local inference (not training). | `torch.cuda.is_available()` |
| **CUDA** | NVIDIA's parallel compute platform. Required for GPU acceleration on RTX 4090/3090. Toolkit + drivers. | `nvcc --version` |
| **cuDNN** | NVIDIA's deep neural net library. Ships with PyTorch. Optimized conv/RNN ops. | — |
| **ROCm** | AMD's CUDA equivalent. Not in fleet (NVIDIA-only shop). | — |
| **ONNX Runtime** | Cross-platform ML inference. Used by fast-embed, faster-whisper for CPU/GPU-agnostic runs. | ORT |
| **TensorRT** | NVIDIA's inference optimizer. Faster than raw CUDA for deployed models. | `trtexec` |
| **Stable Diffusion** | Text-to-image latent diffusion model. Run via ComfyUI or diffusers. | `from diffusers import StableDiffusionPipeline` |
| **ComfyUI** | Node-based Stable Diffusion workflow UI. API mode for headless gen. Port 11086. | `comfyops-mcp` integrates it. |
| **LoRA** | Low-Rank Adaptation — fine-tuning method. Small (10-200 MB) adapter files patched onto base models. | `lora:filename.safetensors` |
| **diffusers** | HuggingFace's diffusion model library. Python. Supports SD, SDXL, FLUX, etc. | `from diffusers import DiffusionPipeline` |
| **HuggingFace** | ML model hub. Source for most open models (transformers, diffusers). Also `huggingface_hub` library. | `HF_TOKEN` env var for gated models |
| **transformers** | HuggingFace's transformer library. BERT, LLAMA, Qwen, etc. | `from transformers import AutoModelForCausalLM` |
| **safetensors** | Safe serialization format for ML weights (no pickle). Replaces `.bin`/`.pt`. | `from safetensors.torch import load_file` |
| **GGUF** | Quantized model format for local LLM inference. Used by Ollama, llama.cpp. | `qwen3.5:27b-Q4_K_M` |
| **Ollama** | Local LLM runner. Pulls GGUF models, exposes OpenAI-compatible API on :11434. Fleet standard for local inference. | `ollama pull qwen3:14b`, `ollama run` |
| **LM Studio** | GUI Ollama alternative with built-in model browser. Port :1234. Also :8000 for compat. | — |
| **vLLM** | High-throughput LLM serving. Faster than Ollama for batch/API workloads. OpenAI-compatible. | Should have a dedicated GPU VM. |
| **llama.cpp** | C++ LLM inference engine. Backend for Ollama. Supports GGUF, GPU offload. | — |
| **faster-whisper** | Fast speech-to-text (CTranslate2 backend). Used by advanced-memory-mcp for dictation. | `model.transcribe(audio)` |
| **Kokoro** | High-quality neural TTS. Used by advanced-memory-mcp for voice. | `pip install kokoro` |
| **OpenCV** | Computer vision library (cv2). Used in CUA smoke tests for template matching. | `cv2.matchTemplate()` |
| **ffmpeg** | Universal media transcoder. Fleet standard for audio/video processing in MCP tools. | `ffmpeg -i input.mp4 output.mp3` |
| **Pinokio** | One-click app launcher for AI tools. Browser-based GUI that manages git clones + dependency installs. Runs local web UI. | `pinokio` (start via CLI) |
| **Gitingest** | One-shot text bundle of any public GitHub tree. No clone needed. `gitingest.com/owner/repo`. | `gitops` has `gitingest_link` tool. |
| **fast-embed** | Fast text embeddings (ONNX). Used by LanceDB RAG in arxiv-mcp, advanced-memory-mcp. | `pip install fast-embed` |

| Tool | What | Notes |
|------|------|-------|
| **Prometheus** | Metrics collection. Fleet unified stack on ports 12000-12010. | `node_exporter`, `blackbox_exporter` |
| **Grafana** | Dashboarding. Fleet unified Grafana on port 12000. | — |
| **Loki** | Log aggregation. Fleet unified Loki on port 12002. | Promtail ships logs |
| **aiwatcher** | Fleet event router / webhook receiver. `GET /api/fleet/priority` on port 10717. | — |
| **admiral-mcp** | Alert escalation. Receives high-competency PR alerts. Port 11089. | POST `/api/fleet/alert` |
