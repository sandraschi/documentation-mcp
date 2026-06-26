# App Resilience & Anti-Crash Tools

**Comprehensive guide to building resilient MCP applications with crash recovery, health monitoring, and auto-restart mechanisms**

## Overview

This document covers the complete ecosystem of tools and patterns for building resilient MCP applications that can withstand crashes, handle failures gracefully, and recover automatically.

---

## 📚 Related Documentation

- **[Orphan Guard Pattern](../patterns/MCP_ORPHAN_GUARD_PATTERN.md)** - Process monitoring and zombie prevention
- **[MCP Monitoring Standards](../monitoring/MCP_MONITORING_STANDARDS.md)** - Comprehensive observability
- **[Production Deployment](../deployment/README.md)** - Health checks and container resilience

---

## 🎯 Resilience Categories

### 1. Development Resilience
- File watching and hot reload
- Auto-restart during development
- Error recovery and debugging

### 2. Runtime Resilience
- Process management and monitoring
- Health checks and liveness probes
- Crash recovery and restart policies

### 3. Application Resilience
- Circuit breakers and fallback patterns
- Graceful degradation
- Error boundaries and recovery

### 4. Infrastructure Resilience
- Container health checks
- Service discovery and load balancing
- Backup and disaster recovery

---

## 🔍 File Watching & Hot Reload

### Nodemon (Node.js)

**Best for**: Node.js MCP servers, Express APIs, development workflow

#### Basic Setup
```json
// package.json
{
  "scripts": {
    "dev": "nodemon src/server.js",
    "dev:inspect": "nodemon --inspect src/server.js"
  },
  "nodemonConfig": {
    "watch": ["src/**/*.js", "src/**/*.ts"],
    "ext": "js,ts,json",
    "ignore": ["src/**/*.test.js", "src/**/*.spec.js"],
    "exec": "node --inspect=0.0.0.0:9229 src/server.js",
    "env": {
      "NODE_ENV": "development"
    }
  }
}
```

#### Advanced Configuration
```json
// nodemon.json
{
  "watch": [
    "src/**/*.js",
    "src/**/*.ts",
    "config/**/*.json",
    "migrations/**/*.js"
  ],
  "ext": "js,ts,json,env",
  "ignore": [
    "src/**/*.test.js",
    "src/**/*.spec.js",
    "logs/*",
    "node_modules/*"
  ],
  "exec": "node --max-old-space-size=4096 --inspect=0.0.0.0:9229",
  "env": {
    "NODE_ENV": "development",
    "LOG_LEVEL": "debug"
  },
  "delay": 500,
  "verbose": true,
  "restartable": "rs",
  "colours": true,
  "legacyWatch": false,
  "signal": "SIGUSR2"
}
```

#### MCP Server Integration
```javascript
// src/server.js - MCP server with nodemon support
import { FastMCP } from 'fastmcp';
import { OrphanGuard } from './mcp-orphan-guard.js';

const mcp = new FastMCP({
  name: 'resilient-mcp-server',
  version: '1.0.0'
});

// Graceful shutdown handling for nodemon restarts
process.on('SIGUSR2', () => {
  console.log('🔄 Nodemon restart signal received, shutting down gracefully...');
  mcp.close().then(() => {
    process.exit(0);
  });
});

// Orphan guard for crash protection
const orphanGuard = new OrphanGuard();
orphanGuard.protect();

// Your MCP tools here
mcp.tool('health_check', 'Check server health', {}, async () => {
  return {
    status: 'healthy',
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    timestamp: new Date().toISOString()
  };
});

mcp.start();
```

### Chokidar (Universal)

**Best for**: Cross-platform file watching, custom build processes

#### Basic Usage
```javascript
// watch-build.js
import chokidar from 'chokidar';
import { exec } from 'child_process';

const watcher = chokidar.watch(['src/**/*', 'config/**/*'], {
  ignored: /(^|[\/\\])\../, // ignore dotfiles
  persistent: true,
  ignoreInitial: true,
  awaitWriteFinish: {
    stabilityThreshold: 300,
    pollInterval: 100
  }
});

let buildTimeout;
function debouncedBuild() {
  clearTimeout(buildTimeout);
  buildTimeout = setTimeout(() => {
    console.log('🔄 Files changed, rebuilding...');
    exec('npm run build', (error, stdout, stderr) => {
      if (error) {
        console.error(`❌ Build failed: ${error}`);
        return;
      }
      console.log('✅ Build completed successfully');
    });
  }, 500);
}

watcher
  .on('add', path => console.log(`📁 File ${path} has been added`))
  .on('change', path => {
    console.log(`📝 File ${path} has been changed`);
    debouncedBuild();
  })
  .on('unlink', path => console.log(`🗑️ File ${path} has been removed`))
  .on('error', error => console.error(`❌ Watcher error: ${error}`));

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('🛑 Stopping file watcher...');
  watcher.close();
  process.exit(0);
});
```

