# 2026-10-14 Goliath GSOD postmortem (two bugchecks, dumps present)

Machine: Goliath - Ryzen 9 5900X, RTX 4090, ASUS ROG STRIX B550-F GAMING
(WI-FI). Follow-up to [2026-09-27](./2026-09-27_goliath-gsod-postmortem.md)
(which had no dump: hard hang, BIOS reset, heat/PSU suspected).

## Timeline

- 09:35: first green screen, unnoticed (asleep). Clean reboot on wake.
- 18:18: `llama-server.exe` (local-LLM GPU server) AppCrash x3 within
  5 seconds (WER archive, userspace - not the kernel story, but noted).
- 22:25: second green screen, noticed. Rebooted.
- 22:28-22:49: WER kernel + OneDrive AppHang reports archived.

## Evidence (all read live from the machine)

- `C:\Windows\Minidump`: two dumps, 6.3 + 6.4 MB, both with **PAGEDU64**
  kernel-dump headers (not MDMP small dumps despite the directory).
- 09:35 dump: bugcheck **0xCA PLUGPLAY_NO_DEVICE** (params 2,
  fffffdbf23da12f0, 0, 0) - device vanished during PnP, idle/sleep hours.
- 22:25 dump: bugcheck **0xA IRQL_NOT_LESS_OR_EQUAL** (read at DISPATCH_LEVEL,
  faulting IP fffff806de120121) - driver touched paged memory at high IRQL.
- `MEMORY.DMP`: absent. `LiveKernelReports`: empty.
- NVIDIA 4090 driver 32.0.16.1088 (2026-07-22) - three months old, not
  obviously culpable; 0xA is not the TDR pattern (no 0x116/0x117).
- N: drive is a fixed NVMe (not USB), so the overnight 0xCA is not the
  trivial external-disk case - NVMe sleep-state transitions are suspects.
- Tooling gaps hit during analysis (filed BUG-080/081): `analyze_minidump`
  is MDMP-only, `windbg_analyze` needs classic `cdb.exe` (only GUI WinDbg
  1.2610.1001.0 on the box). Headers parsed by hand with struct instead.

## Diagnosis

1. Two *different* bugchecks ~13 h apart argues against a single bad driver
   and toward hardware-or-power (flaky RAM produces exactly this spread:
   different codes, idle + load) or two independent issues.
2. The 0xCA overnight fits NVMe sleep-state dropout (open case, M.2 in 4090
   exhaust - same thermal geography as the 09-27 suspicion, different
   mechanism: sleep transition, not sustained writes).
3. The 0xA under evening load (concurrent Ghidra JVMs, Frida injection,
   analyses) fits a driver race; JVMs/Frida are userspace and cannot
   green-screen a healthy kernel, but load pushes marginal drivers over.
4. `llama-server` triple-crash is userspace GPU-compute instability - worth
   its own look (VRAM temps/load during inference), not the kernel story.

## Prevention (ordered by leverage)

1. **Rule out RAM**: Windows Memory Diagnostic (reboot test,
   `mdsched.exe`). One clean pass deflates the hardware hypothesis more than
   anything else. If it errors, reseat/replace before any driver hunting.
2. **Update NVIDIA driver** (32.0.16.1088 is 2026-07): cheap, reversible,
   kills the most likely 0xA candidate class. Use the Studio driver if this
   box does more CUDA/LLM than gaming.
3. **BIOS**: 1401 (2020-12-03) on a Ryzen 5000 board is six years of missed
   AGESA stability fixes. Update only on a calm day with a UPS-ish mindset
   (no storms, no concurrent load); re-apply the 09-27 settings (SVM, fTPM,
   Secure Boot) after, since this board resets them.
4. **NVMe sleep**: if 0xCA repeats overnight, disable link-state power
   management for the NVMe (Power Options > PCI Express > Link State > Off)
   and Samsung NVMe driver (not the MS inbox one) for the 990 PRO.
5. **Keep the dumps working**: they worked this time (unlike 09-27) - do not
   "clean" Minidump. Copy new dumps to temp for analysis (ACLs need admin).
6. **Watch, don't chase**: a third crash breaks the tie (third distinct code
   -> RAM; repeat 0xA -> elevated `!analyze` driver hunt; repeat 0xCA ->
   NVMe power). Driver Verifier stays OFF unless a repeat 0xA names no one -
   it bluescreens on purpose and wastes days.

## Tooling added

- `integrations/windbg-mcp/README.md` (official WinDbg MCP, evaluated).
- BUG-080 (PAGEDU64 support), BUG-081 (cdb discovery) filed on
  system-admin-mcp with fix sketches.
