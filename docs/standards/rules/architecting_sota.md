# SOTA 2026 Architecting with LLMs

**Scope:** Strategic architecture generation (systems, pipelines, multi-service stacks).
**NOT** for tactical MCP server or webapp scaffolding (see `mcp_scaffolding.md`, `WEBAPP_STANDARDS.md`).

## The Problem

Large language models suffer from a **"look what I know" failure mode** when architecting:
they reach for exotic-sounding real projects to demonstrate breadth, even when those
projects are the wrong tool (or don't exist as imagined). A 200-line Python shim is
rejected in favor of a Docker image that doesn't expose the required API.

## The Standard

### 1. Architecture Spec First, Code Second

Never generate code in the same pass as the architecture. Two-prompt sequence:

1. **Spec pass:** Generate component list, external deps, API contracts, network topology.
   Every third-party dependency must include a specific version tag + one-sentence
   description of what API surface it exposes.
2. **Code pass:** Only after the spec is approved. No new external deps in code pass.

This catches fiction at the spec level before it's baked into 41 files.

### 2. Default to a Shim

For every external dependency (Docker image, third-party API, library), the model must
answer: **"Why can't this be a 50-line Python/FastAPI script?"**

- Acceptable justifications: existing fleet integration, battle-tested security boundary,
  protocol compliance that's non-trivial to reimplement.
- Unacceptable: "it's a well-known project," "it has a cool name," "it was designed for this."

The default answer is a custom shim. Exotic dependencies are the exception, not the rule.

### 3. Pin-and-Verify Every External Image

Every external Docker image or API dependency in the architecture must include:

- Specific version tag (SHA or semver, not `latest`)
- Exact API endpoints it exposes (path, method, request/response shape)
- Network requirements (WAN yes/no, ports)

If the model cannot credibly describe the API surface of a dependency, it is
hallucinated. Remove it and replace with a shim.

### 4. Self-Own the Critical Path

The pipeline's critical path components must be self-owned (custom code the team
controls). Third-party dependencies are only acceptable for:

- **Peripheral** concerns (monitoring, logging, auth providers)
- **Hard** problems the team won't solve better (cryptography, protocol parsing)

The sanitizer, adjudicator, and worker in an execution pipeline are critical path.
DeepSeek API (cloud LLM-as-a-service) is acceptable because it provides unique
value. The glue around it should be custom.

### 5. Recognize the Failure Mode

Train yourself and the model to spot the pattern:

- Architecture includes a name-dropped project you've heard of but never used
- The dependency is from a domain the model is likely to "know about" but not
  "have used" (agent frameworks, security tools, exotic databases)
- The README describes the project doing something different from what the
  architecture assigns it

When any of these trigger, apply step 2: default to a shim.

### 6. Spec Must Survive Context Resets

The architecture spec (step 1) must be written to a file (`ARCHITECTURE.md` or
`SPEC.md`) before any code is generated. This is the source of truth that:

- Survives context compaction and resets
- Can be reviewed by humans before implementation
- Prevents the model from introducing new hallucinated dependencies during code pass
