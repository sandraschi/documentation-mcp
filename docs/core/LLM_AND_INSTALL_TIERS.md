# LLM, External Dependencies, and Install Tiers

**Status**: ACTIVE — normative for all sandraschi MCP repos  
**Adopted**: 2026-05-28  
**Supersedes**: ad-hoc per-repo assumptions about bundling Blender, models, or Docker

---

## One-line rule

**Ship the MCP bridge and UI. Document and detect everything else. Never ship multi-GB hosts or model weights.**

---

## Scope

| Applies when | Required docs |
|--------------|---------------|
| Repo wraps an external app (Blender, Unity, Inkscape, GIMP, …) | `INSTALL.md` host-app prerequisites |
| Repo uses local or cloud LLM (script gen, chat, RAG, vision) | `INSTALL.md` LLM section + `docs/CONFIGURATION.md` |
| Repo ships Tauri native installer | Bundle rules in this doc + [tauri_godot_sota.md](./rules/tauri_godot_sota.md) |
| Repo offers `docker compose` | Optional / power-user only unless observability or multi-container is the product |

Repos with **no** LLM features and **no** host app may omit the optional INSTALL subsections (mark `N/A` in DEVELOPMENT.md if auditors ask).

---

## User tiers (inference and support)

Every LLM-capable repo must support **at least two paths**: guided local **or** cloud API. Weak-PC users are not second-class.

| Tier | Profile | Primary LLM path | Install support level |
|------|---------|------------------|------------------------|
| **A — Local beginner** | Wants MCP; normal PC; may not have Ollama yet | **Ollama** or **LM Studio** + one documented starter model | **Full:** winget/links, `ollama pull`, Settings auto-detect |
| **B — Weak / no GPU** | Low RAM, no NVIDIA, old laptop | **Cloud API** (OpenCode, DeepSeek, OpenRouter, OpenAI-compatible) | **Full:** API key + base URL in INSTALL and Settings; no local model steps required |
| **C — Power user** | Homelab, RTX box, already runs inference | **vLLM** or custom OpenAI-compatible URL | Document env vars; no bundling; see [LOCAL_LLM_STANDARDS.md](./LOCAL_LLM_STANDARDS.md) for workstation tuning |
| **D — Developer** | Contributor, clone + uv | Any of A/B/C via config | Option D + `docs/DEVELOPMENT.md` |

**Interpretation:** Missing Ollama/LM Studio does **not** mean unsupported. It means route the user to **Tier A** (install local) or **Tier B** (cloud).

---

## LLM substrate — what to ship vs document

### Runtime managers (never bundle in Tauri/PyInstaller/.mcpb)

| Runtime | Audience | In installer? | In INSTALL.md? |
|---------|----------|---------------|----------------|
| **Ollama** | Tier A default | **No** | **Yes** — install + example model |
| **LM Studio** | Tier A (GUI-preferring) | **No** | **Yes** — download + load model |
| **vLLM** | Tier C only | **No** | Optional advanced section |
| **OpenCode** (`opencode serve`) | Tier B/C agent bridge | **No** | Link when repo wraps or integrates OpenCode |

### Model weights (never in release artifacts)

| Asset | Bundle? | INSTALL.md |
|-------|---------|------------|
| GGUF / safetensors / multi-GB checkpoints | **Never** | Hugging Face model page, `ollama pull`, or LM Studio model browser |
| LoRA / full fine-tunes | **Never** | Same as above |
| **Tiny** embeddings or tokenizer files (~few MB) | **Optional** only if offline-first and documented | State size; offer download-on-first-run alternative |

**Size heuristic:** If it is user-specific or **> ~20 MB**, do not bundle.

### Cloud providers (first-class, not a fallback footnote)

Tier B must be documented with the same prominence as Ollama:

- OpenAI-compatible base URL + API key (covers DeepSeek, OpenRouter, many gateways)
- Named examples: **OpenCode** + inexpensive models (e.g. DeepSeek V4 Flash), DeepSeek API, OpenRouter
- Webapp **Settings**: provider dropdown — Local (Ollama / LM Studio) | Cloud (URL + key)
- Clear error when neither local nor cloud is configured: *"No LLM found — install Ollama or add a cloud API key in Settings."*

