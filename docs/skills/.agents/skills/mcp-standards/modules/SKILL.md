<!--
SOURCE: MCP Standards Collection - Unified Skill
AUTHOR: MCP Community
LICENSE: MIT
CREATED: 2026-01-20
-->

---
name: mcp-standards
description: Complete MCP standards reference - scaffolding, packaging, sampling, documentation, testing, error handling, monitoring, and CI/CD workflows.
---

# MCP Standards - Complete Reference

The comprehensive standards collection for the MCP (Model Context Protocol) ecosystem. This skill provides access to all MCP standards documentation, from initial scaffolding to production deployment.

## Standards Overview

### Core Standards Categories

#### 🚀 **Development Standards**
- **[MCP Scaffolding](./docs/standards/mcp-scaffolding.md)** - Project structure, FastMCP server templates, initial setup
- **[MCPB Packaging](./docs/standards/mcpb-packaging.md)** - Build, distribution, PyPI/MCP Registry publishing
- **[AI Sampling](./docs/standards/ai-sampling.md)** - FastMCP 2.14.3+ sampling methods for creative AI workflows

#### 🎨 **Creative & Specialized MCP Servers**
- **Blender MCP** - 3D modeling and rendering integration
- **GIMP MCP** - Image editing and manipulation
- **Inkscape MCP** - Vector graphics and design
- **Unity MCP** - Game engine integration
- **VRChat MCP** - VR social platform integration

#### 🌐 **Web & Integration**
- **[Frontend SOTA](./docs/standards/frontend-sota.md)** - React, TypeScript, Tailwind CSS development
- **[MCP-WebApp Integration](./docs/standards/mcp-webapp-integration.md)** - Backend-frontend MCP bridging

#### 🛠️ **Operations & Quality**
- **[GitHub Workflows](./docs/standards/github-workflows.md)** - CI/CD, releases, pre-commit hooks, issues/PR management
- **[Testing Standards](./docs/standards/testing.md)** - Unit, integration, E2E testing, coverage, automation
- **[Error Handling](./docs/standards/error-handling.md)** - Exception management, recovery patterns, circuit breakers
- **[Logging Standards](./docs/standards/logging.md)** - Structured logging, correlation, aggregation
- **[Monitoring Standards](./docs/standards/monitoring.md)** - Prometheus, Grafana, Loki, alerting
- **[Docker Standards](./docs/standards/docker-containerization.md)** - Container architecture, security, orchestration

#### 📖 **Documentation & Process**
- **[Documentation Standards](./docs/standards/documentation.md)** - Repository docs, README structures, CHANGELOG, PRD
- **Security Standards** - Authentication, authorization, data protection
- **Performance Standards** - Optimization, scaling, benchmarking

## FastMCP Version Requirements

**All MCP servers MUST use FastMCP 2.14.3+ for SOTA compliance.**

### Key Features in 2.14.3+
- ✅ **Sampling Method Support** - True AI workflows for creative MCP servers
- ✅ **Enhanced Response Patterns** - Rich AI dialogue capabilities
- ✅ **Server Lifespan Management** - Stateful server operations
- ✅ **Advanced Tool Management** - Improved tool orchestration

### Version Update Commands
```bash
# Update all MCP servers to latest version
standards update-versions --version 2.14.3

# Check version compatibility
standards check-versions

# Update single repository
standards update-fastmcp --repo blender-mcp --version 2.14.3
```

## Repository Structure Standards

### Required Structure for All MCP Servers
```
mcp-server-name/
├── src/mcp_server_name/
│   ├── __init__.py
│   ├── server.py          # Main FastMCP server
│   └── tools/            # Tool implementations
├── tests/
│   ├── __init__.py
│   └── test_server.py
├── docs/
│   ├── integrations/    # Integration guides
│   ├── api/            # API documentation
│   └── examples/       # Usage examples
├── pyproject.toml        # FastMCP 2.14.3+
├── .mcp-standards.yaml   # Standards compliance config
├── .cursorrules         # IDE-specific rules
├── .cursorignore       # IDE ignore patterns
├── README.md           # Short overview
├── INSTALL.md          # Detailed installation
├── CHANGELOG.md        # Version history
├── PRD.md             # Product requirements
└── CONTRIBUTING.md    # Contribution guidelines
```

