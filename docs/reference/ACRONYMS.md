---
title: "Fleet Acronym Reference"
category: reference
status: active
audience: everyone
last_updated: 2026-10-18
---

# Dev Acronyms, Abbreviated

~150 TLAs and initialisms you'll hit in daily fleet work. Short explanation + fleet-relevant example where useful.

---

~210 TLAs and initialisms, plus ~60 more from Fable's gap analysis. Short explanation + fleet-relevant example where useful.

---

## MCP Ecosystem

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| MCP | Model Context Protocol | Protocol for AI models to call tools and read resources | Every repo in `D:\Dev\repos\` |
| SOTA | Service-Oriented Thinking Architecture | Fleet architectural framework -- standards, quality gates, tooling conventions | `standards/SOTA_REQUIREMENTS.md` |
| MCD | MCP Central Docs | Fleet documentation hub at `mcp-central-docs/` | `mcp-central-docs/standards/` |
| ACP | Agent Client Protocol | Open-source protocol for AI agent communication | `standards/AGENT_PROTOCOLS.md` |
| OTel | OpenTelemetry | Observability framework for traces, metrics, logs | `patterns/OPENTELEMETRY_FLEET_ROLLOUT.md` |
| OT | Operation Transform | Data transformer concept | OpenTelemetry OT pipeline |
| OTLP | OpenTelemetry Protocol | Wire format for telemetry data | gRPC :4317, HTTP :4318 |
| SOP | Standard Operating Procedure | Step-by-step guide for recurring tasks — assfix, spec, drift, deps audit, onboard | `patterns/` (multiple files) |
| SSE | Server-Sent Events | HTTP-based one-directional stream | FastMCP SSE transport |
| stdio | Standard I/O | Process stdin/stdout as transport | `uv run python server.py` mode |
| RAG | Retrieval-Augmented Generation | Chunk documents → embed (vectorize) → store in vector DB → retrieve relevant chunks by semantic similarity → inject into LLM prompt as context → generate grounded answer. Without RAG, the LLM only knows what it was trained on. With RAG, it can answer questions about your specific documents, codebase, or data. Fleet stack: LanceDB (vector store), `fastembed`/`sentence-transformers` (embeddings), chunk size 500-1000 chars with overlap. Repos: `arxiv-mcp` depot (paper full-text), `calibre-mcp` (ebook RAG), `documentation-mcp` (fleet docs), `immich-mcp` (photo metadata). See `patterns/INDUSTRIAL_RAG_PATTERN.md`. |
| TLA | Three-Letter Acronym | Meta — the thing itself | This column |
| SEP | Something-Extension-Proposal | FastMCP extension specification | `fastmcp/sep-1577-sampling-with-tools.md` |
| MCPB | MCP Bundle | .mcpb packaging format for Claude Desktop | `MCPB_PACKAGING_STANDARDS.md` |
| NSIS | Nullsoft Scriptable Install System | Windows installer generator. Fleet's PRIMARY installer format. Supports PREINSTALL/PREUNINSTALL hooks (process kill), `currentUser` mode (no admin), silent `setup.exe /S`. See `packaging/NSIS_BUILD.md`. | Tauri NSIS `*-setup.exe` |
| ASGI | Asynchronous Server Gateway Interface | Python async web server spec (Starlette, Uvicorn, FastAPI). In FastMCP 3.4+, `mcp.http_app()` returns a Starlette app whose `lifespan` MUST be passed to the parent ASGI constructor or streamable HTTP crashes with 500. | `fastmcp/3.4-features.md` SS7 |
| CUA | Computer Use Agent | Agent that uses mouse/keyboard like a human | `cua_nsis_smoke_testing.md` |
| PREFAB | Prefabricated UI | FastMCP in-chat rich UI components | `prefab-ui>=0.14.0` |
| FTS | Full-Text Search | Keyword search over ingested text | SQLite FTS5 in arxiv-mcp depot |
| HuJSON | Human JSON | JSON with `//` comments and trailing commas allowed (used by Tailscale ACL policies and other configs). Strict `json.loads` fails on it — strip full-line `//` comments and trailing commas before parsing. Fleet reference: `tailscalemcp.operations.network._hujson_to_json` (tailscale-mcp). Pitfall: Tailscale's `GET /acl` serves raw HuJSON text, not JSON. | Tailscale ACL `GET/POST /acl` |

