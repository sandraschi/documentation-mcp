# Uvicorn Integration Guide

**Timestamp**: 2026-01-23
**Status**: Backend Standard

## Overview

Uvicorn is an ASGI (Asynchronous Server Gateway Interface) web server implementation for Python. It is the lightning-fast engine that powers FastAPI applications.

## Role in MyHomeServer

Uvicorn is responsible for:
1.  Running the FastAPI backend on port `10500`.
2.  Handling concurrent requests from the React frontend.
3.  Managing the lifespan of the application (startup/shutdown of MCP clients).

## Execution Patterns

### 1. Development (with Hot Reload)
```powershell
uvicorn main:app --reload --port 10500
```

### 2. Programmatic Start (Professional)
Used in `backend/main.py`:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=10500, 
        log_level="info"
    )
```

## Key Configuration

*   **--reload**: Automatically restarts the server when code changes. (Dev only)
*   **--workers**: Increases the number of worker processes for high-traffic production environments.
*   **--loop**: Use `uvloop` for maximum performance on Linux systems.

## Troubleshooting

*   **Port in Use**: If you see `[Errno 10048]`, another instance of MyHomeServer is running. Use `.\start-clean.ps1` to kill zombie processes.
*   **Keep-Alive**: Uvicorn maintains connections to the browser; if the backend seems "stuck", check for long-running async tasks that aren't properly `awaited`.
