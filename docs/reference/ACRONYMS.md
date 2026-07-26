---
title: "Fleet Acronym Reference"
category: reference
status: active
audience: everyone
last_updated: 2026-07-12
---

# Dev Acronyms, Abbreviated

~150 TLAs and initialisms you'll hit in daily fleet work. Short explanation + fleet-relevant example where useful.

---

~200 TLAs and initialisms, plus ~60 more from Fable's gap analysis. Short explanation + fleet-relevant example where useful.

---

## MCP Ecosystem

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| MCP | Model Context Protocol | Protocol for AI models to call tools and read resources | Every repo in `D:\Dev\repos\` |
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
| CUA | Computer Use Agent | Agent that uses mouse/keyboard like a human | `cua_nsis_smoke_testing.md` |
| PREFAB | Prefabricated UI | FastMCP in-chat rich UI components | `prefab-ui>=0.14.0` |
| FTS | Full-Text Search | Keyword search over ingested text | SQLite FTS5 in arxiv-mcp depot |

## AI / ML

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| LLM | Large Language Model | Generative text model | The thing talking to the MCP tools |
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
| QAT | Quantization-Aware Training | Train with simulated quantization | Local model optimisation |
| GGUF | GPT-Generated Unified Format | llama.cpp model format | Local inference via Ollama |
| MoE | Mixture of Experts | Model architecture with sparse expert routing | DeepSeek-V4 |
| MMLU | Massive Multitask Language Understanding | Benchmark (undergrad knowledge) | Standard eval |
| HHH | Helpful, Honest, Harmless | Anthropic's alignment principles | System prompts |
| RLHF | Reinforcement Learning from Human Feedback | Align model via human preferences | Precursor to DPO |
| AI | Artificial Intelligence | Broad field of intelligent systems | Everything in this table |
| ML | Machine Learning | Models that learn from data | Subset of AI |
| DL | Deep Learning | Neural network-based ML | Transformers, diffusion models |
| NLP | Natural Language Processing | Text understanding/generation | All MCP tool descriptions |
| CV | Computer Vision | Image/video understanding | `comfyops-mcp` vision-refine loop |
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
| HF | HuggingFace (see above) | ML model hub | `comfy_models` download |
 
## Protocols & Standards

| TLA | Stands For | What | Fleet Example |
|-----|------------|------|---------------|
| HTTP | HyperText Transfer Protocol | Web request protocol | `http://localhost:10770` |
| HTTPS | HTTP Secure | Encrypted HTTP | `https://tauri.localhost` |
| gRPC | gRPC Remote Procedure Call | High-performance RPC over HTTP/2 | OTLP gRPC export |
| REST | Representational State Transfer | Resource-oriented HTTP API pattern | `GET /api/health` |
| JSON | JavaScript Object Notation | Ubiquitous data interchange format | Tool return values |
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
| DAP | Debug Adapter Protocol | Standard for IDE debugging | Python debugger |
| WASM | WebAssembly | Binary format for browser execution | Not yet in fleet |
| TS | TypeScript | Typed JavaScript superset | Fleet webapp standard |
| JS | JavaScript | Web scripting language | Bun runtime |
| JSX | JavaScript XML | React's HTML-in-JS syntax | `.tsx` files |
| CSS | Cascading Style Sheets | Web styling language | TailwindCSS |
| SCSS | Sassy CSS | CSS preprocessor | Rare in fleet (Tailwind) |
| AST | Abstract Syntax Tree | Code structure representation | Linters, formatters |
| RFC | Request for Comments | Design proposal document | Architecture patterns |
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
| A11Y | Accessibility | Numeronym for "accessibility" | `aria-label`, `data-testid` |
| I18N | Internationalization | Numeronym — 18 letters between I and N | Locale support |
| L10N | Localization | Numeronym — 10 letters between L and N | Translations |
| RWD | Responsive Web Design | Layout adapts to screen size | Tailwind breakpoints |
| BEM | Block Element Modifier | CSS naming convention | Not fleet standard (Tailwind) |

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
| COM | Component Object Model (see above) | Microsoft interop | Also Component Object Model |
| UAC | User Account Control | Windows privilege elevation prompt | Admin prompts |
| ACL | Access Control List | NTFS permissions | `winops_acl_*` tools |
| NTFS | New Technology File System | Windows filesystem | Fleet storage |
| FAT | File Allocation Table | Legacy filesystem | USB drives |
| ReFS | Resilient File System | Modern Windows filesystem | Storage spaces |
| GUID | Globally Unique Identifier | 128-bit identifier | Registry keys |
| HWND | Handle to a Window | Window identifier in Win32 | AutoHotkey interop |
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
| MTU | Maximum Transmission Unit | Largest packet size | Network tuning |
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
| NPU | Neural Processing Unit | On-device AI accelerator | Snapdragon X Elite |
| TPU | Tensor Processing Unit | Google's ML ASIC | Not in fleet |
| VRAM | Video Random Access Memory | GPU memory | 24 GB GDDR6X on RTX 4090 |
| RAM | Random Access Memory | System memory | 64 GB DDR4 |
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
