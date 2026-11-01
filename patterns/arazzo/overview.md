# Arazzo Specification 1.0.1: MCP Fleet Standard

**Version**: 1.0.1  
**Status**: DRAFT (February 2026 SOTA)  
**Context**: Advanced Agentic Orchestration

---

## I. Introduction

The **Arazzo Specification** defines a machine-readable format for describing API workflows—sequences of calls that achieve a specific objective. In the Antigravity/Sandra ecosystem, Arazzo serves as the **Logic Bridge** between individual MCP tools and complex Agentic Missions.

### Why Arazzo?
- **Deterministic Sequences**: Unlike raw LLM tool-calling, Arazzo defines specific dependency chains.
- **State Management**: Pass outputs from one step as inputs to the next with structured mapping.
- **Fail-Fast Logic**: Define success criteria for each step to prevent cascading errors.
- **SEP-1577 Compatibility**: Arazzo workflows can be executed autonomously by the Antigravity sampling engine.

---

## II. Core Structures

### 1. Workflow Object
The top-level object describing a mission.
```yaml
arazzo: 1.0.1
info:
  title: "VRChat Content Pipeline"
  version: 1.0.0
sourceDescriptions:
  - name: "vrchat-api"
    url: "http://localhost:10712/openapi.json"
    type: openapi
```

### 2. Steps
Individual actions within a workflow.
```yaml
workflows:
  - workflowId: "process-avatar"
    steps:
      - stepId: "download-model"
        operationId: "get_model_url"
        parameters:
          - name: "avatarId"
            value: "$inputs.avatarId"
      - stepId: "trigger-import"
        operationId: "unity_import"
        requestBody:
          payload:
            url: "$steps.download-model.outputs.url"
```

---

## III. Integration Patterns

### Workflow Providers
Every SOTA MCP server MUST expose `GET /api/v1/workflows` providing its local workflow catalog.

### Arazzo Runner
An executor component (integrated into Antigravity) that:
1. Parses the Arazzo definition.
2. Resolves dependencies.
3. Executes calls via MCP transport.
4. Validates outputs against `successCriteria`.

---

## IV. Best Practices

- **Zero Over-Automation**: Use Arazzo for deterministic logic; let the LLM handle semantic decisions.
- **Sanitized Inputs**: Use Arazzo parameters to enforce type safety before calling tools.
- **Traceability**: All Arazzo execution steps MUST log to the `observability-mcp` bus.
