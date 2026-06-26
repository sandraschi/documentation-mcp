# Moltbot — Nodes, Devices, and Apps

**Last updated:** 2025-01-28  
**See also:** [moltbot-00-overview](moltbot-00-overview.md) | [Nodes](https://docs.molt.bot/nodes) | [macOS](https://docs.molt.bot/platforms/macos) | [iOS](https://docs.molt.bot/platforms/ios) | [Android](https://docs.molt.bot/platforms/android)

---

## 1. Nodes Overview

**Nodes** are devices or processes that connect to the Gateway over WebSocket with `role: node`. They declare **caps** (e.g. camera, canvas, screen, location, voice) and **commands** (e.g. `camera.snap`, `screen.record`, `location.get`). The Gateway routes `node.invoke` and similar requests to the appropriate node. Exec runs where the **Gateway** lives; device-local actions (camera, screen, canvas) run where the **node** lives.

---

## 2. Node Connect and Identity

- **role:** `node`.
- **device:** Stable `device.id` (e.g. keypair fingerprint), `publicKey`, `signature`, `signedAt`, `nonce` for challenge signing.
- **caps:** High-level categories (e.g. `camera`, `canvas`, `screen`, `location`, `voice`).
- **commands:** Allowlist of invokable commands.
- **permissions:** Granular toggles (e.g. `camera.capture`, `screen.record`).

Pairing is **device-based**. New device IDs require approval unless local auto-approve applies.

---

## 3. Device Commands (Examples)

| Command | Description |
|---------|-------------|
| `camera.snap` | Take a photo. |
| `camera.clip` | Short video clip. |
| `screen.record` | Screen recording. |
| `location.get` | Device location. |
| `canvas.*` | Canvas push, navigate, eval, etc. |
| `system.run` | Run a local command (macOS node); may require screen-recording permission. |
| `system.notify` | Post a local notification. |

---

## 4. macOS Companion App (Moltbot.app)

- **Menu bar** control for Gateway and health.
- **Voice Wake** and push-to-talk overlay.
- **WebChat** and debug tools.
- **Remote gateway** control over SSH (or Tailscale).
- **Node mode:** Can run as a node, advertising caps/commands and exposing `system.run`, `system.notify`, canvas, camera, screen.

macOS-specific behavior (permissions, signing, menu bar, XPC) is documented under [macOS](https://docs.molt.bot/platforms/macos), [Dev setup](https://docs.molt.bot/platforms/mac/dev-setup), [Release](https://docs.molt.bot/platforms/mac/release).

---

## 5. Voice Wake and Talk Mode

- **Voice Wake:** Always-on voice trigger; forwards to agent (e.g. `moltbot-mac agent --message "${text}" --thinking low`). Uses launchd PATH; ensure pnpm/moltbot bins are on PATH for the app’s agent.
- **Talk Mode:** Continuous speech overlay; listen and speak. macOS, iOS, Android (ElevenLabs, etc.).

---

## 6. Canvas and A2UI

- **Canvas:** Visual workspace for the agent. Nodes can host or interact with Canvas.
- **A2UI:** Markup/ui system. iOS/Android nodes expose Canvas surface; macOS app can too.

---

## 7. iOS Node

- Pairs as a node via the Bridge.
- Voice trigger forwarding, Canvas surface.
- Camera, screen recording, Bonjour pairing.
- Runbook: [iOS connect](https://docs.molt.bot/platforms/ios).

---

## 8. Android Node

- Same Bridge and pairing flow as iOS.
- Canvas, camera, screen capture.
- Optional SMS.
- Runbook: [Android connect](https://docs.molt.bot/platforms/android).

---

## 9. Remote macOS Nodes (Linux Gateway)

If the Gateway runs on **Linux** and a **macOS node** is connected with `system.run` allowed, Moltbot can treat macOS-only skills as eligible when binaries exist on that node. The agent runs those skills via the **nodes** tool (e.g. `nodes.run`). Skills remain visible if the node goes offline; invocations may fail until it reconnects.

---

## 10. Presence and Node Helper Methods

- **system-presence:** Lists devices (operators and nodes). One row per device; same device can have both operator and node roles.
- **skills.bins:** Nodes may call this to fetch skill executables for auto-allow checks.

---

## 11. Exec Approvals

When an exec request requires approval, the Gateway emits `exec.approval.requested`. Operator clients with `operator.approvals` scope resolve via `exec.approval.resolve`.

---

## 12. Platform Notes

- **Windows:** Official support via WSL2. Native Windows node not primary.
- **Linux:** Gateway, Docker sandbox, headless nodes. [Linux](https://docs.molt.bot/platforms/linux), [Fly.io](https://docs.molt.bot/platforms/fly), [Hetzner](https://docs.molt.bot/platforms/hetzner), [GCP](https://docs.molt.bot/platforms/gcp).

---

## References

- [Nodes](https://docs.molt.bot/nodes)
- [Camera](https://docs.molt.bot/nodes/camera)
- [Images](https://docs.molt.bot/nodes/images)
- [Audio](https://docs.molt.bot/nodes/audio)
- [Location](https://docs.molt.bot/nodes/location-command)
- [Voice Wake](https://docs.molt.bot/nodes/voicewake)
- [Talk](https://docs.molt.bot/nodes/talk)
- [macOS](https://docs.molt.bot/platforms/macos)
- [iOS](https://docs.molt.bot/platforms/ios)
- [Android](https://docs.molt.bot/platforms/android)
- [Canvas](https://docs.molt.bot/platforms/mac/canvas)
