# Arazzo Integration Guide for MCP Servers

This guide outlines how to implement Arazzo Standard (1.0.1) workflows within the MCP SOTA architecture.

---

## 📋 Integration Strategy

The primary goal is to enable MCP servers to serve **Workflow Descriptions** alongside their standard tool registrations. This allows agents to discover and execute pre-defined sequences of tools.

### 1. Workflow Exposure Endpoint
SOTA-compliant MCP servers should implement a standardized endpoint for workflow discovery:

- **Endpoint**: `/api/v1/workflows`
- **Method**: `GET`
- **Response**: A JSON/YAML list of Arazzo Description Objects.

### 2. Referencing Tools as Source Descriptions
In an Arazzo document, the `sourceDescriptions` should point to the MCP server's OpenAPI schema or a dedicated tool manifest.

```yaml
arazzo: 1.0.1
info:
  title: Unity Scene Setup Workflow
  version: 1.0.0
sourceDescriptions:
  - name: unity-mcp
    type: openapi
    url: http://localhost:10831/openapi.json
```

### 3. Defining Steps
Workflow steps reference operations from the source description.

```yaml
workflows:
  - workflowId: setup_basic_scene
    description: Creates a new scene and adds a logic controller.
    steps:
      - stepId: create_scene
        operationId: create_new_scene
        parameters:
          - name: name
            in: body
            value: "MainScene"
      - stepId: add_controller
        operationId: add_component
        parameters:
          - name: scene
            in: body
            value: "$steps.create_scene.outputs.sceneId"
          - name: componentType
            in: body
            value: "LogicController"
```

## 🛠️ Implementation with FastMCP

If using `FastMCP`, you can store Arazzo YAML files in an `assets/workflows/` directory and serve them via a custom FastAPI route.

### Example (Python/FastAPI):

```python
from fastapi import APIRouter
import yaml

router = APIRouter()

@router.get("/api/v1/workflows")
async def get_workflows():
    with open("assets/workflows/scene_setup.yaml", "r") as f:
        return yaml.safe_load(f)
```

## 🧪 Verification

1. **Schema Validation**: Use the Arazzo 1.0.1 JSON Schema to validate your YAML at build time.
2. **Execution Test**: Use `arazzo-runner` to verify that the sequence executes correctly against a running instance of your MCP server.

```bash
uv run arazzo-runner run ./workflows/scene_setup.yaml --env-file .env
```