#### MCP Integration
```javascript
// mcp-file-watcher.js
import chokidar from 'chokidar';

export class MCPFileWatcher {
  constructor(mcpServer) {
    this.mcpServer = mcpServer;
    this.watchers = new Map();
  }

  watchDirectory(path, pattern = '**/*') {
    const key = `${path}:${pattern}`;

    if (this.watchers.has(key)) {
      return; // Already watching
    }

    const watcher = chokidar.watch(pattern, {
      cwd: path,
      ignored: /(^|[\/\\])\../,
      persistent: true,
      ignoreInitial: true
    });

    watcher.on('change', (filePath) => {
      // Notify MCP clients of file changes
      this.mcpServer.notifyClients('file_changed', {
        path: filePath,
        directory: path,
        timestamp: new Date().toISOString()
      });
    });

    this.watchers.set(key, watcher);
    return watcher;
  }

  unwatchDirectory(path, pattern = '**/*') {
    const key = `${path}:${pattern}`;
    const watcher = this.watchers.get(key);

    if (watcher) {
      watcher.close();
      this.watchers.delete(key);
    }
  }

  close() {
    for (const watcher of this.watchers.values()) {
      watcher.close();
    }
    this.watchers.clear();
  }
}
```

### Watchfiles (Python)

**Best for**: Python MCP servers, Django applications

#### Basic Setup
```python
# watchfiles_config.py
from watchfiles import watch
import subprocess
import signal
import os

WATCH_PATHS = [
    'src/',
    'config/',
    'requirements.txt',
    'pyproject.toml'
]

IGNORE_PATTERNS = [
    '*/__pycache__/*',
    '*/.pytest_cache/*',
    '*.pyc',
    '*.pyo',
    '.git/',
    'logs/',
    'node_modules/'
]

def should_restart(file_path):
    """Determine if file change should trigger restart"""
    for pattern in IGNORE_PATTERNS:
        if pattern in file_path:
            return False
    return True

def restart_server():
    """Restart the MCP server"""
    print("🔄 File changed, restarting MCP server...")

    # Send SIGTERM to gracefully shutdown
    try:
        with open('.pid', 'r') as f:
            pid = int(f.read().strip())
        os.kill(pid, signal.SIGTERM)

        # Wait a moment for graceful shutdown
        import time
        time.sleep(2)
    except (FileNotFoundError, ProcessLookupError, ValueError):
        pass  # No existing process

    # Start new server instance
    process = subprocess.Popen([
        'python', '-m', 'uvicorn',
        'src.main:app',
        '--host', '0.0.0.0',
        '--port', '8000',
        '--reload'
    ])

    # Save PID for next restart
    with open('.pid', 'w') as f:
        f.write(str(process.pid))

if __name__ == '__main__':
    print("👀 Starting file watcher for MCP server...")

    for changes in watch(*WATCH_PATHS):
        changed_files = [path for _, path in changes]
        if any(should_restart(str(path)) for path in changed_files):
            restart_server()
```

#### FastMCP Integration
```python
# src/mcp_server.py
from fastmcp import FastMCP
from watchfiles import watch
import asyncio
import threading

mcp = FastMCP(
    name="resilient-mcp-server",
    version="1.0.0"
)

@mcp.tool()
async def file_watch_status() -> dict:
    """Get file watching status"""
    return {
        "watching": True,
        "paths": ["src/", "config/"],
        "patterns": ["*.py", "*.json", "*.md"]
    }

def start_file_watcher():
    """Run file watcher in background thread"""
    def watch_files():
        for changes in watch('src/', 'config/'):
            # Handle file changes
            changed_files = [str(path) for _, path in changes]
            print(f"📝 Files changed: {changed_files}")

            # Notify MCP clients
            asyncio.run(notify_file_changes(changed_files))

    watcher_thread = threading.Thread(target=watch_files, daemon=True)
    watcher_thread.start()

async def notify_file_changes(files):
    """Notify MCP clients of file changes"""
    # Implementation depends on your MCP client notification system
    pass

# Start file watcher when server starts
start_file_watcher()

if __name__ == '__main__':
    mcp.run()
```