## AI / ML

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| LLM | Large Language Model | Generative text model | The thing talking to the MCP tools |
| GPT | Generative Pre-trained Transformer | Transformer-based LLM architecture from OpenAI | `gpt-4o`, `gpt-4.1` in fleet chat |
| VLM | Vision Language Model | LLM that also processes images | Gemini, GPT-4o |
| VLA | Vision-Language-Action | Model that sees, understands, and controls robots | `yahboom-mcp`, `unitree-mcp` |
| dLLM | Diffusion Language Model | Non-autoregressive LLM (generate all tokens at once) | `diffusiongemma` |
| LWM | Large World Model | Video-generation model that simulates physics | `worldlabs-mcp` |
| HLE | Human-Level Evaluation | Benchmark that requires human-level reasoning | DiffusionGemma reporting |
| RFT | Reinforcement Fine-Tuning | Train model via reward signals from a grader | `finetuning` skill |
| SFT | Supervised Fine-Tuning | Train model on labeled examples | `finetuning` skill |
| DPO | Direct Preference Optimization | Align model to human preferences | `finetuning` skill |
| RAI | Responsible AI | Content filtering, safety guardrails | Azure Foundry RAI policy |
| GPU | Graphics Processing Unit | Parallel compute unit | RTX 4090 in Goliath |
| TPU | Tensor Processing Unit | Google's ML accelerator | Not in fleet |
| NPU | Neural Processing Unit | On-device ML accelerator | Snapdragon X Elite laptops |
| LoRA | Low-Rank Adaptation | Efficient fine-tuning method | LoRA adapters for diffusion models |
| QLoRA | Quantized Low-Rank Adaptation | LoRA with 4-bit model quantization -- halves VRAM again | Unsloth fine-tuning on consumer GPUs |
| QAT | Quantization-Aware Training | Train with simulated quantization | Local model optimisation |
| Quant | Quantization (shorthand) | Reduce model weight precision (16-bit -> 8/4-bit) to fit bigger models in less VRAM at slightly lower quality | a 4-bit quant of glm-5.3 for local inference |
| CUDA | Compute Unified Device Architecture | NVIDIA parallel computing platform | All fleet GPU workloads |
| NVENC | NVIDIA Encoder | Fixed-function GPU video-encode block, separate from CUDA cores; near-zero compute and VRAM cost | Sunshine streaming on Goliath RTX 4090 |
| ONNX | Open Neural Network Exchange | Interchangeable model format | `stems-mcp` HTDemucs, ComfyUI export |
| AGI | Artificial General Intelligence | Human-level AI across all tasks | Research frontier |
| GGUF | GPT-Generated Unified Format | llama.cpp model format | Local inference via Ollama |
| MoE | Mixture of Experts | Model architecture with sparse expert routing | DeepSeek-V4 |
| GLM | General Language Model | Zhipu/Z.AI open-weight LLM family; long-context coding models | glm-5.3 (1M ctx) in opencode providers |
| Opus | Anthropic flagship model tier (name, not an acronym) | Top-capability Claude tier for hard codegen and architecture work | Opus 5.5 built storytold ArtCraft; fleet sampling-model option |
| MLA | Multi-head Latent Attention | KV-cache compression via latent vectors; cheap long-context serving | DeepSeek-V2 |
| DeepSeekMoE | DeepSeek Mixture-of-Experts | Fine-grained expert segmentation plus isolated shared experts | DeepSeek-V2 |
| MTP | Multi-Token Prediction | Predict several future tokens per step; denser training signal | DeepSeek-V3 |
| DualPipe | Bidirectional pipeline parallelism | Overlap computation and communication in both directions | DeepSeek-V3 |
| FP8 | 8-bit Floating Point | Low-precision training format; headline V3 efficiency bet | DeepSeek-V3 |
| PPO | Proximal Policy Optimization | Baseline policy-gradient RL | Precursor to GRPO |
| GRPO | Group Relative Policy Optimization | RL without a critic model; group-scored advantages | DeepSeek-R1 |
| Qwen | Tongyi Qianwen (Alibaba) | Open-weight LLM family; coder and vision-language variants | `qwen3.8-tools` in Ollama provider |
| Kimi | Moonshot AI | Long-context chat and coding models (Kimi K2) | API clients |
| Hunyuan | Tencent Hunyuan | LLM plus 3D generation (Hunyuan3D meshes) | ArtCraft 3D catalog |
| Doubao-Seed | ByteDance Seed team | Doubao chat brand; sibling video/image models Seedance and Seedream | ArtCraft video/image catalog |
| MiniMax | MiniMax (Hailuo) | Video and audio models | ArtCraft catalog |
| Kling | Kuaishou Kling | Video generation models (1.6 through 3.0) | ArtCraft video catalog |
| ERNIE | Baidu ERNIE | Search-grounded LLM family; China enterprise default | Competitor watch |
| MMLU | Massive Multitask Language Understanding | Benchmark (undergrad knowledge) | Standard eval |
| HHH | Helpful, Honest, Harmless | Anthropic's alignment principles | System prompts |
| RLHF | Reinforcement Learning from Human Feedback | Align model via human preferences | Precursor to DPO |
| AI | Artificial Intelligence | Broad field of intelligent systems | Everything in this table |
| ML | Machine Learning | Models that learn from data | Subset of AI |
| DL | Deep Learning | Neural network-based ML | Transformers, diffusion models |
| NLP | Natural Language Processing | Text understanding/generation | All MCP tool descriptions |
| CV | Computer Vision | Image/video understanding | `comfyops-mcp` vision-refine loop |
| OCR | Optical Character Recognition | Extract text from images/screenshots | CUA smoke test page verification |
| TTS | Text-to-Speech | Convert written text to spoken audio | `speech-mcp`, fleet chat SpeakButton |
| STT | Speech-to-Text | Convert spoken audio to written text | `speech-mcp`, fleet chat MicButton |
| AR | Augmented Reality | Digital overlay on real world | Future fleet frontpage |
| VR | Virtual Reality | Fully digital environment | `resonite-mcp`, `vrchat-mcp` |
| XR | Extended Reality | Umbrella for AR/VR/MR | Teleoperator XR client |
| HF | HuggingFace | ML model/dataset hub | Model downloads, `transformers` |
| SAE | Sparse Autoencoder | Interpretability feature extraction | Anthropic monosemanticity research |
| RL | Reinforcement Learning | Learning via reward signals | DPO, RFT, future sim training |
| IL | Imitation Learning | Learning from demonstrations | Future robot skill acquisition |
| TO | Tool Orchestration | LLM selecting and calling tools | The entire MCP protocol |
| FT | Fine-Tuning | Adapting a pretrained model | LoRA, SFT, RFT |
| MoA | Mixture of Agents | Multiple agents collaborating | Future fleet-agent-mcp topology |
| ICL | In-Context Learning | Learning from examples in prompt | Few-shot prompting patterns |
| CoT | Chain of Thought | Step-by-step reasoning | `ctx.sample()` pattern |
| ToT | Tree of Thoughts | Branching reasoning exploration | Advanced agentic patterns |
| HITL | Human In The Loop | Human oversight in automated systems | `admiral-mcp` agent approval pager |
| HF | HuggingFace (see above) | ML model hub | `comfy_models` download |
 
