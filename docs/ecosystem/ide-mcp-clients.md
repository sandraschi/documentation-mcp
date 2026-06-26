# IDE MCP Client Comparison

**Last Updated:** 2026-03-17
**Status:** Active — field-tested, corrections applied
**Source:** Mix of official docs + daily use observations

MCP client support varies significantly across IDEs. This doc tracks the real state,
including UI quirks, tool limits, and dev-loop features that matter for our workflow.

---

## Summary Table

| IDE / Client | MCP Support | Tool Limit | Hot Reload | Notes |
|---|---|---|---|---|
| **Claude Desktop** | Full, mature | None documented | Restart required | No sampling yet. **MCP chain hang bug: long sessions or blocking tools (e.g. PowerShell) can freeze entire stack — hard restart only fix.** |
| **Cursor** | Full, mature | Was 40, quietly raised (~80?), no official announcement | **Yes — disable/enable server slider in MCP settings** | Plugin Marketplace bundles MCPs + skills |
| **Windsurf** | Full | None documented | No | Cascade agentic; stable MCP config |
| **Google Antigravity** | Full | None documented | **Yes — MCP stack restart without IDE restart** | UI hidden, see below. Supports MCP sampling. **Systemically unstable since ~Feb 21 2026 release. Known issues: IDE hang in long chats, Accept/Accept-All button unresponsive, quota lockouts (7-day instead of 5-hour on Pro), workspace failures. Active bug reports on Google AI Developers Forum. Avoid for production use until stabilised.** |
| **VS Code + Copilot** | Full (since v1.5/1.6 2025) | None documented | No | Newer, less mature than Cursor/Windsurf |
| **Claude Code** | Full, first-class | None documented | N/A (CLI) | Best for terminal-first agentic workflows |
| **Zed** | Via ACP (external agents) | Agent-dependent | N/A | Agents (Claude Code, Codex) run inside Zed via ACP |

---

## Google Antigravity — Field Notes

Antigravity has **excellent** local MCP server support. At least one published review
(lushbinary.com, March 2026) incorrectly stated "no MCP support" — the reviewer
simply didn't find the UI.

### Accessing MCP in Antigravity

The UI is non-obvious. Access via:

```
Agent pane → "..." (three-dot menu, top right) → MCP Servers → MCP Store
```

From the MCP Store you can:
- Install Google Cloud services one-click (BigQuery, AlloyDB, Spanner, Firebase, etc.)
- Click **Manage MCP Servers** → **View raw config** to edit `mcp_config.json` directly

### Config file location

```
C:\Users\[username]\.gemini\antigravity\mcp_config.json
```

Note: **not** in `AppData\Roaming` — this trips people up.

### MCP stack hot reload — key dev feature

Antigravity can **restart the MCP server stack without restarting the IDE**.
This is the standout feature for MCP development:

- Edit a tool in your MCP server
- Trigger MCP stack restart from within Antigravity
- Changes are live immediately — no full IDE restart cycle

Claude Desktop requires a full restart to pick up MCP server changes.
Cursor and Windsurf similarly require restart or manual reconnect.
Antigravity's hot reload is a genuine productivity win during MCP development.

### Known Issues (as of 2026-03-18)

Antigravity has been systemically unstable since the February 21 2026 release.
Active bug reports on the Google AI Developers Forum confirm these are widespread:

| Symptom | Status |
|---------|--------|
| Long chat → green Accept/Accept-All button appears but does nothing | Confirmed widespread |
| After stuck Accept button: full IDE hang, must restart | Confirmed widespread |
| IDE freezes immediately after sending prompt | Feb 21 release regression |
| Quota showing 168-hour (7-day free tier) lockout instead of 5-hour Pro refresh | Active today (2026-03-18) |
| Workspace failures, slash commands disappearing | Systemic since late Feb |
| "Agent execution terminated due to error" on all prompts | Reported periodically |

**The Accept button hang** is your specific symptom. It appears to be a combination
of: a long-standing "Accept All" approval flow bug (pre-existing, has a community
workaround extension: `pesosz/antigravity-auto-accept` on Open VSX) compounded by
the February regression that causes the UI to lose connection to the agent session
in long chats. Cancel + restart is currently the only reliable fix.

