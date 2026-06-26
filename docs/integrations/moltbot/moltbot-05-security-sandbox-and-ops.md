# Moltbot — Security, Sandbox, and Operations

**Last updated:** 2025-01-28  
**See also:** [moltbot-00-overview](moltbot-00-overview.md) | [Security](https://docs.molt.bot/gateway/security) | [Sandboxing](https://docs.molt.bot/gateway/sandboxing) | [Doctor](https://docs.molt.bot/gateway/doctor)

---

## 1. Threat Model and Default Behavior

Moltbot connects to **real messaging surfaces** and, by default, has **full system access** for the main session (shell, files, browser). The docs explicitly state: *"Running an AI agent with shell access on your machine is… spicy."* There is **no "perfectly secure" setup.** Threats include:

- **Prompt injection / social engineering** — Tricking the AI into doing unintended actions.
- **Untrusted inbound** — Group chats, open DMs, or exposed channels.
- **Exposed control plane** — Gateway UI or WebSocket reachable from the internet without auth.

---

## 2. Defaults (Main vs Non-Main)

- **Main session:** Tools run on the host; full access. Appropriate for single-user, trusted use.
- **Non-main sessions** (groups, certain channels): Use **sandbox mode** so execution runs in per-session Docker containers. Bash (and allowlisted tools) run inside the sandbox; browser, canvas, nodes, cron, etc. can be denylisted.

**Config:**

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main"
      }
    }
  }
}
```

Sandbox allowlist (typical): `bash`, `process`, `read`, `write`, `edit`, `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`. Denylist: `browser`, `canvas`, `nodes`, `cron`, `discord`, `gateway`. Adjust via sandbox config.

---

## 3. DM Policy and Pairing

- **Default:** `dmPolicy: "pairing"`. Unknown senders get a pairing code; the bot does not process their message until you run `moltbot pairing approve <code>`.
- **Open DMs:** `dmPolicy: "open"` and `"*"` in allowlist. Use only when you explicitly accept public DMs.

Run **`moltbot doctor`** to surface risky or misconfigured DM policies.

---

## 4. Gateway Auth and Exposure

- **Token:** Set `CLAWDBOT_GATEWAY_TOKEN` (or `--token`). `connect.params.auth.token` must match or the socket is closed.
- **Bind:** Keep Gateway on **loopback** when possible. Never expose the Gateway UI or WebSocket directly to the internet without auth.

**Bitdefender (Jan 2026):** Hundreds of internet-facing Moltbot/ClawdBot control panels were exposed (localhost trust assumptions + reverse proxy misconfig). Result: config leaks, API keys, conversation history, and in some cases unauthenticated execution. **Takeaway:** Always use Tailscale (Serve/Funnel) with password auth, or SSH tunnels, and never rely on "localhost only" when a reverse proxy or tunnel exposes the service.

---

## 5. Tailscale and Remote Access

- **Tailscale Serve:** Tailnet-only HTTPS. Gateway stays loopback.
- **Tailscale Funnel:** Public HTTPS. **Requires** `gateway.auth.mode: "password"`.
- **SSH tunnel:** e.g. `ssh -N -L 18789:127.0.0.1:18789 user@host`. Same handshake and token apply.

When using Serve/Funnel, `gateway.bind` must remain loopback. Optional `gateway.tailscale.resetOnExit` to undo on shutdown.

---

## 6. Sandbox vs Tool Policy vs Elevated

- **Sandbox:** Isolates **where** code runs (Docker per session).
- **Tool policy:** **Which** tools are available (allow/deny lists).
- **Elevated:** Per-session **privilege** toggle (`/elevated on|off`) when enabled and allowlisted.

See [Sandbox vs Tool Policy vs Elevated](https://docs.molt.bot/gateway/sandbox-vs-tool-policy-vs-elevated), [Sandboxing](https://docs.molt.bot/gateway/sandboxing).

---

## 7. Skills and Secrets

- **skills.entries.*.env** and **apiKey** inject into the **host** process for that agent run, not the sandbox. Don’t put secrets in prompts or logs.
- Treat third-party skills as **trusted code**; review before enabling.

---

## 8. Operations

### 8.1 Doctor

- **`moltbot doctor`** — Migrations, config checks, risky DM policy, and other diagnostics. Run after upgrades and when changing security-related config.

### 8.2 Health and Heartbeat

- **Health:** Exposed over WS (`health` request, also in `hello-ok`). Use for monitoring.
- **Heartbeat:** Periodic heartbeat events; optional cron vs heartbeat distinction. See [Health](https://docs.molt.bot/gateway/health), [Heartbeat](https://docs.molt.bot/gateway/heartbeat).

### 8.3 Logging

- Gateway logs to stdout (or configured sink). [Logging](https://docs.molt.bot/gateway/logging).
- macOS: `./scripts/clawlog.sh` for unified logs (Moltbot subsystem).

### 8.4 Background Process and Lock

- **Background process:** launchd/systemd for gateway. [Background process](https://docs.molt.bot/gateway/background-process).
- **Gateway lock:** Prevents multiple Gateway instances. [Gateway lock](https://docs.molt.bot/gateway/gateway-lock).

---

## 9. Hardening Checklist

- [ ] Use **sandbox mode** for non-main sessions (groups, untrusted channels).
- [ ] Keep **DM policy** strict (pairing); run `moltbot doctor` regularly.
- [ ] **Never** expose Gateway UI/WS to the public internet without auth (Tailscale + password, or SSH tunnel).
- [ ] Set **CLAWDBOT_GATEWAY_TOKEN** (or `--token`) when using remote access.
- [ ] Restrict **allowlists** per channel (`allowFrom`, groups).
- [ ] Review **skills** and **extensions** before enabling; avoid injecting secrets into prompts.
- [ ] Use **Tailscale Serve** (tailnet-only) or **Funnel** with **password** when exposing UI.

---

## 10. Formal Verification and Security Docs

- [Formal verification (security models)](https://docs.molt.bot/security/formal-verification) — For deeper security analysis.
- [Security](https://docs.molt.bot/gateway/security) — Full security guide.
- [Troubleshooting](https://docs.molt.bot/gateway/troubleshooting) — Gateway-level debugging.

---

## References

- [Security](https://docs.molt.bot/gateway/security)
- [Sandboxing](https://docs.molt.bot/gateway/sandboxing)
- [Sandbox vs Tool Policy vs Elevated](https://docs.molt.bot/gateway/sandbox-vs-tool-policy-vs-elevated)
- [Doctor](https://docs.molt.bot/gateway/doctor)
- [Tailscale](https://docs.molt.bot/gateway/tailscale)
- [Remote](https://docs.molt.bot/gateway/remote)
- [Authentication](https://docs.molt.bot/gateway/authentication)