### File Standards Checklist
- [ ] `pyproject.toml` - FastMCP 2.14.3+ dependency
- [ ] `README.md` - Links to INSTALL.md, API docs
- [ ] `INSTALL.md` - Platform-specific installation
- [ ] `CHANGELOG.md` - Semantic versioning format
- [ ] `PRD.md` - Success metrics and requirements
- [ ] `docs/` - Integration and API documentation
- [ ] `tests/` - Minimum 80% coverage
- [ ] `.mcp-standards.yaml` - Compliance configuration

## Status Classification System

### Implementation Status Indicators
- **✅ Tested and Working** - Verified functionality with tests
- **🟡 Implemented but Untested** - Code exists but needs testing
- **🔄 Planned** - On roadmap but not yet implemented
- **❌ Deprecated** - Will be removed in future version

### Example Status Usage
```markdown
## Features

### ✅ Tested and Working
- Basic MCP server functionality
- Tool registration and execution
- Error handling and logging

### 🟡 Implemented but Untested
- Advanced sampling features
- Multi-server orchestration

### 🔄 Planned
- Real-time collaboration features
- Advanced AI integration
```

## Critical Standards by Category

### Error Handling - Zero Tolerance Policy
**MANDATORY**: All errors must be handled. No empty catch blocks allowed.

```python
# ✅ CORRECT - Detailed error handling
try:
    risky_operation()
except ValueError as e:
    logger.error(f"Invalid value provided: {e}", extra={
        "operation": "risky_operation",
        "error_type": type(e).__name__,
        "user_id": user_id
    })
    raise ValidationError("Invalid input value", details={"original_error": str(e)})

# ❌ WRONG - Empty catch
try:
    risky_operation()
except:
    pass  # NEVER ALLOWED
```

### Logging - Structured and Comprehensive
**MANDATORY**: All logs must include context, correlation IDs, and actionable information.

```python
logger.error(
    f"Tool execution failed: {tool_name}",
    extra={
        "tool_name": tool_name,
        "request_id": request_id,
        "user_id": user_id,
        "execution_time_ms": execution_time,
        "error_type": type(e).__name__,
        "suggested_actions": ["Check network connectivity", "Verify API credentials"]
    }
)
```

### Testing - Minimum Coverage Requirements
- **Unit Tests**: 80% minimum coverage
- **Integration Tests**: 70% minimum coverage
- **Critical Paths**: 95% coverage required

### Documentation - Multi-Level Structure
- **README.md**: Short overview with links
- **INSTALL.md**: Platform-specific installation
- **API Documentation**: Complete reference with examples
- **Integration Guides**: Third-party service integration

## Development Workflow Standards

### Repository Creation
```bash
# Create new MCP server with full standards compliance
standards create-repo --type mcp-server --name my-server

# This generates:
# - Complete project structure
# - All required documentation
# - CI/CD pipelines
# - Testing framework
# - Standards compliance configuration
```

### Compliance Checking
```bash
# Check single repository
standards check-repo --repo /path/to/repo

# Check all repositories
standards check-all-repos

# Generate compliance report
standards compliance-report --format html --output report.html
```

### Documentation Generation
```bash
# Generate all documentation for repository
standards generate-docs --repo /path/to/repo

# Generate specific document
standards generate-doc --type README --repo /path/to/repo

# Update all documentation
standards docs-update --repos all
```

## CI/CD Standards

### Required GitHub Actions Workflows
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: pip install -e ".[dev]"
    - name: Run tests
      run: pytest --cov=src/ --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Docker Containerization Standards

### Container Security Requirements
```dockerfile
# Non-root user
RUN useradd --create-home --shell /bin/bash mcp
USER mcp

# Minimal base image
FROM python:3.11-slim

# No privileged operations
# Proper permission management
```

### Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "
import sys
try:
    from mcp_server import app
    tools = app.list_tools()
    print(f'Health check passed: {len(tools)} tools available')
    sys.exit(0)
except Exception as e:
    print(f'Health check failed: {e}')
    sys.exit(1)
"
```

## Monitoring Standards

### Prometheus Metrics
```python
# Required MCP server metrics
from prometheus_client import Counter, Histogram, Gauge

