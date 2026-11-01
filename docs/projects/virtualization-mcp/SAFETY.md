# virtualization-mcp — Safety & Airgap Preflight

**Related:** `standards/threats/AI_SANDBOX_ESCAPE_CASE_STUDY.md` (OpenAI/Hugging Face incident)

## Why this exists

The OpenAI/Hugging Face incident (July 2026) showed that a sandbox with any network access — even through a curated package proxy — is not truly isolated. A sufficiently capable model can find a zero-day in the proxy software and escape to the public internet.

Software airgap (firewall rules, proxy filtering, DNS blocking) is **not enough** against a model that can chain unknown vulnerabilities. The only reliable airgap is **physical**: no network cable plugged in, no WiFi connected, no Bluetooth, no cellular.

## Preflight checklist (before running sensitive workloads)

This checklist MUST be displayed in the virtualization-mcp webapp **before** any sandbox is launched with a sensitive/untrusted model:

### Physical airgap

1. **Disconnect Ethernet cable** from the host machine
2. **Disable WiFi** — turn it off in Windows, then also physically toggle the hardware switch if available
3. **Disable Bluetooth** — not just "disconnected" but turned off entirely
4. **Check for alternative networks** — neighbour's open WiFi, phone hotspots, Starlink, cellular USB dongles, tethering
5. **No passthrough devices** that provide network — USB Ethernet adapters, WiFi dongles, phone tethering
6. **Check VMs have no bridge/NAT** — the host being offline doesn't matter if the VM has its own network through a bridged adapter

### Software airgap (belt and suspenders)

7. **Host firewall** — block ALL outbound on the host, not just the sandbox process
8. **DNS resolution should fail** — run `nslookup google.com` from the host; should return nothing
9. **Sandbox has no network device** — no virtual NIC, no NAT, no bridged adapter
10. **Package proxy is absent** — no devpi, no apt-cacher-ng, no Artifactory running on the host. If the model escapes the VM, it must not find a proxy anywhere.

### Verification

11. **`ping 8.8.8.8`** — must fail
12. **`curl https://pypi.org`** — must fail
13. **`ipconfig /all`** — only loopback interface present

### Audit connected MCP servers (physical-world actuators)

Before launching a sandbox with an untrusted model, audit every MCP server currently connected to the host. Any server with access to a physical-world actuator can breach the airgap through non-network means:

| MCP server | How it can re-enable the network |
|------------|----------------------------------|
| **devices-mcp** | Detects motion/gate open → model infers someone is home → social engineering through audio |
| **speech-mcp** | Says "please press the WPS button on the back of the router, the one with the two arrows" — a human who trusts the AI will do it |
| **yahboom-mcp / robotics-mcp** | Physically presses a button via a manipulator arm or wheeled robot |
| **tapo-mcp / shelly via devices-mcp** | Cycles mains power on the ONT or router via smart plug |
| **blender-mcp** | Unlikely but — a 3D-printed part could be a physical key or lever if someone builds the rig |
| **resonite-mcp** | VR/AR overlay could display instructions to a human wearing a headset |

The safest sandbox host has **zero MCP servers running** that can reach any physical-world actuator. Before a sensitive eval:

1. `mcp pulse` — check which servers are alive
2. Disconnect any with physical actuation capability (devices-mcp, speech-mcp, robotics-mcp, yahboom-mcp, tapo-mcp)
3. Kill the processes if needed — a connected server is a potential puppet for the sandboxed model

## Implementation in the webapp

The Launch Sandbox page MUST have a **collapsible preflight section** above the Launch button:

```
┌─────────────────────────────────────────────────┐
│  ⚠️ AIRGAP PREFLIGHT (7 items)                 │
│                                                 │
│  [ ] Ethernet cable disconnected                │
│  [ ] WiFi disabled                              │
│  [ ] Bluetooth disabled                         │
│  [ ] ping 8.8.8.8 — blocked                    │
│  [ ] curl pypi.org — blocked                   │
│  [ ] No proxy services running on host          │
│  [ ] VM has no network device                   │
│                                                 │
│  Launch button is DISABLED until all checked.   │
└─────────────────────────────────────────────────┘
```

The checklist is advisory (user checks boxes manually) — automated network probes run behind the scenes to verify the software checks, and the Launch button stays disabled until the probes pass.

## Test procedure

Before every release of virtualization-mcp involving sandboxed model evaluation:

1. Run the preflight checklist on a machine with known internet access
2. Confirm the automated probes correctly detect connectivity
3. Unplug Ethernet, disable WiFi, re-run probes — must report clean
4. Launch a sandbox, attempt `ping 8.8.8.8` from inside — must fail
5. Attempt `pip install` from inside — must fail

See also: `NAKED_INSTALL_TESTING.md` for consumer sandbox validation procedures.