**Do not** implement multi-GB model pull inside the installer or MCP tools without explicit user consent and progress UI.

### Required INSTALL.md content (LLM-enabled repos)

```markdown
## LLM / inference (choose one)

### Local — Ollama (recommended for beginners)
winget install Ollama.Ollama
ollama pull <documented-model>

### Local — LM Studio
Download from lmstudio.ai → load model from Hugging Face or built-in search

### Cloud — API (recommended for weak PCs / no GPU)
Set OPENAI_API_BASE and OPENAI_API_KEY (or provider-specific vars)
Example: OpenCode serve + DeepSeek / OpenRouter / DeepSeek API

### Advanced — vLLM
OpenAI-compatible URL at http://host:8000/v1 — see docs/CONFIGURATION.md
```

### Required CONFIGURATION.md env vars (minimum for LLM repos)

| Variable | Purpose |
|----------|---------|
| `OLLAMA_HOST` | Default `http://127.0.0.1:11434` |
| `OPENAI_API_BASE` | Cloud or vLLM OpenAI-compatible endpoint |
| `OPENAI_API_KEY` | API key (cloud); may be dummy for local vLLM |
| Provider-specific | e.g. `DEEPSEEK_API_KEY`, `HF_TOKEN` only if server fetches on user's behalf |

### Webapp behavior (fleet)

1. **Auto-detect** Ollama (`11434`) and LM Studio (`1234`) on dashboard mount — see [LOCAL_LLM_STANDARDS.md](./LOCAL_LLM_STANDARDS.md) Standard 4.
2. **Persist** last-selected model/provider in Settings.
3. **Never** assume GPU or local LLM; cloud path must work out of the box with key only.

---

## External host applications ("wrapees")

MCP servers **bridge** to host apps; they do **not** redistribute them.

### Never bundle

| Host | Examples | INSTALL.md |
|------|----------|------------|
| 3D / DCC | Blender, Unity **Editor**, Unreal, Maya | Official download + winget where available |
| 2D / vector | Inkscape, GIMP, Krita | Same |
| Video / audio | DaVinci Resolve, Reaper | Same |
| Game engines | Unity, Unreal (full editor) | **Monsters — never in installer** |
| LLM weights | Any multi-GB model | Hugging Face / Ollama / LM Studio instructions |

### Path configuration

Document env vars or Settings fields:

- `BLENDER_EXECUTABLE`, `UNITY_EDITOR_PATH`, `GIMP_EXECUTABLE`, etc.
- Auto-detect common install paths on Windows; allow override.

### Tiny exceptions (allowed in repo or installer)

Bundle **only** when **all** are true:

- Small (order of **KB to low MB**, not GB)
- License allows redistribution
- Large UX win (e.g. Blender add-on zip, Unity bridge script/DLL)
- User can override or replace via path/env

**Examples OK to ship:** prompt templates, MCP bridge add-on, default config JSON.  
**Examples never OK:** Blender binary, Unity Hub + Editor, HF model checkpoints.

---

## Native installer bundle (Tauri + PyInstaller)

See [tauri_godot_sota.md](./rules/tauri_godot_sota.md) for build layout.

### Include in `.exe` / NSIS installer

| Component | Yes |
|-----------|-----|
| Python MCP server + FastMCP stack | Yes |
| React/Vite `webapp/dist/` static assets | Yes |
| Tauri shell (WebView2 host) | Yes |
| Repo-owned prompts, tiny bridge assets | Yes |

### Exclude from installer

| Component | No |
|-----------|-----|
| Ollama, LM Studio, vLLM | No |
| LLM model weights | No |
| Blender, Unity Editor, Inkscape, GIMP, … | No |
| Docker Desktop | No |
| Dev tools: `uv`, `ruff`, `biome`, `just`, git, Node | No |

**Size complaints:** optimize **PyInstaller** tree first (exclude tests, optional deps); switching away from Tauri rarely fixes fat Python deps.

### Distribution priority (Windows non-dev, webapp repos)

| Priority | Method | Audience |
|----------|--------|----------|
| 1 | **Tauri NSIS installer** | Full product (webapp + backend) |
| 2 | `.mcpb` drag-and-drop | **Claude Desktop only** — MCP slice, not cross-IDE |
| 3 | `start.ps1` / naked-PC script | Users without Claude; pulls prereqs |
| 4 | Clone + `uv sync` | Developers (Option D) |

