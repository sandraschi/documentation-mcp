# Dev Sandbox Hardening Profile (Fleet, Stepwise)

## Why

Sandbox guidance is often too vague ("just run in sandbox").  
This document defines an incremental hardening model that reduces compromise risk while keeping developer recoverability.

## Non-negotiables

- no profile is bulletproof
- controls are optional and stepwise
- recovery path must be tested before strict controls are enforced

## Fleet Profiles

## Profile 0 - Baseline

- project-local virtual envs and lockfiles
- pinned dependencies with cooling-off policy
- no production secrets in development context
- regular VM/project snapshots

## Profile 1 - Balanced

- host sharing disabled by default (enable case-by-case)
- clipboard integration minimized
- short-lived scoped credentials
- dependency upgrades run in disposable snapshot first
- scanner preflight before upgrade promotion

## Profile 2 - Strict

- no host mounts or clipboard integration
- egress allow-list network policy
- disposable environment per risky test cycle
- strict scanner gates for package/tool intake

## Profile 3 - Quarantine

- isolated network segment
- no host integration channels
- forensic logging and evidence capture
- used for suspicious package execution and incident triage

## Stepwise Adoption Pattern

- start at baseline
- move to balanced for dependency/tooling changes
- move to strict for untrusted or high-risk testing
- use quarantine for suspected compromise

Do not jump to strict globally without rollback rehearsal.

## Lockout Avoidance

- keep at least one known-good snapshot
- maintain one emergency admin access path
- keep profile rollback checklist next to hardening config
- stage one control at a time and verify access

## Fast Incident Path (Poisoned Dependency Scenario)

1. isolate machine/VM
2. rotate potentially exposed credentials
3. capture evidence
4. rebuild from known-good image/snapshot
5. restore from pre-incident backup
6. validate before reconnecting to trusted networks

## CI/CD Policy Tie-In

- default 7-day cooling-off for dependency upgrades
- urgent security hotfix exceptions allowed with explicit approval
- release lane should include malware-heuristic and vuln scans

## Suggested Ownership

- security owner defines profile policy and exceptions
- repo owners apply profile escalation during risky changes
- platform owner maintains snapshots, rollback docs, and drills

## Agentic Workflow Pattern (Sandbox Runbook)

Recommended run sequence for risky dependency/tooling work:

1. start disposable sandbox
2. install pinned dev toolchain via scripted bootstrap
3. run development/test/scan workflow inside sandbox
4. write all outputs to a single sandbox output directory
5. export outputs to host
6. tear down sandbox or revert snapshot

This pattern improves repeatability, reduces host exposure, and keeps evidence centralized.

### Output Discipline

- one run id per execution
- one output folder per run
- include:
  - scanner reports
  - test results
  - console logs
  - environment metadata

### Safety Notes

- never export entire sandbox filesystem to host
- export only predesignated output folder
- use short-lived credentials for each run and revoke on teardown

## Access Gating Matrix (Optional, Recommended)

Per-run access should be declared explicitly:

- local LLM/Ollama: `disabled | proxy_bridged | direct_host`
- RTX 4090/GPU: `disabled | enabled`
- Docker: `disabled | socket_proxy | host_engine`
- GitHub: `disabled | read_only | read_write`

Default guidance:

- baseline/balanced: favor `proxy_bridged`, `socket_proxy`, and `read_only`
- strict: disable by default; enable only with explicit justification
- quarantine: disable all unless forensic workflow requires temporary exception

## Pre-Run Questionnaire Gate

Use a startup questionnaire before each risky run:

1. run objective (`scan`, `upgrade`, `incident`, `test`)
2. untrusted dependency/tool involved?
3. local LLM access level needed?
4. GPU access needed?
5. Docker access needed?
6. GitHub scope needed?
7. production secrets required? (should be no)
8. selected profile and reason
9. rollback snapshot verified?
10. output folder and run id set?

If requested access exceeds profile policy, require approval or profile escalation.