---

## 🔄 Process Management

### PM2 (Node.js)

**Best for**: Production Node.js deployments, cluster management

#### Ecosystem Configuration
```json
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'mcp-server',
    script: 'src/server.js',
    instances: 1,
    autorestart: true,
    watch: false, // Disable in production
    max_memory_restart: '1G',
    max_restarts: 10,
    min_uptime: '10s',
    env: {
      NODE_ENV: 'production',
      PORT: 8000
    },
    env_development: {
      NODE_ENV: 'development',
      PORT: 3000,
      DEBUG: 'mcp:*'
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true,
    merge_logs: true,
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
  }],

  deploy: {
    production: {
      user: 'node',
      host: 'your-server.com',
      ref: 'origin/main',
      repo: 'git@github.com:your-org/mcp-server.git',
      path: '/var/www/production',
      'pre-deploy-local': '',
      'post-deploy': 'npm install && pm2 reload ecosystem.config.js --env production',
      'pre-setup': ''
    }
  }
};
```

#### MCP Server Integration
```javascript
// src/server.js
import { FastMCP } from 'fastmcp';

const mcp = new FastMCP({
  name: 'pm2-managed-mcp-server',
  version: '1.0.0'
});

// PM2-specific health endpoint
mcp.tool('pm2_health', 'Get PM2-specific health metrics', {}, async () => {
  const metrics = {
    pm2_id: process.env.pm_id,
    pm2_instance: process.env.NODE_APP_INSTANCE,
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    cpu: process.cpuUsage(),
    restarts: process.env.restart_time || 0
  };

  return metrics;
});

// Graceful shutdown for PM2 restarts
process.on('SIGINT', async () => {
  console.log('🛑 PM2 shutdown signal received, cleaning up...');

  // Cleanup resources
  await cleanupConnections();
  await saveState();

  console.log('✅ Cleanup complete, shutting down gracefully');
  process.exit(0);
});

// Your MCP tools here...

mcp.start();
```

#### PM2 Commands
```bash
# Development
pm2 start ecosystem.config.js --env development
pm2 logs mcp-server --lines 100
pm2 restart mcp-server

# Production
pm2 start ecosystem.config.js --env production
pm2 save  # Save current state
pm2 startup  # Auto-start on boot

# Monitoring
pm2 monit  # Real-time monitoring
pm2 show mcp-server  # Detailed info
pm2 reloadLogs  # Reload log files

# Deployment
pm2 deploy production setup  # Initial setup
pm2 deploy production  # Deploy updates
```

### Systemd (Linux)

**Best for**: Linux production deployments, system integration

#### Service File
```ini
# /etc/systemd/system/mcp-server.service
[Unit]
Description=MCP Server
After=network.target
Wants=network.target

[Service]
Type=simple
User=mcp-user
Group=mcp-user
WorkingDirectory=/opt/mcp-server
ExecStart=/opt/mcp-server/venv/bin/python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=5
Environment=NODE_ENV=production
Environment=PYTHONPATH=/opt/mcp-server/src
StandardOutput=journal
StandardError=journal
SyslogIdentifier=mcp-server

# Security settings
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ReadWritePaths=/opt/mcp-server/logs /opt/mcp-server/data
ProtectHome=yes

# Resource limits
MemoryLimit=1G
CPUQuota=50%

[Install]
WantedBy=multi-user.target
```

#### Python MCP Integration
```python
# src/main.py
import asyncio
import signal
import logging
from fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

mcp = FastMCP(
    name="systemd-managed-mcp-server",
    version="1.0.0"
)

shutdown_event = asyncio.Event()

@mcp.tool()
async def systemd_health() -> dict:
    """Get systemd-specific health information"""
    import psutil
    import os

    return {
        "pid": os.getpid(),
        "ppid": os.getppid(),
        "systemd_service": os.environ.get('SYSTEMD_SERVICE', 'unknown'),
        "memory_percent": psutil.Process().memory_percent(),
        "cpu_percent": psutil.Process().cpu_percent(),
        "uptime": psutil.Process().create_time()
    }

def signal_handler(signum, frame):
    """Handle systemd signals"""
    if signum == signal.SIGHUP:
        logging.info("🔄 SIGHUP received, reloading configuration...")
        # Reload config logic here
    elif signum == signal.SIGTERM:
        logging.info("🛑 SIGTERM received, initiating graceful shutdown...")
        shutdown_event.set()

# Register signal handlers
signal.signal(signal.SIGHUP, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

async def main():
    # Your MCP tools here...

    # Wait for shutdown signal
    await shutdown_event.wait()

    logging.info("✅ Graceful shutdown complete")

if __name__ == '__main__':
    asyncio.run(main())
```

