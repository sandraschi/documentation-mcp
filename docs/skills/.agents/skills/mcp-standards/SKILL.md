---
name: mcp-standards
description: Use when developing MCP servers to access comprehensive standards for scaffolding, packaging, sampling, documentation, testing, error handling, monitoring, and CI/CD workflows.
---

# MCP Standards - Complete Reference

The comprehensive standards collection for the MCP (Model Context Protocol) ecosystem. This skill provides access to all MCP standards documentation, from initial scaffolding to production deployment.

## When to Use This Skill

**Use this skill for:**
- MCP server development and standards compliance
- FastMCP version requirements and migration
- Repository structure and project setup
- Documentation standards and practices
- Testing, error handling, and monitoring standards
- CI/CD workflows and deployment patterns

**Don't use for:**
- General programming questions
- Non-MCP specific development
- Individual coding problems

## Standards Categories

### 🚀 **Development Standards**
- [MCP Scaffolding](./modules/mcp-scaffolding.md) - Project structure and server templates
- [MCPB Packaging](./modules/mcpb-packaging.md) - Build and distribution standards
- [AI Sampling](./modules/ai-sampling.md) - FastMCP 3.2+ sampling workflows

### 🎨 **Frontend & Integration**
- [Frontend SOTA](./modules/frontend-sota.md) - React, TypeScript, Tailwind standards
- [MCP-WebApp Integration](./modules/mcp-webapp-integration.md) - Backend-frontend bridging

### 🛠️ **DevOps & Quality**
- [GitHub Workflows](./modules/github-workflows.md) - CI/CD and release management
- [Testing Standards](./modules/testing.md) - Comprehensive testing requirements
- [Error Handling](./modules/error-handling.md) - Exception management and recovery
- [Logging Standards](./modules/logging.md) - Structured logging patterns
- [Monitoring](./modules/monitoring.md) - Prometheus, Grafana, Loki setup
- [Docker Standards](./modules/docker-containerization.md) - Container architecture

### 📖 **Documentation & Process**
- [Documentation Standards](./modules/documentation.md) - README, CHANGELOG, PRD standards

## Key Requirements

### FastMCP Version
**Minimum: FastMCP 3.2+** - Required for sampling support and enhanced AI workflows.

### Status Classification
- ✅ **Tested and Working** - Verified functionality with tests
- 🟡 **Implemented but Untested** - Code complete, testing needed
- 🔄 **Planned** - On development roadmap
- ❌ **Deprecated** - Will be removed

### Error Handling - Zero Tolerance
All errors must be handled with detailed logging - no empty catch blocks allowed.

## Quick Implementation Guide

### 1. Repository Setup
```bash
# Create new MCP server
mkdir my-mcp-server
cd my-mcp-server

# Initialize with proper structure
# (See MCP Scaffolding standards)
```

### 2. FastMCP Configuration
```python
from fastmcp import FastMCP

# Minimum version requirement
app = FastMCP("server-name", version="1.0.0")

# Implement sampling for creative servers
@app.tool()
async def sample_workflow(iterations: int = 5):
    # (See AI Sampling standards)
    pass
```

### 3. Error Handling
```python
try:
    result = await risky_operation()
except SpecificError as e:
    logger.error(f"Detailed error: {e}", extra={
        "correlation_id": request_id,
        "operation": "risky_operation"
    })
    # Recovery logic
```

### 4. Testing Requirements
- Unit tests: 80% minimum coverage
- Integration tests: 70% minimum coverage
- End-to-end tests for critical workflows

## Progressive Usage

### Level 1: Basic Setup
Start with [MCP Scaffolding](./modules/mcp-scaffolding.md) for project structure.

### Level 2: Core Development
Implement [AI Sampling](./modules/ai-sampling.md) for creative workflows.

### Level 3: Quality Assurance
Apply [Testing Standards](./modules/testing.md) and [Error Handling](./modules/error-handling.md).

### Level 4: Production Ready
Implement [Monitoring](./modules/monitoring.md) and [Docker Standards](./modules/docker-containerization.md).

## Common Patterns

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

### Tool Implementation
```python
@app.tool()
async def example_tool(ctx, param: str) -> dict:
    """Tool with proper error handling and logging."""
    try:
        result = await process_data(param)
        logger.info("Tool executed successfully", extra={
            "tool": "example_tool",
            "param_length": len(param)
        })
        return {"success": True, "result": result}
    except Exception as e:
        logger.error(f"Tool execution failed: {e}", extra={
            "tool": "example_tool",
            "error_type": type(e).__name__,
            "correlation_id": ctx.get("correlation_id")
        })
        return {"error": str(e)}
```

## Standards Compliance Checklist

- [ ] FastMCP 3.2+ minimum version
- [ ] Proper project structure (MCP Scaffolding)
- [ ] Comprehensive error handling (no empty catches)
- [ ] Detailed logging with correlation IDs
- [ ] 80%+ test coverage
- [ ] Multi-level documentation (README, INSTALL, CHANGELOG)
- [ ] CI/CD workflows configured
- [ ] Monitoring and health checks implemented

## Getting Help

### Standards Reference
- [Table of Contents](./_toc.md) - Complete overview
- [Specific Standards](./modules/) - Detailed implementation guides
- [MCP Central Docs](https://github.com/sandraschi/mcp-central-docs) - Source documentation

### Troubleshooting
- Check [Error Handling](./modules/error-handling.md) for common issues
- Review [Testing Standards](./modules/testing.md) for validation problems
- Consult [Logging Standards](./modules/logging.md) for debugging setup

---

**This skill provides hierarchical access to thousands of lines of MCP standards documentation, loading only the relevant sections for your current development task.**