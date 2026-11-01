# 2026-09-27 Goliath GSOD postmortem (green screen, no dump, BIOS reset)

Machine: Goliath - Ryzen 9 5900X, RTX 4090, ASUS ROG STRIX B550-F GAMING (WI-FI)
BIOS 1401 (2020-12-03), Windows Dev Insider build 29671, open case, dust problem.
First hard crash in years (prior crashes only after borked MS/driver updates).

## Timeline

- 12:09-13:39: 10+ `python.exe` APPCRASH events (`c0000374` heap corruption in
  `ntdll.dll`, `StackHash_47bc`, python 3.12.9150.1013). Possible early warning,
  faulting python path still unidentified.
- 16:42: last benign event before the fall (DCOM 10016, noise).
- 16:58:42: unexpected shutdown (EventLog 6008).
- Then: green screen, dropped to BIOS, refused to boot. Powered off 1 hour.
- 19:33: booted (Kernel-Power 41 logged), PIN reset requested.

## Evidence (all read live from the machine)

- `C:\Windows\MEMORY.DMP`: absent. Normal for this box - `CrashControl`
  `CrashDumpEnabled = 3` (minidump only).
- `C:\Windows\Minidump`: exists, empty. No minidump was written.
- `C:\Windows\LiveKernelReports`: empty. No watchdog dumps.
- WER `ReportQueue`: 0. `ReportArchive`: python APPCRASH pileup only.
- System log crash IDs: 41 present, 6008 present, **BugCheck 1001 absent**.
- `Microsoft-Windows-WHEA-Logger`: nothing in last 7 days.
- All disks `Healthy / OK` (CT2000P3PSSD8, Samsung 990 PRO 4TB, USB externals).
- GPU calm post-reboot (4090 at 47C idle). SMART temps unreadable unelevated
  (CIM access denied - needs Administrator).
- Green screen = expected BSOD color on Insider Dev builds, not a separate symptom.

## Diagnosis

1. No 1001 + no dump artefacts = the OS never got a chance to write a dump.
   Hard hang, power loss, or storage dropout - below the OS, not a driver that
   bugchecked cleanly. The 1-hour-off recovery points at heat soak or PSU
   over-current reset.
2. The failed boots reset firmware to defaults (confirmed from Windows):
   `VirtualizationFirmwareEnabled = False` (SVM off), `UEFISecureBootEnabled = 0`,
   fTPM provisioned before but invisible now. This explains every post-reboot
   symptom at once: Docker "virtualization support not detected", VRChat/EAC
   "TPM missing", PIN reset (TPM re-measurement), Discord hang (protected
   storage fallout).
3. Open case cuts both ways: no room heat buildup, but dust settles directly on
   fins and M.2 heatsinks and there is no directed airflow over the M.2 area.
   The primary M.2 sits in 4090 exhaust (300-450W). NVMe dropout under sustained
   writes fits: crash, no dump, no boot device until cooldown.
4. Libation (Audible tool, ran that day) is userspace .NET - no mechanism,
   treated as coincidence.

## Fix applied

BIOS re-enables (Del on POST, ASUS B550-F paths):
- Advanced > CPU Configuration > SVM Mode > Enabled
- Advanced > Trusted Computing > Security Device Support > Enable,
  TPM Device Selection > Firmware TPM
- Boot > Secure Boot > OS Type > Windows UEFI mode, Mode > Standard
- Optional: AMD CBS > IOMMU > Enabled. CSM stays disabled.
- Verify elevated: `Get-Tpm`, `Confirm-SecureBootUEFI`,
  `(Get-CimInstance Win32_Processor).VirtualizationFirmwareEnabled` should be True.

## Tooling added (system-admin-mcp)

Four `system_admin` ops, one Prefab card, one prompt (commits bcdd383, 1405a9f):
- `list_crash_dumps` - MEMORY.DMP, Minidump, LiveKernelReports, WER, CrashControl
- `get_bugcheck_history` - 41/1001/6008/1074 correlation with interpretation
- `analyze_minidump` - pure-python MDMP triage (code, params, faulting module)
- `windbg_analyze` - cdb.exe `!analyze -v` when Debugging Tools exist
- `crash_postmortem_card`, `crash_postmortem_expert` prompt

## Follow-ups (open)

- Identify the heap-crashing python (Application Error 1000 detail has the path).
- 990 PRO firmware (known degradation bug), board BIOS update only after stable.
- `mdsched` RAM pass, `sfc /scannow`, SMART via Magician/HWiNFO64 elevated.
- Dust clean of fins + M.2 heatsinks, check thermal pad contact.
- Consider Automatic dump (7) + system-managed pagefile so the next clean
  crash leaves a dump. Reseat 12VHPWR while the case is open.