## Protocols & Standards

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| HTTP | HyperText Transfer Protocol | Web request protocol | `http://localhost:10770` |
| HTTPS | HTTP Secure | Encrypted HTTP | `https://tauri.localhost` |
| gRPC | gRPC Remote Procedure Call | High-performance RPC over HTTP/2 | OTLP gRPC export |
| REST | Representational State Transfer | Resource-oriented HTTP API pattern | `GET /api/health` |
| JSON | JavaScript Object Notation | Ubiquitous data interchange format | Tool return values |
| NDJSON | Newline-Delimited JSON | One JSON value per line, no enclosing array — stream-friendly. Emitted by `gh api --jq '.[] | …'` and OpenSERP `format=ndjson`. Parse by splitting lines and `json.loads` per line; `json.loads` on the whole blob fails with "Extra data". | `gh api --jq`, openserp `format=ndjson` |
| JSON-RPC | JSON Remote Procedure Call | RPC protocol using JSON | MCP protocol messages |
| YAML | YAML Ain't Markup Language | Config file format (recursive acronym) | `docker-compose.yml` |
| TOML | Tom's Obvious Minimal Language | Config file format | `pyproject.toml` |
| XML | eXtensible Markup Language | Verbose structured data format | Legacy configs (rare in fleet) |
| CSV | Comma-Separated Values | Tabular data format | Export tools |
| W3C | World Wide Web Consortium | Web standards body | `traceparent` header |
| CORS | Cross-Origin Resource Sharing | Browser security policy for cross-origin requests | `tauri://localhost` in `allow_origins` |
| CSP | Content Security Policy | Browser security headers | Must be null for Tauri WebView |
| SCIM | System for Cross-domain Identity Management | User provisioning API | In federation router |
| LDAP | Lightweight Directory Access Protocol | Directory service protocol | Enterprise auth |
| OAuth | Open Authorization | Delegated access protocol | Cloud API tokens |
| JWT | JSON Web Token | Signed token format | Auth headers |
| URI | Uniform Resource Identifier | Resource identifier | `skill://email-compose/SKILL.md` |
| URL | Uniform Resource Locator | Web address | `https://arxiv.org/abs/2401.00001` |
| URN | Uniform Resource Name | Persistent name identifier | DOI `10.1038/nature` |
| BOM | Byte Order Mark | Unicode signature at file start indicating encoding (e.g. `\xef\xbb\xbf` for UTF-8) | Often causes parser/compilation errors in JS engines |
| FM | Frontmatter | YAML metadata block at the start of Markdown files for RAG metadata indexing | `standards/FRONTMATTER_STANDARD.md` |

## Infrastructure & Ops

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| VM | Virtual Machine | Emulated computer | Not fleet standard (bare metal) |
| VPS | Virtual Private Server | Cloud VM | Not in fleet |
| VPC | Virtual Private Cloud | Isolated cloud network | Not in fleet |
| DNS | Domain Name System | Name-to-IP resolution | mcp.local resolution |
| DHCP | Dynamic Host Configuration Protocol | Automatic IP assignment | Home network |
| NAT | Network Address Translation | Map private IPs to public | Tailscale handles this |
| VPN | Virtual Private Network | Encrypted tunnel to another network | Tailscale (preferred) |
| CDN | Content Delivery Network | Geographically distributed cache | Not used (local fleet) |
| LB | Load Balancer | Distributes traffic across instances | Nginx reverse proxy |
| HA | High Availability | Fault-tolerant system design | Docker health checks |
| DR | Disaster Recovery | Plan for catastrophic failure | Backups to NAS |
| SLA | Service Level Agreement | Uptime commitment | Internal fleet target |
| SLO | Service Level Objective | Internal reliability target | Grafana alert thresholds |
| SLI | Service Level Indicator | Measured reliability metric | P99 latency, error rate |
| KPI | Key Performance Indicator | Dashboard metric showing system state | `kpi-gpu`, `kpi-jobs` data-testids |
| MTTR | Mean Time To Recover | Average restoration time | After bug discovery |
| MTBF | Mean Time Between Failures | Average uptime between failures | Rare for MCP servers |
| IaC | Infrastructure as Code | Manage infra via config files | Docker Compose files |
| AMI | Amazon Machine Image | Pre-configured VM image | Not in fleet |
| K8s | Kubernetes (K8s — 8 letters) | Container orchestration | Not used (Docker Compose) |
| K3s | Lightweight Kubernetes | Single-binary K8s for edge | Potential future fit |
| LXC | Linux Containers | OS-level virtualization | Not in fleet |
| OCI | Open Container Initiative | Container image standard | Docker images |
| PID | Process Identifier | OS process number | `$pid` in PowerShell |
| TTY | Teletype | Terminal device | `--tty` in docker |
| SHELL | Shell | Command interpreter | `pwsh` |
| TUI | Terminal User Interface | Text-based UI | CLI tooling |
| GUI | Graphical User Interface | Visual UI | Web dashboard |
| UX | User Experience | Overall user interaction quality | `data-testid` attributes |
| UI | User Interface | Visual layout and controls | React components |
| DX | Developer Experience | Dev workflow quality | `just` recipes, hot reload |
| QoL | Quality of Life | Usability improvements | This document |
| POSIX | Portable Operating System Interface | Unix standard API | Windows Subsystem for Linux |
| WSL | Windows Subsystem for Linux | Linux kernel on Windows | Debugging Linux tools |
| PATH | Executable search path | Where OS looks for binaries | `$env:PATH` |
| EOF | End of File | File terminator | Heredoc delimiter |

