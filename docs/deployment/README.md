# MCP Server Deployment Guide

**Last Updated:** 2025-12-04

Complete guide to deploying MCP servers to production environments.

---

## 📚 In This Section

| Document | Purpose |
|----------|---------|
| **[production-checklist.md](production-checklist.md)** | Pre-deployment checklist |
| **[security.md](security.md)** | Security hardening guide |
| **[monitoring.md](monitoring.md)** | Monitoring and observability |
| **[pypi-zero-install.md](pypi-zero-install.md)** | PyPI & OIDC "Zero-Install" standard |

---

## 🎯 Deployment Options

### 1. Local (Stdio)

**Best for**: Claude Desktop, local development

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["D:/path/to/server.py"]
    }
  }
}
```

**Pros:**
- ✅ Simple setup
- ✅ No network configuration
- ✅ Secure (local only)

**Cons:**
- ❌ Local only
- ❌ No remote access

---

### 2. Docker Container

**Best for**: Production, consistent environments

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "server.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  mcp-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_KEY=${API_KEY}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Deploy:**
```powershell
docker compose up -d
```

→ Complete Docker guide: [../docker/README.md](../docker/README.md)

---

### 3. Cloud Platforms

#### AWS (ECS/Fargate)

```yaml
# task-definition.json
{
  "family": "mcp-server",
  "containerDefinitions": [{
    "name": "mcp-server",
    "image": "your-repo/mcp-server:latest",
    "portMappings": [{
      "containerPort": 8000,
      "protocol": "tcp"
    }],
    "environment": [
      {"name": "API_KEY", "value": "secret"}
    ]
  }]
}
```

#### Google Cloud Run

```powershell
gcloud run deploy mcp-server `
  --image gcr.io/project/mcp-server `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated
```

#### Azure Container Instances

```powershell
az container create `
  --resource-group myResourceGroup `
  --name mcp-server `
  --image your-repo/mcp-server:latest `
  --dns-name-label mcp-server `
  --ports 8000
```

---

### 4. Kubernetes

```yaml
# deployment.yaml
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
        image: your-repo/mcp-server:latest
        ports:
        - containerPort: 8000
        env:
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: mcp-secrets
              key: api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: mcp-server
spec:
  selector:
    app: mcp-server
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

---

## 🔒 Security Checklist

### Essential Security Measures

- [ ] **HTTPS/TLS** - Use SSL certificates (Let's Encrypt)
- [ ] **Authentication** - API keys, OAuth, JWT tokens
- [ ] **Rate Limiting** - Prevent abuse
- [ ] **Input Validation** - Validate all inputs
- [ ] **Environment Variables** - Never hardcode secrets
- [ ] **CORS Configuration** - Restrict origins
- [ ] **Firewall Rules** - Limit network access
- [ ] **Regular Updates** - Keep dependencies current

→ Complete security guide: [security.md](security.md)

---

## 📊 Monitoring Setup

### Health Check Endpoint

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/ready")
async def ready():
    # Check dependencies
    db_ok = await check_database()
    cache_ok = await check_cache()
    
    if db_ok and cache_ok:
        return {"status": "ready"}
    else:
        return {"status": "not ready"}, 503
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Metrics
tool_calls = Counter('mcp_tool_calls_total', 'Total tool calls', ['tool_name', 'status'])
tool_duration = Histogram('mcp_tool_duration_seconds', 'Tool execution time', ['tool_name'])
active_connections = Gauge('mcp_active_connections', 'Active client connections')

@mcp.tool()
def monitored_tool(param: str) -> str:
    """Tool with monitoring"""
    tool_calls.labels(tool_name="monitored_tool", status="started").inc()
    
    try:
        with tool_duration.labels(tool_name="monitored_tool").time():
            result = f"Result: {param}"
        
        tool_calls.labels(tool_name="monitored_tool", status="success").inc()
        return result
    
    except Exception as e:
        tool_calls.labels(tool_name="monitored_tool", status="error").inc()
        raise

# Start metrics server
start_http_server(9090)
```

→ Complete monitoring guide: [monitoring.md](monitoring.md)  
→ Grafana/Prometheus stack: [../../monitoring/README.md](../../monitoring/README.md)

---

## 🚀 Deployment Workflow

### 1. Development

```powershell
# Local testing
fastmcp dev server.py

# Run tests
pytest tests/

# Check linting
ruff check .
```

### 2. Build

```powershell
# Build Docker image
docker build -t mcp-server:latest .

# Test container locally
docker run -p 8000:8000 mcp-server:latest
```

### 3. Deploy

```powershell
# Push to registry
docker push your-repo/mcp-server:latest

# Deploy to production
docker compose -f docker-compose.prod.yml up -d

# Or Kubernetes
kubectl apply -f k8s/
```

### 4. Verify

```powershell
# Check health
curl https://your-server.com/health

# Test tool call
curl -X POST https://your-server.com/mcp/v1/tools/call `
  -H "Content-Type: application/json" `
  -d '{"tool": "example_tool", "params": {"param": "test"}}'

# Check metrics
curl https://your-server.com:9090/metrics
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy MCP Server

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest ruff
      
      - name: Run tests
        run: pytest tests/
      
      - name: Lint
        run: ruff check .
  
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t mcp-server:${{ github.sha }} .
      
      - name: Push to registry
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker push mcp-server:${{ github.sha }}
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Deploy command here
          echo "Deploying..."
```

---

## 📈 Scaling Strategies

### Horizontal Scaling

**Load Balancer + Multiple Instances**

```
                  ┌─► Server 1
Client ─► LB ─────┼─► Server 2
                  └─► Server 3
```

**Kubernetes HPA (Horizontal Pod Autoscaler)**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: mcp-server-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: mcp-server
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Vertical Scaling

**Increase Resources**

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "2000m"
```

---

## 🔧 Configuration Management

### Environment Variables

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Required
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY required")

# Optional with defaults
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
PORT = int(os.getenv("PORT", "8000"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
```

### Config Files

```yaml
# config.yaml
server:
  host: "0.0.0.0"
  port: 8000
  workers: 4

security:
  api_key_required: true
  rate_limit: 100  # requests per minute

monitoring:
  prometheus_port: 9090
  log_level: "INFO"
```

```python
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

PORT = config["server"]["port"]
```

---

## 📚 Related Documentation

- [production-checklist.md](production-checklist.md) - Pre-deployment checklist
- [security.md](security.md) - Security hardening
- [monitoring.md](monitoring.md) - Monitoring setup
- [../docker/README.md](../docker/README.md) - Docker guide
- [../../monitoring/README.md](../../monitoring/README.md) - Grafana/Prometheus

---

**Ready to deploy? Start with the [production-checklist.md](production-checklist.md)!** 🚀

