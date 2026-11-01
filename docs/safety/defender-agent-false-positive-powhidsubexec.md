# Defender False Positive: Trojan:Win32/PowhidSubExec.B vs Agentic Development Workflows

**Last Updated**: 2026-08-04
**Incident Date**: 2026-08-04
**Severity**: PUA-class (Defender severity 5, no file quarantined)
**Verdict**: False positive — Defender flagged the developer's own smoke-test
PowerShell commands, not malware, and not any file in the new repo.

---

## Executive Summary

While building `zoji-mcp` (a FastMCP server that reads a Dymo USB HID postal
scale), Windows Defender fired **three** `Trojan:Win32/PowhidSubExec.B`
detections within ~90 seconds (15:04:35, 15:05:08, 15:06:03). The flagged
"resources" were not files — they were the **command lines of the agent's
own smoke-test PowerShell processes**: port-zombie killing, hidden-window
server spawning, and HTTP JSON-RPC probing.

Defender's behavioral heuristics had matched a legitimate agentic dev
workflow against a malware signature. A side effect: Defender terminated the
flagged processes mid-flight, which is why the server restarts in that window
failed with `spawn EPERM`.

No file in `D:\Dev\repos\zoji-mcp\` was ever flagged. The repo is clean.

---

## Detection Evidence (from Defender)

```
Threat     : Trojan:Win32/PowhidSubExec.B
ThreatID   : 2147941383
Severity   : 5 (High / PUA-class behavioral)
Detected   : 2026-08-04 15:04:35, 15:05:08, 15:06:03
Process    : Unknown (behavioral, no parent file)
Action     : Success (process termination)
Resources  : 3x CmdLine:_C:\Program Files\PowerShell\7\pwsh.exe ...
             (0x file: resources)
```

The three flagged command lines, verbatim (abridged), were the agent's
smoke-test chain:

```powershell
# Detection 1 (15:04:35)
Get-Process python | Stop-Process -Force; ... Start-Process pwsh -WindowStyle Hidden ...

# Detection 2 (15:05:08) — 3 command lines
$conn = Get-NetTCPConnection -LocalPort 11144; ... Stop-Process ... ; taskkill /F /PID 564940
Start-Process pwsh -ArgumentList "-NoProfile","-Command","...uv run python -m zoji_mcp.server..." -WindowStyle Hidden
$r = Invoke-WebRequest ... -Body '{"jsonrpc":"2.0","id":1,"method":"initialize"...}'   # /mcp/ probe

# Detection 3 (15:06:03)
Get-Process python | Stop-Process -Force ... Start-Process pwsh -WindowStyle Hidden ...
```

Every element is a standard fleet dev-operation. Together they spell
"malware" to the heuristic.

---

## Why Defender Thinks This Is Malware

The `PowhidSubExec` family name decomposes as:

| Fragment | Meaning |
|----------|---------|
| **Pow** | PowerShell |
| **Hid** | HID — human interface device interaction (keyboard/mouse injection) |
| **SubExec** | subprocess execution — spawning children from a script |

The behavioral profile the family is built to catch:

1. **PowerShell spawning hidden child processes** (`Start-Process -WindowStyle
   Hidden`) — classic stealth-execution pattern used to run payloads without
   console windows.
2. **Aggressive process termination** (`Stop-Process -Force`, `taskkill /F /T`)
   — used by malware to kill AV, kill its own re-instantiations, or clear
   locks; used by us to clear port zombies.
3. **Network probing from the spawned process** (`Invoke-WebRequest` with
   JSON-RPC bodies against localhost) — malware beaconing / lateral movement
   probes; us checking `/mcp/` streamable HTTP handshake.

Individually innocent; the co-occurrence inside one PowerShell session is
exactly what the signature family looks for. Notably, the project legitimately
uses **HID** (the `hid` package for the Dymo scale) — an amusing but
coincidental thematic overlap; the detections were behavioral (CmdLine), not
static (no file was scanned in).

---

## Why It Is a False Positive (evidence chain)

1. **Zero `file:` resources.** All resources are `CmdLine:` entries. Nothing
   on disk was flagged, matched, or quarantined — `Get-MpThreatDetection`
   shows no `file:_D:\Dev\repos\zoji-mcp\...` resource in any of the three
   detections.
2. **Full provenance.** The flagged commands are traceable 1:1 to the agent
   transcript of the session: port kill -> hidden spawn of `uv run python -m
   zoji_mcp.server` -> `GET /api/health` -> `POST /mcp/` initialize probe.
   Same session produced working REST responses (200s) between detections.
3. **The "malware" process was our server.** The hidden-spawned child was the
   zoji-mcp uvicorn process; its stdout log shows normal startup
   (`Uvicorn running on http://127.0.0.1:11144`, DISPENSE events classified).
