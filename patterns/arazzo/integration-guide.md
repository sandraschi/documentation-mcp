# Arazzo Integration Guide (SOTA Standard)

This guide details how to implement Arazzo-compliant workflow descriptors within individual MCP servers to facilitate autonomous orchestration.

---

## 1. Exposing Workflows

SOTA MCP servers should serve a static YAML or JSON file containing their common logic patterns.

### Directory Structure
```text
/src
  /workflows
    - maintenance-mission.yaml
    - setup-project.yaml
  /web
    - server.py (FastAPI)
```

### FastAPI Implementation
```python
@app.get("/api/v1/workflows")
async def get_workflows():
    # Merge and return all .yaml files in /src/workflows
    return await workflow_manager.list_all()
```

---

## 2. Defining a Mission

A "Mission" is a complex workflow spanning multiple steps.

### Example: OBS Automated Recording
`obs-mcp/src/workflows/record-demo.yaml`

```yaml
arazzo: 1.0.1
info:
  title: "Automated Demo Recording"
workflows:
  - workflowId: "record-and-log"
    steps:
      - stepId: "switch-scene"
        operationId: "set_scene"
        parameters:
          - name: "sceneName"
            value: "Demo"
      - stepId: "start-obs-recording"
        operationId: "start_recording"
      - stepId: "wait-for-completion"
        # Custom wait logic or event trigger
        successCriteria:
          - condition: "$statusCode == 200"
      - stepId: "log-to-memory"
        operationId: "write_note"
        requestBody:
          payload:
            title: "Recording Complete"
            content: "Demo recorded successfully at $steps.start-obs-recording.timestamp"
```

---

## 3. SEP-1577 Sampling Engine

When Antigravity encounters a request matching an Arazzo `workflowId`, it enters **Agentic Execution Mode**:

1. **Resolution**: The engine fetches the Arazzo spec from the registry.
2. **Sampling**: The engine uses the LLM to map user intent to Arazzo `inputs`.
3. **Execution**: The engine runs the sequence, reporting progress via the Task View UI.
4. **Validation**: Each step's output is checked against defined criteria.

---

## 4. Troubleshooting

- **Circular Dependencies**: Arazzo validation will fail if `Step A` requires `Step B` which requires `Step A`.
- **Latency Squashing**: The Arazzo runner executes steps sequentially or in parallel depending on the `dependsOn` graph.