**Workaround for Accept button spam:** Install the Auto Accept extension:
`https://open-vsx.org/extension/pesosz/antigravity-auto-accept`
Settings → Advanced → Terminal → Terminal Command Auto Execution → Turbo or Auto.

**Current recommendation:** Use Cursor as primary dev environment until AG stabilises.
Monitor: https://discuss.ai.google.dev for fix announcements.

---



```json
{
  "mcpServers": {
    "my-mcp": {
      "command": "uv",
      "args": ["--directory", "D:/Dev/repos/my-mcp", "run", "my-mcp"]
    }
  }
}
```

---

## Cursor — MCP Server Reload

Cursor has a per-server disable/enable toggle in the MCP settings UI. This effectively
gives you hot reload without restarting the IDE:

1. Edit the MCP server code in Cursor
2. Open Settings → MCP (or the MCP panel)
3. Toggle the server's slider off → on
4. Server restarts and picks up the changes immediately

This is particularly useful when a server fails to start — fix the bug, flip the slider,
done. No need to restart Cursor or Claude Desktop.

**Practical dev loop:**
```
Edit tool code in Cursor
→ Disable server slider
→ Enable server slider
→ Test in Cursor agent (or Claude Desktop if that's the target client)
```

Note: if Claude Desktop is the target client, you still need a full Claude Desktop
restart to pick up changes — the Cursor slider only affects Cursor's own MCP session.

---

## Cursor — Tool Limit History

| Period | Limit | Status |
|--------|-------|--------|
| Mar 2025 | 40 tools hard cap | Official — Cursor team defended it in forum |
| Jun–Sep 2025 | 40 (reports of "Exceeding total tools limit" warnings) | Unchanged |
| Mar 2026 | ~80 (community reports, unconfirmed) | No official changelog entry found |

The Cursor team said in March 2025 they were building "a better system for the AI to
intelligently select the right tools" — which is exactly what FastMCP's CodeMode does.
The Plugin Marketplace (launched late 2025) bundles MCPs with skills, which likely
enables smarter tool filtering.

**Practical implication for our fleet:** Our portmanteau pattern (1 tool per server,
`operation` param selects action) sidesteps the limit entirely. Each of our servers
contributes 2–5 tools regardless of how many operations it implements.

---

## Claude Desktop — MCP Developer Notes

- Full restart required to reload changed MCP servers
- Logs at: `C:\Users\sandr\AppData\Roaming\Claude\logs\`
- Config at: `C:\Users\sandr\AppData\Roaming\Claude\claude_desktop_config.json`
- No documented tool count limit
- **Sampling not yet supported** — use Antigravity for `ctx.sample()` testing
- **Known issue: MCP server chain hang** — after long sessions or a misbehaving server
  (e.g. a PowerShell tool hanging), the entire MCP stack can freeze. Symptoms: tool
  calls return no result or hang indefinitely. Fix: **full Claude Desktop restart only**
  — no soft reload mechanism exists. Prevention: avoid long-running blocking calls in
  MCP tools (especially PowerShell); use timeout patterns and temp-file output redirect.

---

## When to Use Which IDE for MCP Development

| Task | Recommended |
|------|------------|
| Writing MCP server code | Cursor or Windsurf (best code intelligence) |
| **Iterating on MCP tools (fast feedback loop)** | **Cursor (disable/enable slider) or Antigravity (MCP stack restart)** |
| Testing agentic sampling workflows | Antigravity (confirmed sampling support, currently unstable). Cursor unknown. Claude Desktop: no sampling yet. |
| Terminal-first MCP automation | Claude Code |
| Large codebase context | Cursor (@codebase indexing) |

---

## References

- Antigravity MCP docs: https://antigravity.google/docs/mcp
- Antigravity custom MCP guide: https://antigravity.codes/blog/antigravity-mcp-tutorial
- Google Cloud MCP Store post: https://cloud.google.com/blog/products/data-analytics/connect-google-antigravity-ide-to-googles-data-cloud-services
- Cursor tool limit thread: https://forum.cursor.com/t/increase-the-mcp-tool/69194
- FastMCP CodeMode (tool limit mitigation): `fastmcp/code-mode.md`
