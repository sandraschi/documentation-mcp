# Troubleshooting

## Server doesn't appear in Claude Desktop
**Cause**: Config JSON is malformed
**Fix**: Validate at jsonlint.com, check for trailing commas

## "command not found: uv"
**Cause**: uv not installed or not in PATH
**Fix**: `winget install astral-sh.uv` then restart terminal

## Collector shows "PowerShell exited ... Import-Module"
**Cause**: Defender module missing or named differently
**Fix**: Check `Get-Module -ListAvailable ConfigDefender`; set `SAFETY_DEFENDER_MODULE` to the actual module name

## security_events returns ACCESS_DENIED
**Cause**: Security channels (4688/4624) need elevation
**Fix**: Run safety-mcp as administrator, or grant the service account Read on the Security log

## security_events returns nothing for PowerShell channel
**Cause**: Script-block logging (4104) disabled
**Fix**: Enable via Group Policy or `wevtutil` — check `Get-WinEvent -ListLog Microsoft-Windows-PowerShell/Operational`

## network_evidence: firewall log not found
**Cause**: Firewall logging disabled
**Fix**: `Set-NetFirewallProfile -Profile Domain,Public,Private -LogBlocked 1 -LogAllowed 1`

## network_evidence(sniff) fails
**Cause**: packetsniffer-mcp not running on 10920
**Fix**: Start packetsniffer-mcp; the operation reports the failure (not fatal)

## aiwatcher errors
**Cause**: aiwatcher-mcp not running on 10946
**Fix**: Start aiwatcher-mcp; verdicts still persist locally

## Verdict always "deterministic" (no LLM)
**Cause**: No host LLM (ctx.sample) and Ollama not detected
**Fix**: Start Ollama (or connect a host LLM). The deterministic classifier is
the designed fallback and encodes the false-positive rules.

## Verdict says "benign" for a Defender detection
**Cause**: cmdline-only behavioral detection with dev-process markers and no
egress — the PowhidSubExec pattern
**Fix**: Read the evidence chain. If the flagged process is genuinely unknown
or has egress, the verdict would be suspicious/incident — trust the evidence,
not the label.

## Firewall log grows unbounded
**Cause**: LogAllowed+LogBlocked produces large files
**Fix**: Rotate or disable LogAllowed: `Set-NetFirewallProfile -LogAllowed 0`
