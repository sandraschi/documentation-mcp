# Zig for Systems Programming: The SOTA 2026 Standard

**Compiler**: `zig` 0.12+ (Mandatory)
**Context**: "Better C"
**Role**: Cross-Compilation / Embedded Toolchains / Performant Utilities
**Build System**: `build.zig`
**Linting**: `zig fmt`

> [!IMPORTANT]
> **"Butter bei die Fische"**: This document serves as the **Single Source of Truth** for Zig usage within the Antigravity ecosystem. It integrates global knowledge (Wikipedia) with specific local operational standards (SOTA 2026).

---

## 📑 Table of Contents

1.  [Executive Summary](#executive-summary)
2.  [The Antigravity Zig Standard](#the-antigravity-zig-standard)
    *   [Comptime (Metaprogramming)](#comptime-metaprogramming)
    *   [Error Handling (Result Types)](#error-handling-result-types)
    *   [Memory Management (Explicit Allocators)](#memory-management-explicit-allocators)
3.  [Global Context: Zig Evolution](#global-context-zig-evolution)
    *   [History: Andrew Kelley (2016)](#history-andrew-kelley-2016)
    *   [No Hidden Control Flow](#no-hidden-control-flow)
    *   [The C Compiler (zig cc)](#the-c-compiler-zig-cc)
4.  [Fleet Integration Patterns](#fleet-integration-patterns)
    *   [Cross-Compilation Toolkit](#cross-compilation-toolkit)
    *   [WASM Modules](#wasm-modules)
    *   [Performance Critical Microservices](#performance-critical-microservices)
5.  [Advanced Patterns](#advanced-patterns)
    *   [Generic Data Structures](#generic-data-structures)
    *   [`defer` and `errdefer`](#defer-and-errdefer)
    *   [Packaged C Libraries](#packaged-c-libraries)
6.  [Security Best Practices](#security-best-practices)
7.  [Reference Material](#reference-material)

---

## 1. Executive Summary

In the **Antigravity Fleet**, Zig is the **Universal Toolchain**.
Even when we write Rust or Go, we often build it with `zig cc`.
When we need a small, robust binary that runs on a Raspberry Pi Zero without a glibc nightmare, we write it in Zig.

**Why Zig for SOTA 2026?**
-   **Simplicity**: It fits in your head. No hidden allocations. No operator overloading.
-   **Cross-Compilation**: It just works. `zig build -Dtarget=aarch64-linux-musl` produces a static binary.
-   **Comptime**: The most powerful metaprogramming system since Lisp, but with C-like syntax.

---

## 2. The Antigravity Zig Standard

### Comptime (Metaprogramming)

In Zig, types are values. You can write functions that take types and return types *at compile time*.
This replaces templates (C++), generics (Rust), and macros (C).

```zig
fn List(comptime T: type) type {
    return struct {
        items: []T,
        len: usize,
    };
}

const IntList = List(i32);
```

### Error Handling (Result Types)

Errors are values, but handled specially error unions.
`!T` means "Result of T or Error".

```zig
fn parseU64(buf: []const u8) !u64 {
    return std.fmt.parseInt(u64, buf, 10);
}

// Usage
const num = parseU64("123") catch |err| {
    std.debug.print("Failed: {}\n", .{err});
    return;
};
```

### Memory Management (Explicit Allocators)

There is no default allocator. If a function allocates memory, it must take an `Allocator` as an argument.
This makes hidden allocations impossible.

```zig
fn concat(allocator: Allocator, a: []const u8, b: []const u8) ![]u8 {
    const result = try allocator.alloc(u8, a.len + b.len);
    // ... copy ...
    return result;
}
```

---

## 3. Global Context: Zig Evolution

*(Ingested from Wikipedia Research)*

### History: Andrew Kelley (2016)
Created by **Andrew Kelley**. Goal: A pragmatic language to replace C.
Not C++, but C.

### No Hidden Control Flow
Zig guarantees that code execution flows exactly as written.
-   No operator overloading ( `a + b` is always addition).
-   No properties/getters (Accessing a field is just memory access).
-   No exceptions (Control flow is explicit).

### The C Compiler (zig cc)
Zig includes a full Clang/LLVM toolchain. `zig cc` can compile any C project.
It also includes libc definitions for almost every platform, enabling trivial cross-compilation.

---

## 4. Fleet Integration Patterns

### Cross-Compilation Toolkit

We use `zig cc` to compile our C/C++ dependencies (like `sqlite` or `ffmpeg`) for the robot's ARM64 architecture from our x86_64 dev machines.

### WASM Modules

Zig emits tiny, freestanding WebAssembly. We use this for high-performance modules in our web dashboard (e.g., parsing log files client-side).

### Performance Critical Microservices

For a service that does one thing (e.g., resizing images), Zig provides C-level performance with much better safety ergonomics.

---

## 5. Advanced Patterns

### Generic Data Structures

Using `comptime`, we create type-safe, zero-overhead data structures.

### `defer` and `errdefer`

Cleanup is easy. `defer` runs at end of scope. `errdefer` runs only if returning an error.

```zig
const file = try std.fs.cwd().openFile("data.txt", .{});
defer file.close();

const mem = try allocator.alloc(u8, 100);
errdefer allocator.free(mem); // Cleanup if next line fails

try file.readAll(mem);
```

### Packaged C Libraries

Zig can import `.h` files directly.

```zig
const c = @cImport({
    @cInclude("stdio.h");
});

pub fn main() void {
    _ = c.printf("Hello from C!\n");
}
```

---

## 6. Security Best Practices

1.  **Checked Arithmetic**: `+` checks for overflow by default in Debug/ReleaseSafe modes. Use `+%` for wrapping.
2.  **Slices**: Pointers usually come with a length. Buffer overflows are caught at runtime (panic).
3.  **Use ReleaseSafe**: For production, unless you need absolute max speed (ReleaseFast), stick to ReleaseSafe.

---

## 7. Reference Material

-   [Zig Language Reference](https://ziglang.org/documentation/master/)
-   [Zig by Example](https://zigbyexample.github.io/)
-   [Gamedev Guide to Zig](https://github.com/zig-gamedev/zig-gamedev)

---

**Maintainer:** Sandra S.
**Last Updated:** 2026-02-13
**Status**: SOTA 2026 Compliant