## Build Tools & CI

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| CI | Continuous Integration | Automatically build and test on push | GitHub Actions |
| CD | Continuous Delivery | Automatically deploy after CI | Release workflow |
| TDD | Test-Driven Development | Write tests before code | `just test` |
| PR | Pull Request | Code review workflow | GitHub PRs |
| CR | Code Review | Manual review before merge | Open PRs |
| MVP | Minimum Viable Product | Smallest useful release | Phase 1 features |
| PoC | Proof of Concept | Feasibility demonstration | Experimental branches |
| CLI | Command-Line Interface | Terminal-based tool | `uv run python server.py` |
| API | Application Programming Interface | Programmatic interface | `GET /api/health` |
| SDK | Software Development Kit | Library for building against a platform | MCP SDK |
| E2E | End-to-End (Test) | Full user-journey test | Playwright tests |
| LSP | Language Server Protocol | Standard for IDE code intelligence | Rust Analyzer, Pyright |
| IDE | Integrated Development Environment | Code editor with language intelligence | Cursor, VS Code, Windsurf |
| DAP | Debug Adapter Protocol | Standard for IDE debugging | Python debugger |
| WASM | WebAssembly | Binary format for browser execution | Not yet in fleet |
| TS | TypeScript | Typed JavaScript superset | Fleet webapp standard |
| JS | JavaScript | Web scripting language | Bun runtime |
| JSX | JavaScript XML | React's HTML-in-JS syntax | `.tsx` files |
| CSS | Cascading Style Sheets | Web styling language | TailwindCSS |
| SCSS | Sassy CSS | CSS preprocessor | Rare in fleet (Tailwind) |
| AST | Abstract Syntax Tree | Code structure representation | Linters, formatters |
| RFC | Request for Comments | Design proposal document | Architecture patterns |
| PRD | Product Requirements Document | Spec defining what to build and why | `projects/*/PRD.md` |
| NFR | Non-Functional Requirements | Performance, security, reliability constraints | PRD appendix |
| RAII | Resource Acquisition Is Initialization | C++ resource management pattern | Rust borrow checker |
| ORM | Object-Relational Mapping | DB abstraction layer | SQLAlchemy |
| DTO | Data Transfer Object | Structure for API data | Pydantic models |
| ETL | Extract, Transform, Load | Data pipeline pattern | Depot ingestion |

## Security

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| XSS | Cross-Site Scripting | Injecting scripts into web pages | CSP headers prevent this |
| CSRF | Cross-Site Request Forgery | Tricking user into unintended action | Token-based prevention |
| SQLi | SQL Injection | Injecting SQL queries | Parameterized queries prevent this |
| MITM | Man-in-the-Middle | Intercepting communications | TLS prevents this |
| DOS | Denial of Service | Overwhelming a service | Rate limiting |
| DDOS | Distributed Denial of Service | DOS from many sources | Cloudflare (not in fleet) |
| RBAC | Role-Based Access Control | Permissions by role | Azure Foundry RBAC |
| ACL | Access Control List | Per-resource permissions | NTFS ACLs |
| MFA | Multi-Factor Authentication | Second auth factor | GitHub MFA |
| SSO | Single Sign-On | One login for multiple services | Azure AD |
| TLS | Transport Layer Security | Encrypted connection | HTTPS = HTTP over TLS |
| SSL | Secure Sockets Layer | Deprecated predecessor of TLS | Still in common use as term |
| CA | Certificate Authority | Issues TLS certificates | Let's Encrypt |
| PGP | Pretty Good Privacy | Email encryption | Code signing |
| GPG | GNU Privacy Guard | Open PGP implementation | Git commit signing |
| PKI | Public Key Infrastructure | Certificate management system | Internal CA |
| CIB | Coordinated Inauthentic Behavior | Automated coordination of multiple bot accounts to spread spam or opinion campaigns. Counterexample: our transparent, value-first dev outreach. For design patterns, see arXiv:2308.10620 (SLM propaganda factories) & arXiv:2403.17134 (CIB ecologies). | The PR system (`architecture/FLEET_PUBLIC_RELATIONS_SYSTEM.md`) shields our threads from these bot networks. |
| CVE | Common Vulnerabilities and Exposures | Security vulnerability identifier | Dependency audits |
| OWASP | Open Web Application Security Project | Web security community | Top 10 vulnerabilities |
| CSP | Content Security Policy | XSS prevention headers | Tauri WebView |
| HSM | Hardware Security Module | Dedicated crypto hardware | Not in fleet |
| TPM | Trusted Platform Module | On-device security chip | Windows Hello |
| PII | Personally Identifiable Information | Data that can uniquely identify a person (emails, IPs) | Sanitizing user databases/logs before RAG compilation |
| PHI | Protected Health Information | Healthcare-related personal data | Restricted access for liveness cameras and health logs |
| PoL | Proof of Life | Liveness safety check systems (presence/stillness tests) | `fritz_surveil` camera zone duration alerts |
| POLP | Principle of Least Privilege | Gating processes to minimum required permissions | Workspace tool approval sandboxes and Docker scopes |
| SBOM | Software Bill of Materials | Formal inventory of software dependencies | Package lists for supply-chain security checks |
| RAT | Remote Access Trojan | Malicious backdoor software | Banned binaries; see `standards/RAT_EMERGENCY_PROTOCOL.md` |

