# Moltbot — Architecture and Gateway Protocol

**Last updated:** 2025-01-28  
**See also:** [moltbot-00-overview](moltbot-00-overview.md) | [Gateway protocol](https://docs.molt.bot/gateway/protocol) | [Architecture](https://docs.molt.bot/concepts/architecture)

---

## 1. High-Level Architecture

- **Single Gateway daemon per host.** It owns all provider connections (WhatsApp via Baileys, Telegram, Slack, Discord, etc.) and exposes a typed WebSocket API.
- **Control-plane clients** (macOS app, CLI, web UI, automations) connect over **WebSocket** to the configured bind (default `127.0.0.1:18789`).
- **Nodes** (macOS/iOS/Android/headless) also connect over WebSocket but declare `role: node` and expose capability claims (e.g. camera, canvas, `system.run`).
- **One Gateway per host**; it is the only process that holds a WhatsApp/Baileys session.
- **Canvas host** (default port `18793`) serves agent-editable HTML and A2UI for visual workspaces.

The Gateway validates inbound JSON frames against TypeBox-derived schemas, emits events (`agent`, `chat`, `presence`, `health`, `heartbeat`, `cron`), and routes requests to the Pi agent, channels, and nodes.

---

## 2. Components and Flows

### 2.1 Gateway (daemon)

- Maintains provider connections (WhatsApp, Telegram, etc.).
- Exposes the typed WS API: requests, responses, server-push events.
- Validates frames against JSON Schema (generated from TypeBox).
- Emits events such as `agent`, `chat`, `presence`, `health`, `heartbeat`, `cron`.

### 2.2 Clients (macOS app / CLI / web admin)

- One WebSocket connection per client.
- Send requests: `health`, `status`, `send`, `agent`, `system-presence`, etc.
- Subscribe to events: `tick`, `agent`, `presence`, `shutdown`, etc.

### 2.3 Nodes (macOS / iOS / Android / headless)

- Connect to the **same** WebSocket server with `role: node`.
- Provide a **device identity** in `connect`; pairing is device-based.
- Expose commands: `canvas.*`, `camera.*`, `screen.record`, `location.get`, `system.run`, `system.notify`, etc.

### 2.4 Connection lifecycle (simplified)

1. Client opens WebSocket.
2. First frame **must** be a `connect` request (handshake).
3. Gateway may send `connect.challenge` (nonce) for non-local connects; client signs it.
4. Gateway responds with `res` (e.g. `hello-ok`), including snapshot: presence, health, policy.
5. Client then issues `req` (e.g. `agent`, `send`) and receives `res` and `event` frames.

---

## 3. Gateway WebSocket Protocol

### 3.1 Transport

- **WebSocket**, text frames, JSON payloads.
- **First frame must be `connect`.** Any other frame or non-JSON closes the connection.

### 3.2 Handshake (`connect`)

**Gateway → client (optional pre-connect challenge):**

```json
{"type":"event","event":"connect.challenge","payload":{"nonce":"…","ts":1737264000000}}
```

**Client → Gateway:**

```json
{
  "type": "req",
  "id": "…",
  "method": "connect",
  "params": {
    "minProtocol": 3,
    "maxProtocol": 3,
    "client": {"id": "cli", "version": "1.2.3", "platform": "macos", "mode": "operator"},
    "role": "operator",
    "scopes": ["operator.read", "operator.write"],
    "caps": [],
    "commands": [],
    "permissions": {},
    "auth": {"token": "…"},
    "locale": "en-US",
    "userAgent": "moltbot-cli/1.2.3",
    "device": {
      "id": "<device_fingerprint>",
      "publicKey": "…",
      "signature": "…",
      "signedAt": 1737264000000,
      "nonce": "…"
    }
  }
}
```

**Gateway → client (success):**

```json
{"type":"res","id":"…","ok":true,"payload":{"type":"hello-ok","protocol":3,"policy":{"tickIntervalMs":15000}}}
```

When a device token is issued, `hello-ok` also includes `auth.deviceToken`, `auth.role`, `auth.scopes`.

### 3.3 Node connect example

Nodes use `role: "node"`, plus `caps`, `commands`, `permissions`:

```json
{
  "role": "node",
  "scopes": [],
  "caps": ["camera", "canvas", "screen", "location", "voice"],
  "commands": ["camera.snap", "canvas.navigate", "screen.record", "location.get"],
  "permissions": {"camera.capture": true, "screen.record": false}
}
```

### 3.4 Framing (post-handshake)

| Type | Direction | Structure |
|------|-----------|-----------|
| Request | Client → Gateway | `{type: "req", id, method, params}` |
| Response | Gateway → Client | `{type: "res", id, ok, payload \| error}` |
| Event | Gateway → Client | `{type: "event", event, payload, seq?, stateVersion?}` |

**Idempotency:** Side-effecting methods (`send`, `agent`) require idempotency keys; the server keeps a short-lived dedupe cache for safe retries.

---

## 4. Roles and Scopes

### 4.1 Roles

- **`operator`** — Control-plane client (CLI, web UI, macOS app, automation). Can call `agent`, `send`, `status`, etc.
- **`node`** — Capability host (camera, screen, canvas, `system.run`). Declares `caps` and `commands`; the Gateway enforces allowlists.

### 4.2 Scopes (operator)

Common scopes: `operator.read`, `operator.write`, `operator.admin`, `operator.approvals`, `operator.pairing`. Used for access control and UI visibility.

### 4.3 Node caps / commands / permissions

- **caps** — High-level categories (e.g. camera, canvas, screen).
- **commands** — Allowlist of invokable commands (e.g. `camera.snap`, `screen.record`).
- **permissions** — Granular toggles (e.g. `camera.capture`, `screen.record`).

The Gateway treats these as **claims** and enforces server-side allowlists when routing `node.invoke` or similar.

---

## 5. Auth and Pairing

### 5.1 Gateway token

If `CLAWDBOT_GATEWAY_TOKEN` (or `--token`) is set, `connect.params.auth.token` must match or the socket is closed.

### 5.2 Device identity and pairing

- All WS clients (operators and nodes) include a **device identity** in `connect` (`device.id`, keypair-derived fingerprint, etc.).
- **New device IDs** require pairing approval; the Gateway issues a **device token** for subsequent connects.
- **Local** connects (loopback or the host’s own Tailscale address) can be auto-approved.
- **Non-local** connects must sign the `connect.challenge` nonce and receive explicit approval.

### 5.3 Device tokens

- Returned in `hello-ok.auth.deviceToken`; clients should persist them.
- Rotation/revocation: `device.token.rotate`, `device.token.revoke` (requires `operator.pairing` scope).

---

## 6. Presence

- `system-presence` returns entries keyed by device identity.
- Each entry includes `deviceId`, `roles`, `scopes` so UIs can show one row per device even when it connects as both operator and node.

---

## 7. Exec approvals

When an exec request needs approval, the Gateway broadcasts `exec.approval.requested`. Operator clients with `operator.approvals` scope resolve via `exec.approval.resolve`.

---

## 8. Versioning and Codegen

- **Protocol version** lives in `src/gateway/protocol/schema.ts` (`PROTOCOL_VERSION`).
- Clients send `minProtocol` and `maxProtocol`; the server rejects mismatches.
- TypeBox schemas → JSON Schema → Swift models. Commands: `pnpm protocol:gen`, `pnpm protocol:gen:swift`, `pnpm protocol:check`.

---

## 9. Remote Access

- **Preferred:** Tailscale Serve (tailnet-only) or Funnel (public, with password auth). Gateway stays bound to loopback.
- **Alternative:** SSH tunnel, e.g. `ssh -N -L 18789:127.0.0.1:18789 user@host`. Same handshake and auth apply over the tunnel.
- **TLS:** Supported for WS; optional cert pinning via `gateway.tls`, `gateway.remote.tlsFingerprint`, or CLI `--tls-fingerprint`.

---

## 10. Invariants

- Exactly **one** Gateway controls a single Baileys/WhatsApp session per host.
- Handshake is **mandatory**; any non-JSON or non-`connect` first frame results in a hard close.
- Events are **not replayed**; clients must refresh or handle gaps themselves.

---

## 11. Scope of the Protocol

The protocol exposes the **full gateway API**: status, channels, models, chat, agent, sessions, nodes, approvals, etc. The exact surface is defined by the TypeBox schemas in `src/gateway/protocol/schema.ts`.

---

## References

- [Gateway protocol](https://docs.molt.bot/gateway/protocol)
- [Architecture](https://docs.molt.bot/concepts/architecture)
- [Bridge protocol](https://docs.molt.bot/gateway/bridge-protocol)
- [Pairing](https://docs.molt.bot/gateway/pairing)
- [Security](https://docs.molt.bot/gateway/security)
- [Remote](https://docs.molt.bot/gateway/remote)
