# Moltbot — Channels and Messaging

**Last updated:** 2025-01-28  
**See also:** [moltbot-00-overview](moltbot-00-overview.md) | [Channels index](https://docs.molt.bot/channels) | [Channel routing](https://docs.molt.bot/concepts/channel-routing)

---

## 1. Overview

The Gateway owns **all messaging surfaces**. Inbound messages from WhatsApp, Telegram, Slack, Discord, etc. are routed into the agent loop; outbound replies are delivered back over the same (or configured) channel. Channel adapters use existing SDKs: Baileys (WhatsApp), grammY (Telegram), Bolt (Slack), discord.js (Discord), and so on. Extension channels (MS Teams, Matrix, Zalo, etc.) live under `extensions/` and plug into the same routing layer.

---

## 2. Built-in Channels

| Channel | Adapter | Notes |
|---------|---------|-------|
| WhatsApp | Baileys | Creds in `~/.clawdbot/credentials`. `allowFrom` allowlist. |
| Telegram | grammY | `channels.telegram.botToken`. Optional `groups`, `requireMention`. |
| Slack | Bolt | `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN` (or config). |
| Discord | discord.js | `channels.discord.token`. DM policy, `guilds`, `mediaMaxMb`. |
| Google Chat | Chat API | Google Cloud project, bot config. |
| Signal | signal-cli | `channels.signal` config. |
| iMessage | imsg | macOS only; Messages signed in. |
| BlueBubbles | extension | Extensions repo. |
| Microsoft Teams | extension | Bot Framework app + `msteams` config. |
| Matrix | extension | `extensions/matrix`. |
| Zalo / Zalo Personal | extension | `extensions/zalo`, `zalouser`. |
| WebChat | Gateway WS | No separate port; uses Gateway WebSocket. |

---

## 3. Channel Routing

- **Inbound:** Messages hit the Gateway, are normalized, and routed to a **session** (main, group, or agent-specific). Routing respects allowlists, group rules, and activation mode (mention vs always).
- **Outbound:** Agent replies (or `moltbot message send`) are delivered to the appropriate channel. Streaming is used internally; only **final** replies are sent to external surfaces (WhatsApp, Telegram, etc.) to avoid partial message UX.
- **Group rules:** Per-channel and per-group config. Mention gating, reply tags, allowlists. See [Groups](https://docs.molt.bot/concepts/groups), [Group messages](https://docs.molt.bot/concepts/group-messages).

---

## 4. DM Policy and Pairing

- **Default:** `dmPolicy: "pairing"` (or channel-specific e.g. `channels.discord.dm.policy`, `channels.slack.dm.policy`). Unknown senders get a short pairing code; the bot does not process their message until approved.
- **Approve:** `moltbot pairing approve <code>`. Sender is added to a local allowlist.
- **Open DMs:** Set `dmPolicy: "open"` and include `"*"` in the channel allowlist (`allowFrom`, `channels.discord.dm.allowFrom`, etc.). Use only when you explicitly want public DMs.

Run `moltbot doctor` to surface risky or misconfigured DM policies.

---

## 5. Allowlists and Groups

- **allowFrom:** Per-channel allowlist (e.g. `channels.whatsapp.allowFrom`, `channels.telegram.allowFrom`). Restrict who can talk to the assistant.
- **groups:** When set, acts as a group allowlist. Use `"*"` to allow all groups (with optional `requireMention`).
- **Group activation:** `mention` (only when @mentioned) vs `always`. Owner-only commands for activation toggle in groups.

---

## 6. Extensions

Extension channels live under `extensions/` (e.g. `msteams`, `matrix`, `zalo`, `zalouser`, `voice-call`). They are workspace packages; keep plugin-only deps in the extension `package.json`. When adding or refactoring channel logic, consider **all** built-in and extension channels (routing, allowlists, pairing, onboarding, docs).

---

## 7. Media and Formatting

- **Media pipeline:** Images, audio, video; transcription hooks, size caps, temp file lifecycle. See [Images](https://docs.molt.bot/nodes/images), [Audio](https://docs.molt.bot/nodes/audio).
- **Markdown:** Per-channel formatting and chunking. See [Markdown formatting](https://docs.molt.bot/concepts/markdown-formatting), [Streaming](https://docs.molt.bot/concepts/streaming).

---

## 8. Configuration Snippets

**Telegram:**

```json
{
  "channels": {
    "telegram": {
      "botToken": "123456:ABCDEF"
    }
  }
}
```

**Discord:**

```json
{
  "channels": {
    "discord": {
      "token": "your-bot-token"
    }
  }
}
```

**WhatsApp:** Link via `moltbot channels login`; credentials stored in `~/.clawdbot/credentials`. Configure `channels.whatsapp.allowFrom`, optionally `channels.whatsapp.groups`.

---

## 9. Troubleshooting

- [Channels troubleshooting](https://docs.molt.bot/channels/troubleshooting)
- `moltbot channels status --probe` for connectivity checks.
- Logs: Gateway stdout, or platform-specific (e.g. `./scripts/clawlog.sh` on macOS).

---

## References

- [Channels](https://docs.molt.bot/channels)
- [Channel routing](https://docs.molt.bot/concepts/channel-routing)
- [Groups](https://docs.molt.bot/concepts/groups)
- [Group messages](https://docs.molt.bot/concepts/group-messages)
- [Messages](https://docs.molt.bot/concepts/messages)
- [Streaming](https://docs.molt.bot/concepts/streaming)