## Web Dev

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| DOM | Document Object Model | Browser's page representation | React virtual DOM |
| SPA | Single-Page Application | Webapp with one HTML page, JS-routed | All fleet webapps |
| CTA | Call to Action | UI element prompting a user action (button, link) | Dashboard hero "Start onboarding" button |
| CSR | Client-Side Rendering | Browser renders the page | React default |
| SSR | Server-Side Rendering | Server renders the HTML | Next.js mode |
| SSG | Static Site Generation | Pre-built HTML at build time | Next.js export mode |
| ISR | Incremental Static Regeneration | Update SSG pages after build | Not used in fleet |
| PWA | Progressive Web App | Installable webapp with offline support | `PWA_FLEET_ANALYSIS.md` |
| HMR | Hot Module Replacement | Update code without full reload | Vite dev server |
| DX | Developer Experience | The feel of the dev workflow | Bun's fast install |
| CSP | Content Security Policy | Restricts what resources load | Tauri CSP config |
| CDN | Content Delivery Network | Cached static assets geodistributed | Not in fleet |
| FOUC | Flash of Unstyled Content | Momentary unstyled HTML on load | Prevented by Tailwind + SSR |
| LCP | Largest Contentful Paint | Core Web Vitals metric (loading) | Performance monitoring |
| CLS | Cumulative Layout Shift | Core Web Vitals metric (stability) | Layout stability |
| FID | First Input Delay | Core Web Vitals metric (interactivity) | Performance monitoring |
| INP | Interaction to Next Paint | Core Web Vitals metric (responsiveness) | Replaces FID in 2024+ |
| SEO | Search Engine Optimization | Making pages findable on Google | SPA needs SSR/SSG for this |
| SERP | Search Engine Results Page | The page Google/Bing shows for a query | `integrations/openserp/README.md` — FOSS SERP API |
| A11Y | Accessibility | Numeronym for "accessibility" — lowercase `a11y` in tooling, uppercase `A11Y` in prose. Biome lint category is `lint/a11y/*` (e.g. `useButtonType`, `noStaticElementInteractions`); webapps must pass these as part of `just lint` | `aria-label`, `data-testid`, `lint/a11y/useButtonType` |
| I18N | Internationalization | Numeronym: **i** + 18 letters + **n** = "internationalization". Architecture that makes software localizable (locale dictionaries, no hardcoded copy, date/number/currency formatting per locale) | `src/lib/i18n.tsx` pattern (EN/DE dictionary + topbar dropdown + localStorage); content translation is a separate Phase 2 |
| L10N | Localization | Numeronym: **l** + 10 letters + **n** = "localization". The actual translation/adaptation work per locale (copy, formats, RTL, imagery) that i18n architecture enables | DE UI strings; curated content stays source-language until Phase 2 |
| RWD | Responsive Web Design | Layout adapts to screen size | Tailwind breakpoints |
| BEM | Block Element Modifier | CSS naming convention | Not fleet standard (Tailwind) |

## Fleet-internal numeronyms (Eigengebrauch)

**What a numeronym is** (very dev-nerdy, as requested): a word compressed to
*first letter + count of middle letters + last letter*. The original is
**i18n** = **i** + 18 + **n** for "internationalization" - coined at Digital
Equipment Corporation (DEC) in the 1970s or 1980s by engineers tired of typing
30-page memos about it (Wikipedia: *Internationalization and localization*).
The localization industry added **l10n**, accessibility folks **a11y**,
Google-era infrastructure **K8s**. The pattern only works when the result is
shorter than the word AND the tribe already knows the word - otherwise it's
just showing off.

Same pattern as i18n/a11y (first letter + letter count + last letter), defined
for fleet use. Propose new ones sparingly - an acronym nobody uses is clutter.
**r11n** is in active use as of 2026-10-18 (lowercase in chat, `R11N` in this table).
The public banner bearer is Brandon Thomas (`storytold`) and the 13 Crafting Apps: CADCraft, DeckCraft, DesignCraft, EffectCraft, FigCraft, FilmCraft, GridCraft, LightCraft, PdfCraft, PhotoCraft, SoundCraft, VectorCraft, WordCraft. Fleet r11n borrows his harness. Wrap those apps, do not reimplement them (`standards/rust-artcraft/CRAFT_APPS_MCP_UTILIZATION.md`).
The public banner bearer is Brandon Thomas (`storytold`) and the 13 Crafting Apps: CADCraft, DeckCraft, DesignCraft, EffectCraft, FigCraft, FilmCraft, GridCraft, LightCraft, PdfCraft, PhotoCraft, SoundCraft, VectorCraft, WordCraft. Fleet r11n borrows his harness. Wrap those apps, do not reimplement them (`standards/rust-artcraft/CRAFT_APPS_MCP_UTILIZATION.md`).
The public banner bearer is Brandon Thomas (`storytold`) and the 13 Crafting Apps: CADCraft, DeckCraft, DesignCraft, EffectCraft, FigCraft, FilmCraft, GridCraft, LightCraft, PdfCraft, PhotoCraft, SoundCraft, VectorCraft, WordCraft. Fleet r11n borrows his harness. Wrap those apps, do not reimplement them (`standards/rust-artcraft/CRAFT_APPS_MCP_UTILIZATION.md`).

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| R11N | Rustification | Numeronym: **r** + 11 letters + **n** = "rustification". Fleet program that ports a Python/FastMCP + React repo into a Pure-Rust ArtCraft workspace. Trigger: `repconv <repo>` or `rustify <repo>`. Lineage: `rust-devices-mcp` is the first converted repo and the kernel blueprint (measured 2026-10-17, v0.4.0+). `rust-calibre-mcp` is the first end-to-end daily-driver `repconv` (2026-10-18, v0.4.0). `rust-plex-mcp` and `rust-arr-mcp` followed the same week. Triage: Buckets A and B convert, C splits, D stays Python. SOP: `patterns/REPCONV_SOP.md`. | `standards/RUST_ARTCRAFT_STANDARD.md` |
| D11N | Documentation | **d** + 11 + **n**. The docs corpus itself (this hub, READMEs, INSTALLs, ONBOARDINGs) | `mcp-central-docs/` |
| O11N | Orchestration | **o** + 11 + **n**. MCP servers calling MCP servers (sampling loops, crossconnects, fleet-agent) | `fleet-agent-mcp`, crossconnect pattern |
| P13N | Personalization | **p** + 13 + **n**. Everything tuned to one human (Sandra): memory, PII block, habits, dialect | `pii.json`, Advanced Memory |