#### Service Management
```bash
# Install and start service
sudo systemctl daemon-reload
sudo systemctl enable mcp-server
sudo systemctl start mcp-server

# Check status
sudo systemctl status mcp-server
sudo journalctl -u mcp-server -f

# Restart and reload
sudo systemctl restart mcp-server
sudo systemctl reload mcp-server

# View logs
sudo journalctl -u mcp-server --since today
sudo journalctl -u mcp-server -n 50
```

### Forever (Node.js Alternative)

**Best for**: Simple Node.js process management

#### Configuration
```json
// forever-config.json
{
  "uid": "mcp-server",
  "append": true,
  "watch": false,
  "script": "src/server.js",
  "sourceDir": "/opt/mcp-server",
  "logFile": "/var/log/mcp-server.log",
  "errLogFile": "/var/log/mcp-server-error.log",
  "outFile": "/var/log/mcp-server-out.log",
  "pidFile": "/var/run/mcp-server.pid",
  "minUptime": "10000",
  "spinSleepTime": "5000",
  "max": 10,
  "env": {
    "NODE_ENV": "production",
    "PORT": "8000"
  }
}
```

#### Usage
```bash
# Start server
forever start forever-config.json

# List running processes
forever list

# Stop server
forever stop mcp-server

# Restart server
forever restart mcp-server

# View logs
forever logs mcp-server
forever logs mcp-server -f  # Follow logs
```

---

## 🏥 Health Checks & Monitoring

### HTTP Health Endpoints

**Best for**: Container orchestration, load balancers

#### FastMCP Health Endpoint
```python
# src/health.py
from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import psutil
import asyncio
from typing import Dict, Any

router = APIRouter()

class HealthChecker:
    def __init__(self):
        self.start_time = datetime.now()
        self.last_check = datetime.now()
        self.check_interval = timedelta(seconds=30)
        self.dependencies = {}

    async def check_database(self) -> bool:
        """Check database connectivity"""
        try:
            # Your database check logic here
            await self.db_connection.ping()
            return True
        except Exception:
            return False

    async def check_external_apis(self) -> bool:
        """Check external API connectivity"""
        try:
            # Your API check logic here
            response = await self.http_client.get('https://api.example.com/health')
            return response.status_code == 200
        except Exception:
            return False

    async def check_file_system(self) -> bool:
        """Check file system access"""
        try:
            # Check write access to log directory
            with open('/tmp/health_check', 'w') as f:
                f.write('health_check')
            os.remove('/tmp/health_check')
            return True
        except Exception:
            return False

    async def perform_health_checks(self) -> Dict[str, Any]:
        """Perform all health checks"""
        now = datetime.now()

        # Throttle checks to avoid overwhelming dependencies
        if now - self.last_check < self.check_interval:
            return self.dependencies

        results = await asyncio.gather(
            self.check_database(),
            self.check_external_apis(),
            self.check_file_system(),
            return_exceptions=True
        )

        self.dependencies = {
            'database': results[0] if not isinstance(results[0], Exception) else False,
            'external_apis': results[1] if not isinstance(results[1], Exception) else False,
            'file_system': results[2] if not isinstance(results[2], Exception) else False,
        }

        self.last_check = now
        return self.dependencies

health_checker = HealthChecker()

@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    checks = await health_checker.perform_health_checks()

    # Determine overall health
    all_healthy = all(checks.values())

    status_code = 200 if all_healthy else 503
    status = "healthy" if all_healthy else "unhealthy"

    return {
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "uptime": (datetime.now() - health_checker.start_time).total_seconds(),
        "checks": checks,
        "version": "1.0.0"
    }

@router.get("/health/live")
async def liveness_probe():
    """Kubernetes liveness probe"""
    return {"status": "alive", "timestamp": datetime.now().isoformat()}

@router.get("/health/ready")
async def readiness_probe():
    """Kubernetes readiness probe"""
    checks = await health_checker.perform_health_checks()

    if not all(checks.values()):
        raise HTTPException(status_code=503, detail="Service not ready")

    return {"status": "ready", "timestamp": datetime.now().isoformat()}

@router.get("/health/detailed")
async def detailed_health():
    """Detailed health information for debugging"""
    process = psutil.Process()

    return {
        "status": "healthy",
        "process": {
            "pid": process.pid,
            "cpu_percent": process.cpu_percent(),
            "memory_percent": process.memory_percent(),
            "memory_info": dict(process.memory_info()._asdict()),
            "num_threads": process.num_threads(),
            "create_time": process.create_time()
        },
        "system": {
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent(),
            "memory": dict(psutil.virtual_memory()._asdict()),
            "disk": dict(psutil.disk_usage('/')._asdict())
        },
        "checks": await health_checker.perform_health_checks(),
        "timestamp": datetime.now().isoformat()
    }
```

