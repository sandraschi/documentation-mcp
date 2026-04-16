# Dark App Factory -- Project Status

**Last Updated**: 2026-02-11
**Repo**: `D:\Dev\repos\dark-app-factory` | [GitHub](https://github.com/sandraschi/dark-app-factory)
**Version**: v1.8.0
**Python**: 3.12+ | **Build**: Hatchling
**License**: Private (monetization planned)

---

## What It Is

A local-first "software factory" scaffold that replicates the [StrongDM Factory](https://factory.strongdm.ai) methodology (Specs + Scenarios -> Agents -> Validation) for free using Ollama/DeepSeek/Qwen local models. Expensive models (Opus 4.6) are used only for planning (<1% of tokens); cheap local models handle all code generation (>99%).

**Core loop**: `vibe.md` -> Foreman enriches/plans -> Worker Council builds (19 parallel specialists) -> Satisficer judges (scenario execution + satisfaction scoring) -> output app with marketing kit.

---

## Architecture

```
vibe.md --> [foreman enrich] --> enriched_vibe.md
                                     |
                                     v
            [foreman plan] --> specs.md + scenarios.md
                                     |
                                     v
                              Worker Council (async-parallel)
                                Tier 0: Professor (skills)
                                Tier 1: Plumber, Sculptor, Nervos, Raggy, WebFinder,
                                        Archivist, Maestro, Auditor, Picasso, Registrar
                                Tier 2: Librarian, Shakespeare, Morpheus, Tesla,
                                        Amodei, Houdini
                                Tier 3: Propagandist (marketing)
                                Tier 4: Generalist (catch-all)
                                     |
                                     v
                              DTU (Digital Twin Universe, port 8001)
                              9 mock services (Stripe, Auth, Email, SMS, etc.)
                                     |
                                     v
                              Satisficer (Judge)
                              1. Scenario Parser (GIVEN/WHEN/THEN)
                              2. Scenario Executor (httpx API + Rodney browser)
                              3. Satisfaction Scorer (mechanical + LLM-assisted)
                              4. UI verification (Rodney -> Playwright fallback)
                              SATISFACTORY/PARTIAL/UNSATISFACTORY -> critique.md
                                     |
                                     v
                              SOTA Dashboard (port 8002)
                              Real-time progress, specialist status
```

---

## Current State (v1.8)

### What Works

| Feature | Status | Notes |
|---------|--------|-------|
| Foreman planning | Working | Generates specs + scenarios from vibe |
| Vibe enrichment | Working | LLM expands terse vibes into rich briefs |
| 19-specialist council | Working | Async-parallel with dependency tiers |
| Context injection | Working | Downstream specialists read upstream output |
| Validation hooks | Working | 5 specialists with domain-specific checks |
| Self-declaration | Working | 7 specialists declare files based on specs keywords |
| Per-specialist temperature | Working | 0.1 (precision) to 0.7 (creative) |
| Multi-stack support | Working | Python (FastAPI/Flask/Django), Node (Express), React, HTMX |
| DTU (16 mock services) | Working | Stripe, Auth, Email, SMS, Storage, Discord, Slack, Weather, Webhook, LLM, Calendar, Maps, Analytics, Puzzles, TikTok, YouTube | Stripe, Auth, Email, SMS, Storage, Discord, Slack, Weather, Webhook |
| **Scenario-based testing** | **Working** | Parse GIVEN/WHEN/THEN, execute as real HTTP/browser actions, satisfaction scoring |
| **Satisfaction scorer** | **Working** | Probabilistic 0.0-1.0 scoring with mechanical + LLM-assisted evaluation |
| **Ruffy lint step** | **Working** | Post-Worker ruff check, ruff format, mypy; report to demos/lint-report.txt + Judge |
| **Deploy artifacts (Phase 1)** | **Working** | deploy.sh, deploy_config.example.yaml, docker-compose.prod.yml, nginx.conf |
| **PWA** | **Working** | manifest.json, sw.js, icons, meta injection (add-to-home-screen) |
| **Sample vibe depot** | **Working** | `vibes/vlc-mcp-webapp.md`, `vibes/7zip-mcp-webapp.md`; MCP + webapp pattern |
| **MCP wrapper support** | **Working** | Skill `mcp-windows-app-wrapper.md`, scenario template `mcp-wrapper.md`, Foreman enrich hint |
| Showboat artifacts | Working | Post-build demo document with real command output as proof-of-work |
| Rodney verification | Working | Headless Chrome screenshots and element checks during judge phase |
| Marketing pipeline | Working | Press release, blog, social, Reddit, Discord, PH, landing page |
| SOTA Dashboard | Working | Real-time build monitoring on port 8002 |
| DarkLogger | Working | Rotation, export, tiered help system |
| Deep-crawl imports | Working | Both Python and TSX import scanning |

### Known Issues

| Severity | Issue | File(s) |
|----------|-------|---------|
| RESOLVED | RunManifest: manifest.json now written after worker | `run_manifest.py`, `factory.py` |
| RESOLVED | GitManager wired: initialize() after worker, commit_changes after judge pass | `factory.py` |
| RESOLVED | Token usage reported at end of run; judge shares foreman LLMClient | `factory.py`, `judge.py` |
| RESOLVED | Worker/Judge run in-process (async), no subprocess | `factory.py` |
| LOW | Import path inconsistency (sys.path.append vs src. prefix) | `foreman.py`, `worker.py` |
| LOW | base.py abstract method signature differs from actual implementations | `src/specialists/base.py` |
| DEFERRED | Kitchen-sink dependencies (Registrar hardcodes 35+ packages) | `council.py` |
| RESOLVED | Test suite added (parser, executor, scorer, showboat, rodney) | `tests/` |
| DEFERRED | Full auto deployment (domain, host, HTTPS) | -- |
| DEFERRED | Pyramid Summaries (StrongDM multi-resolution context) | -- |

### Git Status

- 3 commits, last: `3cc6884` (factory dashboard webapp spec)
- 12 modified files, 14 untracked files (new docs, webapp, scripts)
- Uncommitted work from v1.5-v1.7 (dashboard, DTU, monetization, remote client docs)

---

## Roadmap

| Version | Status | Content |
|---------|--------|---------|
| v0.1-0.4 | Done | Prototype |
| v1.0 | Done | Async parallelism, architectural hardening |
| v1.1 | Done | Playwright, Help Oracle, logging, Git |
| v1.2 | Done | Multi-stack (Python/Node, React/HTMX) |
| v1.3 | Done | Council sophistication, enrichment, marketing pipeline |
| v1.4 | Done | DTU integration (9 mocks, env injection) |
| v1.5 | Done | Dashboard, progress protocol, industrial startup |
| v1.6 | Done | StrongDM analysis, remote client demo, monetization plan |
| v1.7 | Done | Token reporting, GitManager wiring, RunManifest manifest.json |
| v1.8 | **Current** | Scenario-based satisfaction testing, scenario parser/executor/scorer |
| v2.0 | Planned | Multi-agent recursive self-healing, meta-mcp agent lifecycle, Pyramid Summaries |
| v2.1 | **Phase 1 Done** | Deploy artifacts (deploy.sh, deploy_config.example.yaml). Phases 2–3 planned |
| **March** | **Planned** | **Expert Panel meta-judge** (12 personas, elaborated analysis, go/no-go synthesis) — see `docs/JURY_ROOM_PLAN.md` |

---

## Economics

| Metric | StrongDM | Dark App Factory |
|--------|----------|-----------------|
| Planning model | Claude/GPT-4 | Opus 4.6 / Llama 3.1 (configurable) |
| Coding model | Claude/GPT-4 | Ollama local (Qwen, DeepSeek) |
| Cost per dev/day | ~$1,000 in API tokens | ~$0 (local inference) |
| Hardware requirement | Cloud API | Local RTX 4090 (24GB) or similar |
| Context window | Managed | 64k+ tokens mandatory (OLLAMA_CONTEXT_LENGTH) |

### Monetization (planned, not yet live)

- **Product A**: EUR 100 "Make My App" -- client describes app, you build it
- **Product B**: EUR 300 "Dark Factory + Support" -- client gets the factory + 30 min support
- **Austrian setup**: Einzelunternehmen, Kleinunternehmer (no VAT under EUR 35k)

---

## File Map

```
dark-app-factory/
  factory.py              # Pipeline orchestrator (DTU lifecycle, worker/judge)
  foreman.py              # Planner (plan, enrich, research, help, log)
  worker.py               # Execution engine (19 specialists, parallel, validation)
  judge.py                # Quality gate (Playwright, RunManifest, LLM verdict)
  run_manifest.py         # Process boot orchestrator (DTU env injection)
  questionnaire.py        # Human feedback loop
  start_factory.ps1       # One-command launcher (zombie cleanup + dashboard)
  vibe.md / vibe_current.md  # User intent input
  .env.example               # Environment variable template
  specs/ scenarios/       # Generated specs and test scenarios
  dtu/main.py             # Digital Twin Universe (9 mock services)
  src/
    llm_client.py         # AsyncOpenAI with token tracking + temperature
    auditor.py            # Playwright-based runtime auditor
    ghost_extractor.py    # (new, untracked)
    specialists/
      base.py             # Abstract Specialist (context injection, validation)
      council.py          # 19 specialist implementations
    deployment/
      deploy_artifacts.py   # Generates deploy.sh, deploy_config.example.yaml, docker-compose.prod.yml
    pwa/
      pwa_artifacts.py     # PWA: manifest.json, sw.js, icons, meta injection
    verification/
      scenario_parser.py    # GIVEN/WHEN/THEN parser from scenarios.md
      scenario_executor.py  # HTTP + browser scenario execution engine
      satisfaction_scorer.py # Probabilistic satisfaction scoring (mechanical + LLM)
      showboat_runner.py    # Showboat CLI wrapper (demo artifacts)
      rodney_runner.py      # Rodney CLI wrapper (browser automation)
      ruffy_runner.py       # Post-Worker ruff + mypy lint (demos/lint-report.txt)
    utils/
      logger.py           # DarkLogger singleton
      help_oracle.py      # Tiered help system
      git_manager.py      # Git init/commit
      stack_profile.py    # Multi-stack parsing/embedding
      progress.py         # ProgressTracker singleton
  web/
    server.py             # Dashboard backend (FastAPI, port 8002)
    index.html            # Dashboard frontend (glassmorphic UI)
  docs/
    JURY_ROOM_PLAN.md     # Expert Panel meta-judge (12 personas, March implementation)
    MOBILE_ROADMAP.md     # PWA done; Capacitor/iOS/Android/AltStore plan
    ARCHITECTURE.md       # System design (DTU, progress, pyramid summaries)
    STRONGDM_ANALYSIS.md  # StrongDM comparison and economics
    META_MCP_INTEGRATION.md  # meta-mcp cross-utilization plan
    REMOTE_CLIENT_DEMO.md    # Client demo (notebook + Tailscale + goliath)
    FULL_AUTO_DEPLOYMENT.md  # Gap analysis (domain, host, HTTPS)
    MONETIZATION_PLAN.md     # EUR 100/300 products, Austrian setup
  demos/
    README.md             # Demo artifact index
    build-report.md       # Showboat-generated build report (auto-created)
    audit-report.md       # Showboat-generated judge audit (auto-created)
    screenshots/          # Rodney-captured browser screenshots
  skills/                 # Domain knowledge files
  tests/
    test_scenario_parser.py     # 15 tests for GIVEN/WHEN/THEN parsing
    test_scenario_executor.py   # Executor tests (path resolution, body gen, assertion eval)
    test_satisfaction_scorer.py # Scorer tests (mechanical, LLM-assisted, aggregation)
    test_showboat_runner.py
    test_rodney_runner.py
    test_stack_profile.py
    test_base_specialist.py
    test_dtu.py
    test_run_manifest.py
  scripts/
    cleanup_zombies.ps1   # Port zombie killer
```

---

## Cross-Ecosystem Links

| Integration | Status | Notes |
|------------|--------|-------|
| meta-mcp | Planned | Expose factory phases as meta-mcp agents (start/poll/report) |
| advanced-memory-mcp | Potential | Worker could query ADN for patterns before code generation |
| Showboat/Rodney | **Integrated** | Post-build demo artifacts (Showboat) + browser verification with screenshots (Rodney) |
| mcp-central-docs | This doc | Status tracking and pattern reference |

---

## Immediate Next Actions (from NEXTSTEPS.md)

1. ~~Wire GitManager~~ -- DONE: initialize() after worker, commit_changes after judge pass
2. ~~Fix RunManifest~~ -- DONE: write_manifest_from_output() after worker
3. ~~Report token usage~~ -- DONE: foreman_client and worker_client get_usage_summary() at end
4. ~~Import factory phases directly~~ -- DONE: worker and judge run in-process via async
5. **Remaining**: Dynamic dependency selection (Registrar), .env.example (DONE), Foreman scenario template hint (DONE)
