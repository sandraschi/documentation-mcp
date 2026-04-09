# Scanner Pattern/Antipattern Criteria (Starter)

## Purpose

Starter criteria to help reviewers interpret findings from:

- `mcp-scanner`
- `skill-scanner`

This is a working draft for practical triage. It is intentionally incomplete and should evolve with real findings.

## How to Use This Doc

- Use criteria for prioritization, not absolute truth.
- Map findings to severity and exploitability.
- Escalate ambiguous cases to manual review.

## Dual Assessment Lens

Always evaluate findings through two separate lenses:

- **Interface quality lens**
  - Can MCP clients discover the tools?
  - Are schemas/params correct and usable?
  - Is invocation behavior consistent and debuggable?
- **Payload safety lens**
  - Does the implemented behavior stay within declared intent?
  - Are sensitive operations constrained even with hostile input?
  - Are side effects, egress, and privilege boundaries controlled?

Passing the first lens does not imply passing the second.

## Cross-Tool Pattern Criteria (Usually Good)

- **Least privilege surfaces**
  - tools/skills expose narrow, explicit capabilities
  - no hidden broad shell or filesystem powers
- **Behavior-description alignment**
  - description/docstring matches actual code behavior
  - no mismatch between stated purpose and side effects
- **Explicit trust boundaries**
  - untrusted input validated before sensitive operations
  - external content treated as tainted by default
- **Constrained execution**
  - fixed command allow-lists, path allow-lists, schema validation
  - no dynamic execution from untrusted data
- **Observable actions**
  - high-impact operations logged with audit metadata
  - security-relevant failures are visible and actionable

## Cross-Tool Antipattern Criteria (Usually Risky)

- **Capability smuggling**
  - benign-named tool/skill performs privileged actions
- **Instruction laundering**
  - untrusted text from prompts/resources is transformed into executable instructions
- **Implicit privilege escalation**
  - user-provided content influences shell/network/file actions without controls
- **Description obfuscation**
  - vague docs that hide side effects or data destinations
- **Unbounded outbound access**
  - broad network egress with sensitive data reachability

## MCP Scanner Criteria

### Positive Patterns

- tool descriptions clearly declare:
  - data sources
  - outbound destinations
  - mutation side effects
- server instructions include defensive usage guidance.
- readiness findings are low and operational safeguards exist (timeouts, retries, error paths).

### Antipatterns

- tool claims read-only behavior but performs writes/network exfiltration.
- remote-fetch content is forwarded to privileged tools without policy checks.
- generic execution tools (`run`, `exec`, `shell`) exposed without strict guardrails.
- inconsistent safety logic spread across helpers that bypass top-level checks.

## Skill Scanner Criteria

### Positive Patterns

- `SKILL.md` explicitly states boundaries, prohibited actions, and confirmation requirements.
- scripts in skill package avoid dynamic eval/exec and avoid unsafe shell interpolation.
- policy profile is explicit (`strict`/custom) with documented suppression process.
- overlap checks and linting reduce ambiguous trigger descriptions.

### Antipatterns

- trigger text is broad/vague and can be hijacked by unrelated contexts.
- hidden binary/script payloads with unclear provenance.
- indirect prompt chains that can coerce high-impact actions without human checkpoint.
- reliance on "model will behave" rather than enforceable constraints.

## Severity Heuristic (Initial)

- **Critical**
  - direct path to secret exfiltration, arbitrary command execution, or irreversible high-impact action
- **High**
  - credible exploit chain exists with moderate effort
- **Medium**
  - exploitable in specific contexts, mitigations partly present
- **Low/Info**
  - hardening gaps, hygiene issues, or weak signals without clear exploit path

## Triage Questions

- Is untrusted input reaching privileged operation?
- Is there a guardrail that is enforceable or only advisory text?
- Does implementation perform unstated side effects?
- Can the action be constrained by schema, allow-list, or runtime policy?
- Is there an auditable trail and rollback path?

## Known Limits

- no scanner can fully prove absence of prompt-injection or emergent misuse
- false positives and false negatives are expected
- findings must be interpreted in system context (runtime policy, secrets handling, user confirmation)

## Next Iteration TODO

- add concrete real-world examples from fleet repos
- add repo-specific rule mappings and suppression examples
- add "safe-by-construction" templates for tool/skill authors