#### Integration with FastMCP
```python
# src/server.py
from fastmcp import FastMCP
from .health import router as health_router

mcp = FastMCP(
    name="healthy-mcp-server",
    version="1.0.0"
)

# Mount health endpoints
mcp.app.include_router(health_router)

@mcp.tool()
async def server_health() -> dict:
    """Get MCP server health status"""
    from .health import health_checker

    checks = await health_checker.perform_health_checks()

    return {
        "mcp_tools_count": len(mcp._tools),
        "mcp_resources_count": len(mcp._resources),
        "health_checks": checks,
        "server_status": "operational"
    }

# Your MCP tools here...

if __name__ == '__main__':
    mcp.run()
```

### Docker Health Checks

**Best for**: Containerized deployments

#### Dockerfile with Health Checks
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Health check configuration
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/live || exit 1

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Docker Compose Health Checks
```yaml
version: '3.8'

services:
  mcp-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - NODE_ENV=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/ready"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped
    depends_on:
      database:
        condition: service_healthy

  database:
    image: postgres:15
    environment:
      POSTGRES_DB: mcp
      POSTGRES_USER: mcp
      POSTGRES_PASSWORD: password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mcp"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Kubernetes Health Probes

**Best for**: Kubernetes deployments

#### Deployment with Health Probes
```yaml
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
        image: your-registry/mcp-server:latest
        ports:
        - containerPort: 8000
        env:
        - name: NODE_ENV
          value: "production"
        # Liveness probe - restart if unhealthy
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        # Readiness probe - don't route traffic until ready
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        # Startup probe - give time for slow starts
        startupProbe:
          httpGet:
            path: /health/live
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 30
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

---

## 🔄 Crash Recovery & Auto-Restart

### Circuit Breaker Pattern

**Best for**: External service dependencies, API resilience

#### Python Implementation
```python
# src/circuit_breaker.py
import asyncio
import time
from enum import Enum
from typing import Callable, Any, Optional
import logging

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Circuit is open, failing fast
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: Exception = Exception
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def can_execute(self) -> bool:
        """Check if circuit allows execution"""
        if self.state == CircuitState.CLOSED:
            return True
        elif self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        else:  # HALF_OPEN
            return True

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt recovery"""
        if self.last_failure_time is None:
            return True
        return time.time() - self.last_failure_time >= self.recovery_timeout

    async def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        if not self.can_execute():
            raise CircuitBreakerOpenException("Circuit breaker is OPEN")

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        """Handle successful execution"""
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            logger.info("Circuit breaker reset to CLOSED state")

    def _on_failure(self):
        """Handle failed execution"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit breaker opened after {self.failure_count} failures")

class CircuitBreakerOpenException(Exception):
    pass
```

#### MCP Integration
```python
# src/mcp_server.py
from fastmcp import FastMCP
from .circuit_breaker import CircuitBreaker, CircuitBreakerOpenException

mcp = FastMCP(
    name="resilient-mcp-server",
    version="1.0.0"
)

# Circuit breaker for external API calls
api_circuit_breaker = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=30
)

@mcp.tool()
async def call_external_api(endpoint: str, data: dict) -> dict:
    """Call external API with circuit breaker protection"""

    async def api_call():
        # Your API call logic here
        response = await make_api_request(endpoint, data)
        return response

    try:
        result = await api_circuit_breaker.execute(api_call)
        return {
            "success": True,
            "data": result,
            "circuit_state": api_circuit_breaker.state.value
        }
    except CircuitBreakerOpenException:
        return {
            "success": False,
            "error": "Service temporarily unavailable",
            "circuit_state": "open",
            "retry_after": api_circuit_breaker.recovery_timeout
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "circuit_state": api_circuit_breaker.state.value
        }

@mcp.tool()
async def circuit_breaker_status() -> dict:
    """Get circuit breaker status"""
    return {
        "api_circuit": {
            "state": api_circuit_breaker.state.value,
            "failure_count": api_circuit_breaker.failure_count,
            "last_failure": api_circuit_breaker.last_failure_time
        }
    }

if __name__ == '__main__':
    mcp.run()
```

