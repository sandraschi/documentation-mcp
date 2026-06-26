# External Agent Security Scanners (Fleet Guidance)

## Scope

Fleet-level guidance for evaluating and adopting external security tooling around:

- `cisco-ai-defense/mcp-scanner`
- `cisco-ai-defense/skill-scanner`
- `cisco-ai-defense/defenseclaw`
- `NVIDIA/OpenShell`
- `NVIDIA/NemoClaw`

This is the primary reference. Project-local copies should defer to this document.

## Live Status (2026-03-26)

- `mcp-scanner`: live, actively maintained, recent releases on PyPI.
- `skill-scanner`: live, actively maintained, recent releases on PyPI.
- `defenseclaw`: live on GitHub, early but active.
- `OpenShell`: live runtime project from NVIDIA.
- `NemoClaw`: live reference stack (early preview/alpha positioning).

## Tool Roles

### MCP Scanner

Best for MCP server attack surface analysis:

- tools/prompts/resources/instructions scanning
- behavioral source scanning
- static/offline scan paths for CI/CD

Primary use: MCP server repos and deployed MCP endpoints.

### Skill Scanner

Best for skills supply chain analysis:

- scans skill packages and `SKILL.md` ecosystems
- supports behavioral + LLM + policy-based tuning
- supports SARIF and pre-commit/CI workflows

Primary use: repositories with `.cursor/skills`, Codex/OpenAI-style skills, or skill bundles.

### DefenseClaw

Best interpreted currently as governance/control-plane direction rather than a drop-in scanner.

Primary use: watchlist and strategic evaluation.

### OpenShell / NemoClaw

Best for runtime policy enforcement and containment:

- isolation boundary around autonomous agent execution
- policy-layer enforcement outside agent control

Primary use: long-running agents with privileged tool/file/network access.

## Fleet Recommendation

Adopt now:

- `mcp-scanner` and `skill-scanner` as practical controls.

Track and evaluate:

- `defenseclaw` for governance maturity.
- `OpenShell`/`NemoClaw` patterns for runtime hardening architecture.

## External Clone Policy (`D:\Dev\repos\external`)

Recommendation: **clone all five repos, but gate production adoption by maturity**.

Why clone:

- source audit and reproducibility
- local patching/experimentation
- commit pinning for deterministic CI behavior
- faster incident triage when detection behavior changes

Suggested layout:

```text
D:\Dev\repos\external\
  cisco-ai-defense\
    mcp-scanner\
    skill-scanner\
    defenseclaw\
  nvidia\
    openshell\
    nemoclaw\
```

## Rollout Sequence

### Phase 1 (Immediate)

- run scanner jobs in report-only mode
- collect baseline findings and false-positive patterns

### Phase 2 (Near-term)

- enforce severity thresholds in CI (`high`/`critical`)
- publish machine-readable scan artifacts (e.g., SARIF where supported)
- maintain explicit suppression baselines with review ownership

### Phase 3 (Strategic)

- add runtime containment patterns inspired by OpenShell
- separate policy definition from agent behavior

## Limits and Risk Model

These tools are best-effort detection, not proof systems.

- no findings does not mean safe
- false positives and false negatives are unavoidable
- behavior may drift as rules/models/versions change

## Indirect Prompt-Injection Hardening

Complete prevention is not realistically automatable in the general case.

Operationally, assume residual risk and combine:

- scanner-based detection
- least-privilege tool interfaces
- runtime policy/sandbox enforcement
- high-impact action confirmation gates
- robust audit logs, monitoring, and rollback

This is defense-in-depth, not single-control security.

Related interpretation guide:

- [SCANNER_PATTERN_ANTIPATTERN_CRITERIA.md](SCANNER_PATTERN_ANTIPATTERN_CRITERIA.md)

## Minimum Control Set for Fleet Repos

For MCP server repos:

- source + endpoint scans with `mcp-scanner`
- required review for new/changed high-risk tools
- capability review when tool descriptions and code behavior diverge

For skill-bearing repos:

- `skill-scanner` in pre-commit and CI
- policy presets tuned per repo risk profile
- manual review for high-severity or ambiguous findings

For autonomous runtime deployments:

- isolate execution context
- constrain filesystem/network/tool permissions
- protect secrets outside the agent execution boundary

## Concrete Usage Plan (30-Day)

### Owners and Cadence

- **Security owner:** defines policy thresholds, approves suppressions.
- **Repo owners:** fix findings in their repos, add missing tests/guards.
- **Cadence:** PR scans + nightly full scans + weekly triage review.

### Week 1: Bootstrap and Baseline

1. Clone external references into `D:\Dev\repos\external`:
   - `cisco-ai-defense/mcp-scanner`
   - `cisco-ai-defense/skill-scanner`
   - `cisco-ai-defense/defenseclaw`
   - `NVIDIA/OpenShell`
   - `NVIDIA/NemoClaw`
2. Install scanner CLIs in a dedicated security venv/tool env.
3. Run report-only baselines on priority repos:
   - MCP repos: `robofang`, `email-mcp`, `ocr-mcp`, `davinci-resolve-mcp`
   - skill-bearing repos: any repo containing `.cursor/skills` or `SKILL.md`
4. Store outputs under each repo at `security-reports\scanner-baseline\`.
5. Open remediation issues grouped by severity and exploitability.

### Week 2: PR Integration (Non-blocking)

- Add PR workflows:
  - `mcp-scanner` for MCP server repos
  - `skill-scanner` for skill-bearing repos
- Keep non-blocking for one week; collect:
  - false positives
  - flaky analyzer behavior
  - average scan duration
- Tune policy presets and suppression workflow.

### Week 3: Enforcement (Blocking)

- Turn on fail gates:
  - fail on `high`/`critical` for new findings
  - do not fail for approved baseline suppressions
- Require human review for:
  - tool capability expansion
  - tool-description/implementation mismatch
  - network egress or shell execution behavior changes

### Week 4: Runtime Controls

- Pilot runtime isolation profile for one high-risk autonomous workflow:
  - strict filesystem allow-list
  - constrained network egress
  - explicit tool permission boundaries
- Evaluate OpenShell patterns for adaptation to fleet environments.

## Reference Command Patterns (PowerShell)

### MCP Scanner

```powershell
# Example: behavioral source scan
mcp-scanner behavioral "D:\Dev\repos\ocr-mcp\src" --format by_severity

# Example: scan remote MCP endpoint
mcp-scanner --analyzers yara,readiness remote --server-url "http://127.0.0.1:8000/mcp" --format summary
```

### Skill Scanner

```powershell
# Example: scan one skill directory with behavioral analysis
skill-scanner scan "D:\Dev\repos\robofang\.cursor\skills\example-skill" --use-behavioral --format markdown

# Example: recursive scan with CI gate
skill-scanner scan-all "D:\Dev\repos\robofang\.cursor\skills" --recursive --use-behavioral --fail-on-severity high --format sarif --output "D:\Dev\repos\robofang\security-reports\skill-scan.sarif"
```

## Merge Gate Policy (Initial)

- Block PR if:
  - any unsuppressed `critical` finding exists
  - any new unsuppressed `high` finding exists
- Warn-only for `medium` in first month; review after trend data is available.
- Suppressions must include:
  - reason
  - expiry date
  - approving owner

## Metrics to Track

- new findings per repo per week (by severity)
- mean time to remediate `high`/`critical`
- suppression count and expiry compliance
- scanner runtime and failure rate
- rate of behavior/code-description mismatch findings