requests_total = Counter('mcp_requests_total', 'Total MCP requests', ['method', 'status'])
request_duration = Histogram('mcp_request_duration_seconds', 'Request duration', ['method'])
tool_executions = Counter('mcp_tool_executions_total', 'Tool executions', ['tool_name', 'status'])
health_status = Gauge('mcp_health_status', 'Health status (1=healthy, 0=unhealthy)')
```

### Grafana Dashboards
- **MCP Server Overview**: Request rates, error rates, tool performance
- **System Health**: Memory usage, CPU utilization, disk space
- **Error Analysis**: Error trends, categorization, resolution tracking

## Security Standards

### Authentication & Authorization
- **API Key Management**: Secure storage and rotation
- **Permission Levels**: Role-based access control
- **Audit Logging**: All security events logged

### Data Protection
- **Encryption**: Data at rest and in transit
- **Input Validation**: All inputs sanitized
- **Output Encoding**: Prevent injection attacks

## Performance Standards

### Response Time Requirements
- **API Calls**: < 200ms average response time
- **Tool Execution**: < 5 seconds for complex operations
- **Health Checks**: < 100ms response time

### Resource Usage Limits
- **Memory**: < 500MB per server instance
- **CPU**: < 50% average utilization
- **Disk**: < 1GB storage per server

## Standards Compliance Verification

### Automated Compliance Checking
```bash
# Comprehensive compliance audit
standards compliance-report --comprehensive --format json

# Results include:
# - Standards version compliance
# - FastMCP version requirements
# - Documentation completeness
# - Testing coverage
# - Security compliance
# - Performance benchmarks
```

### Compliance Score Calculation
- **Documentation**: 20% - README, INSTALL, API docs complete
- **Code Quality**: 25% - Linting, type hints, testing coverage
- **Security**: 20% - Input validation, authentication, logging
- **Performance**: 15% - Response times, resource usage
- **Standards Adherence**: 20% - FastMCP versions, file structure

## Integration Patterns

### MCP-WebApp Integration
```typescript
// React hook for MCP server integration
const useMCPServer = (serverName: string) => {
  const [server, setServer] = useState(null);
  const [loading, setLoading] = useState(false);

  const connect = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/mcp/connect/${serverName}`);
      const session = await response.json();
      setServer(session);
    } finally {
      setLoading(false);
    }
  };

  const callTool = async (toolName: string, args: any) => {
    const response = await fetch(`/api/mcp/${server.session_id}/call/${toolName}`, {
      method: 'POST',
      body: JSON.stringify(args)
    });
    return response.json();
  };

  return { server, loading, connect, callTool };
};
```

### WebSocket Real-time Updates
```python
# FastAPI WebSocket for real-time MCP communication
@app.websocket("/ws/mcp/{session_id}")
async def mcp_websocket(websocket: WebSocket, session_id: str):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()

            if data["type"] == "call_tool":
                result = await mcp_bridge.call_tool(
                    session_id,
                    data["tool_name"],
                    data.get("args", {})
                )
                await websocket.send_json({
                    "type": "tool_result",
                    "result": result
                })
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
```

## Troubleshooting Standards

### Common Issues & Solutions

#### FastMCP Version Conflicts
```
❌ Error: FastMCP version below required 2.14.3
✅ Solution: standards update-versions --version 2.14.3
```

#### Missing Documentation
```
❌ Error: Missing required documentation files
✅ Solution: standards generate-docs --repo . --force
```

#### Compliance Failures
```
❌ Error: Repository not standards compliant
✅ Solution: standards check-repo --repo . --fix
```

#### Testing Coverage Issues
```
❌ Error: Test coverage below 80%
✅ Solution: Add unit tests and integration tests
```

## Version History

### Standards Evolution
- **v1.6**: Initial standards with FastMCP 2.14.1+
- **v1.7**: Enhanced sampling support, modular documentation
- **v1.8**: Complete standards collection, automated management

### FastMCP Version Requirements
- **v1.6-v1.7**: FastMCP 2.14.1+ minimum
- **v1.8+**: FastMCP 2.14.3+ minimum (sampling support)

## Getting Help

### Documentation Resources
- **Central Standards**: [MCP Central Docs STANDARDS.md](https://github.com/sandraschi/mcp-central-docs/blob/main/STANDARDS.md)
- **Specific Standards**: `docs/standards/` directory
- **API References**: Standards-specific API documentation

### Community Support
- **Issues**: [MCP Central Docs Issues](https://github.com/sandraschi/mcp-central-docs/issues)
- **Discussions**: [MCP Community Discussions](https://github.com/modelcontextprotocol/community/discussions)
- **Standards Updates**: Subscribe to standards changelog

---

**This skill serves as the complete reference for all MCP ecosystem standards, ensuring consistency, quality, and interoperability across all MCP servers and tools.**