# OpenClaw Security Vulnerability Scan (February 2026)

**Timestamp**: 2026-02-06
**Method**: Opus 4.6-assisted security analysis
**Source**: Full audit of `D:\Dev\repos\openclaw`

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH | 3 |
| MEDIUM | 6 |
| LOW | 2 |
| INFO | 1 |

---

## HIGH Severity

### 1. `--dangerously-skip-permissions` Hardcoded in CLI Backend Defaults
- **File**: `src/agents/cli-backends.ts`
- **Issue**: Default Claude CLI backend passes `--dangerously-skip-permissions` unconditionally
- **Impact**: Every agent session runs without permission checks by default
- **Mitigation**: Make opt-in via config; remove from defaults

### 2. `dangerouslyDisableDeviceAuth` Config Flag Bypasses Device Identity
- **Files**: `src/gateway/server/ws-connection/message-handler.ts`, `src/config/zod-schema.ts`
- **Issue**: Config flags disable device pairing; no expiry or audit when enabled
- **Impact**: Attacker on local network can authenticate with token only
- **Mitigation**: Require env override; add startup warning; consider time-limited enforcement

### 3. No Rate Limiting on Authentication
- **Files**: `src/gateway/auth.ts`, message-handler
- **Issue**: Unlimited auth attempts over WebSocket
- **Impact**: Brute-force vector when gateway bound to LAN
- **Mitigation**: Per-IP rate limiting with block after N failed attempts

---

## MEDIUM Severity

### 4. Static Tokens with No Expiry or Rotation
- **File**: `src/gateway/auth.ts`
- **Mitigation**: JWT-style expiry, revocation mechanism

### 5. Chrome Extension Connects Over Plaintext WebSocket Without Auth
- **File**: `assets/chrome-extension/background.js`
- **Mitigation**: Shared secret handshake; consider wss://

### 6. `--allow-unconfigured` in Docker Compose Defaults
- **File**: `docker-compose.yml`
- **Mitigation**: Remove from default or document prominently

### 7. Path Traversal in Config Include Resolution
- **File**: `src/security/fix.ts`
- **Mitigation**: Validate resolved path within config directory

### 8. WebSocket JSON.parse Without Size Limits
- **File**: `src/gateway/server/ws-connection/message-handler.ts`
- **Mitigation**: Set maxPayload; validate size before parse

### 9. Tailscale User Header Trust
- **File**: `src/gateway/auth.ts`
- **Mitigation**: Review whois flow; document assumptions

---

## LOW Severity

### 10. Environment Variable Blocklist Gaps
- **File**: `src/agents/bash-tools.exec.ts`
- **Mitigation**: Add PERL5OPT, RUBY_OPT, JAVA_TOOL_OPTIONS; consider whitelist

### 11. No CSRF Protection on HTTP Endpoints
- **Mitigation**: SameSite cookies, double-submit cookie, or custom header

---

## Positive Findings

- Timing-safe comparison for auth
- SSRF protection in web-fetch
- DOMPurify for markdown
- Exec approval system with allowlists
- Security audit tool (`openclaw security audit`)
- No hardcoded secrets

---

## References

- **Full Report**: [OpenClaw repo docs/security/vulnerability-scan-2026-02.md](https://github.com/openclaw/openclaw/blob/main/docs/security/vulnerability-scan-2026-02.md)
- **Mitigation Plan**: [OpenClaw repo docs/security/mitigation-plan-2026-02.md](https://github.com/openclaw/openclaw/blob/main/docs/security/mitigation-plan-2026-02.md)
- **Gateway Security**: [docs.openclaw.ai/gateway/security](https://docs.openclaw.ai/gateway/security)