### Graceful Shutdown

**Best for**: Clean resource cleanup, state persistence

#### Python Graceful Shutdown
```python
# src/graceful_shutdown.py
import asyncio
import signal
import logging
from typing import List, Callable, Awaitable
import atexit

logger = logging.getLogger(__name__)

class GracefulShutdown:
    def __init__(self):
        self.shutdown_handlers: List[Callable[[], Awaitable[None]]] = []
        self.shutdown_event = asyncio.Event()
        self.shutdown_timeout = 30.0  # seconds

    def add_shutdown_handler(self, handler: Callable[[], Awaitable[None]]):
        """Add a shutdown handler function"""
        self.shutdown_handlers.append(handler)

    async def shutdown(self):
        """Initiate graceful shutdown"""
        logger.info("🛑 Initiating graceful shutdown...")

        # Signal shutdown to all components
        self.shutdown_event.set()

        # Execute all shutdown handlers with timeout
        shutdown_tasks = []
        for handler in self.shutdown_handlers:
            task = asyncio.create_task(handler())
            shutdown_tasks.append(task)

        try:
            # Wait for all handlers to complete or timeout
            await asyncio.wait_for(
                asyncio.gather(*shutdown_tasks, return_exceptions=True),
                timeout=self.shutdown_timeout
            )
            logger.info("✅ All shutdown handlers completed successfully")
        except asyncio.TimeoutError:
            logger.warning(f"⚠️ Shutdown timed out after {self.shutdown_timeout}s")
            # Cancel remaining tasks
            for task in shutdown_tasks:
                if not task.done():
                    task.cancel()

        logger.info("🛑 Graceful shutdown complete")

    def handle_signal(self, signum, frame):
        """Handle shutdown signals"""
        signal_names = {
            signal.SIGTERM: "SIGTERM",
            signal.SIGINT: "SIGINT",
            signal.SIGHUP: "SIGHUP"
        }

        signal_name = signal_names.get(signum, f"signal {signum}")
        logger.info(f"📡 Received {signal_name}, initiating graceful shutdown...")

        # Schedule shutdown in event loop
        asyncio.create_task(self.shutdown())

    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        signals = [signal.SIGTERM, signal.SIGINT, signal.SIGHUP]

        for sig in signals:
            try:
                signal.signal(sig, self.handle_signal)
            except ValueError:
                # Signal not supported on this platform
                pass

        # Handle KeyboardInterrupt on Windows
        if hasattr(signal, 'SIGBREAK'):
            signal.signal(signal.SIGBREAK, self.handle_signal)

# Global shutdown manager
shutdown_manager = GracefulShutdown()

def get_shutdown_manager():
    """Get the global shutdown manager"""
    return shutdown_manager
```

#### Integration with FastMCP
```python
# src/server.py
from fastmcp import FastMCP
from .graceful_shutdown import get_shutdown_manager
import asyncio

mcp = FastMCP(
    name="graceful-mcp-server",
    version="1.0.0"
)

shutdown_manager = get_shutdown_manager()

# Add shutdown handlers
@shutdown_manager.add_shutdown_handler
async def close_database_connections():
    """Close database connections"""
    logger.info("Closing database connections...")
    # Your database cleanup logic here
    await asyncio.sleep(0.1)  # Simulate cleanup time

@shutdown_manager.add_shutdown_handler
async def save_application_state():
    """Save application state"""
    logger.info("Saving application state...")
    # Your state saving logic here
    await asyncio.sleep(0.1)

@shutdown_manager.add_shutdown_handler
async def close_external_connections():
    """Close external API connections"""
    logger.info("Closing external connections...")
    # Your connection cleanup logic here
    await asyncio.sleep(0.1)

@mcp.tool()
async def shutdown_status() -> dict:
    """Get shutdown handler status"""
    return {
        "shutdown_handlers_count": len(shutdown_manager.shutdown_handlers),
        "shutdown_timeout": shutdown_manager.shutdown_timeout,
        "shutdown_pending": shutdown_manager.shutdown_event.is_set()
    }

async def main():
    # Setup signal handlers
    shutdown_manager.setup_signal_handlers()

    # Your MCP tools here...

    # Wait for shutdown signal
    await shutdown_manager.shutdown_event.wait()

if __name__ == '__main__':
    asyncio.run(main())
```

