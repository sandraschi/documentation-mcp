# Watchfiles Crashproofing Pattern

**Implement automatic crash recovery and stability for native Python applications**

Perfect for:
- Native Python applications (non-Docker)
- Systems requiring high availability
- Hardware-integrated servers (e.g., USB cameras on Windows)
- Long-running background processes
- Stopgap stability before full containerization

## 🎯 Overview

This pattern uses the `watchfiles` library to create a supervisor process that monitors your application. If the application crashes or the health check fails, the supervisor automatically restarts it with an exponential backoff strategy.

## 📦 Implementation Components

### 1. The Runner (`watchfiles_runner.py`)
A standalone Python script that manages the application lifecycle.

**Key Features:**
- ✅ **Automatic Crash Detection**: Monitors process exit codes.
- ✅ **Exponential Backoff**: Prevents "restart loops" by increasing delay (1s, 1.5s, 2.25s...).
- ✅ **HTTP Health Checks**: Periodically pings an internal endpoint (e.g., `/api/health`).
- ✅ **Structured Logging**: Saves crash reports and stderr to JSON for debugging.
- ✅ **Signal Handling**: Gracefully shuts down the child process on Ctrl+C.

### 2. Application Integration
Your application should expose a simple health endpoint:

```python
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

## 🚀 Usage Guide

### Installation
```powershell
pip install watchfiles aiohttp
```

### Running your App
Instead of running your app directly (e.g., `uvicorn main:app`), run the supervisor:
```powershell
python watchfiles_runner.py
```

## 🛠️ Configuration (Env Vars)

| Variable | Default | Purpose |
|----------|---------|---------|
| `WATCHFILES_MAX_RESTARTS` | `10` | Max attempts before giving up |
| `WATCHFILES_RESTART_DELAY` | `1.0` | Initial delay in seconds |
| `WATCHFILES_BACKOFF_MULTIPLIER` | `1.5` | Backoff multiplier |
| `WATCHFILES_HEALTH_CHECK_INTERVAL` | `30` | Seconds between health pings |

## 📊 Benefits

### Before Pattern:
- ❌ Manual restart required on every crash.
- ❌ Zero visibility into why the process died.
- ❌ Service downtime during off-hours.

### After Pattern:
- ✅ **Zero-touch recovery**: App heals itself in seconds.
- ✅ **Crash Analytics**: JSON reports reveal patterns and error logs.
- ✅ **Production Stability**: Native apps achieve 99.9% uptime.

---

**Reference Implementation**: `mcp-studio/scripts/watchfiles_runner.py`
**Last Updated**: 2026-01-02
