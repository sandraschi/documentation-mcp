# Assembly Language: The Metal

**Architecture**: x86-64 / ARM64 (Mandatory)
**Context**: "No Abstractions"
**Role**: Bootloaders / SIMD / Reverse Engineering
**Assembler**: `nasm` / `gas`
**Debugger**: `gdb` / `radare2`

> [!IMPORTANT]
> **"Butter bei die Fische"**: This document serves as the **Single Source of Truth** for Assembly usage within the Antigravity ecosystem. It integrates global knowledge (Wikipedia) with specific local operational standards (SOTA 2026).

---

## 📑 Table of Contents

1.  [Executive Summary](#executive-summary)
2.  [The Antigravity Assembly Standard](#the-antigravity-assembly-standard)
    *   [Inline Assembly (Rust/C)](#inline-assembly-rustc)
    *   [SIMD (AVX-512 / NEON)](#simd-avx-512--neon)
    *   [Calling Conventions (System V AMD64 ABI)](#calling-conventions-system-v-amd64-abi)
3.  [Global Context: Assembly Evolution](#global-context-assembly-evolution)
    *   [History: EDSAC (1949)](#history-edsac-1949)
    *   [x86 vs ARM (CISC vs RISC)](#x86-vs-arm-cisc-vs-risc)
    *   [The Assembler (Macros)](#the-assembler-macros)
4.  [Fleet Integration Patterns](#fleet-integration-patterns)
    *   [Crash Dump Analysis](#crash-dump-analysis)
    *   [Performance Critical Loops](#performance-critical-loops)
    *   [Bootstrapping (OS Dev)](#bootstrapping-os-dev)
5.  [Advanced Patterns](#advanced-patterns)
    *   [Shellcoding](#shellcoding)
    *   [Self-Modifying Code (JIT)](#self-modifying-code-jit)
6.  [Security Best Practices](#security-best-practices)
7.  [Reference Material](#reference-material)

---

## 1. Executive Summary

In the **Antigravity Fleet**, Assembly is the microscope. We rarely write full programs in it, but we *read* it constantly when debugging Rust panics or C segfaults.

**Why Assembly for SOTA 2026?**
-   **Debugging**: When high-level abstractions leak, they leak into Assembly.
-   **Performance**: Sometimes the compiler is wrong. Hand-tuned AVX-512 can still beat auto-vectorization.
-   **Understanding**: To know how the machine *really* works (registers, stack, heap), you must know Assembly.

---

## 2. The Antigravity Assembly Standard

### Inline Assembly (Rust/C)

We use inline assembly for specific instructions not exposed by the language (e.g., `cpuid`, `rdtsc`).

```rust
// Rust Inline asm
use std::arch::asm;

unsafe {
    asm!("nop");
}
```

### SIMD (AVX-512 / NEON)

Single Instruction, Multiple Data. This is how we process LIDAR point clouds in real-time.

```asm
; Move 8 floats from memory to ZMM0
vmovups zmm0, [rsi]
; Add 8 floats from ZMM1 to ZMM0
vaddps zmm0, zmm0, zmm1
; Store result
vmovups [rdi], zmm0
```

### Calling Conventions (System V AMD64 ABI)

We strictly follow the standard calling convention on Linux/BSD.
-   **Arguments**: `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`
-   **Return**: `rax`, `rdx`
-   **Preserved**: `rbx`, `rbp`, `r12-r15`

---

## 3. Global Context: Assembly Evolution

*(Ingested from Wikipedia Research)*

### History: EDSAC (1949)
Assembly language is a 1-to-1 mapping of machine code (binary) to human-readable mnemonics (`MOV`, `ADD`, `JMP`).
It was the first "programming language". Before that, you toggled switches.

### x86 vs ARM (CISC vs RISC)
-   **x86-64 (CISC)**: Complex Instruction Set Computer. Variable length instructions. Few registers. Huge instruction set. (Intel/AMD).
-   **ARM64 (RISC)**: Reduced Instruction Set Computer. Fixed length (usually). Many registers. Simpler instructions. (Apple Silicon/Raspberry Pi).

### The Assembler (Macros)
Modern assemblers (`nasm`) are powerful macro processors. They allow defining structures, repeating blocks, and conditional assembly.

---

## 4. Fleet Integration Patterns

### Crash Dump Analysis

When a production service creates a core dump, we load it into `gdb` and read the backtrace. If the symbols are stripped, we read the assembly to reconstruct the state.

### Performance Critical Loops

For our custom video codec, the inner loop (DCT transform) is written in hand-optimized assembly to maximize IPC (Instructions Per Clock).

### Bootstrapping (OS Dev)

Our custom realtime microkernel starts in Assembly (`start.S`) to set up the GDT and page tables before jumping to Rust code.

---

## 5. Advanced Patterns

### Shellcoding

Writing position-independent code (PIC) that can be injected into a process memory space. Useful for security research and hot-patching.

### Self-Modifying Code (JIT)

Just-In-Time compilers (like V8 or LuaJIT) generate machine code at runtime. Understanding assembly is prerequisite to working on JITs.

---

## 6. Security Best Practices

1.  **NX Bit**: No-Execute. Ensure stack and heap are not executable.
2.  **ASLR**: Address Space Layout Randomization. Do not rely on fixed addresses.
3.  **Spectre/Meltdown**: Be aware of speculative execution vulnerabilities when writing timing-sensitive code.

---

## 7. Reference Material

-   [Intel® 64 and IA-32 Architectures Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)
-   [ARM Architecture Reference Manual](https://developer.arm.com/documentation/ddi0487/latest)
-   [NASM Documentation](https://www.nasm.us/doc/)

---

**Maintainer:** Sandra S.
**Last Updated:** 2026-02-13
**Status**: SOTA 2026 Compliant
