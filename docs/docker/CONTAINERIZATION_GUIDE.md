# MCP Server Containerization Guide

**Last Updated:** 2025-12-03  
**Status:** Active

---

## Overview

When and how to containerize MCP servers for production deployment, testing, and distribution.

---

## When to Containerize

### ✅ Good Use Cases

**Production Deployment:**
- Running MCP servers as services on remote machines
- Kubernetes/cloud deployments
- Multi-tenant environments
- Isolated environments with specific dependencies

**Development:**
- Consistent development environments across team
- Testing in isolation
- CI/CD pipelines
- Integration testing

**Distribution:**
- MCPB packaging with Docker support
- Easy deployment for users
- Cross-platform compatibility

### ⚠️ Consider Carefully

**Claude Desktop Integration:**
- Claude Desktop typically spawns MCP servers via stdio
- Containerized servers require HTTP transport or Docker exec
- May add complexity without benefit

**Local Development:**
- Virtual environments often simpler
- Direct process spawning is faster
- Easier debugging

### ❌ Don't Containerize If

- MCP server is simple with few dependencies
- Only used with Claude Desktop (stdio)
- Development-only tool
- Adds more complexity than value

---

## Containerization Patterns

### Pattern 1: HTTP Transport + Container

Best for remote servers and multi-machine setups.

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Source code
COPY . .

# Expose HTTP port
EXPOSE 3000

# Run in HTTP mode
CMD ["python", "server.py", "--http", "3000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  mcp-server:
    build: .
    ports:
      - "3000:3000"
    environment:
      - API_KEY=${API_KEY}
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

**Usage:**
```bash
# Start container
docker compose up -d

# Access via HTTP
curl http://localhost:3000/health
curl -X POST http://localhost:3000/mcp/v1/tools/call \
  -d '{"tool": "example", "params": {}}'
```

---

### Pattern 2: Stdio via Docker Exec

For Claude Desktop integration with containerized servers.

**Docker Wrapper Script:**
```python
#!/usr/bin/env python3
"""
Wrapper script for containerized MCP server
Translates stdio to Docker exec calls
"""
import subprocess
import sys
import json

CONTAINER_NAME = "mcp-server"

def main():
    # Ensure container is running
    subprocess.run(["docker", "start", CONTAINER_NAME], 
                   capture_output=True)
    
    # Forward stdio to container
    proc = subprocess.Popen(
        ["docker", "exec", "-i", CONTAINER_NAME, 
         "python", "-m", "server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr
    )
    
    # Copy stdin → container
    for line in sys.stdin:
        proc.stdin.write(line.encode())
        proc.stdin.flush()
    
    proc.stdin.close()
    
    # Copy container stdout → stdout
    for line in proc.stdout:
        sys.stdout.write(line.decode())
        sys.stdout.flush()

if __name__ == "__main__":
    main()
```

**Claude Desktop Config:**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["wrapper.py"]
    }
  }
}
```

---

### Pattern 3: Hybrid (Recommended)

Support both stdio (local) and HTTP (remote) from same container.

**Server Code:**
```python
from fastmcp import FastMCP
import uvicorn
import sys

mcp = FastMCP("hybrid-server")

@mcp.tool()
def example_tool(param: str) -> dict:
    """Works in both modes"""
    return {"result": param}

if __name__ == "__main__":
    if "--http" in sys.argv:
        # HTTP mode for remote access
        port = 3000
        uvicorn.run(mcp.get_app(), host="0.0.0.0", port=port)
    else:
        # Stdio mode for Claude Desktop
        mcp.run(transport="stdio")
```

**Usage:**
```bash
# Local stdio (Claude Desktop)
python server.py

# Containerized HTTP (remote access)
docker run -p 3000:3000 my-server --http 3000
```

---

## Best Practices

### 1. Multi-Stage Builds

Reduce image size with multi-stage builds:

```dockerfile
# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
CMD ["python", "server.py"]
```

### 2. Non-Root User

Run as non-root for security:

```dockerfile
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser
```

### 3. Health Checks

Add health checks to Dockerfile:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

### 4. Environment Variables

Use `.env` file for configuration:

```yaml
services:
  mcp-server:
    env_file: .env
    environment:
      - MODE=production
```

### 5. Volumes for Data

Persist data with volumes:

```yaml
services:
  mcp-server:
    volumes:
      - mcp_data:/app/data
      - ./config:/app/config:ro

volumes:
  mcp_data:
```

---

## Security Considerations

### Production Checklist

- [ ] Run as non-root user
- [ ] Use specific base image versions (not `latest`)
- [ ] Scan images for vulnerabilities (`docker scan`)
- [ ] Minimize image layers
- [ ] Remove build tools in final image
- [ ] Use secrets management (not hardcoded)
- [ ] Enable read-only filesystem where possible
- [ ] Limit container resources (CPU, memory)
- [ ] Use private registries for sensitive images

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker compose logs service-name

# Check if port is in use
Get-NetTCPConnection -LocalPort 3000

# Inspect container
docker inspect container-name
```

### Permission Issues

```bash
# Fix volume permissions
docker compose run --rm service-name chown -R appuser:appuser /app/data
```

### Build Cache Issues

```bash
# Clear build cache
docker builder prune

# Complete rebuild
docker compose build --no-cache
```

### Network Issues

```bash
# Check container network
docker network ls
docker network inspect network-name

# Test connectivity
docker compose exec service-name ping other-service
```

---

## Examples by Project Type

### FastMCP Server (Python)

See: `../projects/*/STRUCTURE.md` for specific examples:
- `plex-mcp` - Media server integration
- `devices-mcp` - IoT device control
- `calibre-mcp` - Library management

### Fullstack App (Python + Node.js)

See: `../projects/myai/STRUCTURE.md`
- Backend + Frontend in separate containers
- Shared networks
- Volume management

### Monitoring Stack

See: `MONITORING_STACK.md`
- Grafana, Prometheus, Loki, Promtail
- Health checks
- Data persistence

---

## Related Documentation

- [BUILD_OPTIMIZATION.md](BUILD_OPTIMIZATION.md) - Fast Docker builds
- [MONITORING_STACK.md](MONITORING_STACK.md) - Complete monitoring setup
- [../monitoring/](../monitoring/) - Full monitoring documentation
- [../projects/](../projects/) - Project-specific Docker setups

---

**Last Updated**: 2025-12-03