### Auto-Restart with Exponential Backoff

**Best for**: Unstable services, temporary failures

#### Python Auto-Restart
```python
# src/auto_restart.py
import asyncio
import logging
import time
from typing import Callable, Awaitable, Optional
import random

logger = logging.getLogger(__name__)

class AutoRestart:
    def __init__(
        self,
        max_attempts: int = 5,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0,
        jitter: bool = True
    ):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.jitter = jitter

        self.attempts = 0
        self.last_attempt_time = None

    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay with exponential backoff and jitter"""
        delay = min(self.base_delay * (self.backoff_factor ** attempt), self.max_delay)

        if self.jitter:
            # Add random jitter (±25%)
            jitter_range = delay * 0.25
            delay += random.uniform(-jitter_range, jitter_range)

        return max(0, delay)

    async def execute_with_retry(
        self,
        func: Callable[[], Awaitable[bool]],
        context: str = "operation"
    ) -> bool:
        """Execute function with auto-restart on failure"""

        for attempt in range(self.max_attempts):
            try:
                self.attempts = attempt + 1
                self.last_attempt_time = time.time()

                logger.info(f"🔄 Attempting {context} (attempt {self.attempts}/{self.max_attempts})")

                success = await func()

                if success:
                    logger.info(f"✅ {context} succeeded on attempt {self.attempts}")
                    return True
                else:
                    logger.warning(f"⚠️ {context} returned false on attempt {self.attempts}")

            except Exception as e:
                logger.error(f"❌ {context} failed on attempt {self.attempts}: {e}")

            if attempt < self.max_attempts - 1:
                delay = self.calculate_delay(attempt)
                logger.info(f"⏳ Waiting {delay:.1f}s before retry...")
                await asyncio.sleep(delay)

        logger.error(f"💥 {context} failed after {self.max_attempts} attempts")
        return False

    def get_status(self) -> dict:
        """Get restart status"""
        return {
            "attempts": self.attempts,
            "max_attempts": self.max_attempts,
            "last_attempt_time": self.last_attempt_time,
            "can_retry": self.attempts < self.max_attempts
        }
```

#### MCP Integration
```python
# src/server.py
from fastmcp import FastMCP
from .auto_restart import AutoRestart
import asyncio

mcp = FastMCP(
    name="auto-restart-mcp-server",
    version="1.0.0"
)

# Auto-restart for critical services
db_restart = AutoRestart(max_attempts=10, base_delay=2.0, max_delay=300.0)
api_restart = AutoRestart(max_attempts=5, base_delay=1.0, max_delay=30.0)

@mcp.tool()
async def restart_database() -> dict:
    """Restart database connection with auto-retry"""

    async def connect_to_database() -> bool:
        try:
            # Your database connection logic here
            await establish_db_connection()
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False

    success = await db_restart.execute_with_retry(
        connect_to_database,
        "database connection"
    )

    return {
        "success": success,
        "attempts": db_restart.attempts,
        "status": db_restart.get_status()
    }

@mcp.tool()
async def restart_external_api() -> dict:
    """Restart external API connection with auto-retry"""

    async def connect_to_api() -> bool:
        try:
            # Your API connection logic here
            await test_api_connection()
            return True
        except Exception as e:
            logger.error(f"API connection failed: {e}")
            return False

    success = await api_restart.execute_with_retry(
        connect_to_api,
        "external API connection"
    )

    return {
        "success": success,
        "attempts": api_restart.attempts,
        "status": api_restart.get_status()
    }

@mcp.tool()
async def restart_status() -> dict:
    """Get restart status for all services"""
    return {
        "database": db_restart.get_status(),
        "external_api": api_restart.get_status()
    }

if __name__ == '__main__':
    mcp.run()
```

---

## 📊 Integration with Monitoring

### Prometheus Metrics for Resilience

**Best for**: Production monitoring and alerting

