# WinDbg MCP - AI-assisted kernel/user crash analysis

Microsoft's official Model Context Protocol bridge for WinDbg (documented
2026-10-06, [Set up and use WinDbg
MCP](https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/set-up-windbg-mcp)).
Not your dad's WinDbg: instead of `!analyze -v` in a console, an AI client
drives debugger tools through MCP while you watch each action in the WinDbg UI.

Status: evaluated 2026-10-14 on Goliath (WinDbg 1.2610.1001.0 = exact minimum
version, Dev Insider build). Not yet wired into any fleet flow.

## How it works

WinDbg runs an MCP server for the current session (`DbgX.Mcp.Proxy.exe`
ships in the Store package). Setup is GUI-driven: File > Settings > MCP
service settings > Enable Server, pick the client (VS Code + Copilot or
Copilot CLI), ribbon: Install MCP (registers with the client) > MCP Service
(starts the server, secure mode ON by default) > Open Chat. Status bar shows
"AI client connected to MCP server". Session tools: `list_sessions`,
`connect_session`, `disconnect_session` (auto-connects when exactly one
WinDbg session exists). Verify prompt: "Use WinDbg MCP to report the current
target type and execution state."

## Why it matters here

- Goliath green-screens (2026-09-27 with no dump; 2026-10-14 0xCA + 0xA with
  kernel dumps). Today's postmortem was done by hand-parsing PAGEDU64 headers
  because no console debugger exists on the box — WinDbg MCP is the sanctioned
  path to agent-driven `!analyze` next time.
- Secure mode (default, irreversible until restart) blocks debugger ops that
  load/execute untrusted code or do unsafe file writes — the right default for
  pointing AI at kernel dumps, which are sensitive by nature.

## Fleet fit and limits

- **Clients are the catch**: officially VS Code Copilot + Copilot CLI only.
  opencode/Claude Desktop are NOT supported (there is a "Custom" dropdown
  entry — experiment, not a claim). Our agents can't consume it today.
- **Community alternative**: `svnscha/mcp-windbg` (MIT-ish, check license)
  bridges any MCP client to WinDbg/CDB for dump analysis + live/remote
  debugging. Needs classic `cdb.exe`, which is NOT on this box (only support
  DLLs under Windows Kits; Store WinDbg ships no console debugger).
- **sysadminops gap (filed 2026-10-14)**: `windbg_analyze` looks for `cdb.exe`
  in PATH + classic SDK paths and errors out; it should also suggest
  `winget install Microsoft.WinDbg` and, longer term, speak to the MCP proxy.
  `analyze_minidump` parses MDMP small dumps only — our 2026-10-14 dumps are
  PAGEDU64 kernel dumps and bounce with "bad MDMP signature".
- Privacy: kernel/memory dumps contain everything in RAM. Microsoft's own doc
  says don't point the server at data you aren't authorized to disclose, and
  to validate every AI finding against visible debugger output. Same rule as
  our ClickerLab receipts: claims need artifacts.

## Suggested next steps (not done)

1. Enable the MCP service once in WinDbg GUI, test the verify prompt via
   Copilot CLI if available; document whether "Custom" client accepts opencode.
2. Evaluate `svnscha/mcp-windbg` against a copy of a real dump (needs cdb
   first — see gap above).
3. If either pans out, wire dump triage into sysadminops (`analyze_minidump`
   gains a PAGEDU64 header path at minimum: bugcheck + params without WinDbg).