4. **Correlated failure.** Restart attempts during the detection window failed
   with `spawn EPERM` — Defender killing the flagged child before it could
   bind. That is Defender acting on the false positive, not a repo problem.
5. **Clean repo.** `Get-MpThreatDetection` history contains no zoji-mcp path.
   The `hid` package (hidapi DLL binding — the only technically
   malware-adjacent dependency) was not flagged either.

---

## The Systemic Lesson: Agent Workflows Are Behaviorally Indistinguishable From Malware

This is the interesting part. A fleet dev loop looks identical to a
post-exploitation toolkit at the OS level:

| Malware behavior | Fleet dev behavior |
|------------------|--------------------|
| Kill processes to avoid detection / clear locks | `Stop-Process` port-zombie cleanup before binding |
| Spawn hidden children to avoid console visibility | `Start-Process -WindowStyle Hidden` for headless servers |
| Probe network endpoints from the child | `Invoke-WebRequest` health/MCP handshake probes |
| PowerShell as the orchestration layer | pwsh as the shell (all agent tooling runs through it) |
| Loop until the payload is running | Retry-with-backoff server startup loops |

Any AV heuristic that fires on this combination will false-positive on every
agentic session that manages long-running servers. Expect more of these; the
fix is exclusion scoping, not changing how we work (except where noted
below).

---

## Mitigations

### 1. Scoped Defender exclusions (recommended, applied at incident time)

```powershell
# Run as admin, once
Add-MpPreference -ExclusionPath "D:\Dev\repos", "C:\Users\<user>\AppData\Local\Temp\opencode"
```

Scoped to the fleet root + agent temp dir. Do **not** add a blanket
`-ExclusionProcess pwsh.exe` — that disables protection for the shell that
would also run genuinely malicious scripts.

### 2. Reduce the trigger surface in agent workflows (optional, low cost)

- Prefer `Start-Process -NoNewWindow` or `-WindowStyle Minimized` over
  `-WindowStyle Hidden` when the child must be visible-on-demand; hidden is
  the strongest trigger signal.
- Batch port kills and spawns into one clearly-commented launcher script
  (e.g. `start.ps1` via the fleet engine) instead of inline one-liners —
  Defender's cmdline heuristics see long inline `-Command` chains as more
  suspicious than a named script file.
- For repeat probes, a tiny named probe script (like the MCP handshake
  helper) reads less like beaconing than ad-hoc `Invoke-WebRequest` bodies.

### 3. If you see `spawn EPERM` during a fleet build

Before assuming a code problem, check Defender:

```powershell
Get-MpThreatDetection | Sort-Object InitialDetectionTime -Descending | Select-Object -First 5
```

A `Trojan:Win32/PowhidSubExec.*` / `PowhidSubExec` entry with CmdLine-only
resources at the same timestamp as your failure is this false positive, not
a build break.

---

## Triage Checklist for Future PowhidSubExec Alerts

Use this before "allow" or "quarantine":

1. `Get-MpThreatDetection` -> do all Resources start with `CmdLine:`? (No
   `file:` entries = behavioral, not a file infection.)
2. Is the flagged command in your shell/agent history verbatim? (Reproduce
   provenance.)
3. Was a legit child process (uvicorn, vite, node) the target of the hidden
   spawn?
4. `Get-MpThreat` -> confirm severity is PUA-class (5) and the family is
   behavioral (`*Powhid*`, `*Pow*SubExec*`, `*Reflect*`).
5. If all yes: add the scoped exclusion above and continue. If any no —
   escalate: quarantine, `Get-MpThreatDetection` the file path, and follow
   [AGENTIC_BOTNETS.md](../standards/threats/AGENTIC_BOTNETS.md) review.

---

## References

- Microsoft Defender threat: `Trojan:Win32/PowhidSubExec.B` (ThreatID
  2147941383)
- Fleet threat index: [standards/threats/](../standards/threats/)
- Related fleet false-positive family: PowerShell behavioral heuristics
  (`Commando`, `Vigorf`, `PowHid*` — same PUA-class behavioral pattern)
- Incident repo: `zoji-mcp` (2026-08-04, first build smoke test)