#### Resilience Metrics
```python
# src/metrics.py
from prometheus_client import Counter, Gauge, Histogram, CollectorRegistry
import time

# Create registry for resilience metrics
registry = CollectorRegistry()

# Circuit breaker metrics
circuit_breaker_state = Gauge(
    'circuit_breaker_state',
    'Current state of circuit breaker (0=closed, 1=open, 2=half_open)',
    ['service'],
    registry=registry
)

circuit_breaker_failures = Counter(
    'circuit_breaker_failures_total',
    'Total number of circuit breaker failures',
    ['service'],
    registry=registry
)

# Health check metrics
health_check_duration = Histogram(
    'health_check_duration_seconds',
    'Time spent performing health checks',
    ['check_type'],
    registry=registry
)

health_check_failures = Counter(
    'health_check_failures_total',
    'Total number of failed health checks',
    ['check_type'],
    registry=registry
)

# Auto-restart metrics
restart_attempts = Counter(
    'service_restart_attempts_total',
    'Total number of service restart attempts',
    ['service', 'result'],
    registry=registry
)

restart_duration = Histogram(
    'service_restart_duration_seconds',
    'Time spent restarting services',
    ['service'],
    registry=registry
)

# File watching metrics
files_changed = Counter(
    'files_changed_total',
    'Total number of files changed',
    ['directory'],
    registry=registry
)

watch_events = Counter(
    'file_watch_events_total',
    'Total number of file watch events',
    ['event_type'],
    registry=registry
)

def update_circuit_breaker_metrics(service: str, state: str, failures: int):
    """Update circuit breaker metrics"""
    state_value = {'closed': 0, 'open': 1, 'half_open': 2}.get(state, 0)
    circuit_breaker_state.labels(service=service).set(state_value)
    circuit_breaker_failures.labels(service=service).set(failures)

def record_health_check(check_type: str, duration: float, success: bool):
    """Record health check metrics"""
    health_check_duration.labels(check_type=check_type).observe(duration)
    if not success:
        health_check_failures.labels(check_type=check_type).inc()

def record_restart_attempt(service: str, success: bool, duration: float):
    """Record restart attempt metrics"""
    result = 'success' if success else 'failure'
    restart_attempts.labels(service=service, result=result).inc()
    restart_duration.labels(service=service).observe(duration)

def record_file_change(directory: str, event_type: str):
    """Record file change metrics"""
    files_changed.labels(directory=directory).inc()
    watch_events.labels(event_type=event_type).inc()
```

#### Integration with FastMCP
```python
# src/server.py
from fastmcp import FastMCP
from .metrics import (
    update_circuit_breaker_metrics,
    record_health_check,
    record_restart_attempt,
    record_file_change
)
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

mcp = FastMCP(
    name="monitored-mcp-server",
    version="1.0.0"
)

@mcp.tool()
async def get_resilience_metrics() -> str:
    """Get resilience metrics in Prometheus format"""
    return generate_latest(registry).decode('utf-8')

@mcp.tool()
async def resilience_status() -> dict:
    """Get current resilience status"""
    return {
        "circuit_breakers": {
            "database": {
                "state": "closed",
                "failures": 0
            },
            "external_api": {
                "state": "closed",
                "failures": 2
            }
        },
        "health_checks": {
            "last_check": "2024-01-15T10:30:00Z",
            "all_healthy": True
        },
        "auto_restarts": {
            "database": {
                "attempts": 1,
                "last_success": "2024-01-15T10:25:00Z"
            }
        }
    }

# Update metrics when operations occur
# (Call these functions from your circuit breaker, health check, etc. implementations)

if __name__ == '__main__':
    mcp.run()
```

---

## 🚀 Best Practices

### Development Resilience
1. **Use file watchers** for hot reload during development
2. **Enable debug modes** with detailed error reporting
3. **Implement auto-restart** for development servers
4. **Use development-specific health checks** for faster feedback

### Production Resilience
1. **Implement circuit breakers** for external dependencies
2. **Use process managers** (PM2, systemd) for auto-restart
3. **Configure health checks** for container orchestration
4. **Implement graceful shutdown** procedures
5. **Set up monitoring and alerting** for resilience metrics

### Monitoring Integration
1. **Export metrics** in Prometheus format
2. **Set up dashboards** for resilience monitoring
3. **Configure alerts** for circuit breaker trips
4. **Monitor restart patterns** and failure rates

### Testing Resilience
1. **Test circuit breaker behavior** under failure conditions
2. **Verify graceful shutdown** procedures
3. **Test auto-restart logic** with various failure scenarios
4. **Validate health check endpoints** under load

This comprehensive resilience framework ensures your MCP applications can withstand failures, recover automatically, and provide reliable service in both development and production environments.
