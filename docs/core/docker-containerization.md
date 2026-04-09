# Docker Containerization Standards

## Overview
Standards for containerizing MCP servers using Docker, ensuring consistent deployment, isolation, and scalability across all MCP projects.

## Container Architecture

### Base Images
```dockerfile
# Use Python slim images for MCP servers
FROM python:3.11-slim

# Use Node.js for webapp-integrated MCP servers
FROM node:18-alpine

# Use multi-stage builds for production
FROM python:3.11-slim as builder
FROM python:3.11-slim as runtime
```

### MCP Server Container Structure
```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash mcp
USER mcp

# Set working directory
WORKDIR /app

# Copy dependency files
COPY --chown=mcp:mcp pyproject.toml uv.lock ./

# Install dependencies
RUN pip install --no-cache-dir -e .

# Copy application code
COPY --chown=mcp:mcp src/ ./src/

# Health check for MCP servers
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from mcp_server import app; print('Server imports successfully')"

# Expose port if web interface
EXPOSE 8000

# Start command
CMD ["python", "-m", "mcp_server.server"]
```

## Multi-Stage Builds for Creative MCP Servers

### Blender MCP Container
```dockerfile
# Multi-stage build for Blender MCP
FROM blender:latest as blender-base

FROM python:3.11-slim

# Copy Blender installation
COPY --from=blender-base /opt/blender /opt/blender

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Set Blender path
ENV BLENDER_PATH=/opt/blender/blender

# Copy MCP server code
COPY src/ ./src/

CMD ["python", "-m", "blender_mcp.server"]
```

### GIMP/Inkscape Creative Tools
```dockerfile
FROM ubuntu:22.04

# Install creative tools
RUN apt-get update && apt-get install -y \
    gimp \
    inkscape \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install MCP server
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY src/ ./src/

# X11 forwarding for GUI tools (optional)
ENV DISPLAY=:0

CMD ["python", "-m", "creative_mcp.server"]
```

## Docker Compose Orchestration

### MCP Server Stack
```yaml
version: '3.8'

services:
  mcp-server:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "${MCP_PORT:-8000}:8000"
    environment:
      - MCP_ENV=production
      - LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config:ro
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "from mcp_server import app; print('healthy')"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - mcp-network

  # Optional web interface
  mcp-web:
    build:
      context: ./webapp
      dockerfile: Dockerfile
    ports:
      - "${WEB_PORT:-3000}:3000"
    depends_on:
      mcp-server:
        condition: service_healthy
    networks:
      - mcp-network

networks:
  mcp-network:
    driver: bridge
```

## Environment Management

### Environment Variables
```bash
# Required environment variables
MCP_ENV=production
LOG_LEVEL=INFO
MCP_PORT=8000

# Database connections (if applicable)
DATABASE_URL=postgresql://user:pass@localhost:5432/mcp_db

# External service integrations
BLENDER_PATH=/opt/blender/blender
GIMP_PATH=/usr/bin/gimp
INKSCAPE_PATH=/usr/bin/inkscape

# Security
SECRET_KEY=your-secret-key-here
API_KEYS=comma,separated,keys
```

### Configuration Management
```python
# Environment-based configuration
import os
from pydantic import BaseSettings

class MCPSettings(BaseSettings):
    env: str = os.getenv("MCP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    port: int = int(os.getenv("MCP_PORT", "8000"))

    # Creative tool paths
    blender_path: str = os.getenv("BLENDER_PATH", "/usr/bin/blender")
    gimp_path: str = os.getenv("GIMP_PATH", "/usr/bin/gimp")

    # Database
    database_url: str = os.getenv("DATABASE_URL")

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret")
    api_keys: list = os.getenv("API_KEYS", "").split(",") if os.getenv("API_KEYS") else []

    class Config:
        env_file = ".env"

settings = MCPSettings()
```

## Security Standards

### Non-Root Containers
```dockerfile
# Create non-root user
RUN useradd --create-home --shell /bin/bash --user-group --uid 1000 mcp

# Set proper permissions
RUN chown -R mcp:mcp /app
USER mcp
```

### Secret Management
```yaml
# docker-compose with secrets
version: '3.8'

services:
  mcp-server:
    # ... other config
    secrets:
      - api_keys
      - database_password

secrets:
  api_keys:
    file: ./secrets/api_keys.txt
  database_password:
    file: ./secrets/db_password.txt
```

### Network Security
```yaml
# Internal network for MCP servers
networks:
  mcp-internal:
    internal: true

  mcp-external:
    # Only expose necessary ports
```

## Performance Optimization

### Resource Limits
```yaml
services:
  blender-mcp:
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2.0'
        reservations:
          memory: 2G
          cpus: '1.0'
```

### GPU Access for Creative Tools
```yaml
# GPU access for Blender, GIMP with GPU acceleration
services:
  creative-mcp:
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=compute,utility
    volumes:
      - /usr/lib/x86_64-linux-gnu/libnvidia-ml.so:/usr/lib/x86_64-linux-gnu/libnvidia-ml.so:ro
```

## Monitoring and Observability

### Health Checks
```dockerfile
# Comprehensive health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "
import sys
try:
    from mcp_server import app
    # Test basic functionality
    tools = app.list_tools()
    print(f'Health check passed: {len(tools)} tools available')
    sys.exit(0)
except Exception as e:
    print(f'Health check failed: {e}')
    sys.exit(1)
"
```

### Logging Configuration
```python
# Structured logging for containers
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        return json.dumps(log_entry)

# Configure for containerized environments
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Logs to stdout for Docker
    ]
)
```

## Development vs Production

### Development Containers
```yaml
# Development with hot reload
services:
  mcp-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app
      - /app/node_modules  # Don't overwrite node_modules
    environment:
      - MCP_ENV=development
      - LOG_LEVEL=DEBUG
    ports:
      - "8000:8000"
    command: ["uvicorn", "mcp_server:app", "--reload", "--host", "0.0.0.0"]
```

### Production Containers
```yaml
# Production with optimizations
services:
  mcp-prod:
    build:
      context: .
      dockerfile: Dockerfile.prod
    environment:
      - MCP_ENV=production
      - LOG_LEVEL=WARNING
    ports:
      - "8000:8000"
    restart: unless-stopped
```

## Testing Containerized MCP Servers

### Container Integration Tests
```python
# Test MCP server in container
import docker
import requests

def test_mcp_container():
    client = docker.from_env()

    # Start container
    container = client.containers.run(
        "mcp-server:latest",
        detach=True,
        ports={"8000/tcp": 8000}
    )

    try:
        # Wait for health check
        import time
        time.sleep(10)

        # Test MCP functionality
        response = requests.post(
            "http://localhost:8000/mcp/call",
            json={"tool": "test_tool", "args": {}}
        )

        assert response.status_code == 200
        assert "result" in response.json()

    finally:
        container.stop()
        container.remove()
```

## Deployment Strategies

### Docker Swarm/Kubernetes
```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcp-server
  template:
    metadata:
      labels:
        app: mcp-server
    spec:
      containers:
      - name: mcp-server
        image: mcp-server:latest
        ports:
        - containerPort: 8000
        env:
        - name: MCP_ENV
          value: "production"
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

## Next Steps
After containerization, proceed to:
1. [CI/CD Standards](./cicd.md) - Automated building and deployment
2. [Monitoring Standards](./monitoring.md) - Container observability
3. [Scaling Standards](./scaling.md) - Performance and load balancing
