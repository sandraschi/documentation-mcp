# Fleet API endpoint hardening sweep

**Priority:** P1  
**Scope:** All fleet `*-mcp` HTTP backends

## Problem

Unprotected API calls: POST handlers propagate service exceptions, missing try/except, unvalidated bodies, async endpoints that crash on connection drops.

## Per-repo checklist

- Every `@router.post` / `@router.get` wraps body in `try/except Exception`
- Service calls never propagate raw exceptions to handler
- Request models use Pydantic `BaseModel` with `Field(description=...)`
- Async handlers catch `asyncio.CancelledError` and connection drops
- `BackgroundTasks` have own try/except
- User file ops bounded (max size, depth, timeout)
- No bare `request.json()` without schema or size limit

**Trigger:** Webapp polling without backoff, malformed tool params, deserialization panics.
