# Craft Anything: VM Detonation Sandboxing, IDA Pro Retro Gap, and Upstream PR Strategy

**Status:** Living Research & Operational Spec | **Date:** 2026-11-01  
**Originating Repos:** `_upstream/craft-anything`, `_upstream/texturecraft`, `craft-sandbox-vbox`, `virtualization-mcp`, `reversing-mcp`  
**Issues Tracked:** [storytold/craft-anything#144](https://github.com/storytold/craft-anything/issues/144), [storytold/craft-anything#147](https://github.com/storytold/craft-anything/issues/147), [storytold/craft-anything#163](https://github.com/storytold/craft-anything/issues/163), [storytold/craft-anything#164](https://github.com/storytold/craft-anything/issues/164), [storytold/craft-anything#175](https://github.com/storytold/craft-anything/issues/175), [storytold/craft-anything#179](https://github.com/storytold/craft-anything/issues/179)  
**Reference Implementations:** [`sandraschi/craft-sandbox-vbox`](https://github.com/sandraschi/craft-sandbox-vbox), [`virtualization-mcp`](https://github.com/sandraschi/virtualization-mcp)  

---

## 1. Context & Architectural Overview

On November 1, 2026, Storytold / ArtCraft released two major creative applications in pure Rust:
1. **TextureCraft** (`storytold/texturecraft`): An open-source clone of Adobe Substance 3D Painter (GPU ray-traced mesh map baking, multi-channel PBR painting, F10 path tracing).
2. **Craft Anything** (`storytold/craft-anything`): An adaptation of the 400,000-star `morluto/rea` (rea.tools) repo into an autonomous "Reverse-to-Craft" engine (Study → Build → Check → Ready) powered by Claude Code.

While Craft Anything successfully ports 284 reverse-engineering tools to pure Rust, our deep dive revealed two critical architectural tensions:
1. **The Dynamic Detonation Problem:** Dynamic execution relies on OS-level isolation (Win32 Job Objects on Windows, Bubblewrap on Linux), which is insufficient for malware, packed scene keygens, and evasive binaries.
2. **The Retro Architecture Blind Spot:** Dropping IDA Pro in favor of stock Ghidra 12.1.4 leaves Craft Anything incapable of analyzing vintage 1980s game ROMs (MOS 6502, Z80, 68k) with bank-switched memory mappers.

---

## 2. Deep Dive: The Safe Detonation Problem

### 2.1 The Vulnerability of OS-Level Process Sandboxes
Craft Anything implements process capture in `crates/platform/src/capture.rs`:
- On Linux, it attempts `bwrap` (Bubblewrap) if installed.
- On Windows, it binds child processes to a Win32 **Job Object** with wall-clock and idle deadlines.

While Job Objects cleanly terminate hung processes and runaway CPU loops, **they are not a security sandbox**:
* **Kernel Exploits:** Malicious binaries can exploit unpatched host kernel vulnerabilities to escape user-mode job constraints.
* **Network & LAN Infiltration:** A detonated binary retains access to the host's physical network adapter, enabling port scans, credential harvesting, or lateral movement across local network shares.
* **Registry & User-Space Persistence:** If run with standard user rights, binaries can write persistence mechanisms in `HKCU` outside the monitored paths.
* **Anti-Analysis Evasion:** Modern stealers (RedLine, Lumma, Vidar) and sophisticated protectors (Themida, VMProtect) easily detect Job Objects and fake terminal PTYs, altering their behavior or refusing to run.

### 2.2 The Keygen Detonation Paradigm
Reverse engineers frequently analyze scene keygens and cracked utilities:
* They contain valuable, elegant cryptographic validation algorithms (modular arithmetic, Feistel networks, CRC/MD5 transformations, rolling hashes) that an agent could convert into clean Rust.
* However, nearly 100% of keygens are wrapped in aggressive packers (UPX, ASPack, Petite, Yoda Protector), trigger AV heuristics, and increasingly carry trojanized infostealers.
* **The Solution:** Execute dynamic analysis exclusively inside a disposable, hypervisor-managed guest VM (VirtualBox or Windows Sandbox), extract the decompiled algorithm, and destroy the VM.

---

## 3. Deep Dive: The IDA Pro Omission & Retro ROM Gap

### 3.1 Why ArtCraft Omitted IDA Pro
1. **Licensing & Redistribution:** IDA Pro (Hex-Rays) is proprietary software costing thousands of dollars. It cannot be headless-pinned or auto-downloaded like Ghidra.
2. **Warez / Piracy Liability:** A substantial portion of hobbyists use cracked versions of IDA Pro ("legally or lees legally"). ArtCraft’s strict open-source (Apache-2.0 / MIT) clean-room doctrine cannot tolerate legal entanglements.
3. **Pure-Rust Mandate:** ArtCraft wanted zero heavy external dependencies for baseline operation, building their own disassembler in `crates/disasm`.

### 3.2 Why Stock Ghidra Fails on 1980s Retro ROMs
Abandoning IDA Pro restricts reversing targets:
1. **Hardware Memory Mappers (Bank Switching):** 8-bit systems (NES, Game Boy, Sega Master System) have a 16-bit address bus (64 KB). Cartridges used custom ASIC mappers (Nintendo MMC1–MMC5, Konami VRC, Game Boy MBC1–5) to swap 8 KB or 16 KB PRG-ROM banks into the same virtual window (`$8000–$BFFF`). IDA Pro natively understands segmented memory and selector banking; Ghidra's flat address space model collapses into overlapping symbol collisions.
2. **The 8-Bit Decompiler Fallacy:** Ghidra's core strength is its decompiler. However, 1980s assembly code (MOS 6502, Z80) has no standard C calling convention or stack frames. Arguments are passed in flags (Carry flag = status), registers (A, X, Y), or Zero-Page globals (`$00–$FF`). Ghidra’s decompiler emits unreadable, broken pointer math. IDA Pro is built as an interactive disassembler where control flow, jump tables, and data/code cross-references can be structured cleanly.
3. **Symbolic I/O Maps:** IDA includes decades of `.til` and `.cfg` files mapping hardware registers (NES PPU at `$2000`, APU at `$4000`) to human-readable names automatically.

---

## 4. The Solution: `craft-sandbox-vbox`

To resolve the dynamic detonation problem, we built, tested, and published a standalone, zero-panic Rust library: **[`craft-sandbox-vbox`](https://github.com/sandraschi/craft-sandbox-vbox)**.

### 4.1 Architecture & Design
* **Crate Path:** `d:\Dev\repos\craft-sandbox-vbox`
* **Zero Panic Rule:** Built under `#![deny(clippy::unwrap_used, clippy::expect_used, clippy::panic)]`.
* **Zero C FFI:** Interacts strictly via non-shell argument vectors through `VBoxManage` / `VBoxManage.exe`, preventing path injection and shell interpretation bugs.
* **Windows Host Support:** Uses `CREATE_NO_WINDOW` (0x08000000) to prevent console popup flashing during automated runs.
* **Disposable RAII Session (`SandboxSession`):**
  1. Automatically takes a named pre-detonation snapshot (`craft-detonate-<timestamp>`) while the guest is clean.
  2. Boots the VM headlessly (`--type headless`).
  3. Executes commands inside the guest via `VBoxManage guestcontrol run`.
  4. On `Drop` (or timeout / panic / cancellation), forcibly terminates the VM, rolls back the snapshot, and deletes the temporary snapshot, leaving the host and guest 100% clean.

### 4.2 Verified Local Test Run
Tested against VirtualBox 7.2.22 on the Windows host (`GOLIATH`):
```text
running 3 tests
test tests::parse_empty_vm_list ... ok
test tests::parse_standard_vm_list ... ok
Detected VirtualBox version: 7.2.22r175245
Found 3 registered VMs:
 - win11-automated (431ac83c-18b1-4917-93e5-8605b122dd1d)
 - ubu-2404-lts (ef4f7178-1087-42a5-9539-e6d37a0c5616)
 - batocera-clean (8a9b25ff-bba3-43b3-865e-2b22bcdd05fb)
test tests::live_host_virtualbox_query ... ok

test result: ok. 3 passed; 0 failed; 0 ignored; finished in 0.65s
```
Clippy audit (`cargo clippy --all-targets`) passed with **0 errors and 0 warnings**.

---

## 5. Upstream Issue Tracking on `storytold/craft-anything`

Two formal proposals were filed under identity **`sandraschi`**:

| Issue | Title | URL | Labels Applied |
|---|---|---|---|
| **#144** | `[Idea] Hypervisor-level VM sandboxing (VirtualBox / headless detonation) for untrusted runtime execution` | [Issue #144](https://github.com/storytold/craft-anything/issues/144) | `plugins`, `priority: low` |
| **#147** | `[Idea] Optional IDA Pro engine adapter for legitimate license holders (BYOL / license check) to cover retro architectures & banked ROMs` | [Issue #147](https://github.com/storytold/craft-anything/issues/147) | `plugins`, `priority: low` |
| **#163** | `[Idea] Built-in Windows Sandbox (.wsb) support for zero-config disposable detonation (companion to #144)` | [Issue #163](https://github.com/storytold/craft-anything/issues/163) | `backlog`, `priority: low` |
| **#164** | `[Idea] Embedded loopback TLS/HTTPS intercepting proxy for reversing desktop app APIs into standin backends` | [Issue #164](https://github.com/storytold/craft-anything/issues/164) | `backlog` |
| **#175** | `[Idea] Native WebAssembly (WASM) instruction disassembly and control-flow in crates/disasm` | [Issue #175](https://github.com/storytold/craft-anything/issues/175) | Triaged / New |
| **#179** | `[Idea] One-click source tree extraction from bundled or leaked source maps (sourcesContent)` | [Issue #179](https://github.com/storytold/craft-anything/issues/179) | Triaged / New |

### 5.1 Initial Maintainer Reaction
Within minutes of filing:
* Both issues were accepted and labeled with **`plugins`** and **`priority: low`**.
* The automated triage bot (`ticket-craft`) commented on **#147**:
  > *"Possibly related: #57 and #144."*
* This explicitly linked:
  * **#144:** VirtualBox VM Sandboxing
  * **#147:** IDA Pro BYOL Engine Adapter
  * **#57:** Deep Interactive Resultset Inspection (Discord ticket by user IPL)
* This confirms the maintainers view these issues as a unified cluster: **Advanced Reversing Environments & External Engine Plugins**.

---

## 6. PR Execution Playbook: If & When Accepted

Because Storytold operates with extreme merge velocity (10–15 PRs merged per day on release), we have pre-staged the implementation:

```
┌────────────────────────────────────────────────────────────────────────┐
│ DECISION GATE ON ISSUE #144                                            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
           ┌────────────────────────┴────────────────────────┐
           ▼                                                 ▼
┌───────────────────────────────────┐     ┌───────────────────────────────────┐
│ PATH 1: COMMUNITY PR (WE WRITE)   │     │ PATH 2: CORE ADOPTION (THEY WRITE)│
│                                   │     │                                   │
│ Maintainer says "PRs welcome"     │     │ Maintainer pulls into plugin tier │
│ 1. Checkout fork branch:          │     │ 1. Core adapts craft-sandbox-vbox │
│    feature/virtualbox-sandbox     │     │    logic into crates/engines      │
│ 2. Wire crates/engines/vbox.rs    │     │ 2. Issue #144 closed via commit   │
│ 3. Register in engines/table.rs   │     │ 3. Credit given to sandraschi     │
│ 4. Run cargo xtask layers && test │     │                                   │
│ 5. Open PR via gh pr create       │     │                                   │
└───────────────────────────────────┘     └───────────────────────────────────┘
```

### 6.1 Concrete Integration Plan for `crates/engines`
If we submit the PR:
1. **Engine Entry (`crates/engines/src/table.rs`):**
   ```rust
   manual(
       "virtualbox",
       "VirtualBox",
       "Running suspicious binaries inside an isolated disposable guest VM",
       &["VBoxManage"],
       &["VBoxManage.exe"],
   )
   ```
2. **Platform Capture Hook (`crates/platform/src/capture.rs`):**
   Extend `SandboxRequest` with hypervisor dispatch:
   ```rust
   pub enum SandboxRequest {
       Off,
       IfAvailable, // Bubblewrap
       VirtualMachine { vm_name: String },
   }
   ```
3. **Engine Bridge (`crates/engines/src/virtualbox.rs`):**
   Import `craft-sandbox-vbox` primitives into the engine dispatch loop.
4. **Validation:** Ensure `cargo xtask layers` passes (no higher-level dependencies leaked into L3 `engines`).

---

## 7. Summary of Assets & Locations

* **TextureCraft Upstream:** [`_upstream/texturecraft`](file:///D:/Dev/repos/_upstream/texturecraft) (fork: `sandraschi/texturecraft`)
* **Craft Anything Upstream:** [`_upstream/craft-anything`](file:///D:/Dev/repos/_upstream/craft-anything) (fork: `sandraschi/craft-anything`)
* **Local Sandbox Crate:** [`craft-sandbox-vbox`](file:///D:/Dev/repos/craft-sandbox-vbox) (repo: [`sandraschi/craft-sandbox-vbox`](https://github.com/sandraschi/craft-sandbox-vbox))
* **MCD Research Docs:**
  * [`2026-11-01-texturecraft-substance-painter-analysis.md`](file:///D:/Dev/repos/mcp-central-docs/research/2026-11-01-texturecraft-substance-painter-analysis.md)
  * [`2026-11-01-craft-anything-and-rea-deep-dive.md`](file:///D:/Dev/repos/mcp-central-docs/research/2026-11-01-craft-anything-and-rea-deep-dive.md)
  * [`2026-11-01-craft-anything-sandbox-vbox-and-ida-strategy.md`](file:///D:/Dev/repos/mcp-central-docs/research/2026-11-01-craft-anything-sandbox-vbox-and-ida-strategy.md)
* **MCD Reference Index:** [`COOL_REPOS.md`](file:///D:/Dev/repos/mcp-central-docs/reference/COOL_REPOS.md)
