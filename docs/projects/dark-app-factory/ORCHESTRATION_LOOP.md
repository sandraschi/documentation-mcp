# The Orchestration Loop

The **Dark App Factory** follows a rigorous, step-by-step industrial pipeline. This loop ensures that the transition from a qualitative "vibe" to a quantitative "verified app" is seamless and auditable.

## 🔄 The 7-Step Lifecycle

### Step 1: Research (`foreman research`)
The Foreman uses `WebFinder` to crawl the latest 2026 SOTA standrads for the requested domain.
- **Goal**: Ensure the stack is modern.
- **Output**: `research_data/` directory.

### Step 2: Planning (`foreman plan`)
The Foreman converts the research and vibe into a concrete technical specification.
- **Goal**: Define the blueprint.
- **Output**: `specs.md` and `scenarios.md`.

### Step 3: DTU Spawning (`factory dtu`)
The Digital Twin Universe starts on port 8001.
- **Goal**: Provide a safe, mocked environment for the build phase.

### Step 4: Parallel Build (`worker build`)
The Specialist Council executes in tiers using `asyncio.gather`.
- **Goal**: Parallelized code generation.
- **Logic**: Tier 0 -> Tier 1 -> Tier 2 -> Tier 3 -> Tier 4.

### Step 5: Landing Page Generation
The Foreman generates a self-contained marketing landing page.
- **Goal**: Immediate distribution readiness.

### Step 6: Satisficer Audit (`judge audit`)
The Judge boots the app and runs Playwright against the `scenarios.md`.
- **Goal**: Empirical verification.
- **Output**: `critique.md` (Feedback loop if failed).

### Step 7: Final Launch
The orchestrator packages the verified app with its PR kit.
- **Goal**: Ready for deployment.

## 🛠️ The Feedback Loop
If the Satisficer fails an audit, the `critique.md` is fed back into the `Generalist` specialist. The build process (Step 4) is then re-triggered for the specific failing components, creating a self-healing loop that persists until the Satisficer issues a **PASS** verdict.