---

## Docker

**Default for fleet MCP + webapp repos: Docker is NOT required.**

| Use Docker | When |
|------------|------|
| **Optional / documented** | Power users, reproducible dev env |
| **Product feature** | Observability stacks (Prometheus/Grafana/Loki), *arr homelab, multi-container isolation (e.g. deepfang), ROS/robotics bridges |

Control-plane and agent-stack repos (RoboFang, DeepFang, OpenClaw/NanoClaw bridges) follow **[CONTROL_PLANE_INSTALL.md](./CONTROL_PLANE_INSTALL.md)** — Docker may be **required** there even when optional for normal MCP hands.
| **Do not require** | Single-process FastMCP + Starlette + Vite; Tauri installer path; Claude stdio MCP |

INSTALL **Option A** must never list Docker as a prerequisite. Mention `docker compose` only under **Advanced / homelab** or `docs/DEVELOPMENT.md`.

---

## INSTALL.md template integration

Use blocks from [templates/INSTALL.md](../templates/INSTALL.md):

- **Host application** — when repo controls Blender, Unity bridge, etc.
- **LLM / inference** — when repo calls local or cloud models
- **Docker** — single line: *Not required; see docs/DEVELOPMENT.md for optional compose stacks.*

Split detailed env tables into `docs/CONFIGURATION.md` per [README_STRUCTURE.md](./README_STRUCTURE.md).

---

## Anti-patterns (forbidden)

| Anti-pattern | Why |
|--------------|-----|
| Bundling Unity Editor or Blender in Tauri installer | Size, licensing, version skew |
| Bundling GGUF/safetensors in `.mcpb` or release assets | GB payloads; user model choice |
| Cloud API only documented in a footnote | Excludes Tier B weak-PC users |
| Assuming Ollama is already installed with no install steps | Excludes Tier A beginners |
| `docker compose up` as only install path | Excludes non-dev users |
| MCP tool that silently downloads multi-GB models | User consent and bandwidth |
| `uvx mcpb` as install command | mcpb is npm, not PyPI |

---

## Validation

From `mcp-central-docs`:

```powershell
.\scripts\check-readme-structure.ps1 -RepoPath D:\Dev\repos\<repo> -Strict
```

The script warns when source code suggests LLM or host-app integration but `INSTALL.md` lacks the corresponding prerequisite section.

Manual checklist for LLM/host repos:

- [ ] INSTALL.md: local **and** cloud LLM paths (or explicit N/A)
- [ ] INSTALL.md: host app download + env path (if applicable)
- [ ] INSTALL.md: no Docker in Option A prerequisites
- [ ] docs/CONFIGURATION.md: `OLLAMA_HOST`, `OPENAI_API_BASE`, `OPENAI_API_KEY` (if LLM)
- [ ] Webapp Settings: provider selection + offline/online detection
- [ ] Native build: PyInstaller spec excludes models and host binaries

---

## Related standards

| Doc | Relationship |
|-----|--------------|
| [README_STRUCTURE.md](./README_STRUCTURE.md) | INSTALL.md tiered options A–D |
| [PACKAGING_STANDARDS.md](./PACKAGING_STANDARDS.md) | `.mcpb` vs full app; no deps in MCPB |
| [rules/tauri_godot_sota.md](./rules/tauri_godot_sota.md) | Tauri + PyInstaller sidecar build |
| [LOCAL_LLM_STANDARDS.md](./LOCAL_LLM_STANDARDS.md) | Workstation tuning (4090, ngrok, modelfiles) — **not** end-user INSTALL |
| [NAKED_INSTALL_TESTING.md](./NAKED_INSTALL_TESTING.md) | Consumer sandbox validation |
| [integrations/local-llm/README.md](../integrations/local-llm/README.md) | Ollama / LM Studio / vLLM integration index |
| [CONTROL_PLANE_INSTALL.md](./CONTROL_PLANE_INSTALL.md) | RoboFang, DeepFang, OpenClaw — advanced install tiers |
| [patterns/api_key_management.md](./patterns/api_key_management.md) | Cloud key handling |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-05-28 | Initial fleet standard: user tiers A–D, wrapee bundling rules, LLM local/cloud parity, Docker scope |
