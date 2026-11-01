# 03 - Clean Batocera VM Build Log (Goliath, 2026-10-15)

**Purpose:** Reproducible proof that the legal path works: stock Batocera, no ROMs, no BIOS, running virtualized on fleet hardware via virtualization-mcp. Everything below was executed and verified this day; no step is aspirational.

## 1. Recipe card

| Item | Value |
|------|-------|
| Host | Goliath, Windows 11, Ryzen 9 5900X (Zen3), 64GB RAM, VirtualBox 7.2.6 |
| Image | `batocera-zen3-x86-64-v3-43.1-20260529.img.gz` (zen3-optimized, correct for this CPU), 4,326,809,618 bytes compressed, 11,275,358,208 bytes raw |
| Source | `https://updates.batocera.org/x86-64-v3/stable/last/...` (linked from `batocera.org/download`, stable 43.1) |
| VM name | `batocera-clean` (ostype `ArchLinux_64` - closest VirtualBox profile for Buildroot Linux) |
| Spec | 4 CPU / 4096MB RAM / 32GB dynamic VDI, VBoxSVGA + 3D accel, xHCI USB, HDA audio, NAT |
| Disk home | `D:\VMs\batocera-clean\` (C: had only 5.3GB free - image work must live on D:) |
| Access | VRDE RDP `127.0.0.1:3392`, SSH forward `127.0.0.1:2222` -> guest 22 (root/linux), SMB forward `127.0.0.1:4445` -> guest 445 |
| Snapshot | `clean-booted-43.1` (uuid 99efbccb-699b-4f56-a853-dee3df95d9eb) |
| Verified | Boot splash `43.1 2026/05/28` on screenshot; HDA mixer activity (= boot video audio playing); `SSH-2.0-dropbear_2024.86` banner on port 2222 |

## 2. Pipeline (what was actually run)

1. `vm_management(action="create", vm_name="batocera-clean", os_type="ArchLinux_64", memory_mb=4096, disk_size_gb=32)` - note: tool rejects `Linux_64`, use `ArchLinux_64`.
2. Tuned via VBoxManage: `--cpus 4 --vram 256 --usbxhci on --audiocontroller hda --audioout on`, boot order disk-only.
3. Downloaded image with **detached** `curl.exe` (`Start-Process ... -WindowStyle Hidden`). Reason: each shell-tool call is an isolated process; `Start-Job` background downloads die with the parent shell (observed: 256MB stall). Detached curl resumed with `-C -` after the stall.
4. Decompressed with .NET `GzipStream` (`[IO.Compression.CompressionMode]::Decompress`) - full detached script at `D:\VMs\batocera-clean\build.ps1`, log `build.log`.
5. `VBoxManage convertfromraw batocera.img batocera.vdi --format VDI` then `modifymedium disk --resize 32768`; attached to SATA port 0, replacing the empty placeholder VDI (placeholder deleted, repo dir kept clean).
6. First boot: partition auto-expansion + settling. Then display iteration (section 3), then snapshot via `snapshot_management(action="create", snapshot_name="clean-booted-43.1")`.

## 3. Quirks found + fixes (future builders read this first)

1. **Isolated shells kill background jobs.** Never `Start-Job` a download and expect it in the next call. Use detached `Start-Process` + poll file size. (Same root cause as the fleet "subshell statelessness" rule.)
2. **PowerShell `[System.IO.Compression.Decompress]` is not a type.** GzipStream needs `[System.IO.Compression.CompressionMode]::Decompress`. Wrong enum = silent death between log lines, no output file. Cost 10 min of confusion.
3. **C: full, D: empty.** Check `Get-PSDrive` free space before downloading multi-GB images. All Batocera artifacts on D:.
4. **VMSVGA + 3D = screenshot blindness.** `screenshotpng` captures the VGA framebuffer, not accelerated GL output: black 3KB PNGs while the guest is demonstrably running (audio mixer moving, disk writes). Do not mistake for a hung boot.
5. **EmulationStation needs GL.** Without 3D accel the boot splash shows, then black after ES starts. Working combo on this host: **VBoxSVGA + `--accelerate3d on`**. View via VirtualBox GUI (Show) or VRDE RDP, not via screenshots.
6. **Health signals better than screenshots:** VDI growth (expansion writes), HDA mixer volume changes in VBox.log (audio = guest alive), NAT link up, SSH banner on forwarded port. In that order of cheapness.
7. **ACPI shutdown works.** Guest honors power button; no `poweroff` force needed when reconfiguring (verify `VMState="poweroff"` before `modifyvm` anyway).

## 4. Operating notes

* **Add content only via legal paths** (doc 01 section 4): own dumps over Samba (`\\127.0.0.1@4445\share`), homebrew, BIOS from your own consoles. Snapshot before experimenting; restore is one call.
* **Keep `batocera.img.gz` on D:** it doubles as a USB-flash source for bare-metal boot (Balena Etcher / `dd`), which is the recommended path for PS2-era and newer systems - the VM has no GPU passthrough, so 3D systems will lag here by design.
* **Old systems are the VM sweet spot:** Gameboy through PS1-era and arcade run full speed virtualized; that is the honest scope of this VM.
* **Reproduce on another host:** same image URL pattern (`updates.batocera.org/<arch>/stable/last/`), generic `x86_64` image if CPU is not Zen3+. Everything else transfers as-is.
