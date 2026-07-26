# MCP Standards Skill Table of Contents

## Overview
- [SKILL.md](SKILL.md) - Main skill definition and overview
- [README.md](../README.md) - Installation and usage guide

## Standards Documentation

### Core Development Standards
- [MCP Scaffolding](modules/mcp-scaffolding.md) - Project structure, FastMCP server templates, initial setup
- [MCPB Packaging](modules/mcpb-packaging.md) - Build, distribution, PyPI/MCP Registry publishing
- [AI Sampling](modules/ai-sampling.md) - FastMCP 3.2+ sampling methods for creative AI workflows

### Frontend & Integration
- [Frontend SOTA](modules/frontend-sota.md) - React, TypeScript, Tailwind CSS development standards
- [MCP-WebApp Integration](modules/mcp-webapp-integration.md) - Backend-frontend MCP bridging patterns

### DevOps & Quality
- [GitHub Workflows](modules/github-workflows.md) - CI/CD, releases, pre-commit hooks, issues/PR management
- [Testing Standards](modules/testing.md) - Unit, integration, E2E testing, coverage, automation
- [Error Handling](modules/error-handling.md) - Exception management, recovery patterns, circuit breakers
- [Logging Standards](modules/logging.md) - Structured logging, correlation, aggregation
- [Monitoring](modules/monitoring.md) - Prometheus, Grafana, Loki, alerting
- [Docker Standards](modules/docker-containerization.md) - Container architecture, security, orchestration

### Documentation & Process
- [Documentation Standards](modules/documentation.md) - README structures, CHANGELOG, PRD, integrations

## Quick Reference

### FastMCP Requirements
- Minimum Version: FastMCP 3.2+
- Sampling Support: Required for creative MCP servers
- Enhanced Patterns: Rich AI dialogue capabilities

### Status Classification
- ✅ **Tested and Working** - Verified functionality
- 🟡 **Implemented but Untested** - Needs testing
- 🔄 **Planned** - On roadmap
- ❌ **Deprecated** - Will be removed

### Error Handling - Zero Tolerance
- All errors must be handled - no empty catch blocks
- Detailed error logging with correlation IDs
- Comprehensive recovery mechanisms

## Implementation Examples

### Repository Structure
```
mcp-server/
├── src/mcp_server_name/
├── tests/
├── docs/
├── pyproject.toml
├── README.md
└── .mcp-standards.yaml
```

### FastMCP Server Template
```python
from fastmcp import FastMCP

app = FastMCP("server-name", version="1.0.0")

@app.tool()
async def example_tool(param: str) -> dict:
    """Tool with proper error handling."""
    try:
        result = await process_data(param)
        return {"success": True, "result": result}
    except ValueError as e:
        logger.error(f"Invalid parameter: {e}", extra={
            "operation": "example_tool",
            "param": param,
            "error_type": type(e).__name__
        })
        return {"error": "Invalid parameter", "details": str(e)}
```

## Next Steps

1. **Browse specific standards** using the modules above
2. **Check implementation status** for your MCP server
3. **Apply standards compliance** to ensure quality
4. **Reference detailed examples** for proper implementation

---

**This hierarchical structure allows Claude Desktop to load only the relevant standards documentation for the current task, providing thousands of lines of detailed guidance without overwhelming the context window.**