## Windows / Systems

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| API | Application Programming Interface | System call interface | Win32 API, WinRT |
| ABI | Application Binary Interface | Binary-level interface between modules | COM, FFI |
| COM | Component Object Model | Microsoft interop technology | Some hardware SDKs |
| DLL | Dynamic Link Library | Shared Windows library | `.pyd` files |
| EXE | Executable | Windows program | `*-operator.exe` |
| MSI | Microsoft Installer | Windows enterprise installer format (`.msi`). Supports Group Policy deployment, silent install via `msiexec /i`, Active Directory publishing. **Fleet standard is NSIS** (supports installer hooks like process kill, currentUser install, smaller single artifact). MSI is optional — only add `"msi"` to Tauri `targets` if enterprise deployment is required. Do NOT upload both as equal citizen releases.  See `packaging/MSI_BUILD.md`. |
| CAB | Cabinet | Windows archive format | `expand.exe` extraction |
| VBS | VBScript | Legacy Windows scripting language | Not used |
| IIS | Internet Information Services | Windows web server | Not fleet standard (nginx) |
| AD | Active Directory | Microsoft directory service | Enterprise auth |
| GPO | Group Policy Object | Centralized Windows config | Enterprise mgmt |
| WMI | Windows Management Instrumentation | System management interface | `Win32_Processor` queries |
| NSSM | Non-Sucking Service Manager | Run any program as a Windows service | `unsloth-mcp` queue worker daemon |
| IPC | Inter-Process Communication | Data exchange between processes | WebSocket bridge, stdio pipes |
| COM | Component Object Model (see above) | Microsoft interop | Also Component Object Model |
| UAC | User Account Control | Windows privilege elevation prompt | Admin prompts |
| ACL | Access Control List | NTFS permissions | `winops_acl_*` tools |
| NTFS | New Technology File System | Windows filesystem | Fleet storage |
| FAT | File Allocation Table | Legacy filesystem | USB drives |
| ReFS | Resilient File System | Modern Windows filesystem | Storage spaces |
| GUID | Globally Unique Identifier | 128-bit identifier | Registry keys |
| HWND | Handle to a Window | Window identifier in Win32 | AutoHotkey interop |
| AHK | AutoHotkey | Windows automation scripting language | `autohotkey-mcp`, fleet macro hotkeys |
| UIA | UI Automation | Windows accessibility framework for programmatic UI controls | pywinauto CUA tests, `descendants(title=...)` |
| HKEY | Handle to a Key | Registry hive root | Registry paths |
| MSVC | Microsoft Visual C++ | Microsoft C++ compiler | Tauri builds |
| CRT | C Runtime | Standard C library for Windows | MSVC runtime |
| PE | Portable Executable | Windows exe/dll format | EXE headers |
| WSL | Windows Subsystem for Linux | Linux kernel compatibility layer | Occasional Linux tool use |
| UWP | Universal Windows Platform | Modern Windows app framework | Not fleet standard |
| WinRT | Windows Runtime | Modern Windows API | Not fleet standard |

## Networking

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| IP | Internet Protocol | Network address | `127.0.0.1` |
| TCP | Transmission Control Protocol | Reliable connection-oriented protocol | `localhost:10770` |
| UDP | User Datagram Protocol | Unreliable connectionless protocol | Streaming, gaming |
| ICMP | Internet Control Message Protocol | Network diagnostics | `ping` |
| ARP | Address Resolution Protocol | IP to MAC address mapping | Local network |
| MAC | Media Access Control | Hardware address of network interface | Network interface ID |
| LAN | Local Area Network | Network within a single site | Fleet 192.168.x.x, Tailscale virtual LAN |
| MTU | Maximum Transmission Unit | Largest packet size | Network tuning |
| PCAP | Packet Capture | File format for captured network traffic (.pcap/.pcapng); also the act of sniffing | `packetsniffer-mcp` `analyze_pcap` / `sniff` ops |
| BPF | Berkeley Packet Filter | Filter expression language for captures (e.g. `tcp port 80`, `udp port 53`) | `packetsniffer-mcp` `filter_expr` parameter |
| Npcap | Npcap | Windows packet capture driver (Wireshark's capture backend); required for live sniffing on Windows | `packetsniffer-mcp` live capture (admin required) |
| RTT | Round-Trip Time | Network latency | Performance monitoring |
| QoS | Quality of Service | Traffic prioritization | Media streaming |
| VLAN | Virtual Local Area Network | Network segmentation | Not in fleet |
| NIC | Network Interface Controller | Physical network card | Goliath hardware |
| SMTP | Simple Mail Transfer Protocol | Email sending | `email-mcp` |
| IMAP | Internet Message Access Protocol | Email reading | `email-mcp` |
| POP3 | Post Office Protocol v3 | Email download (not sync) | Rarely used |
| FTP | File Transfer Protocol | Legacy file transfer | Not used (HTTP) |
| SFTP | SSH File Transfer Protocol | Encrypted file transfer | `scp` alternative |
| SSH | Secure Shell | Encrypted remote shell | Git remote operations |
| HTTP/2 | HTTP version 2 | Multiplexed HTTP | gRPC runs over this |
| HTTP/3 | HTTP version 3 | HTTP over QUIC (UDP) | Not yet in fleet |
| QUIC | Quick UDP Internet Connections | Google's HTTP/3 transport | Modern web |
| WebRTC | Web Real-Time Communication | Browser-to-browser media | Media MCP servers |
| WebSocket | Web Socket | Full-duplex communication over TCP | `/ws` endpoints |
| mDNS | Multicast DNS | Local network service discovery | Tailscale |
| Funnel | Tailscale Funnel | Expose a local port to the public internet via the tailnet, no port forwarding | funnel-landing playbooks, `/multigpu/` deployment |
| MIDI | Musical Instrument Digital Interface | Music hardware/software protocol | `osc-mcp`, `mixx-dj-mcp`, `vcv-rack-mcp` |

## Storage & DB

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| DB | Database | Structured data store | SQLite, LanceDB |
| RDBMS | Relational Database Management System | SQL database | SQLite |
| SQL | Structured Query Language | Database query language | `SELECT * FROM papers` |
| ACID | Atomicity, Consistency, Isolation, Durability | Transaction guarantees | SQLite WAL mode |
| CRUD | Create, Read, Update, Delete | Basic data operations | REST endpoints |
| OLTP | Online Transaction Processing | Many small transactions | Most MCP servers |
| OLAP | Online Analytical Processing | Complex analytical queries | Grafana queries |
| ETL | Extract, Transform, Load | Data pipeline | Depot ingestion |
| CDC | Change Data Capture | Track DB changes in real time | Not in fleet |
| FTS | Full-Text Search | Keyword document search | SQLite FTS5 |
| BLOB | Binary Large Object | Large binary data in DB | Images, PDFs |
| JSON | JavaScript Object Notation | Flexible data type in SQLite | `json_extract()` |
| ORM | Object-Relational Mapping | Programmatic DB access | SQLAlchemy (rare in fleet) |
| WAL | Write-Ahead Logging | Performance mode for SQLite | Concurrent reads |
| MVCC | Multi-Version Concurrency Control | Snapshot isolation model | SQLite WAL mode |
| TTL | Time To Live | Expiry duration | Cache entries |
| LRU | Least Recently Used | Cache eviction policy | Memory caches |
| CAP | Consistency, Availability, Partition Tolerance | Distributed systems tradeoff | DB selection |
| BASE | Basically Available, Soft state, Eventually consistent | NoSQL tradeoff | LanceDB |
| VDB | Vector Database | Stores embeddings for similarity search | LanceDB |
| ANN | Approximate Nearest Neighbor | Fast vector similarity search | LanceDB IVF index |
| HNSW | Hierarchical Navigable Small World | ANN algorithm | Vector index type |

## CAD & Manufacturing

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| CAD | Computer-Aided Design | Design parts with software | `codecad-mcp` |
| PCB | Printed Circuit Board | Board connecting electronic components | `kicad-mcp` |
| CAM | Computer-Aided Manufacturing | Toolpath generation from CAD | Downstream of codecad-mcp |
| CAE | Computer-Aided Engineering | Simulation/analysis of designs | FEM, CFD (future) |
| FEM | Finite Element Method | Structural/stress simulation | Parked, needs a consumer |
| CFD | Computational Fluid Dynamics | Fluid flow simulation | Parked, needs a consumer |
| CAS | Computer Algebra System | Symbolic mathematics engine | `mathops-mcp` (`sympy`) |
| GDSII | Graphic Design System II | Chip layout file format (binary) | `chip-design-mcp` output |
| STEP | Standard for the Exchange of Product Model Data | ISO 10303 — CAD interchange format | `cad_export.step` |
| STL | Stereolithography | Mesh format (triangle soup, no units) | `cad_export.stl` for slicing |
| DXF | Drawing Exchange Format | Autodesk 2D CAD interchange | `cad_export.dxf` → kicad board outline |
| GLTF | GL Transmission Format | 3D scene format (glTF 2.0 standard) | `cad_export.gltf` → blender/godot |
| GLB | GLTF Binary | Single-file glTF variant (binary container) | Overte entity models, 3D asset depot |
| 3MF | 3D Manufacturing Format | Additive manufacturing format (preserves units, colors) | `cad_export.3mf` |
| SVG | Scalable Vector Graphics | Vector image format | `cad_export.technical_drawing` via `ExportSVG` |
| BREP | Boundary Representation | Solid geometry kernel representation | OCCT BREP, the native format |
| DRC | Design Rule Check | PCB layout validation | `kicad_drc` |
| BOM | Bill of Materials | Component list for assembly | `kicad_fab` BOM CSV |
| DFM | Design for Manufacturing | Design rules for producibility | Future codecad quality gate |

## Hardware & Robotics

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| CPU | Central Processing Unit | General-purpose processor | AMD Ryzen 9 5900X |
| GPU | Graphics Processing Unit | Parallel compute processor | RTX 4090 24 GB |
| USB | Universal Serial Bus | Peripheral connection standard | Dymo HID scale, RPLidar, cameras |
| NPU | Neural Processing Unit | On-device AI accelerator | Snapdragon X Elite |
| TPU | Tensor Processing Unit | Google's ML ASIC | Not in fleet |
| VRAM | Video Random Access Memory | GPU memory | 24 GB GDDR6X on RTX 4090 |
| RAM | Random Access Memory | System memory | 64 GB DDR4 |
| SRAM | Static RAM | Fast cache memory (no refresh) | CPU L1/L2/L3 cache |
| DRAM | Dynamic RAM | Main system memory (requires refresh) | DDR4/DDR5 DIMMs |
| SSD | Solid State Drive | Flash storage | Fleet boot drives |
| HDD | Hard Disk Drive | Magnetic storage | NAS bulk storage |
| NVMe | NVM Express | High-speed SSD interface | `C:\` drive protocol |
| NAS | Network Attached Storage | Shared file server | Fleet backup target |
| OOM | Out of Memory | Allocation failure | `vram_guard` preventing this |
| RTX | Ray Tracing Texel eXtreme | NVIDIA GPU brand | Goliath's 4090 |
| ROS 2 | Robot Operating System 2 | Distributed robot middleware | yahboom ROS 2 container |
| SLAM | Simultaneous Localization And Mapping | Build map + locate simultaneously | Future Boomy RPLidar nav |
| AMCL | Adaptive Monte Carlo Localization | Particle-filter robot localization | Nav2 stack |
| EKF | Extended Kalman Filter | Sensor fusion algorithm | Wheel odometry + IMU fusion |
| IMU | Inertial Measurement Unit | Accelerometer + gyroscope | Boomy's orientation sensing |
| LIDAR | Light Detection And Ranging | Laser distance scanning | RPLidar A1/C1 (future purchase) |
| SONAR | Sound Navigation And Ranging | Acoustic distance sensing | Raspbot V2 sonar cone |
| ROS | Robot Operating System | Precursor to ROS 2 | Legacy packages |
| DOF | Degrees of Freedom | Number of independent movements | 6-DOF arm, 12-DOF quadruped |
| PID | Proportional-Integral-Derivative | Control loop algorithm | Boomy `goto_pose` P-controller |
| HIL | Hardware-in-the-Loop | Real hardware with simulated inputs | Sim-to-real transfer validation |
| PNP | Pick and Place | Robot manipulation task | Future arm robotics |
| AGV | Automated Guided Vehicle | Floor-following robot | Boomy patrol mode |
| VDI | Virtual Disk Image | VirtualBox native disk container (dynamic or fixed) | `win11-automated.vdi` (80 GB dynamic) |
| VMDK | Virtual Machine Disk | VMware disk format; also readable by VirtualBox | Cross-hypervisor imports |
| VHDX | Virtual Hard Disk v2 | Hyper-V disk format (large, resilient) | Hyper-V guests, Windows backup images |
| VHD | Virtual Hard Disk | Legacy Hyper-V/Virtual PC format, 2 TB limit | Older Windows images |
| QCOW2 | QEMU Copy-On-Write v2 | QEMU/KVM sparse format with internal snapshots | libvirt guests |

## Version Control

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| VCS | Version Control System | Source code history | Git |
| DVCS | Distributed VCS | Peer-to-peer version control | Git |
| SHA | Secure Hash Algorithm | Cryptographic hash (Git commit id) | `git log --oneline` |
| HEAD | Current branch tip | Git pointer | `git reset HEAD~1` |
| PR | Pull Request | Proposed change on GitHub | Code review |
| MR | Merge Request | Same as PR (GitLab term) | Not in fleet |
| WIP | Work In Progress | Unfinished change | Draft PR |
| LFS | Large File Storage | Git extension for big files | Not fleet standard |
| DAG | Directed Acyclic Graph | Git commit graph structure | `git log --graph` |
| CLI | Command-Line Interface (again) | Also: Command-Line Interface | `git add .` |
| GUI | Graphical User Interface (again) | Visual tool | GitHub Desktop |
| TUI | Terminal User Interface (again) | Text interface | `tig` for git browsing |

## Miscellaneous Good-To-Know

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| GNU | GNU's Not Unix | Recursive acronym for free software | GPG, bash |
| GPL | GNU Public License | Copyleft license | Some dependencies |
| MIT | Massachusetts Institute of Technology | Permissive license (short) | Fleet standard license |
| AGPL | Affero GPL | Copyleft for network services | Some self-hosted tools |
| FOSS | Free and Open Source Software | Free + open source | All fleet dependencies |
| OSS | Open Source Software | Software with source code accessible | Community contributions |
| EPUB | Electronic Publication | E-book file format | `calibre-mcp` library management |
| DAW | Digital Audio Workstation | Music production software | `reaper-mcp` OSC bridge |
| DRY | Don't Repeat Yourself | Software principle | Portmanteau tools |
| WET | We Enjoy Typing / Write Everything Twice | Anti-DRY | Legacy code |
| SOLID | SRP, OCP, LSP, ISP, DIP | OOP design principles | Architecture patterns |
| YAGNI | You Ain't Gonna Need It | Don't over-engineer | Karpathy Simplicity (CLAUDE.md) |
| KISS | Keep It Simple, Stupid | Simplicity principle | 200-line shim over Docker |
| RTFM | Read The Fucking Manual | Go read the docs | This document |
| TL;DR | Too Long; Didn't Read | Summary needed | Architecture decision records |
| FOMO | Fear Of Missing Out | Irrational urgency | Acronym du jour |
| DF | Daily Fleet | Pseudo-acronym used by the fleet team | `df: decision needed` |
| ETA | Estimated Time of Arrival | When it'll be done | Feature timelines |
| WFM | Works For Me | Hard-to-repro bug status | Bug triage |
| PEBCAK | Problem Exists Between Chair And Keyboard | User error | Help desk classic |
| TBD | To Be Determined | Undecided | Spec gaps |
| SSRF | Server-Side Request Forgery | Attacker tricks server into making requests to internal resources (localhost APIs, cloud metadata `169.254.169.254`) | FastMCP 3.4.3 blocks NAT64/6to4/Teredo transition addresses to prevent SSRF bypass of private IP allowlists |
| FWIW | For What It's Worth | Tentative opinion | Code review comments |
| IIRC | If I Recall Correctly | Uncertain memory | Pull request discussions |
| AFAIK | As Far As I Know | Current understanding | Technical discussions |
| IMHO | In My Humble Opinion | Subjective view | Design debates |
| BDFL | Benevolent Dictator For Life | Project leader with final say | Fleet maintainer role |
